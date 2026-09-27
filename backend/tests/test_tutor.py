import pytest
from types import SimpleNamespace
from dataclasses import dataclass

from langchain_core.runnables import RunnableLambda

from app.ai.rag.retrieval import RetrievedChunk
from app.ai.agents.tutor.schemas import TutorResponse, TutorCitation
from tests.test_courses import seed_course


@dataclass
class FakeEmbeddingModel:
    dim: int = 384

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [
            [float(index + 1) / 100 for index in range(self.dim)]
            for _ in texts
        ]

    def embed_query(self, text: str) -> list[float]:
        return [float(index + 1) / 100 for index in range(self.dim)]


class FakeTutorLLM:
    def __init__(self, answer: str = "Test answer from tutor", citations: list | None = None):
        self._answer = answer
        self._citations = citations or []

    def with_structured_output(self, schema, method=None):
        async def ainvoke(input_data):
            # Handle GroundingValidation schema
            if schema.__name__ == "GroundingValidation":
                from app.ai.agents.tutor.validation import GroundingValidation
                return GroundingValidation(grounded=True, reason="Supported by context")
            return TutorResponse(answer=self._answer, citations=self._citations)

        return RunnableLambda(ainvoke)


def _auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def _seed_course_with_doc(session, tmp_path, monkeypatch) -> tuple:
    """Seed a course and ingest a test document."""
    course = await seed_course(session, title="Data Structures", slug="data-structures")

    file = tmp_path / "course.md"
    file.write_text(
        "# Arrays\n\nArrays are contiguous memory structures that store elements of the same type.\n"
        "They support random access by index in O(1) time.\n\n"
        "# Linked Lists\n\nLinked lists are dynamic data structures composed of nodes.\n"
        "Each node contains data and a pointer to the next node.",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "app.ai.rag.ingestion.create_embedding_model",
        lambda: FakeEmbeddingModel(),
    )

    from app.ai.rag.ingestion import ingest_document
    document_id = await ingest_document(
        session=session,
        course_id=course.id,
        file_path=file,
        title="Data Structures Notes",
    )

    return course, document_id


from app.schemas.tutor import TutorCitationResponse


async def test_ask_tutor_success(client, user_token, session, tmp_path, monkeypatch):
    token = await user_token("tutor@example.com")
    course, _ = await _seed_course_with_doc(session, tmp_path, monkeypatch)

    async def fake_ask_tutor(session, student_id, course_id, question):
        return {
            "answer": "Test answer from tutor",
            "citations": [
                TutorCitationResponse(
                    chunk_id=1,
                    document_id=1,
                    source="course.md",
                    page_number=1,
                ),
            ],
        }

    monkeypatch.setattr("app.api.tutor.ask_tutor", fake_ask_tutor)

    response = await client.post(
        "/api/v1/tutor/ask",
        headers=_auth_header(token),
        json={"course_id": course.id, "question": "What are arrays?"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] == "Test answer from tutor"
    assert "citations" in data
    assert len(data["citations"]) == 1
    assert data["citations"][0]["chunk_id"] == 1
    assert data["citations"][0]["document_id"] == 1
    assert data["citations"][0]["source"] == "course.md"


async def test_ask_tutor_with_multiple_citations(client, user_token, session, tmp_path, monkeypatch):
    token = await user_token("tutor2@example.com")
    course, _ = await _seed_course_with_doc(session, tmp_path, monkeypatch)

    async def fake_ask_tutor(session, student_id, course_id, question):
        return {
            "answer": "Test answer from tutor",
            "citations": [
                TutorCitationResponse(
                    chunk_id=1,
                    document_id=1,
                    source="course.md",
                    page_number=1,
                ),
                TutorCitationResponse(
                    chunk_id=2,
                    document_id=1,
                    source="course.md",
                    page_number=1,
                ),
            ],
        }

    monkeypatch.setattr("app.api.tutor.ask_tutor", fake_ask_tutor)

    response = await client.post(
        "/api/v1/tutor/ask",
        headers=_auth_header(token),
        json={"course_id": course.id, "question": "Compare arrays and linked lists"},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["citations"]) == 2
    assert data["citations"][0]["chunk_id"] == 1
    assert data["citations"][1]["chunk_id"] == 2


async def test_ask_tutor_no_documents(client, user_token, session, monkeypatch):
    token = await user_token("tutor3@example.com")
    course = await seed_course(session, title="Empty Course", slug="empty-course")

    async def fake_retrieve_empty(session, query, course_id, top_k):
        return []

    monkeypatch.setattr("app.ai.agents.tutor.nodes.retrieve", fake_retrieve_empty)
    monkeypatch.setattr("app.ai.agents.tutor.nodes.get_llm", lambda: FakeTutorLLM(
        answer="The available course material is insufficient to answer confidently."
    ))

    response = await client.post(
        "/api/v1/tutor/ask",
        headers=_auth_header(token),
        json={"course_id": course.id, "question": "What is this course about?"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "insufficient" in data["answer"].lower() or "no relevant" in data["answer"].lower()
    assert data["citations"] == []


async def test_ask_tutor_unauthorized(client):
    response = await client.post(
        "/api/v1/tutor/ask",
        json={"course_id": 1, "question": "What are arrays?"},
    )
    assert response.status_code == 401


async def test_ask_tutor_invalid_token(client):
    response = await client.post(
        "/api/v1/tutor/ask",
        headers=_auth_header("invalid-token"),
        json={"course_id": 1, "question": "What are arrays?"},
    )
    assert response.status_code == 401


async def test_ask_tutor_course_not_found(client, user_token, monkeypatch):
    token = await user_token("tutor4@example.com")

    async def fake_retrieve(session, query, course_id, top_k):
        return []

    monkeypatch.setattr("app.ai.agents.tutor.nodes.retrieve", fake_retrieve)
    monkeypatch.setattr("app.ai.agents.tutor.nodes.get_llm", lambda: FakeTutorLLM())

    response = await client.post(
        "/api/v1/tutor/ask",
        headers=_auth_header(token),
        json={"course_id": 999, "question": "What are arrays?"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data


async def test_ask_tutor_empty_question(client, user_token, session, monkeypatch):
    token = await user_token("tutor5@example.com")
    course = await seed_course(session, title="Test Course", slug="test-course")

    monkeypatch.setattr("app.ai.agents.tutor.nodes.get_llm", lambda: FakeTutorLLM())

    response = await client.post(
        "/api/v1/tutor/ask",
        headers=_auth_header(token),
        json={"course_id": course.id, "question": ""},
    )

    assert response.status_code == 422


async def test_ask_tutor_question_too_long(client, user_token, session, monkeypatch):
    token = await user_token("tutor6@example.com")
    course = await seed_course(session, title="Test Course", slug="test-course-2")

    monkeypatch.setattr("app.ai.agents.tutor.nodes.get_llm", lambda: FakeTutorLLM())

    long_question = "x" * 2001

    response = await client.post(
        "/api/v1/tutor/ask",
        headers=_auth_header(token),
        json={"course_id": course.id, "question": long_question},
    )

    assert response.status_code == 422


async def test_ask_tutor_citations_structure(client, user_token, session, tmp_path, monkeypatch):
    token = await user_token("tutor7@example.com")
    course, _ = await _seed_course_with_doc(session, tmp_path, monkeypatch)

    async def fake_ask_tutor(session, student_id, course_id, question):
        return {
            "answer": "Test answer from tutor",
            "citations": [
                TutorCitationResponse(
                    chunk_id=5,
                    document_id=2,
                    source="custom.pdf",
                    page_number=3,
                ),
            ],
        }

    monkeypatch.setattr("app.api.tutor.ask_tutor", fake_ask_tutor)

    response = await client.post(
        "/api/v1/tutor/ask",
        headers=_auth_header(token),
        json={"course_id": course.id, "question": "Test question"},
    )

    assert response.status_code == 200
    data = response.json()
    citation = data["citations"][0]
    assert citation["chunk_id"] == 5
    assert citation["document_id"] == 2
    assert citation["source"] == "custom.pdf"
    assert citation["page_number"] == 3
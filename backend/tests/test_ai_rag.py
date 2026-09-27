from types import SimpleNamespace

import pytest
from langchain_core.documents import Document
from sqlalchemy import select

from app.ai.rag.chunking import split_documents
from app.ai.rag.embeddings import embed_query
from app.ai.rag.ingestion import ingest_document
from app.ai.rag.loaders import load_document
from app.ai.rag.retrieval import (
    RetrievedChunk,
    retrieve,
    search_similar_chunks,
)
from app.models.course import Course
from app.models.document import Document as DocumentModel
from app.models.document import DocumentChunk


class FakeEmbeddingModel:
    def __init__(self, dim: int = 384):
        self.dim = dim

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [
            [float(index + 1) / 100 for index in range(self.dim)]
            for _ in texts
        ]

    def embed_query(self, text: str) -> list[float]:
        return [float(index + 1) / 100 for index in range(self.dim)]


async def seed_course(session) -> Course:
    course = Course(
        title="AI Course",
        slug="ai-course",
        description="Test course for RAG",
    )
    session.add(course)
    await session.commit()
    await session.refresh(course)
    return course


def test_load_markdown_document(tmp_path):
    file = tmp_path / "notes.md"
    file.write_text("# Hello\n\nRAG pipeline test.", encoding="utf-8")

    documents = load_document(file)

    assert len(documents) == 1
    assert documents[0].page_content == "# Hello\n\nRAG pipeline test."
    assert documents[0].metadata["source"] == str(file)
    assert documents[0].metadata["file_name"] == "notes.md"
    assert documents[0].metadata["document_type"] == "md"


def test_load_missing_document_raises():
    with pytest.raises(FileNotFoundError):
        load_document("does-not-exist.pdf")


def test_load_unsupported_extension_raises(tmp_path):
    file = tmp_path / "data.txt"
    file.write_text("not supported", encoding="utf-8")

    with pytest.raises(ValueError):
        load_document(file)


def test_split_long_document_assigns_chunk_index():
    content = " ".join(["word"] * 4000)

    chunks = split_documents(
        [Document(page_content=content)],
        chunk_size=1000,
        chunk_overlap=200,
    )

    assert len(chunks) > 1
    indexes = [chunk.metadata["chunk_index"] for chunk in chunks]
    assert indexes == list(range(len(chunks)))


def test_short_document_single_chunk_index_zero():
    chunks = split_documents([Document(page_content="short content")])

    assert len(chunks) == 1
    assert chunks[0].metadata["chunk_index"] == 0


def test_chunks_inherit_source_metadata():
    content = " ".join(["word"] * 4000)

    chunks = split_documents(
        [
            Document(
                page_content=content,
                metadata={
                    "source": "notes.md",
                    "file_name": "notes.md",
                    "document_type": "md",
                },
            )
        ],
        chunk_size=1000,
        chunk_overlap=200,
    )

    assert chunks[0].metadata["source"] == "notes.md"
    assert chunks[0].metadata["file_name"] == "notes.md"
    assert chunks[0].metadata["document_type"] == "md"


def test_embed_query_returns_mock_vector(monkeypatch):
    monkeypatch.setattr(
        "app.ai.rag.embeddings.create_embedding_model",
        lambda: FakeEmbeddingModel(),
    )

    vector = embed_query("hello")

    assert len(vector) == 384


def test_embed_query_real_model_returns_384_dimensions():
    vector = embed_query(
        "The quick brown fox jumps over the lazy dog"
    )

    assert len(vector) == 384


async def test_ingest_document_persists_document_and_chunks(
    session,
    tmp_path,
    monkeypatch,
):
    course = await seed_course(session)

    file = tmp_path / "notes.md"
    file.write_text(" ".join(["content"] * 3000), encoding="utf-8")

    monkeypatch.setattr(
        "app.ai.rag.ingestion.create_embedding_model",
        lambda: FakeEmbeddingModel(),
    )

    document_id = await ingest_document(
        session=session,
        course_id=course.id,
        file_path=file,
        title="Notes",
    )

    assert isinstance(document_id, int)

    document = await session.get(DocumentModel, document_id)
    assert document is not None
    assert document.course_id == course.id
    assert document.title == "Notes"
    assert document.source == str(file)
    assert document.document_type == "md"

    chunks = (
        await session.execute(
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        )
    ).scalars().all()

    assert len(chunks) > 1
    assert [chunk.chunk_index for chunk in chunks] == list(
        range(len(chunks))
    )
    assert chunks[0].embedding is not None
    assert len(chunks[0].embedding) == 384


async def test_ingest_document_rejects_duplicate_source(
    session,
    tmp_path,
    monkeypatch,
):
    course = await seed_course(session)

    file = tmp_path / "notes.md"
    file.write_text(" ".join(["content"] * 200), encoding="utf-8")

    monkeypatch.setattr(
        "app.ai.rag.ingestion.create_embedding_model",
        lambda: FakeEmbeddingModel(),
    )

    await ingest_document(
        session=session,
        course_id=course.id,
        file_path=file,
    )

    with pytest.raises(ValueError):
        await ingest_document(
            session=session,
            course_id=course.id,
            file_path=file,
        )


async def test_search_similar_chunks_builds_retrieved_chunks():
    def make_chunk(chunk_id):
        return SimpleNamespace(
            id=chunk_id,
            document_id=1,
            content=f"content {chunk_id}",
            page_number=1,
            module_id=1,
            lesson_id=1,
        )

    class FakeResult:
        def __init__(self, rows):
            self._rows = rows

        def all(self):
            return self._rows

    class FakeSession:
        def __init__(self, rows):
            self._rows = rows

        async def execute(self, statement):
            return FakeResult(self._rows)

    rows = [
        (make_chunk(1), "notes.md", 0.9),
        (make_chunk(2), "notes.md", 0.8),
    ]

    results = await search_similar_chunks(
        session=FakeSession(rows),
        query_embedding=[0.1] * 384,
        course_id=1,
        top_k=5,
    )

    assert len(results) == 2
    assert results[0].chunk_id == 1
    assert results[0].document_id == 1
    assert results[0].content == "content 1"
    assert results[0].page_number == 1
    assert results[0].module_id == 1
    assert results[0].lesson_id == 1
    assert results[0].source == "notes.md"
    assert results[0].similarity == pytest.approx(0.9)
    assert results[1].similarity == pytest.approx(0.8)


async def test_retrieve_orchestrates_embed_and_search(monkeypatch):
    captured = {}

    def fake_embed_query(query):
        captured["query"] = query
        return [0.5] * 4

    async def fake_search_similar_chunks(
        session,
        query_embedding,
        course_id,
        top_k,
    ):
        captured["query_embedding"] = query_embedding
        captured["course_id"] = course_id
        captured["top_k"] = top_k
        return [
            RetrievedChunk(
                chunk_id=1,
                document_id=1,
                content="content",
                page_number=1,
                module_id=None,
                lesson_id=None,
                source="notes.md",
                similarity=0.9,
            )
        ]

    monkeypatch.setattr(
        "app.ai.rag.retrieval.embed_query",
        fake_embed_query,
    )
    monkeypatch.setattr(
        "app.ai.rag.retrieval.search_similar_chunks",
        fake_search_similar_chunks,
    )

    results = await retrieve(
        session=None,
        query="hello",
        course_id=3,
        top_k=10,
    )

    assert captured == {
        "query": "hello",
        "query_embedding": [0.5] * 4,
        "course_id": 3,
        "top_k": 10,
    }
    assert len(results) == 1
    assert results[0].chunk_id == 1


def test_to_langchain_documents_maps_metadata():
    chunks = [
        RetrievedChunk(
            chunk_id=7,
            document_id=2,
            content="text",
            page_number=3,
            module_id=None,
            lesson_id=4,
            source="file.md",
            similarity=0.77,
        )
    ]

    documents = [chunk.to_langchain_document() for chunk in chunks]

    assert len(documents) == 1
    assert documents[0].page_content == "text"
    metadata = documents[0].metadata
    assert metadata["chunk_id"] == 7
    assert metadata["document_id"] == 2
    assert metadata["source"] == "file.md"
    assert metadata["page_number"] == 3
    assert metadata["lesson_id"] == 4
    assert metadata["similarity"] == pytest.approx(0.77)
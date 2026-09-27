from langchain_core.documents import Document
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.agents.tutor.prompts import TUTOR_PROMPT
from app.ai.agents.tutor.schemas import (
    TutorCitation,
    TutorResponse,
)
from app.ai.llm.factory import get_llm
from app.ai.rag.retrieval import retrieve
from app.ai.agents.tutor.validation import GroundingValidation
from app.ai.agents.tutor.validation_prompt import GROUNDING_PROMPT

async def load_student_context(
    state: dict,
    session: AsyncSession,
) -> dict:
    return {
        "student_context": {
            "student_id": state["student_id"],
        }
    }


async def retrieve_context(
    state: dict,
    session: AsyncSession,
) -> dict:
    results = await retrieve(
        session=session,
        query=state["question"],
        course_id=state["course_id"],
        top_k=5,
    )

    documents = [
        result.to_langchain_document()
        for result in results
    ]

    return {
        "retrieved_documents": documents,
    }

def build_context(
    documents: list[Document],
) -> str:
    if not documents:
        return "No relevant course material was found."

    sections: list[str] = []

    for index, document in enumerate(documents, start=1):
        metadata = document.metadata

        sections.append(
            f"""
SOURCE {index}
Source: {metadata.get("source")}
Page: {metadata.get("page_number")}
Chunk ID: {metadata.get("chunk_id")}

Content:
{document.page_content}
""".strip()
        )

    return "\n\n---\n\n".join(sections)

async def generate_answer(state: dict) -> dict:
    documents = state.get(
        "retrieved_documents",
        [],
    )

    context = build_context(documents)

    llm = get_llm()

    structured_llm = llm.with_structured_output(TutorResponse,method="json_schema")

    chain = TUTOR_PROMPT | structured_llm

    response: TutorResponse = await chain.ainvoke(
        {
            "context": context,
            "question": state["question"],
        }
    ) # type: ignore

    citations = []

    for document in documents:
        metadata = document.metadata

        citations.append(
            TutorCitation(
                chunk_id=metadata["chunk_id"],
                document_id=metadata["document_id"],
                source=metadata["source"],
                page_number=metadata.get(
                    "page_number"
                ),
            )
        )

    return {
        "answer": response.answer,
        "citations": citations,
    }
    
async def validate_grounding(
    state: dict,
) -> dict:
    documents = state.get(
        "retrieved_documents",
        [],
    )

    answer = state.get(
        "answer",
        "",
    )

    context = build_context(documents)

    llm = get_llm()

    validator = llm.with_structured_output(
        GroundingValidation
    )

    chain = GROUNDING_PROMPT | validator

    result: GroundingValidation = await chain.ainvoke(
        {
            "context": context,
            "answer": answer,
        }
    ) # type: ignore

    return {
        "grounded": result.grounded,
        "grounding_reason": result.reason,
    }
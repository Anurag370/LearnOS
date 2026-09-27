from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.agents.tutor.graph import build_tutor_graph
from app.ai.agents.tutor.schemas import TutorCitation
from app.schemas.tutor import TutorCitationResponse


async def ask_tutor(
    session: AsyncSession,
    student_id: int,
    course_id: int,
    question: str,
):
    graph = build_tutor_graph(session)

    result = await graph.ainvoke(
        {
            "student_id": student_id,
            "course_id": course_id,
            "question": question,
            "retry_count": 0,
        }
    )
    
    if not result.get("grounded", False):
        return {
            "answer": (
                "I couldn't find enough support in the "
                "available course material to answer that "
                "confidently."
            ),
            "citations": result.get(
                "citations",
                [],
            ),
        }

    citations = result.get("citations", [])
    converted_citations = [
        TutorCitationResponse(
            chunk_id=c.chunk_id,
            document_id=c.document_id,
            source=c.source,
            page_number=c.page_number,
        )
        for c in citations
        if isinstance(c, TutorCitation)
    ]

    return {
        "answer": result["answer"],
        "citations": converted_citations,
        "grounded": result.get("grounded"),
        "grounding_reason": result.get("grounding_reason"),
    }
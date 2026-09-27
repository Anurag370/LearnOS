from typing import TypedDict

from langchain_core.documents import Document

MAX_TUTOR_RETRIES = 1

class TutorState(TypedDict, total=False):
    student_id: int
    course_id: int

    question: str

    student_context: dict

    retrieved_documents: list[Document]

    answer: str

    citations: str

    grounded: bool
    grounding_reason: str
    retry_count: int
from pydantic import BaseModel, Field


class TutorQuestionRequest(BaseModel):
    course_id: int
    question: str = Field(
        min_length=1,
        max_length=2000,
    )


class TutorCitationResponse(BaseModel):
    chunk_id: int
    document_id: int
    source: str
    page_number: int | None = None


class TutorAnswerResponse(BaseModel):
    answer: str
    citations: list[TutorCitationResponse]
    grounded: bool | None = None
    grounding_reason: str | None = None
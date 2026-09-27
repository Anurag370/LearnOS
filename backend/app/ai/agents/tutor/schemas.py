from pydantic import BaseModel, Field


class TutorCitation(BaseModel):
    chunk_id: int
    document_id: int
    source: str
    page_number: int | None = None


class TutorResponse(BaseModel):
    answer: str = Field(
        description="The final answer shown directly to the student."
    )

    citations: list[TutorCitation] = Field(
        default_factory=list,
        description="Course-material chunks directly supporting the answer."
    )
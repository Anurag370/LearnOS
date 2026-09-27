from pydantic import BaseModel, Field


class GroundingValidation(BaseModel):
    grounded: bool

    reason: str = Field(
        min_length=1,
        max_length=1000,
    )
from pydantic import BaseModel, Field


class StudentProfileResponse(BaseModel):
    id:int
    user_id:int
    current_skill_level:str | None
    available_study_minutes:int | None

    model_config = {
        "from_attributes": True
    }


class StudentProfileUpdate(BaseModel):
    current_skill_level : str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    available_study_minutes:int | None = Field(
        default=None,
        ge=1,
        le=1440
    )
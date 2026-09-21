from datetime import date

from pydantic import BaseModel, Field

class LearningGoalCreate(BaseModel):

    course_id: int
    description: str = Field(min_length=3, max_length=1000)
    target_date:date | None = Field(default=None, max_length=2000)
    desired_outcome: str | None = Field(default=None, max_length=2000)

class LearningGoalUpdate(BaseModel):
    description: str | None = Field(default=None, min_length=3, max_length=1000)
    target_date:date | None = None
    desired_outcome: str | None = Field(default=None, max_length=2000)

class LearningGoalResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    description: str
    target_date: date | None
    desired_outcome: str | None
    status: str

    model_config = {
        "from_attributes": True
        }
from pydantic import BaseModel, Field


class LearningPlanItemResponse(BaseModel):
    id: int
    plan_id: int
    lesson_id: int
    position: int
    status: str

    model_config = {
        "from_attributes": True,
    }


class LearningPlanResponse(BaseModel):
    id: int
    user_id: int
    learning_goal_id: int
    status: str
    items: list[LearningPlanItemResponse]

    model_config = {
        "from_attributes": True,
    }


class LearningPlanCreateItem(BaseModel):
    lesson_id: int
    position: int = Field(ge=1)


class LearningPlanCreate(BaseModel):
    learning_goal_id: int
    items: list[LearningPlanCreateItem] = Field(
        min_length=1,
    )


class LearningPlanStatusUpdate(BaseModel):
    status: str


class LearningPlanItemStatusUpdate(BaseModel):
    status: str
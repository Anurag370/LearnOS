from datetime import datetime
from pydantic import BaseModel, ConfigDict

class LessonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    title:str
    slug:str
    content:str | None
    position:int

class ModuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    title:str
    description:str | None
    position:int
    lessons:list[LessonResponse]


class TopicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    name:str
    slug:str
    description:str | None

class CourseListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    title:str
    slug:str
    description:str | None

class CourseResponse(CourseListResponse):
    created_at: datetime
    updated_at: datetime
    modules: list[ModuleResponse]
    topics: list[TopicResponse]
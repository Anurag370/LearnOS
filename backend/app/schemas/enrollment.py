from pydantic import BaseModel, ConfigDict
from datetime import datetime


class EnrollmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:int
    user_id:int
    course_id:int
    status:str
    enrolled_at:datetime

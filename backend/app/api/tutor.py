from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.tutor import (
    TutorAnswerResponse,
    TutorQuestionRequest,
)
from app.services.tutor import ask_tutor


router = APIRouter(
    prefix="/tutor",
    tags=["Tutor"],
)


@router.post(
    "/ask",
    response_model=TutorAnswerResponse,
)
async def ask_tutor_endpoint(
    request: TutorQuestionRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    result = await ask_tutor(
        session=session,
        student_id=current_user.id,
        course_id=request.course_id,
        question=request.question,
    )

    return TutorAnswerResponse(
        answer=result["answer"],
        citations=result["citations"],
        grounded=result.get("grounded"),
        grounding_reason=result.get("grounding_reason"),
    )
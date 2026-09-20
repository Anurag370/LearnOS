from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import require_student
from app.core.database import get_db
from app.models.user import User
from app.repositories.course import CourseRepository
from app.repositories.learning_goal import LearningGoalRepository
from app.schemas.learning_goal import (
    LearningGoalCreate,
    LearningGoalResponse,
    LearningGoalUpdate,
)
from app.services.learning_goal import (
    CourseNotFoundError,
    LearningGoalNotFoundError,
    LearningGoalService,
)


router = APIRouter(
    prefix="/learning-goals",
    tags=["Learning Goals"],
)


def get_learning_goal_service(
    session: AsyncSession = Depends(get_db),
) -> LearningGoalService:
    return LearningGoalService(
        session=session,
        repository=LearningGoalRepository(session),
        course_repository=CourseRepository(session),
    )


@router.get(
    "",
    response_model=list[LearningGoalResponse],
)
async def list_learning_goals(
    current_user: User = Depends(require_student),
    service: LearningGoalService = Depends(get_learning_goal_service),
):
    return await service.list_goals(current_user.id)


@router.post(
    "",
    response_model=LearningGoalResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_learning_goal(
    data: LearningGoalCreate,
    current_user: User = Depends(require_student),
    service: LearningGoalService = Depends(get_learning_goal_service),
):
    try:
        return await service.create_goal(
            current_user.id,
            course_id=data.course_id,
            description=data.description,
            target_date=data.target_date,
            desired_outcome=data.desired_outcome,
        )

    except CourseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )


@router.put(
    "/{goal_id}",
    response_model=LearningGoalResponse,
)
async def update_learning_goal(
    goal_id: int,
    data: LearningGoalUpdate,
    current_user: User = Depends(require_student),
    service: LearningGoalService = Depends(get_learning_goal_service),
):
    try:
        return await service.update_goal(
            current_user.id,
            goal_id,
            description=data.description,
            target_date=data.target_date,
            desired_outcome=data.desired_outcome,
        )

    except LearningGoalNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning goal not found",
        )
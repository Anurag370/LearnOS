from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import require_student
from app.core.database import get_db
from app.models.user import User
from app.repositories.learning_plan import (
    LearningPlanRepository,
)
from app.schemas.learning_plan import (
    LearningPlanItemResponse,
    LearningPlanResponse,
    LearningPlanStatusUpdate,
    LearningPlanItemStatusUpdate,
    LearningPlanCreate
)
from app.services.learning_plan import (
    InvalidPlanItemStatusError,
    InvalidPlanStatusError,
    LearningGoalNotFoundError,
    LearningPlanAlreadyExistsError,
    LearningPlanItemNotFoundError,
    LearningPlanNotFoundError,
    InvalidPlanItemsError,
    LessonNotFoundError,
    LessonNotInGoalCourseError,
    LearningPlanService,
    LearningGoalRepository
)
from app.repositories.lesson import LessonRepository
from app.repositories.learning_goal import LearningGoalRepository

router = APIRouter(
    prefix="/learning-plans",
    tags=["Learning Plans"],
)


def get_learning_plan_service(
    session: AsyncSession = Depends(get_db),
) -> LearningPlanService:
    return LearningPlanService(
        session=session,
        repository=LearningPlanRepository(session),
        learning_goal_repository=LearningGoalRepository(session),
        lesson_repository=LessonRepository(session),
    )


@router.get(
    "",
    response_model=list[LearningPlanResponse],
)
async def list_learning_plans(
    current_user: User = Depends(require_student),
    service: LearningPlanService = Depends(
        get_learning_plan_service
    ),
):
    return await service.list_plans(current_user.id)


@router.post(
    "",
    response_model=LearningPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_learning_plan(
    data: LearningPlanCreate,
    current_user: User = Depends(require_student),
    service: LearningPlanService = Depends(
        get_learning_plan_service
    ),
):
    try:
        return await service.create_plan(
            current_user.id,
            data.learning_goal_id,
            [(item.lesson_id, item.position) for item in data.items],
        )

    except LearningGoalNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning goal not found",
        )

    except LearningPlanAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A learning plan already exists for this goal",
        )

    except LessonNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    except LessonNotInGoalCourseError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Lesson is not part of the goal's course",
        )

    except InvalidPlanItemsError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid plan items",
        )


@router.get(
    "/goal/{learning_goal_id}",
    response_model=LearningPlanResponse,
)
async def get_learning_plan_by_goal(
    learning_goal_id: int,
    current_user: User = Depends(require_student),
    service: LearningPlanService = Depends(
        get_learning_plan_service
    ),
):
    try:
        return await service.get_plan_by_goal(
            current_user.id,
            learning_goal_id,
        )

    except LearningPlanNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning plan not found",
        )

@router.get(
    "/{plan_id}",
    response_model=LearningPlanResponse,
)
async def get_learning_plan(
    plan_id: int,
    current_user: User = Depends(require_student),
    service: LearningPlanService = Depends(
        get_learning_plan_service
    ),
):
    try:
        return await service.get_plan(
            current_user.id,
            plan_id,
        )

    except LearningPlanNotFoundError:
        raise HTTPException(    
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning plan not found",
        )

@router.put(
    "/{plan_id}/status",
    response_model=LearningPlanResponse,
)
async def update_learning_plan_status(
    plan_id: int,
    data: LearningPlanStatusUpdate,
    current_user: User = Depends(require_student),
    service: LearningPlanService = Depends(
        get_learning_plan_service
    ),
):
    try:
        return await service.update_plan_status(
            current_user.id,
            plan_id,
            data.status,
        )

    except LearningPlanNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning plan not found",
        )

    except InvalidPlanStatusError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid learning plan status",
        )


@router.put(
    "/items/{item_id}/status",
    response_model=LearningPlanItemResponse,
)
async def update_learning_plan_item_status(
    item_id: int,
    data: LearningPlanItemStatusUpdate,
    current_user: User = Depends(require_student),
    service: LearningPlanService = Depends(
        get_learning_plan_service
    ),
):
    try:
        return await service.update_item_status(
            current_user.id,
            item_id,
            data.status,
        )

    except LearningPlanItemNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning plan item not found",
        )

    except InvalidPlanItemStatusError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid learning plan item status",
        )
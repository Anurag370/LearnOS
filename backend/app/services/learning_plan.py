from sqlalchemy.ext.asyncio import AsyncSession

from app.models.learning_plan import LearningPlan
from app.repositories.learning_plan import (
    LearningPlanRepository,
)
from app.core.learning_plan import (
    PLAN_ITEM_STATUSES,
    PLAN_STATUSES,
)
from app.repositories.learning_goal import LearningGoalRepository
from app.repositories.lesson import LessonRepository


class LearningPlanNotFoundError(Exception):
    pass

class LearningPlanItemNotFoundError(Exception):
    pass


class InvalidPlanStatusError(Exception):
    pass


class InvalidPlanItemStatusError(Exception):
    pass

class LearningGoalNotFoundError(Exception):
    pass


class LearningPlanAlreadyExistsError(Exception):
    pass


class InvalidPlanItemsError(Exception):
    pass


class LessonNotFoundError(Exception):
    pass


class LessonNotInGoalCourseError(Exception):
    pass

class LearningPlanService:
    def __init__(
        self,
        session: AsyncSession,
        repository: LearningPlanRepository,
        learning_goal_repository: LearningGoalRepository,
        lesson_repository: LessonRepository,
    ):
        self.session = session
        self.repository = repository
        self.learning_goal_repository = learning_goal_repository
        self.lesson_repository = lesson_repository

    async def get_plan(
        self,
        user_id: int,
        plan_id: int,
    ) -> LearningPlan:
        plan = await self.repository.get_by_id(plan_id)

        if plan is None or plan.user_id != user_id:
            raise LearningPlanNotFoundError

        return plan

    async def get_plan_by_goal(
        self,
        user_id: int,
        learning_goal_id: int,
    ) -> LearningPlan:
        plan = await self.repository.get_by_goal_id(
            learning_goal_id
        )

        if plan is None or plan.user_id != user_id:
            raise LearningPlanNotFoundError

        return plan

    async def list_plans(
        self,
        user_id: int,
    ) -> list[LearningPlan]:
        return await self.repository.get_by_user(user_id)

    async def create_plan(
        self,
        user_id: int,
        learning_goal_id: int,
        items: list[tuple[int, int]],
    ) -> LearningPlan:
        goal = await self.learning_goal_repository.get_by_id(
            learning_goal_id
        )

        if goal is None or goal.user_id != user_id:
            raise LearningGoalNotFoundError

        existing_plan = await self.repository.get_by_goal_id(
            learning_goal_id
        )

        if existing_plan is not None:
            raise LearningPlanAlreadyExistsError

        if not items:
            raise InvalidPlanItemsError

        positions = [position for _, position in items]

        if len(positions) != len(set(positions)):
            raise InvalidPlanItemsError

        if set(positions) != set(range(1, len(items) + 1)):
            raise InvalidPlanItemsError

        for lesson_id, _ in items:
            lesson = await self.lesson_repository.get_by_id(
                lesson_id
            )

            if lesson is None:
                raise LessonNotFoundError

            course_id = await self.lesson_repository.get_course_id(
                lesson_id
            )

            if course_id != goal.course_id:
                raise LessonNotInGoalCourseError

        plan = await self.repository.create(
            user_id=user_id,
            learning_goal_id=learning_goal_id,
        )

        for lesson_id, position in items:
            await self.repository.create_item(
                plan_id=plan.id,
                lesson_id=lesson_id,
                position=position,
            )

        await self.session.commit()

        created_plan = await self.repository.get_by_id(
            plan.id
        )

        if created_plan is None:
            raise LearningPlanNotFoundError

        return created_plan

    async def update_plan_status(
        self,
        user_id: int,
        plan_id: int,
        status: str,
    ) -> LearningPlan:
        if status not in PLAN_STATUSES:
            raise InvalidPlanStatusError

        plan = await self.get_plan(
            user_id,
            plan_id,
        )

        await self.repository.update_status(
            plan,
            status,
        )

        await self.session.commit()

        await self.session.refresh(plan)

        return plan

    async def update_item_status(
        self,
        user_id: int,
        item_id: int,
        status: str,
    ):
        if status not in PLAN_ITEM_STATUSES:
            raise InvalidPlanItemStatusError

        item = await self.repository.get_item_by_id(
            item_id
        )

        if item is None:
            raise LearningPlanItemNotFoundError

        plan = await self.repository.get_by_id(
            item.plan_id
        )

        if plan is None or plan.user_id != user_id:
            raise LearningPlanItemNotFoundError

        await self.repository.update_item_status(
            item,
            status,
        )

        await self.session.commit()

        await self.session.refresh(item)

        return item
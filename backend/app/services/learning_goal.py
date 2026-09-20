from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.learning_goal import LearningGoals
from app.repositories.course import CourseRepository
from app.repositories.learning_goal import LearningGoalRepository


class CourseNotFoundError(Exception):
    pass


class LearningGoalNotFoundError(Exception):
    pass


class LearningGoalService:
    def __init__(
        self,
        session: AsyncSession,
        repository: LearningGoalRepository,
        course_repository: CourseRepository,
    ):
        self.session = session
        self.repository = repository
        self.course_repository = course_repository

    async def list_goals(self, user_id: int) -> list[LearningGoals]:
        return await self.repository.list_by_user(user_id)

    async def create_goal(
        self,
        user_id: int,
        course_id: int,
        description: str,
        target_date: date | None,
        desired_outcome: str | None,
    ) -> LearningGoals:
        course = await self.course_repository.get_by_id(course_id)

        if course is None:
            raise CourseNotFoundError

        return await self.repository.create(
            user_id=user_id,
            course_id=course_id,
            description=description,
            target_date=target_date,
            desired_outcome=desired_outcome,
        )

    async def update_goal(
        self,
        user_id: int,
        goal_id: int,
        description: str | None,
        target_date: date | None,
        desired_outcome: str | None,
    ) -> LearningGoals:
        goal = await self.repository.get_by_id_and_user(goal_id, user_id)

        if goal is None:
            raise LearningGoalNotFoundError

        return await self.repository.update(
            goal,
            description=description,
            target_date=target_date,
            desired_outcome=desired_outcome,
        )
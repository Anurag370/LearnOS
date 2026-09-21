from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.learning_goal import LearningGoal
from app.repositories.course import CourseRepository
from app.repositories.learning_goal import LearningGoalRepository
from app.repositories.enrollment import EnrollementRepository


class CourseNotFoundError(Exception):
    pass


class LearningGoalNotFoundError(Exception):
    pass

class CourseNotEnrolledError(Exception):
    pass

class LearningGoalService:
    def __init__(
        self,
        session: AsyncSession,
        repository: LearningGoalRepository,
        course_repository: CourseRepository,
        enrollment_repository: EnrollementRepository
    ):
        self.session = session
        self.repository = repository
        self.course_repository = course_repository
        self.enrollment_repository = enrollment_repository

    async def list_goals(
        self,
        user_id: int,
    ) -> list[LearningGoal]:
        return await self.repository.get_by_user(user_id)

    async def create_goal(
        self,
        user_id: int,
        *,
        course_id: int,
        description: str,
        target_date: date | None,
        desired_outcome: str | None,
    ) -> LearningGoal:
        course = await self.course_repository.get_by_id(course_id)

        if course is None:
            raise CourseNotFoundError
        
        enrollment = (await self.enrollment_repository.get_by_user_and_course(
            user_id=user_id,
            course_id=course_id
        ))

        if enrollment is None:
            raise CourseNotEnrolledError

        goal = await self.repository.create(
            user_id=user_id,
            course_id=course_id,
            description=description,
            target_date=target_date,
            desired_outcome=desired_outcome,
        )

        await self.session.commit()
        await self.session.refresh(goal)

        return goal

    async def update_goal(
        self,
        user_id: int,
        goal_id: int,
        *,
        description: str | None,
        target_date: date | None,
        desired_outcome: str | None,
    ) -> LearningGoal:
        goal = await self.repository.get_by_id(goal_id)

        if goal is None or goal.user_id != user_id:
            raise LearningGoalNotFoundError

        await self.repository.update(
            goal,
            description=description,
            target_date=target_date,
            desired_outcome=desired_outcome,
        )

        await self.session.commit()
        await self.session.refresh(goal)

        return goal
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.learning_goal import LearningGoals


class LearningGoalRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_by_user(self, user_id: int) -> list[LearningGoals]:
        result = await self.session.execute(
            select(LearningGoals)
            .where(LearningGoals.user_id == user_id)
            .order_by(LearningGoals.id)
        )

        return list(result.scalars().all())

    async def get_by_id_and_user(
        self, goal_id: int, user_id: int
    ) -> LearningGoals | None:
        result = await self.session.execute(
            select(LearningGoals).where(
                LearningGoals.id == goal_id,
                LearningGoals.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        user_id: int,
        course_id: int,
        description: str,
        target_date: date | None,
        desired_outcome: str | None,
    ) -> LearningGoals:
        goal = LearningGoals(
            user_id=user_id,
            course_id=course_id,
            description=description,
            target_date=target_date,
            desired_outcome=desired_outcome,
        )
        self.session.add(goal)

        await self.session.commit()
        await self.session.refresh(goal)

        return goal

    async def update(
        self,
        goal: LearningGoals,
        description: str | None,
        target_date: date | None,
        desired_outcome: str | None,
    ) -> LearningGoals:
        if description is not None:
            goal.description = description
        if target_date is not None:
            goal.target_date = target_date
        if desired_outcome is not None:
            goal.desired_outcome = desired_outcome

        await self.session.commit()
        await self.session.refresh(goal)

        return goal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.learning_goal import LearningGoal


class LearningGoalRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, goal_id:int) ->  LearningGoal | None:

        result = await self.session.execute(
            select(LearningGoal)
            .where(LearningGoal.id == goal_id)
        )

        return result.scalar_one_or_none()

    async def get_by_user(self, user_id:int) -> list[LearningGoal]:

        result = await self.session.execute(
            select(LearningGoal)
            .where(LearningGoal.user_id == user_id)
            .order_by(LearningGoal.created_at.desc())
        )

        return list(result.scalars().all())

    async def create(self, *, user_id:int, course_id:int, description:str, target_date, desired_outcome:str | None) ->  LearningGoal:

        goal = LearningGoal(
            user_id=user_id,
            course_id=course_id,
            description=description,
            target_date=target_date,
            desired_outcome=desired_outcome
        )

        self.session.add(goal)

        await self.session.flush()

        return goal

    async def update(self, goal:LearningGoal, *, description:str | None, target_date, desired_outcome: str | None) -> LearningGoal:

        if description is not None:
            goal.description = description

        if target_date is not None:
            goal.target_date = target_date

        if desired_outcome is not None:
            goal.desired_outcome = desired_outcome

        await self.session.flush()

        return goal
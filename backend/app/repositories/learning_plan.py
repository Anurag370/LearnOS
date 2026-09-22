from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.learning_plan import (
    LearningPlan,
    LearningPlanItem,
)


class LearningPlanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        plan_id: int,
    ) -> LearningPlan | None:
        result = await self.session.execute(
            select(LearningPlan)
            .where(LearningPlan.id == plan_id)
            .options(
                selectinload(LearningPlan.items)
            )
        )

        return result.scalar_one_or_none()

    async def get_by_goal_id(
        self,
        learning_goal_id: int,
    ) -> LearningPlan | None:
        result = await self.session.execute(
            select(LearningPlan)
            .where(
                LearningPlan.learning_goal_id
                == learning_goal_id
            )
            .options(
                selectinload(LearningPlan.items)
            )
        )

        return result.scalar_one_or_none()

    async def get_by_user(
        self,
        user_id: int,
    ) -> list[LearningPlan]:
        result = await self.session.execute(
            select(LearningPlan)
            .where(LearningPlan.user_id == user_id)
            .options(
                selectinload(LearningPlan.items)
            )
            .order_by(LearningPlan.created_at.desc())
        )

        return list(result.scalars().all())

    async def create(
        self,
        *,
        user_id: int,
        learning_goal_id: int,
    ) -> LearningPlan:
        plan = LearningPlan(
            user_id=user_id,
            learning_goal_id=learning_goal_id,
            status="ACTIVE",
        )

        self.session.add(plan)

        await self.session.flush()

        return plan

    async def create_item(
        self,
        *,
        plan_id: int,
        lesson_id: int,
        position: int,
    ) -> LearningPlanItem:
        item = LearningPlanItem(
            plan_id=plan_id,
            lesson_id=lesson_id,
            position=position,
            status="PENDING",
        )

        self.session.add(item)

        await self.session.flush()

        return item

    async def update_status(
    self,
    plan: LearningPlan,
    status: str,
) -> LearningPlan:
        plan.status = status

        await self.session.flush()

        return plan

    async def get_item_by_id(
    self,
    item_id: int,
) -> LearningPlanItem | None:
        result = await self.session.execute(
            select(LearningPlanItem).where(
                LearningPlanItem.id == item_id
            )
        )

        return result.scalar_one_or_none()

    async def update_item_status(
    self,
    item: LearningPlanItem,
    status: str,
) -> LearningPlanItem:
        item.status = status

        await self.session.flush()

        return item
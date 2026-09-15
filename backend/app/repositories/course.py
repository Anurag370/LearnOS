from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.course import Course, Module


class CourseRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Course]:
        result = await self.session.execute(
            select(Course)
            .options(
                selectinload(Course.modules),
                selectinload(Course.topics),
            )
            .order_by(Course.id)
        )

        return list(result.scalars().unique().all())

    async def get_by_id(self, course_id: int) -> Course | None:
        result = await self.session.execute(
            select(Course)
            .options(
                selectinload(Course.modules)
                .selectinload(Module.lessons),
                selectinload(Course.topics),
            )
            .where(Course.id == course_id)
        )

        return result.scalars().unique().first()

    async def get_by_slug(self, slug:str)-> Course | None:
        result = await self.session.execute(
            select(Course)
            .options(
                selectinload(Course.modules)
                .selectinload(Module.lessons),
                selectinload(Course.topics)
            )
            .where(Course.slug == slug)
        )

        return result.scalars().unique().first()
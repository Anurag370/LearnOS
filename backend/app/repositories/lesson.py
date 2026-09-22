from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Lesson, Module


class LessonRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        lesson_id: int,
    ) -> Lesson | None:
        result = await self.session.execute(
            select(Lesson).where(
                Lesson.id == lesson_id
            )
        )

        return result.scalar_one_or_none()

    async def get_course_id(
        self,
        lesson_id: int,
    ) -> int | None:
        result = await self.session.execute(
            select(Module.course_id)
            .join(
                Lesson,
                Lesson.module_id == Module.id,
            )
            .where(
                Lesson.id == lesson_id
            )
        )

        return result.scalar_one_or_none()
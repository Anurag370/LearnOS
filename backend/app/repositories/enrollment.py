from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enrollment import Enrollment

class EnrollementRepository:
    def __init__(self, session:AsyncSession):
        self.session = session

    async def get_by_user_and_course(self, user_id:int, course_id:int) -> Enrollment | None:
        result = await self.session.execute(
            select(Enrollment).where(
                Enrollment.user_id == user_id,
                Enrollment.course_id == course_id,
            )
        )

        return result.scalar_one_or_none()

    async def create(self, user_id:int, course_id:int) -> Enrollment:
        enrollment = Enrollment(user_id = user_id, course_id = course_id, status="ACTIVE")
        self.session.add(enrollment)

        await self.session.commit()
        await self.session.refresh(enrollment)

        return enrollment
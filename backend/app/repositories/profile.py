from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import StudentProfile


class StudentProfileRepository:
    def __init__(self, session:AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id:int) -> StudentProfile | None:  

        result = await self.session.execute(
            select(StudentProfile)
            .where(StudentProfile.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def update(self, profile:StudentProfile,*,current_skill_level:str | None, available_study_minutes:int | None) -> StudentProfile:

        profile.current_skill_level = current_skill_level
        profile.available_study_minutes = available_study_minutes

        await self.session.flush()

        return profile
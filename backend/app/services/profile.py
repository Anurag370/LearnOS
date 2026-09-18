from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import StudentProfile
from app.repositories.profile import StudentProfileRepository


class StudentProfileService:
    def __init__(self, session:AsyncSession, repository:StudentProfileRepository):
        self.session = session
        self.repository = repository

    async def get_profile(self, user_id:int) -> StudentProfile | None:
        return await self.repository.get_by_user_id(user_id)

    async def update_profile(self, user_id:int,  current_skill_level:str | None, available_study_minutes:int | None) -> StudentProfile:
        profile = await self.repository.get_by_user_id(user_id)

        if profile is None:
            profile = StudentProfile(user_id=user_id)
            self.session.add(profile)

            await self.session.flush()

        await self.repository.update(
            profile,
            current_skill_level=current_skill_level,
            available_study_minutes=available_study_minutes
        )

        await self.session.commit()
        await self.session.refresh(profile)

        return profile
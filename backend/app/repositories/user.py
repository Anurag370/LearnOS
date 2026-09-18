from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.profile import StudentProfile


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id:int) -> User | None:

        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    async def get_by_email(self, email:str) -> User | None:

        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, eamil:str, password_hash) -> User:

        user = User(
            email = eamil,
            password_hash = password_hash,
            role = "STUDENT"
        )

        self.session.add(user)
        await self.session.flush()

        return user

    async def create_student_profile(self, user:User):

        profile = StudentProfile(user_id = user.id)
        self.session.add(profile)

        return profile
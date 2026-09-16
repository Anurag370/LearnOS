from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.auth.jwt import create_access_token


class EmailAlreadyRegisteredError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class AuthService:
    def __init__(self, session: AsyncSession, user_repository:UserRepository):

        self.session = session
        self.user_repository = user_repository

    async def register(self, email:str, password:str) -> User:
        existing_user = await self.user_repository.get_by_email(email)

        if existing_user is not None:
            raise EmailAlreadyRegisteredError

        password_hash = hash_password(password)

        user = await self.user_repository.create(email, password_hash)

        await self.user_repository.create_student_profile(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def login(self, email:str, password:str) -> str:

        user = await self.user_repository.get_by_email(email)

        if user is None:
            raise InvalidCredentialsError

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError

        access_token = create_access_token(user_id=user.id)

        return access_token
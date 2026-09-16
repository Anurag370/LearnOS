from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.user import UserRepository
from app.schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, TokenResponse
from app.services.auth import AuthService, EmailAlreadyRegisteredError, InvalidCredentialsError


router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_auth_service(session:AsyncSession = Depends(get_db)) -> AuthService:

    repository = UserRepository(session)

    return AuthService(session, repository)

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, service: AuthService = Depends(get_auth_service)):
    try:
        user = await service.register(email=data.email, password=data.password)

        return user

    except EmailAlreadyRegisteredError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

@router.post("/login", response_model=TokenResponse)
async def login(data:LoginRequest, service: AuthService = Depends(get_auth_service)):

    try:
        access_token = await service.login(email=data.email, password=data.password)

        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
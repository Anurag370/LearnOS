from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, require_student
from app.core.database import get_db
from app.models.user import User
from app.repositories.profile import StudentProfileRepository
from app.schemas.profile import StudentProfileResponse, StudentProfileUpdate
from app.services.profile import StudentProfileService


router = APIRouter(
    prefix="/profile",
    tags=["Student Profile"]
)


def get_profile_service(session:AsyncSession = Depends(get_db)) -> StudentProfileService:
    repository = StudentProfileRepository(session)

    return StudentProfileService(session, repository)

@router.get("", response_model=StudentProfileResponse)
async def get_profile(current_user:User = Depends(require_student), service:StudentProfileService = Depends(get_profile_service)):
    profile = await service.get_profile(current_user.id)

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )
    return profile

@router.put("", response_model=StudentProfileResponse)
async def update_profile(data:StudentProfileUpdate, current_user:User = Depends(require_student), service:StudentProfileService = Depends(get_profile_service)):

    return await service.update_profile(
        current_user.id,
        current_skill_level=data.current_skill_level,
        available_study_minutes=data.available_study_minutes
    )
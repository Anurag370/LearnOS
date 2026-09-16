from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.course import CourseRepository
from app.schemas.course import CourseListResponse, CourseResponse
from app.services.course import CourseService
from app.api.dependencies import get_current_user_id
from app.repositories.enrollment import EnrollementRepository
from app.schemas.enrollment import EnrollmentResponse
from app.services.enrollment import AlreadyEnrolledError, CourseNotFoundError, EnrollmentService


router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)

def get_course_service(session: AsyncSession = Depends(get_db)) -> CourseService:

    repository = CourseRepository(session)
    return CourseService(repository)

def get_enrollemnt_service(session:AsyncSession = Depends(get_db)) -> EnrollmentService:

    course_repository = CourseRepository(session)
    enrollment_repository = EnrollementRepository(session)

    return EnrollmentService(
        course_repository=course_repository,
        enrollment_repository=enrollment_repository
    )

@router.get("", response_model=list[CourseListResponse])
async def list_course(service: CourseService = Depends(get_course_service)):

    return await service.list_courses()

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, service: CourseService = Depends(get_course_service)):
    course = await service.get_course(course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course mot found"
        )
    return course


@router.post("/{course_id}/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll_in_courses(course_id: int, user_id:int = Depends(get_current_user_id), service: EnrollmentService = Depends(get_enrollemnt_service)):

    try:
        return await service.enroll(user_id, course_id)

    except CourseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Couse not found",
        )

    except AlreadyEnrolledError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already enrolled in this course"
        )


@router.get("/{course_id}/enrollment", response_model=EnrollmentResponse)
async def get_course_enrollment(course_id:int, user_id:int = Depends(get_current_user_id), service:EnrollmentService = Depends(get_enrollemnt_service)):

    enrollment = await service.get_enrollment(user_id=user_id, course_id=course_id)

    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollemnt not found"
        )

    return enrollment
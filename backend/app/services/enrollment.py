from app.models.enrollment import Enrollment
from app.repositories.course import CourseRepository
from app.repositories.enrollment import EnrollementRepository


class CourseNotFoundError(Exception):
    pass

class AlreadyEnrolledError(Exception):
    pass

class EnrollmentService:
    def __init__(self, course_repository: CourseRepository, enrollment_repository) -> None:
        self.course_repository = course_repository
        self.enrollment_repository = enrollment_repository

    async def enroll(self, user_id:int, course_id:int) -> Enrollment:

        course = await self.course_repository.get_by_id(course_id)

        if course is None:
            raise CourseNotFoundError

        existing = await self.enrollment_repository.get_by_user_and_course(user_id, course_id)

        if existing is not None:
            raise AlreadyEnrolledError

        return await self.enrollment_repository.create(user_id, course_id)

    async def get_enrollment(self, user_id:int, course_id:int) -> Enrollment | None:

        return await self.enrollment_repository.get_by_user_and_course(user_id, course_id)
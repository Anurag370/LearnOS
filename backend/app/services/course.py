from app.repositories.course import CourseRepository
from app.models.course import Course


class CourseService:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    async def list_courses(self) -> list[Course]:
        return await self.repository.get_all()

    async def get_course(self, course_id: int) -> Course | None:
        return await self.repository.get_by_id(course_id)
import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.course import Course, Lesson, Module, Topic


async def seed_dsa_course():
    async with AsyncSessionLocal() as session:
        existing = await session.scalar(
            select(Course).where(
                Course.slug == "data-structures-algorithms"
            )
        )

        if existing:
            print("DSA course already exists.")
            return

        course = Course(
            title="Data Structures & Algorithms",
            slug="data-structures-algorithms",
            description=(
                "A structured course covering fundamental "
                "data structures and algorithms."
            ),
        )

        arrays = Module(
            title="Arrays & Hashing",
            description="Fundamental array and hashing techniques.",
            position=1,
        )

        recursion = Module(
            title="Recursion",
            description="Recursive thinking, base cases, and call stacks.",
            position=2,
        )

        trees = Module(
            title="Trees",
            description="Tree structures and traversal algorithms.",
            position=3,
        )

        arrays.lessons = [
            Lesson(
                title="Array Fundamentals",
                slug="array-fundamentals",
                content=(
                    "Arrays store elements in contiguous memory locations "
                    "and support indexed access."
                ),
                position=1,
            ),
            Lesson(
                title="Hashing Fundamentals",
                slug="hashing-fundamentals",
                content=(
                    "Hash tables provide efficient average-case lookup "
                    "using a hash function."
                ),
                position=2,
            ),
        ]

        recursion.lessons = [
            Lesson(
                title="Recursion Fundamentals",
                slug="recursion-fundamentals",
                content=(
                    "Recursion is a technique where a function solves "
                    "a problem by calling itself on a smaller instance. "
                    "A recursive solution requires a base case and a "
                    "recursive case."
                ),
                position=1,
            ),
            Lesson(
                title="Call Stack",
                slug="call-stack",
                content=(
                    "Recursive function calls are stored on the call "
                    "stack. Each call creates a new stack frame."
                ),
                position=2,
            ),
        ]

        trees.lessons = [
            Lesson(
                title="Tree Fundamentals",
                slug="tree-fundamentals",
                content=(
                    "A tree is a hierarchical data structure consisting "
                    "of nodes connected by edges."
                ),
                position=1,
            ),
        ]

        course.modules = [
            arrays,
            recursion,
            trees,
        ]

        course.topics = [
            Topic(
                name="Arrays",
                slug="arrays",
                description="Array data structures and common operations.",
            ),
            Topic(
                name="Hashing",
                slug="hashing",
                description="Hash tables and hash-based techniques.",
            ),
            Topic(
                name="Recursion",
                slug="recursion",
                description="Recursive problem solving and call stacks.",
            ),
            Topic(
                name="Trees",
                slug="trees",
                description="Tree structures and traversal.",
            ),
        ]

        session.add(course)
        await session.commit()

        print("DSA course created successfully.")


if __name__ == "__main__":
    asyncio.run(seed_dsa_course())
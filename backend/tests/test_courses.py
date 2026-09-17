from app.models.course import Course, Lesson, Module, Topic

COURSES_PREFIX = "/api/v1/courses"


async def seed_course(session, title: str = "Data Structures", slug: str = "data-structures") -> Course:
    course = Course(
        title=title,
        slug=slug,
        description="Learn DSA from scratch",
    )
    course.modules = [
        Module(
            title="Arrays",
            position=1,
            lessons=[
                Lesson(
                    title="Intro to Arrays",
                    slug="intro-arrays",
                    content="The beginning.",
                    position=1,
                )
            ],
        )
    ]
    course.topics = [
        Topic(name="Arrays", slug="arrays", description="Arrays deep-dive")
    ]

    session.add(course)
    await session.commit()
    await session.refresh(course)

    return course


async def test_list_courses_when_empty(client):
    response = await client.get(COURSES_PREFIX)

    assert response.status_code == 200
    assert response.json() == []


async def test_list_courses_returns_seeded(client, session):
    course = await seed_course(session, title="Linked Lists", slug="linked-lists")

    response = await client.get(COURSES_PREFIX)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == course.id
    assert data[0]["title"] == "Linked Lists"
    assert data[0]["slug"] == "linked-lists"


async def test_get_course_detail_includes_nested_content(client, session):
    course = await seed_course(session)

    response = await client.get(f"{COURSES_PREFIX}/{course.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == course.id
    assert len(data["modules"]) == 1
    assert data["modules"][0]["title"] == "Arrays"
    assert len(data["modules"][0]["lessons"]) == 1
    assert data["modules"][0]["lessons"][0]["slug"] == "intro-arrays"
    assert len(data["topics"]) == 1
    assert data["topics"][0]["name"] == "Arrays"


async def test_get_course_not_found(client):
    response = await client.get(f"{COURSES_PREFIX}/999")

    assert response.status_code == 404
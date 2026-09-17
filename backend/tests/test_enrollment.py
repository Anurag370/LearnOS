from app.models.course import Course

COURSES_PREFIX = "/api/v1/courses"


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def seed_course(session, slug: str = "enrollment-course") -> Course:
    course = Course(title="Enrollment Course", slug=slug)

    session.add(course)
    await session.commit()
    await session.refresh(course)

    return course


async def test_enroll_creates_enrollment_for_current_user(client, session, user_token):
    course = await seed_course(session)
    token = await user_token("student@example.com")

    me = await client.get("/api/v1/auth/me", headers=_auth(token))
    user_id = me.json()["id"]

    response = await client.post(f"{COURSES_PREFIX}/{course.id}/enroll", headers=_auth(token))

    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user_id
    assert data["course_id"] == course.id
    assert data["status"] == "ACTIVE"


async def test_enroll_returns_409_when_already_enrolled(client, session, user_token):
    course = await seed_course(session)
    token = await user_token("repeat@example.com")

    first = await client.post(f"{COURSES_PREFIX}/{course.id}/enroll", headers=_auth(token))
    assert first.status_code == 201

    second = await client.post(f"{COURSES_PREFIX}/{course.id}/enroll", headers=_auth(token))

    assert second.status_code == 409


async def test_enroll_returns_404_for_missing_course(client, user_token):
    token = await user_token("ghost@example.com")

    response = await client.post(f"{COURSES_PREFIX}/999/enroll", headers=_auth(token))

    assert response.status_code == 404


async def test_enroll_requires_authentication(client, session):
    course = await seed_course(session)

    response = await client.post(f"{COURSES_PREFIX}/{course.id}/enroll")

    assert response.status_code == 401


async def test_get_enrollment_when_enrolled(client, session, user_token):
    course = await seed_course(session)
    token = await user_token("enrolled@example.com")

    await client.post(f"{COURSES_PREFIX}/{course.id}/enroll", headers=_auth(token))

    response = await client.get(f"{COURSES_PREFIX}/{course.id}/enrollment", headers=_auth(token))

    assert response.status_code == 200
    data = response.json()
    assert data["course_id"] == course.id
    assert data["status"] == "ACTIVE"


async def test_get_enrollment_not_found(client, session, user_token):
    course = await seed_course(session)
    token = await user_token("not-enrolled@example.com")

    response = await client.get(f"{COURSES_PREFIX}/{course.id}/enrollment", headers=_auth(token))

    assert response.status_code == 404
from app.models.course import Course, Lesson, Module
from app.models.learning_goal import LearningGoal

PLANS_PREFIX = "/api/v1/learning-plans"
GOALS_PREFIX = "/api/v1/learning-goals"

_COUNTER = 0

GOAL_PAYLOAD = {
    "description": "Learn the plan course",
    "target_date": "2026-12-31",
    "desired_outcome": "Be proficient",
}


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def seed_course_with_lessons(session):
    global _COUNTER

    _COUNTER += 1

    course = Course(
        title="Plan Course",
        slug=f"plan-course-{_COUNTER}",
    )

    session.add(course)
    await session.commit()
    await session.refresh(course)

    module = Module(
        course_id=course.id,
        title="Module 1",
        position=1,
    )

    session.add(module)
    await session.commit()
    await session.refresh(module)

    lesson_one = Lesson(
        module_id=module.id,
        title="Lesson 1",
        slug=f"plan-l1-{_COUNTER}",
        position=1,
    )

    lesson_two = Lesson(
        module_id=module.id,
        title="Lesson 2",
        slug=f"plan-l2-{_COUNTER}",
        position=2,
    )

    session.add_all([lesson_one, lesson_two])
    await session.commit()
    await session.refresh(lesson_one)
    await session.refresh(lesson_two)

    return course, lesson_one, lesson_two


async def enroll(client, token: str, course_id: int):
    response = await client.post(
        f"/api/v1/courses/{course_id}/enroll",
        headers=_auth(token),
    )
    assert response.status_code == 201


async def create_goal(client, token: str, course_id: int) -> int:
    await enroll(client, token, course_id)

    response = await client.post(
        GOALS_PREFIX,
        json={"course_id": course_id, **GOAL_PAYLOAD},
        headers=_auth(token),
    )
    assert response.status_code == 201

    return response.json()["id"]


def plan_payload(goal_id: int, lesson_ids: list[int]) -> dict:
    return {
        "learning_goal_id": goal_id,
        "items": [
            {"lesson_id": lesson_id, "position": position}
            for position, lesson_id in enumerate(lesson_ids, start=1)
        ],
    }


async def create_plan(client, token: str, goal_id: int, lesson_ids: list[int]) -> dict:
    response = await client.post(
        PLANS_PREFIX,
        json=plan_payload(goal_id, lesson_ids),
        headers=_auth(token),
    )
    assert response.status_code == 201

    return response.json()


async def test_list_learning_plans(client, session, user_token):
    course, lesson_one, lesson_two = await seed_course_with_lessons(session)
    token = await user_token("plan-list-owner@example.com")
    goal_id = await create_goal(client, token, course.id)
    plan = await create_plan(client, token, goal_id, [lesson_one.id, lesson_two.id])

    response = await client.get(PLANS_PREFIX, headers=_auth(token))

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == plan["id"]
    assert data[0]["learning_goal_id"] == goal_id
    assert len(data[0]["items"]) == 2


async def test_list_learning_plans_returns_only_current_user(
    client, session, user_token
):
    course, lesson_one, _ = await seed_course_with_lessons(session)
    owner = await user_token("plan-list-owner@example.com")
    stranger = await user_token("plan-list-stranger@example.com")

    owner_goal_id = await create_goal(client, owner, course.id)
    await create_plan(client, owner, owner_goal_id, [lesson_one.id])

    stranger_goal_id = await create_goal(client, stranger, course.id)
    await create_plan(client, stranger, stranger_goal_id, [lesson_one.id])

    response = await client.get(PLANS_PREFIX, headers=_auth(owner))

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["learning_goal_id"] == owner_goal_id


async def test_list_learning_plans_returns_empty(client, session, user_token):
    token = await user_token("plan-list-empty@example.com")

    response = await client.get(PLANS_PREFIX, headers=_auth(token))

    assert response.status_code == 200
    assert response.json() == []


async def test_list_learning_plans_requires_authentication(client):
    response = await client.get(PLANS_PREFIX)

    assert response.status_code == 401


async def test_create_learning_plan(client, session, user_token):
    course, lesson_one, lesson_two = await seed_course_with_lessons(session)
    token = await user_token("plan-creator@example.com")
    goal_id = await create_goal(client, token, course.id)

    response = await client.post(
        PLANS_PREFIX,
        json=plan_payload(goal_id, [lesson_one.id, lesson_two.id]),
        headers=_auth(token),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["learning_goal_id"] == goal_id
    assert data["status"] == "ACTIVE"
    assert len(data["items"]) == 2
    assert data["items"][0]["lesson_id"] == lesson_one.id
    assert data["items"][0]["position"] == 1
    assert data["items"][0]["status"] == "PENDING"
    assert data["items"][1]["lesson_id"] == lesson_two.id
    assert data["items"][1]["position"] == 2
    assert data["items"][1]["status"] == "PENDING"


async def test_create_learning_plan_requires_authentication(client, session, user_token):
    course, lesson_one, _ = await seed_course_with_lessons(session)
    token = await user_token("plan-no-auth@example.com")

    me = await client.get("/api/v1/auth/me", headers=_auth(token))
    user_id = me.json()["id"]

    goal = LearningGoal(
        user_id=user_id,
        course_id=course.id,
        description="Seeded goal",
    )
    session.add(goal)
    await session.commit()
    await session.refresh(goal)

    response = await client.post(
        PLANS_PREFIX,
        json=plan_payload(goal.id, [lesson_one.id]),
    )

    assert response.status_code == 401


async def test_create_plan_returns_404_for_missing_goal(client, session, user_token):
    course, lesson_one, _ = await seed_course_with_lessons(session)
    token = await user_token("plan-missing-goal@example.com")
    await enroll(client, token, course.id)

    response = await client.post(
        PLANS_PREFIX,
        json=plan_payload(999, [lesson_one.id]),
        headers=_auth(token),
    )

    assert response.status_code == 404


async def test_create_plan_returns_409_for_duplicate_plan(
    client, session, user_token
):
    course, lesson_one, _ = await seed_course_with_lessons(session)
    token = await user_token("plan-duplicate@example.com")
    goal_id = await create_goal(client, token, course.id)

    await create_plan(client, token, goal_id, [lesson_one.id])

    response = await client.post(
        PLANS_PREFIX,
        json=plan_payload(goal_id, [lesson_one.id]),
        headers=_auth(token),
    )

    assert response.status_code == 409


async def test_create_plan_returns_404_for_missing_lesson(
    client, session, user_token
):
    course, _, _ = await seed_course_with_lessons(session)
    token = await user_token("plan-missing-lesson@example.com")
    goal_id = await create_goal(client, token, course.id)

    response = await client.post(
        PLANS_PREFIX,
        json=plan_payload(goal_id, [999]),
        headers=_auth(token),
    )

    assert response.status_code == 404


async def test_create_plan_returns_422_for_lesson_not_in_goal_course(
    client, session, user_token
):
    course, _, _ = await seed_course_with_lessons(session)
    other_course, other_lesson, _ = await seed_course_with_lessons(session)
    token = await user_token("plan-wrong-course@example.com")
    goal_id = await create_goal(client, token, course.id)

    await enroll(client, token, other_course.id)

    response = await client.post(
        PLANS_PREFIX,
        json=plan_payload(goal_id, [other_lesson.id]),
        headers=_auth(token),
    )

    assert response.status_code == 422


async def test_create_plan_returns_422_for_duplicate_positions(
    client, session, user_token
):
    course, lesson_one, lesson_two = await seed_course_with_lessons(session)
    token = await user_token("plan-bad-positions@example.com")
    goal_id = await create_goal(client, token, course.id)

    response = await client.post(
        PLANS_PREFIX,
        json={
            "learning_goal_id": goal_id,
            "items": [
                {"lesson_id": lesson_one.id, "position": 1},
                {"lesson_id": lesson_two.id, "position": 1},
            ],
        },
        headers=_auth(token),
    )

    assert response.status_code == 422


async def test_get_learning_plan(client, session, user_token):
    course, lesson_one, lesson_two = await seed_course_with_lessons(session)
    token = await user_token("plan-getter@example.com")
    goal_id = await create_goal(client, token, course.id)
    plan = await create_plan(client, token, goal_id, [lesson_one.id, lesson_two.id])

    response = await client.get(
        f"{PLANS_PREFIX}/{plan['id']}",
        headers=_auth(token),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == plan["id"]
    assert data["learning_goal_id"] == goal_id
    assert len(data["items"]) == 2


async def test_get_plan_returns_404_for_other_user(client, session, user_token):
    course, lesson_one, _ = await seed_course_with_lessons(session)
    owner = await user_token("plan-owner@example.com")
    stranger = await user_token("plan-stranger@example.com")
    goal_id = await create_goal(client, owner, course.id)
    plan = await create_plan(client, owner, goal_id, [lesson_one.id])

    response = await client.get(
        f"{PLANS_PREFIX}/{plan['id']}",
        headers=_auth(stranger),
    )

    assert response.status_code == 404


async def test_get_learning_plan_by_goal(client, session, user_token):
    course, lesson_one, _ = await seed_course_with_lessons(session)
    token = await user_token("plan-by-goal@example.com")
    goal_id = await create_goal(client, token, course.id)
    plan = await create_plan(client, token, goal_id, [lesson_one.id])

    response = await client.get(
        f"{PLANS_PREFIX}/goal/{goal_id}",
        headers=_auth(token),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == plan["id"]
    assert data["learning_goal_id"] == goal_id


async def test_get_plan_by_goal_returns_404_for_other_user(
    client, session, user_token
):
    course, lesson_one, _ = await seed_course_with_lessons(session)
    owner = await user_token("plan-by-goal-owner@example.com")
    stranger = await user_token("plan-by-goal-stranger@example.com")
    goal_id = await create_goal(client, owner, course.id)
    await create_plan(client, owner, goal_id, [lesson_one.id])

    response = await client.get(
        f"{PLANS_PREFIX}/goal/{goal_id}",
        headers=_auth(stranger),
    )

    assert response.status_code == 404


async def test_update_learning_plan_status(client, session, user_token):
    course, lesson_one, _ = await seed_course_with_lessons(session)
    token = await user_token("plan-status@example.com")
    goal_id = await create_goal(client, token, course.id)
    plan = await create_plan(client, token, goal_id, [lesson_one.id])

    response = await client.put(
        f"{PLANS_PREFIX}/{plan['id']}/status",
        json={"status": "COMPLETED"},
        headers=_auth(token),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == plan["id"]
    assert data["status"] == "COMPLETED"
    assert len(data["items"]) == 1


async def test_update_plan_status_returns_422_for_invalid_status(
    client, session, user_token
):
    course, lesson_one, _ = await seed_course_with_lessons(session)
    token = await user_token("plan-bad-status@example.com")
    goal_id = await create_goal(client, token, course.id)
    plan = await create_plan(client, token, goal_id, [lesson_one.id])

    response = await client.put(
        f"{PLANS_PREFIX}/{plan['id']}/status",
        json={"status": "BOGUS"},
        headers=_auth(token),
    )

    assert response.status_code == 422


async def test_update_plan_status_returns_404_for_other_user(
    client, session, user_token
):
    course, lesson_one, _ = await seed_course_with_lessons(session)
    owner = await user_token("plan-status-owner@example.com")
    stranger = await user_token("plan-status-stranger@example.com")
    goal_id = await create_goal(client, owner, course.id)
    plan = await create_plan(client, owner, goal_id, [lesson_one.id])

    response = await client.put(
        f"{PLANS_PREFIX}/{plan['id']}/status",
        json={"status": "COMPLETED"},
        headers=_auth(stranger),
    )

    assert response.status_code == 404


async def test_update_learning_plan_item_status(client, session, user_token):
    course, lesson_one, _ = await seed_course_with_lessons(session)
    token = await user_token("plan-item-status@example.com")
    goal_id = await create_goal(client, token, course.id)
    plan = await create_plan(client, token, goal_id, [lesson_one.id])
    item_id = plan["items"][0]["id"]

    response = await client.put(
        f"{PLANS_PREFIX}/items/{item_id}/status",
        json={"status": "IN_PROGRESS"},
        headers=_auth(token),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["status"] == "IN_PROGRESS"


async def test_update_plan_item_status_returns_422_for_invalid_status(
    client, session, user_token
):
    course, lesson_one, _ = await seed_course_with_lessons(session)
    token = await user_token("plan-item-bad-status@example.com")
    goal_id = await create_goal(client, token, course.id)
    plan = await create_plan(client, token, goal_id, [lesson_one.id])
    item_id = plan["items"][0]["id"]

    response = await client.put(
        f"{PLANS_PREFIX}/items/{item_id}/status",
        json={"status": "BOGUS"},
        headers=_auth(token),
    )

    assert response.status_code == 422


async def test_update_plan_item_status_returns_404_for_other_user(
    client, session, user_token
):
    course, lesson_one, _ = await seed_course_with_lessons(session)
    owner = await user_token("plan-item-owner@example.com")
    stranger = await user_token("plan-item-stranger@example.com")
    goal_id = await create_goal(client, owner, course.id)
    plan = await create_plan(client, owner, goal_id, [lesson_one.id])
    item_id = plan["items"][0]["id"]

    response = await client.put(
        f"{PLANS_PREFIX}/items/{item_id}/status",
        json={"status": "COMPLETED"},
        headers=_auth(stranger),
    )

    assert response.status_code == 404
from app.models.course import Course

GOALS_PREFIX = "/api/v1/learning-goals"


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def seed_course(session, slug: str = "goals-course") -> Course:
    course = Course(title="Goals Course", slug=slug)

    session.add(course)
    await session.commit()
    await session.refresh(course)

    return course


GOAL_PAYLOAD = {
    "description": "Learn Python fundamentals",
    "target_date": "2026-12-31",
    "desired_outcome": "Comfortable building scripts",
}


async def test_create_learning_goal(client, session, user_token):
    course = await seed_course(session)
    token = await user_token("goal-creator@example.com")

    response = await client.post(
        GOALS_PREFIX,
        json={"course_id": course.id, **GOAL_PAYLOAD},
        headers=_auth(token),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["course_id"] == course.id
    assert data["description"] == GOAL_PAYLOAD["description"]
    assert data["target_date"] == GOAL_PAYLOAD["target_date"]
    assert data["desired_outcome"] == GOAL_PAYLOAD["desired_outcome"]
    assert data["status"] == "in_progress"


async def test_create_learning_goal_returns_404_for_missing_course(
    client, user_token
):
    token = await user_token("goal-ghost@example.com")

    response = await client.post(
        GOALS_PREFIX,
        json={"course_id": 999, **GOAL_PAYLOAD},
        headers=_auth(token),
    )

    assert response.status_code == 404


async def test_create_learning_goal_requires_authentication(client, session):
    course = await seed_course(session)

    response = await client.post(
        GOALS_PREFIX,
        json={"course_id": course.id, **GOAL_PAYLOAD},
    )

    assert response.status_code == 401


async def test_list_learning_goals_returns_only_current_user(client, session, user_token):
    course = await seed_course(session)
    token = await user_token("list-owner@example.com")

    await client.post(GOALS_PREFIX, json={"course_id": course.id, **GOAL_PAYLOAD}, headers=_auth(token))

    me = await client.get("/api/v1/auth/me", headers=_auth(token))
    user_id = me.json()["id"]

    response = await client.get(GOALS_PREFIX, headers=_auth(token))

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == user_id
    assert data[0]["course_id"] == course.id


async def test_update_learning_goal(client, session, user_token):
    course = await seed_course(session)
    token = await user_token("goal-updater@example.com")

    created = await client.post(
        GOALS_PREFIX,
        json={"course_id": course.id, **GOAL_PAYLOAD},
        headers=_auth(token),
    )
    goal_id = created.json()["id"]

    response = await client.put(
        f"{GOALS_PREFIX}/{goal_id}",
        json={"desired_outcome": "Aimed outcome updated"},
        headers=_auth(token),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == goal_id
    assert data["description"] == GOAL_PAYLOAD["description"]
    assert data["desired_outcome"] == "Aimed outcome updated"


async def test_update_learning_goal_returns_404_for_other_user_goal(
    client, session, user_token
):
    course = await seed_course(session)
    owner_token = await user_token("goal-owner@example.com")
    other_user_token = await user_token("goal-stranger@example.com")

    created = await client.post(
        GOALS_PREFIX,
        json={"course_id": course.id, **GOAL_PAYLOAD},
        headers=_auth(owner_token),
    )
    goal_id = created.json()["id"]

    response = await client.put(
        f"{GOALS_PREFIX}/{goal_id}",
        json={"description": "Hijacked description"},
        headers=_auth(other_user_token),
    )

    assert response.status_code == 404


async def test_update_learning_goal_returns_404_for_missing_goal(client, user_token):
    token = await user_token("goal-missing@example.com")

    response = await client.put(
        f"{GOALS_PREFIX}/999",
        json={"description": "Nope"},
        headers=_auth(token),
    )

    assert response.status_code == 404
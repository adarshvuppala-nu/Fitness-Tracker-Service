from fastapi.testclient import TestClient


def test_create_workout_session(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "athlete", "email": "athlete@example.com"}
    )
    user_id = user_response.json()["id"]

    response = client.post(
        "/api/v1/workout-sessions/",
        json={
            "user_id": user_id,
            "type": "running",
            "duration": 30,
            "calories_burned": 250.0,
            "date": "2025-10-27",
            "notes": "Morning run"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "running"
    assert data["duration"] == 30
    assert data["calories_burned"] == 250.0
    assert "id" in data


def test_create_workout_session_invalid_user(client: TestClient):
    response = client.post(
        "/api/v1/workout-sessions/",
        json={
            "user_id": "00000000-0000-0000-0000-000000000000",
            "type": "running",
            "duration": 30,
            "calories_burned": 250.0,
            "date": "2025-10-27"
        }
    )
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


def test_get_workout_session(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "athlete", "email": "athlete@example.com"}
    )
    user_id = user_response.json()["id"]

    create_response = client.post(
        "/api/v1/workout-sessions/",
        json={
            "user_id": user_id,
            "type": "cycling",
            "duration": 45,
            "calories_burned": 300.0,
            "date": "2025-10-27"
        }
    )
    workout_id = create_response.json()["id"]

    response = client.get(f"/api/v1/workout-sessions/{workout_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "cycling"
    assert data["duration"] == 45


def test_get_workout_session_not_found(client: TestClient):
    response = client.get("/api/v1/workout-sessions/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_workout_sessions(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "athlete", "email": "athlete@example.com"}
    )
    user_id = user_response.json()["id"]

    client.post(
        "/api/v1/workout-sessions/",
        json={
            "user_id": user_id,
            "type": "running",
            "duration": 30,
            "calories_burned": 250.0,
            "date": "2025-10-27"
        }
    )
    client.post(
        "/api/v1/workout-sessions/",
        json={
            "user_id": user_id,
            "type": "cycling",
            "duration": 45,
            "calories_burned": 300.0,
            "date": "2025-10-28"
        }
    )

    response = client.get("/api/v1/workout-sessions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_workout_sessions_by_user(client: TestClient):
    user1_response = client.post(
        "/api/v1/users/",
        json={"username": "user1", "email": "user1@example.com"}
    )
    user1_id = user1_response.json()["id"]

    user2_response = client.post(
        "/api/v1/users/",
        json={"username": "user2", "email": "user2@example.com"}
    )
    user2_id = user2_response.json()["id"]

    client.post(
        "/api/v1/workout-sessions/",
        json={
            "user_id": user1_id,
            "type": "running",
            "duration": 30,
            "calories_burned": 250.0,
            "date": "2025-10-27"
        }
    )
    client.post(
        "/api/v1/workout-sessions/",
        json={
            "user_id": user2_id,
            "type": "cycling",
            "duration": 45,
            "calories_burned": 300.0,
            "date": "2025-10-27"
        }
    )

    response = client.get(f"/api/v1/workout-sessions/?user_id={user1_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["type"] == "running"


def test_update_workout_session(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "athlete", "email": "athlete@example.com"}
    )
    user_id = user_response.json()["id"]

    create_response = client.post(
        "/api/v1/workout-sessions/",
        json={
            "user_id": user_id,
            "type": "running",
            "duration": 30,
            "calories_burned": 250.0,
            "date": "2025-10-27"
        }
    )
    workout_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/workout-sessions/{workout_id}",
        json={"duration": 45, "calories_burned": 350.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["duration"] == 45
    assert data["calories_burned"] == 350.0


def test_delete_workout_session(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "athlete", "email": "athlete@example.com"}
    )
    user_id = user_response.json()["id"]

    create_response = client.post(
        "/api/v1/workout-sessions/",
        json={
            "user_id": user_id,
            "type": "running",
            "duration": 30,
            "calories_burned": 250.0,
            "date": "2025-10-27"
        }
    )
    workout_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/workout-sessions/{workout_id}")
    assert response.status_code == 204

    get_response = client.get(f"/api/v1/workout-sessions/{workout_id}")
    assert get_response.status_code == 404

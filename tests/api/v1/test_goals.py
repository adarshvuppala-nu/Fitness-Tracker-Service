from fastapi.testclient import TestClient


def test_create_fitness_goal(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "goalseeker", "email": "goalseeker@example.com"}
    )
    user_id = user_response.json()["id"]

    response = client.post(
        "/api/v1/fitness-goals/",
        json={
            "user_id": user_id,
            "goal_type": "weight_loss",
            "target_value": 75.0,
            "current_value": 85.0,
            "unit": "kg",
            "deadline": "2026-01-31"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["goal_type"] == "weight_loss"
    assert data["target_value"] == 75.0
    assert data["current_value"] == 85.0
    assert data["status"] == "active"
    assert "id" in data


def test_create_fitness_goal_invalid_user(client: TestClient):
    response = client.post(
        "/api/v1/fitness-goals/",
        json={
            "user_id": "00000000-0000-0000-0000-000000000000",
            "goal_type": "weight_loss",
            "target_value": 75.0,
            "unit": "kg",
            "deadline": "2026-01-31"
        }
    )
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


def test_get_fitness_goal(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "goalseeker", "email": "goalseeker@example.com"}
    )
    user_id = user_response.json()["id"]

    create_response = client.post(
        "/api/v1/fitness-goals/",
        json={
            "user_id": user_id,
            "goal_type": "muscle_gain",
            "target_value": 80.0,
            "current_value": 75.0,
            "unit": "kg",
            "deadline": "2026-06-30"
        }
    )
    goal_id = create_response.json()["id"]

    response = client.get(f"/api/v1/fitness-goals/{goal_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["goal_type"] == "muscle_gain"
    assert data["target_value"] == 80.0


def test_get_fitness_goal_not_found(client: TestClient):
    response = client.get("/api/v1/fitness-goals/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_fitness_goals(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "goalseeker", "email": "goalseeker@example.com"}
    )
    user_id = user_response.json()["id"]

    client.post(
        "/api/v1/fitness-goals/",
        json={
            "user_id": user_id,
            "goal_type": "weight_loss",
            "target_value": 75.0,
            "unit": "kg",
            "deadline": "2026-01-31"
        }
    )
    client.post(
        "/api/v1/fitness-goals/",
        json={
            "user_id": user_id,
            "goal_type": "muscle_gain",
            "target_value": 80.0,
            "unit": "kg",
            "deadline": "2026-06-30"
        }
    )

    response = client.get("/api/v1/fitness-goals/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_fitness_goals_by_user(client: TestClient):
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
        "/api/v1/fitness-goals/",
        json={
            "user_id": user1_id,
            "goal_type": "weight_loss",
            "target_value": 75.0,
            "unit": "kg",
            "deadline": "2026-01-31"
        }
    )
    client.post(
        "/api/v1/fitness-goals/",
        json={
            "user_id": user2_id,
            "goal_type": "muscle_gain",
            "target_value": 80.0,
            "unit": "kg",
            "deadline": "2026-06-30"
        }
    )

    response = client.get(f"/api/v1/fitness-goals/?user_id={user1_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["goal_type"] == "weight_loss"


def test_list_fitness_goals_by_status(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "goalseeker", "email": "goalseeker@example.com"}
    )
    user_id = user_response.json()["id"]

    create_response = client.post(
        "/api/v1/fitness-goals/",
        json={
            "user_id": user_id,
            "goal_type": "weight_loss",
            "target_value": 75.0,
            "unit": "kg",
            "deadline": "2026-01-31"
        }
    )
    goal_id = create_response.json()["id"]

    client.put(
        f"/api/v1/fitness-goals/{goal_id}",
        json={"status": "completed"}
    )

    response = client.get(f"/api/v1/fitness-goals/?user_id={user_id}&status=completed")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "completed"


def test_update_fitness_goal(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "goalseeker", "email": "goalseeker@example.com"}
    )
    user_id = user_response.json()["id"]

    create_response = client.post(
        "/api/v1/fitness-goals/",
        json={
            "user_id": user_id,
            "goal_type": "weight_loss",
            "target_value": 75.0,
            "current_value": 85.0,
            "unit": "kg",
            "deadline": "2026-01-31"
        }
    )
    goal_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/fitness-goals/{goal_id}",
        json={"current_value": 80.0, "status": "active"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["current_value"] == 80.0
    assert data["status"] == "active"


def test_delete_fitness_goal(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "goalseeker", "email": "goalseeker@example.com"}
    )
    user_id = user_response.json()["id"]

    create_response = client.post(
        "/api/v1/fitness-goals/",
        json={
            "user_id": user_id,
            "goal_type": "weight_loss",
            "target_value": 75.0,
            "unit": "kg",
            "deadline": "2026-01-31"
        }
    )
    goal_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/fitness-goals/{goal_id}")
    assert response.status_code == 204

    get_response = client.get(f"/api/v1/fitness-goals/{goal_id}")
    assert get_response.status_code == 404

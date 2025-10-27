from fastapi.testclient import TestClient


def test_create_progress_metric(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "tracker", "email": "tracker@example.com"}
    )
    user_id = user_response.json()["id"]

    response = client.post(
        "/api/v1/progress-metrics/",
        json={
            "user_id": user_id,
            "metric": "weight",
            "value": 82.5,
            "unit": "kg",
            "date": "2025-10-27",
            "notes": "Weekly weigh-in"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["metric"] == "weight"
    assert data["value"] == 82.5
    assert data["unit"] == "kg"
    assert "id" in data


def test_create_progress_metric_invalid_user(client: TestClient):
    response = client.post(
        "/api/v1/progress-metrics/",
        json={
            "user_id": "00000000-0000-0000-0000-000000000000",
            "metric": "weight",
            "value": 82.5,
            "unit": "kg",
            "date": "2025-10-27"
        }
    )
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


def test_get_progress_metric(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "tracker", "email": "tracker@example.com"}
    )
    user_id = user_response.json()["id"]

    create_response = client.post(
        "/api/v1/progress-metrics/",
        json={
            "user_id": user_id,
            "metric": "body_fat_percentage",
            "value": 18.5,
            "unit": "percent",
            "date": "2025-10-27"
        }
    )
    progress_id = create_response.json()["id"]

    response = client.get(f"/api/v1/progress-metrics/{progress_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["metric"] == "body_fat_percentage"
    assert data["value"] == 18.5


def test_get_progress_metric_not_found(client: TestClient):
    response = client.get("/api/v1/progress-metrics/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_progress_metrics(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "tracker", "email": "tracker@example.com"}
    )
    user_id = user_response.json()["id"]

    client.post(
        "/api/v1/progress-metrics/",
        json={
            "user_id": user_id,
            "metric": "weight",
            "value": 82.5,
            "unit": "kg",
            "date": "2025-10-20"
        }
    )
    client.post(
        "/api/v1/progress-metrics/",
        json={
            "user_id": user_id,
            "metric": "weight",
            "value": 81.8,
            "unit": "kg",
            "date": "2025-10-27"
        }
    )

    response = client.get("/api/v1/progress-metrics/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_progress_metrics_by_user(client: TestClient):
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
        "/api/v1/progress-metrics/",
        json={
            "user_id": user1_id,
            "metric": "weight",
            "value": 82.5,
            "unit": "kg",
            "date": "2025-10-27"
        }
    )
    client.post(
        "/api/v1/progress-metrics/",
        json={
            "user_id": user2_id,
            "metric": "weight",
            "value": 75.0,
            "unit": "kg",
            "date": "2025-10-27"
        }
    )

    response = client.get(f"/api/v1/progress-metrics/?user_id={user1_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["value"] == 82.5


def test_list_progress_metrics_by_metric_type(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "tracker", "email": "tracker@example.com"}
    )
    user_id = user_response.json()["id"]

    client.post(
        "/api/v1/progress-metrics/",
        json={
            "user_id": user_id,
            "metric": "weight",
            "value": 82.5,
            "unit": "kg",
            "date": "2025-10-27"
        }
    )
    client.post(
        "/api/v1/progress-metrics/",
        json={
            "user_id": user_id,
            "metric": "body_fat_percentage",
            "value": 18.5,
            "unit": "percent",
            "date": "2025-10-27"
        }
    )

    response = client.get(f"/api/v1/progress-metrics/?user_id={user_id}&metric=weight")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["metric"] == "weight"


def test_update_progress_metric(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "tracker", "email": "tracker@example.com"}
    )
    user_id = user_response.json()["id"]

    create_response = client.post(
        "/api/v1/progress-metrics/",
        json={
            "user_id": user_id,
            "metric": "weight",
            "value": 82.5,
            "unit": "kg",
            "date": "2025-10-27"
        }
    )
    progress_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/progress-metrics/{progress_id}",
        json={"value": 82.0, "notes": "Corrected measurement"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["value"] == 82.0
    assert data["notes"] == "Corrected measurement"


def test_delete_progress_metric(client: TestClient):
    user_response = client.post(
        "/api/v1/users/",
        json={"username": "tracker", "email": "tracker@example.com"}
    )
    user_id = user_response.json()["id"]

    create_response = client.post(
        "/api/v1/progress-metrics/",
        json={
            "user_id": user_id,
            "metric": "weight",
            "value": 82.5,
            "unit": "kg",
            "date": "2025-10-27"
        }
    )
    progress_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/progress-metrics/{progress_id}")
    assert response.status_code == 204

    get_response = client.get(f"/api/v1/progress-metrics/{progress_id}")
    assert get_response.status_code == 404

from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    response = client.post(
        "/api/v1/users/",
        json={"username": "testuser", "email": "test@example.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_user_duplicate_username(client: TestClient):
    client.post(
        "/api/v1/users/",
        json={"username": "testuser", "email": "test1@example.com"}
    )
    response = client.post(
        "/api/v1/users/",
        json={"username": "testuser", "email": "test2@example.com"}
    )
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]


def test_create_user_duplicate_email(client: TestClient):
    client.post(
        "/api/v1/users/",
        json={"username": "testuser1", "email": "test@example.com"}
    )
    response = client.post(
        "/api/v1/users/",
        json={"username": "testuser2", "email": "test@example.com"}
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_get_user(client: TestClient):
    create_response = client.post(
        "/api/v1/users/",
        json={"username": "testuser", "email": "test@example.com"}
    )
    user_id = create_response.json()["id"]

    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_get_user_not_found(client: TestClient):
    response = client.get("/api/v1/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_users(client: TestClient):
    client.post(
        "/api/v1/users/",
        json={"username": "user1", "email": "user1@example.com"}
    )
    client.post(
        "/api/v1/users/",
        json={"username": "user2", "email": "user2@example.com"}
    )

    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["username"] == "user1"
    assert data[1]["username"] == "user2"


def test_list_users_pagination(client: TestClient):
    for i in range(5):
        client.post(
            "/api/v1/users/",
            json={"username": f"user{i}", "email": f"user{i}@example.com"}
        )

    response = client.get("/api/v1/users/?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["username"] == "user2"
    assert data[1]["username"] == "user3"


def test_update_user(client: TestClient):
    create_response = client.post(
        "/api/v1/users/",
        json={"username": "testuser", "email": "test@example.com"}
    )
    user_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/users/{user_id}",
        json={"username": "updateduser", "email": "updated@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"
    assert data["email"] == "updated@example.com"


def test_update_user_not_found(client: TestClient):
    response = client.put(
        "/api/v1/users/00000000-0000-0000-0000-000000000000",
        json={"username": "updated"}
    )
    assert response.status_code == 404


def test_delete_user(client: TestClient):
    create_response = client.post(
        "/api/v1/users/",
        json={"username": "testuser", "email": "test@example.com"}
    )
    user_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204

    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404


def test_delete_user_not_found(client: TestClient):
    response = client.delete("/api/v1/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

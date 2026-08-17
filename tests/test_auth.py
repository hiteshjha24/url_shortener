from fastapi.testclient import TestClient


def test_register_and_login_user(client: TestClient):
    """A new user can register and then log in with the same credentials."""
    payload = {
        "email": "newuser@example.com",
        "password": "StrongPass123!",
    }

    register = client.post("/api/v1/auth/register", json=payload)
    assert register.status_code == 201
    assert register.json()["email"] == payload["email"]

    login = client.post(
        "/api/v1/auth/login",
        data={"username": payload["email"], "password": payload["password"]},
    )
    assert login.status_code == 200
    data = login.json()
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 20


def test_duplicate_email_registration_fails(client: TestClient):
    """Registering the same email twice should be rejected."""
    payload = {
        "email": "duplicate@example.com",
        "password": "StrongPass123!",
    }

    first = client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 201

    second = client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 400
    assert "already exists" in second.json()["detail"].lower()


def test_login_with_wrong_password_fails(client: TestClient):
    """Incorrect credentials should fail cleanly."""
    payload = {
        "email": "wrongpass@example.com",
        "password": "CorrectPass123!",
    }

    client.post("/api/v1/auth/register", json=payload)

    login = client.post(
        "/api/v1/auth/login",
        data={"username": payload["email"], "password": "WrongPass123!"},
    )

    assert login.status_code == 400
    assert "incorrect" in login.json()["detail"].lower()

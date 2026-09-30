from tests.helpers import (
    DEFAULT_PASSWORD,
    login_user,
    register_user,
)


def test_register_user_success(client):

    response = register_user(client)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["is_active"] is True

    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email(client):

    first_response = register_user(client)

    assert first_response.status_code == 201

    second_response = register_user(client)

    assert second_response.status_code == 409

    assert (
        second_response.json()["detail"]
        == "Email already registered"
    )


def test_register_invalid_email(client):

    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "invalid-email",
            "password": DEFAULT_PASSWORD,
        },
    )

    assert response.status_code == 422


def test_register_short_password(client):

    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "123",
        },
    )

    assert response.status_code == 422


def test_login_success(client):

    register_user(client)

    response = login_user(client)

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):

    register_user(client)

    response = login_user(
        client,
        password="WrongPassword123",
    )

    assert response.status_code == 401


def test_login_unknown_email(client):

    response = login_user(
        client,
        email="unknown@example.com",
    )

    assert response.status_code == 401
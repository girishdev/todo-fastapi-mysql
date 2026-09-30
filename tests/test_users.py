from tests.helpers import (
    get_auth_headers,
    register_user,
)


def test_get_current_user_success(client):

    register_user(client)

    headers = get_auth_headers(client)

    response = client.get(
        "/api/v1/users/me",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test User"

    assert (
        data["email"]
        == "test@example.com"
    )

    assert data["is_active"] is True


def test_get_current_user_without_token(
    client,
):

    response = client.get(
        "/api/v1/users/me"
    )

    assert response.status_code == 401


def test_get_current_user_invalid_token(
    client,
):

    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization":
                "Bearer invalid-token"
        },
    )

    assert response.status_code == 401
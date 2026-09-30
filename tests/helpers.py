DEFAULT_PASSWORD = "Password123"


def register_user(
    client,
    name="Test User",
    email="test@example.com",
    password=DEFAULT_PASSWORD,
):
    return client.post(
        "/api/v1/auth/register",
        json={
            "name": name,
            "email": email,
            "password": password,
        },
    )


def login_user(
    client,
    email="test@example.com",
    password=DEFAULT_PASSWORD,
):
    return client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )


def get_auth_headers(
    client,
    email="test@example.com",
    password=DEFAULT_PASSWORD,
):
    response = login_user(
        client,
        email=email,
        password=password,
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization":
            f"Bearer {token}"
    }


def create_task(
    client,
    headers,
    title="Test Task",
    description="Test Description",
    is_completed=False,
    due_date=None,
):
    return client.post(
        "/api/v1/tasks",
        headers=headers,
        json={
            "title": title,
            "description": description,
            "is_completed": is_completed,
            "due_date": due_date,
        },
    )
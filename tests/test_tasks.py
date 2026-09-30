from tests.helpers import (
    create_task,
    get_auth_headers,
    register_user,
)


def authenticated_user(client):

    response = register_user(client)

    assert response.status_code == 201

    headers = get_auth_headers(client)

    return response.json(), headers


def test_create_task(client):

    user, headers = (
        authenticated_user(client)
    )

    response = create_task(
        client,
        headers,
        title="Learn Pytest",
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn Pytest"

    assert (
        data["user_id"]
        == user["id"]
    )


def test_get_tasks(client):

    _, headers = (
        authenticated_user(client)
    )

    create_task(
        client,
        headers,
        title="Task One",
    )

    create_task(
        client,
        headers,
        title="Task Two",
    )

    response = client.get(
        "/api/v1/tasks",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2

    assert len(
        data["items"]
    ) == 2


def test_get_task_by_id(client):

    _, headers = (
        authenticated_user(client)
    )

    create_response = create_task(
        client,
        headers,
        title="Learn FastAPI",
    )

    task_id = (
        create_response.json()["id"]
    )

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
    )

    assert response.status_code == 200

    assert (
        response.json()["title"]
        == "Learn FastAPI"
    )


def test_update_task_put(client):

    _, headers = (
        authenticated_user(client)
    )

    create_response = create_task(
        client,
        headers,
        title="Old Title",
    )

    task_id = (
        create_response.json()["id"]
    )

    response = client.put(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
        json={
            "title": "New Title",
            "description": "Updated",
            "is_completed": True,
            "due_date": None,
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["title"]
        == "New Title"
    )


def test_patch_task(client):

    _, headers = (
        authenticated_user(client)
    )

    create_response = create_task(
        client,
        headers,
        title="Learn Python",
    )

    task_id = (
        create_response.json()["id"]
    )

    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
        json={
            "is_completed": True
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["is_completed"]
        is True
    )


def test_delete_task(client):

    _, headers = (
        authenticated_user(client)
    )

    create_response = create_task(
        client,
        headers,
        title="Delete Me",
    )

    task_id = (
        create_response.json()["id"]
    )

    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
    )

    assert (
        get_response.status_code
        == 404
    )


def test_user_cannot_access_another_users_task(
    client,
):

    # User A
    register_user(
        client,
        name="User A",
        email="usera@example.com",
    )

    headers_a = get_auth_headers(
        client,
        email="usera@example.com",
    )

    task_response = create_task(
        client,
        headers_a,
        title="Private Task",
    )

    task_id = (
        task_response.json()["id"]
    )


    # User B
    register_user(
        client,
        name="User B",
        email="userb@example.com",
    )

    headers_b = get_auth_headers(
        client,
        email="userb@example.com",
    )


    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=headers_b,
    )

    assert response.status_code == 404


def test_task_pagination(client):

    _, headers = (
        authenticated_user(client)
    )

    for index in range(12):

        create_task(
            client,
            headers,
            title=f"Task {index + 1}",
        )

    response = client.get(
        (
            "/api/v1/tasks"
            "?page=2"
            "&page_size=5"
        ),
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert data["page_size"] == 5
    assert data["total"] == 12
    assert data["total_pages"] == 3

    assert len(
        data["items"]
    ) == 5


def test_filter_completed_tasks(
    client,
):

    _, headers = (
        authenticated_user(client)
    )

    create_task(
        client,
        headers,
        title="Completed Task",
        is_completed=True,
    )

    create_task(
        client,
        headers,
        title="Pending Task",
        is_completed=False,
    )

    response = client.get(
        (
            "/api/v1/tasks"
            "?is_completed=true"
        ),
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1

    assert (
        data["items"][0]["title"]
        == "Completed Task"
    )


def test_search_tasks(client):

    _, headers = (
        authenticated_user(client)
    )

    create_task(
        client,
        headers,
        title="Learn FastAPI",
        description="Backend",
    )

    create_task(
        client,
        headers,
        title="Learn React",
        description="Frontend",
    )

    response = client.get(
        (
            "/api/v1/tasks"
            "?search=FastAPI"
        ),
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1

    assert (
        data["items"][0]["title"]
        == "Learn FastAPI"
    )
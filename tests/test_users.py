from http import HTTPStatus

from todolist_api.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "nometeste",
            "email": "emailteste@teste.com",
            "password": "senhateste123",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "nometeste",
        "email": "emailteste@teste.com",
    }


def test_create_user_username_error(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "nometeste",
            "email": "nometeste2@teste.com",
            "password": "senhateste123",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Username already exists"}


def test_create_user_email_error(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "nometeste2",
            "email": "emailteste@teste.com",
            "password": "senhateste123",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Email already exists"}


def test_read_users(client):
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_read_user_by_id(client, user):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "nometeste",
        "email": "emailteste@teste.com",
    }


def test_read_user_by_id_error(client):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "nometeste2",
            "email": "nometeste2@teste.com",
            "password": "novasenhateste",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": user.id,
        "username": "nometeste2",
        "email": "nometeste2@teste.com",
    }


def test_update_user_unauthorized(client):
    response = client.put(
        "/users/1",
        json={
            "username": "nometeste2",
            "email": "nometeste2@teste.com",
            "password": "novasenhateste",
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_update_user_pathvariable_error(client, user, token):
    response = client.put(
        f"/users/{user.id + 1}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "nometeste2",
            "email": "nometeste2@teste.com",
            "password": "novasenhateste",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission"}


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_unauthorized(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_user_pathvariable_error(client, user, token):
    response = client.delete(
        f"/users/{user.id + 1}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission"}

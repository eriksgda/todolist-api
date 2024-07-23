from http import HTTPStatus

from todolist_api.schemas import UserPublic


def test_read_root_return_ok_and_json(client):
    response = client.get("/")  # act

    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {"message": "Hello World!"}


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


def test_update_user(client, user):
    response = client.put(
        "/users/1",
        json={
            "username": "nometeste2",
            "email": "nometeste2@teste.com",
            "password": "novasenhateste",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "nometeste2",
        "email": "nometeste2@teste.com",
    }


def test_update_user_error(client):
    response = client.put(
        "/users/1",
        json={
            "username": "nometeste2",
            "email": "nometeste2@teste.com",
            "password": "novasenhateste",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_user(client, user):
    response = client.delete("/users/1")

    assert response.json() == {"message": "User deleted"}


def test_delete_user_error(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_get_token_error_with_password(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": "senhaerrada"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}


def test_get_token_error_with_email(client, user):
    response = client.post(
        "/token",
        data={
            "username": "emailerrado@teste.com",
            "password": "senhateste123",  # senha correta!
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}


def test_get_token(client, user):
    response = client.post(
        "/token",
        data={
            "username": user.email,
            "password": "senhateste123",
        },
    )

    return_token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert return_token["token_type"] == "Bearer"
    assert "access_token" in return_token

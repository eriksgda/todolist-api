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


def test_read_users(client):
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}

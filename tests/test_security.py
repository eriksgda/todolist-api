from http import HTTPStatus

from jwt import decode

from todolist_api.security import ALGORITHM, SECRET_KEY, create_access_token


def test_create_jwt_token():
    data = {"sub": "emailteste@teste.com"}
    token = create_access_token(data)

    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert result["sub"] == data["sub"]
    assert result["exp"]


def test_jwt_invalid_token(client):
    response = client.delete(
        "/users/1", headers={"Authorization": "Bearer token-invalido"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_jwt_invalid_user(client, user, token):
    user.email = ""
    response = client.delete(
        f"users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}

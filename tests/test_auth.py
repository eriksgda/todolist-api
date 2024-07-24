from http import HTTPStatus


def test_get_token_error_with_password(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": "senhaerrada"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}


def test_get_token_error_with_email(client, user):
    response = client.post(
        "/auth/token",
        data={
            "username": "emailerrado@teste.com",
            "password": "senhateste123",  # senha correta!
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect email or password"}


def test_get_token(client, user):
    response = client.post(
        "/auth/token",
        data={
            "username": user.email,
            "password": "senhateste123",
        },
    )

    return_token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert return_token["token_type"] == "Bearer"
    assert "access_token" in return_token

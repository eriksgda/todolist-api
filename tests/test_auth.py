from http import HTTPStatus

from freezegun import freeze_time


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


def test_token_time_expired(client, user):
    with freeze_time("2023-07-14 12:00:00"):
        response = client.post(
            "/auth/token/",
            data={"username": user.email, "password": "senhateste123"},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2023-07-14 12:31:00"):
        response = client.put(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "username": "testestes",
                "email": "emailtset@teste.com",
                "password": "testestse23",
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}


def test_refresh_token(client, token):
    response = client.post(
        "/auth/refresh_token",
        headers={"Authorization": f"Bearer {token}"},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "Bearer"


def test_token_time_expired_dont_refresh(client, user):
    with freeze_time("2023-07-14 12:00:00"):
        response = client.post(
            "/auth/token/",
            data={"username": user.email, "password": "senhateste123"},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2023-07-14 12:31:00"):
        response = client.post(
            "/auth/refresh_token",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}

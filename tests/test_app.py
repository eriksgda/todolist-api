from http import HTTPStatus


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

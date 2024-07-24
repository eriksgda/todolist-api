from http import HTTPStatus


def test_read_root_return_ok_and_json(client):
    response = client.get("/")  # act

    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {"message": "Hello World!"}

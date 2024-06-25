from http import HTTPStatus

from fastapi.testclient import TestClient

from todolist_api.app import app


def test_read_root_return_ok_and_json():
    client = TestClient(app)  # arrange

    response = client.get("/")  # act

    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {"message": "Hello World!"}


def test_html_response_return_ok_and_html():
    client = TestClient(app)

    response = client.get("/html_response")

    assert response.status_code == HTTPStatus.OK

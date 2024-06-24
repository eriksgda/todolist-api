from http import HTTPStatus

from fastapi.testclient import TestClient

from todolist_api.app import app


def test_read_root_return_ok_and_json():
    client: TestClient = TestClient(app)  # arrange

    response: HTTPStatus = client.get('/')  # act

    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {"message": "Hello World!"}

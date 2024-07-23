from jwt import decode

from todolist_api.security import ALGORITHM, SECRET_KEY, create_access_token


def test_create_jwt_token():
    data = {"sub": "emailteste@teste.com"}
    token = create_access_token(data)

    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert result["sub"] == data["sub"]
    assert result["exp"]

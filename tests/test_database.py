from todolist_api.models import User


def test_create_user():
    user = User(
        username="teste", email="teste@teste.com", password="senhateste"
    )

    assert user.username == "teste"

from sqlalchemy import select

from todolist_api.models import User


def test_create_user(session):
    user = User(
        username="teste", email="teste@teste.com", password="senhateste"
    )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == "teste@teste.com")
    )

    assert result.username == "teste"

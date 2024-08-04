from sqlalchemy import select

from todolist_api.models import Todo, User


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


def test_create_todo(session, user: User):
    todo = Todo(
        title="Test Todo",
        description="Test Desc",
        state="draft",
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos

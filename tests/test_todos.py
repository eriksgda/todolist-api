from http import HTTPStatus

import factory.fuzzy

from todolist_api.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker("text")
    description = factory.Faker("text")
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


def test_create_todo(client, token):
    response = client.post(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test todo",
            "description": "Test todo description",
            "state": "draft",
        },
    )

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test todo"
    assert data["description"] == "Test todo description"
    assert data["state"] == "draft"

    assert "created_at" in data
    assert "update_at" in data


def test_read_todos_should_return_five_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        "/todos/", headers={"Authorization": f"Bearer {token}"}
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_pagination_should_return_two_todos(
    session, user, client, token
):
    expected_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        "/todos/?offset=1&limit=2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_filter_title_should_return_five_todos(
    session, user, client, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, title="Test todo 1")
    )
    session.commit()

    response = client.get(
        "/todos/?title=Test todo 1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_filter_description_should_return_five_todos(
    session, user, client, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, description="description")
    )
    session.commit()

    response = client.get(
        "/todos/?description=desc",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_filter_state_should_return_five_todos(
    session, user, client, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft)
    )
    session.commit()

    response = client.get(
        "/todos/?state=draft",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_filter_combined_should_return_five_todos(
    session, user, client, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title="Test todo combined",
            description="combined description",
            state=TodoState.done,
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title="Other title",
            description="other description",
            state=TodoState.todo,
        )
    )
    session.commit()

    response = client.get(
        "/todos/?title=combined&description=combined&state=done",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_update_todo_error(client, token):
    response = client.patch(
        "/todos/1", headers={"Authorization": f"Bearer {token}"}, json={}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Task not found."}


def test_upadte_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f"/todos/{todo.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "teste!"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == "teste!"


def test_delete_todo_error(client, token):
    response = client.delete(
        "/todos/1", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Task not found."}


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.delete(
        f"/todos/{todo.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": "Task has been deleted successfully."
    }

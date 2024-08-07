import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from todolist_api.app import app
from todolist_api.database import get_session
from todolist_api.models import User, table_registry
from todolist_api.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"test{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    password = factory.LazyAttribute(lambda obj: f"senha={obj.username}")


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

    yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    pwd = "senhateste123"
    user_test = User(
        username="nometeste",
        email="emailteste@teste.com",
        password=get_password_hash(pwd),
    )

    session.add(user_test)
    session.commit()
    session.refresh(user_test)

    return user_test


@pytest.fixture()
def other_user(session):
    pwd = "senhateste123"
    other_user_test = UserFactory(password=get_password_hash(pwd))

    session.add(other_user_test)
    session.commit()
    session.refresh(other_user_test)

    return other_user_test


@pytest.fixture()
def token(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": "senhateste123"},
    )

    return response.json()["access_token"]

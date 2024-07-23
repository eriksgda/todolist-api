import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from todolist_api.app import app
from todolist_api.database import get_session
from todolist_api.models import User, table_registry
from todolist_api.security import get_password_hash


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

    yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
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

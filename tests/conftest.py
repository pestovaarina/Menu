import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..v1.config import (POSTGRES_USER_TEST, POSTGRES_PASSWORD_TEST,
                         POSTGRES_DB_TEST)
from ..v1.database import Base
from ..v1.dependencies import get_db
from ..v1.main import app

DB_URL = (f"postgresql://{POSTGRES_USER_TEST}:{POSTGRES_PASSWORD_TEST}"
          f"@test_db:4321/{POSTGRES_DB_TEST}")

engine_test = create_engine(
    DB_URL,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine_test)


@pytest.fixture()
def session():

    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture(scope='module')
def saved_data():
    """Фикстура для сохранения объектов тестирования."""

    return {}

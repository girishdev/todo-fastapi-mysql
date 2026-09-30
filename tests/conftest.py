import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base, get_db
from app.main import app
from app.models import Task, User


# Prevent accidental use of development DB
if settings.TEST_DB_NAME == settings.DB_NAME:
    raise RuntimeError(
        "TEST_DB_NAME must be different from DB_NAME"
    )


TEST_DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.TEST_DB_NAME,
    query={
        "charset": "utf8mb4",
    },
)


test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)


TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(
    scope="session",
    autouse=True,
)
def setup_test_database():

    Base.metadata.drop_all(
        bind=test_engine
    )

    Base.metadata.create_all(
        bind=test_engine
    )

    yield

    Base.metadata.drop_all(
        bind=test_engine
    )


@pytest.fixture()
def client():

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(
    autouse=True
)
def clean_database():

    yield

    with TestingSessionLocal() as db:

        db.execute(
            delete(Task)
        )

        db.execute(
            delete(User)
        )

        db.commit()
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models
from app.config import settings
from app.database import Base, engine
from app.routes.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(
        bind=engine
    )

    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "ToDo REST API using FastAPI, "
        "SQLAlchemy and MySQL"
    ),
    lifespan=lifespan,
)


app.include_router(
    tasks_router,
    prefix="/api/v1",
)


@app.get(
    "/",
    tags=["Health"],
)
def root():
    return {
        "message": "ToDo API V2 is running"
    }


@app.get(
    "/health",
    tags=["Health"],
)
def health_check():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
    }
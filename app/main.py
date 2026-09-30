from contextlib import (
    asynccontextmanager,
)

from fastapi import FastAPI

from app import models
from app.config import settings
from app.database import (
    Base,
    engine,
)
from app.routes.auth import (
    router as auth_router,
)
from app.routes.tasks import (
    router as tasks_router,
)
from app.routes.users import (
    router as users_router,
)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Authenticated ToDo REST API "
        "using FastAPI, SQLAlchemy, "
        "JWT and MySQL"
    ),
)


app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    users_router,
    prefix="/api/v1",
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
        "message":
        "ToDo API V3 is running"
    }


@app.get(
    "/health",
    tags=["Health"],
)
def health_check():

    return {
        "status": "healthy",
        "version":
        settings.APP_VERSION,
    }
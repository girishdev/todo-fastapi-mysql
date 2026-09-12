from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import TaskRepository
from app.schemas import (
    TaskCreate,
    TaskListResponse,
    TaskPatch,
    TaskResponse,
    TaskUpdate,
)
from app.services import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


def get_task_service(
    db: Session = Depends(get_db),
) -> TaskService:
    repository = TaskRepository(
        db
    )

    return TaskService(
        repository
    )


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(
        get_task_service
    ),
):
    return service.create_task(
        task_data
    )


@router.get(
    "",
    response_model=TaskListResponse,
)
def get_tasks(
    page: int = Query(
        default=1,
        ge=1,
    ),

    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
    ),

    is_completed: bool | None = Query(
        default=None,
    ),

    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=255,
    ),

    service: TaskService = Depends(
        get_task_service
    ),
):
    return service.get_tasks(
        page=page,
        page_size=page_size,
        is_completed=is_completed,
        search=search,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: int = Path(
        ...,
        gt=0,
    ),

    service: TaskService = Depends(
        get_task_service
    ),
):
    return service.get_task(
        task_id
    )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_data: TaskUpdate,

    task_id: int = Path(
        ...,
        gt=0,
    ),

    service: TaskService = Depends(
        get_task_service
    ),
):
    return service.update_task(
        task_id,
        task_data,
    )


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
def patch_task(
    task_data: TaskPatch,

    task_id: int = Path(
        ...,
        gt=0,
    ),

    service: TaskService = Depends(
        get_task_service
    ),
):
    return service.patch_task(
        task_id,
        task_data,
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
)
def delete_task(
    task_id: int = Path(
        ...,
        gt=0,
    ),

    service: TaskService = Depends(
        get_task_service
    ),
):
    service.delete_task(
        task_id
    )

    return {
    "message": "Task deleted successfully"
    }
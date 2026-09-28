from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.repositories import (
    TaskRepository,
)
from app.schemas import (
    TaskCreate,
    TaskListResponse,
    TaskPatch,
    TaskResponse,
    TaskUpdate,
)
from app.security.dependencies import (
    get_current_user,
)
from app.services import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


def get_task_service(
    db: Session = Depends(
        get_db
    ),
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
    status_code=(
        status.HTTP_201_CREATED
    ),
)
def create_task(
    task_data: TaskCreate,

    current_user: User = Depends(
        get_current_user
    ),

    service: TaskService = Depends(
        get_task_service
    ),
):

    return service.create_task(
        task_data=task_data,
        user_id=current_user.id,
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

    current_user: User = Depends(
        get_current_user
    ),

    service: TaskService = Depends(
        get_task_service
    ),
):

    return service.get_tasks(
        user_id=current_user.id,
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

    current_user: User = Depends(
        get_current_user
    ),

    service: TaskService = Depends(
        get_task_service
    ),
):

    return service.get_task(
        task_id=task_id,
        user_id=current_user.id,
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

    current_user: User = Depends(
        get_current_user
    ),

    service: TaskService = Depends(
        get_task_service
    ),
):

    return service.update_task(
        task_id=task_id,
        user_id=current_user.id,
        task_data=task_data,
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

    current_user: User = Depends(
        get_current_user
    ),

    service: TaskService = Depends(
        get_task_service
    ),
):

    return service.patch_task(
        task_id=task_id,
        user_id=current_user.id,
        task_data=task_data,
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

    current_user: User = Depends(
        get_current_user
    ),

    service: TaskService = Depends(
        get_task_service
    ),
):

    service.delete_task(
        task_id=task_id,
        user_id=current_user.id,
    )

    return {
        "message":
        "Task deleted successfully"
    }
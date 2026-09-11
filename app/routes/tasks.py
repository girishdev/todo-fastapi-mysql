from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskResponse, TaskUpdate


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


def get_task_or_404(
    task_id: int,
    db: Session,
) -> Task:
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


# ---------------------------------------------------------
# CREATE TASK
# ---------------------------------------------------------

@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
):
    try:
        task = Task(
            title=task_data.title,
            description=task_data.description,
            is_completed=task_data.is_completed,
            due_date=task_data.due_date,
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return task

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create task",
        )


# ---------------------------------------------------------
# READ ALL TASKS
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[TaskResponse],
)
def get_tasks(
    skip: Annotated[
        int,
        Query(ge=0)
    ] = 0,

    limit: Annotated[
        int,
        Query(ge=1, le=100)
    ] = 100,

    db: Session = Depends(get_db),
):
    statement = (
        select(Task)
        .order_by(Task.id.desc())
        .offset(skip)
        .limit(limit)
    )

    tasks = db.scalars(statement).all()

    return tasks


# ---------------------------------------------------------
# READ SINGLE TASK
# ---------------------------------------------------------

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: Annotated[
        int,
        Path(gt=0)
    ],

    db: Session = Depends(get_db),
):
    task = get_task_or_404(
        task_id=task_id,
        db=db,
    )

    return task


# ---------------------------------------------------------
# UPDATE TASK
# ---------------------------------------------------------

@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_id: Annotated[
        int,
        Path(gt=0)
    ],

    task_data: TaskUpdate,

    db: Session = Depends(get_db),
):
    task = get_task_or_404(
        task_id=task_id,
        db=db,
    )

    try:
        task.title = task_data.title
        task.description = task_data.description
        task.is_completed = task_data.is_completed
        task.due_date = task_data.due_date

        db.commit()
        db.refresh(task)

        return task

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update task",
        )


# ---------------------------------------------------------
# DELETE TASK
# ---------------------------------------------------------

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: Annotated[
        int,
        Path(gt=0)
    ],

    db: Session = Depends(get_db),
):
    task = get_task_or_404(
        task_id=task_id,
        db=db,
    )

    try:
        db.delete(task)
        db.commit()

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete task",
        )
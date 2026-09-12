from fastapi import HTTPException, status

from app.models import Task
from app.repositories import TaskRepository
from app.schemas import (
    TaskCreate,
    TaskListResponse,
    TaskPatch,
    TaskUpdate,
)


class TaskService:
    def __init__(
        self,
        repository: TaskRepository,
    ):
        self.repository = repository

    def create_task(
        self,
        task_data: TaskCreate,
    ) -> Task:
        return self.repository.create(
            task_data
        )

    def get_task(
        self,
        task_id: int,
    ) -> Task:
        task = self.repository.get_by_id(
            task_id
        )

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return task

    def get_tasks(
        self,
        page: int,
        page_size: int,
        is_completed: bool | None = None,
        search: str | None = None,
    ) -> TaskListResponse:
        tasks, total = self.repository.get_all(
            page=page,
            page_size=page_size,
            is_completed=is_completed,
            search=search,
        )

        total_pages = (
            total + page_size - 1
        ) // page_size

        return TaskListResponse(
            items=tasks,
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        )

    def update_task(
        self,
        task_id: int,
        task_data: TaskUpdate,
    ) -> Task:
        task = self.get_task(
            task_id
        )

        update_data = task_data.model_dump()

        return self.repository.update(
            task,
            update_data,
        )

    def patch_task(
        self,
        task_id: int,
        task_data: TaskPatch,
    ) -> Task:
        task = self.get_task(
            task_id
        )

        update_data = task_data.model_dump(
            exclude_unset=True
        )

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        return self.repository.update(
            task,
            update_data,
        )

    def delete_task(
        self,
        task_id: int,
    ) -> None:
        task = self.get_task(
            task_id
        )

        self.repository.delete(
            task
        )
from sqlalchemy import (
    func,
    or_,
    select,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate


class TaskRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db


    def create(
        self,
        task_data: TaskCreate,
        user_id: int,
    ) -> Task:

        task = Task(
            user_id=user_id,
            **task_data.model_dump(),
        )

        try:

            self.db.add(task)

            self.db.commit()

            self.db.refresh(task)

            return task

        except SQLAlchemyError:

            self.db.rollback()

            raise


    def get_by_id(
        self,
        task_id: int,
        user_id: int,
    ) -> Task | None:

        query = (
            select(Task)
            .where(
                Task.id == task_id,
                Task.user_id == user_id,
            )
        )

        return self.db.scalar(
            query
        )


    def get_all(
        self,
        user_id: int,
        page: int,
        page_size: int,
        is_completed: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[Task], int]:

        filters = [
            Task.user_id == user_id
        ]

        if is_completed is not None:

            filters.append(
                Task.is_completed
                == is_completed
            )

        if search:

            search = search.strip()

            if search:

                search_pattern = (
                    f"%{search}%"
                )

                filters.append(
                    or_(
                        Task.title.ilike(
                            search_pattern
                        ),
                        Task.description.ilike(
                            search_pattern
                        ),
                    )
                )

        query = (
            select(Task)
            .where(*filters)
        )

        count_query = (
            select(func.count())
            .select_from(Task)
            .where(*filters)
        )

        total = (
            self.db.scalar(
                count_query
            )
            or 0
        )

        offset = (
            page - 1
        ) * page_size

        query = (
            query
            .order_by(
                Task.id.desc()
            )
            .offset(offset)
            .limit(page_size)
        )

        tasks = (
            self.db.scalars(
                query
            )
            .all()
        )

        return (
            list(tasks),
            total,
        )


    def update(
        self,
        task: Task,
        update_data: dict,
    ) -> Task:

        for field, value in (
            update_data.items()
        ):

            setattr(
                task,
                field,
                value,
            )

        try:

            self.db.commit()

            self.db.refresh(task)

            return task

        except SQLAlchemyError:

            self.db.rollback()

            raise


    def delete(
        self,
        task: Task,
    ) -> None:

        try:

            self.db.delete(task)

            self.db.commit()

        except SQLAlchemyError:

            self.db.rollback()

            raise
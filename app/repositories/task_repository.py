from sqlalchemy import func, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        task_data: TaskCreate,
    ) -> Task:
        task = Task(
            **task_data.model_dump()
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
    ) -> Task | None:
        return self.db.get(
            Task,
            task_id,
        )

    def get_all(
        self,
        page: int,
        page_size: int,
        is_completed: bool | None = None,
        search: str | None = None,
    ) -> tuple[list[Task], int]:
        filters = []

        if is_completed is not None:
            filters.append(
                Task.is_completed == is_completed
            )

        if search:
            search = search.strip()

            if search:
                search_pattern = f"%{search}%"

                filters.append(
                    or_(
                        Task.title.ilike(search_pattern),
                        Task.description.ilike(search_pattern),
                    )
                )

        query = select(Task)

        count_query = (
            select(func.count())
            .select_from(Task)
        )

        if filters:
            query = query.where(*filters)
            count_query = count_query.where(*filters)

        total = self.db.scalar(
            count_query
        ) or 0

        offset = (
            page - 1
        ) * page_size

        query = (
            query
            .order_by(Task.id.desc())
            .offset(offset)
            .limit(page_size)
        )

        tasks = self.db.scalars(
            query
        ).all()

        return list(tasks), total

    def update(
        self,
        task: Task,
        update_data: dict,
    ) -> Task:
        for field, value in update_data.items():
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
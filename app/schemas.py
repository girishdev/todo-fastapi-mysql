from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["Learn FastAPI"],
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
        examples=["Complete FastAPI CRUD implementation"],
    )

    due_date: datetime | None = Field(
        default=None,
        examples=["2026-09-20T18:00:00"],
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty")

        return value


class TaskCreate(TaskBase):
    is_completed: bool = False


class TaskUpdate(TaskBase):
    is_completed: bool = False


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    is_completed: bool
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
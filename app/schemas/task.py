from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class TaskCreate(BaseModel):

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    is_completed: bool = False

    due_date: datetime | None = None

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    @field_validator("title")
    @classmethod
    def validate_title(
        cls,
        value: str,
    ) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Title cannot be empty"
            )

        return value


class TaskUpdate(BaseModel):

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    description: str | None = Field(
        ...,
        max_length=2000,
    )

    is_completed: bool

    due_date: datetime | None

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    @field_validator("title")
    @classmethod
    def validate_title(
        cls,
        value: str,
    ) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Title cannot be empty"
            )

        return value


class TaskPatch(BaseModel):

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    is_completed: bool | None = None

    due_date: datetime | None = None

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    @field_validator("title")
    @classmethod
    def validate_title(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            raise ValueError(
                "Title cannot be null"
            )

        value = value.strip()

        if not value:
            raise ValueError(
                "Title cannot be empty"
            )

        return value

    @field_validator("is_completed")
    @classmethod
    def validate_is_completed(
        cls,
        value: bool | None,
    ) -> bool | None:

        if value is None:
            raise ValueError(
                "is_completed cannot be null"
            )

        return value


class TaskResponse(BaseModel):

    id: int

    user_id: int

    title: str

    description: str | None

    is_completed: bool

    due_date: datetime | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class TaskListResponse(BaseModel):

    items: list[TaskResponse]

    page: int

    page_size: int

    total: int

    total_pages: int
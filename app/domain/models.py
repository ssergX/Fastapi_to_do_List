from enum import StrEnum
from typing import Annotated
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Status(StrEnum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: Annotated[
        str,
            Field(min_length=1, example="Buy milk", description="Заголовок задачи")
    ]
    description: Annotated[
        str | None,
        Field(default=None, example="2% жирности, 1 литр")
    ]
    completed: bool = Field(False, description="Признак выполнения")

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: Annotated[
        str,
        Field(..., min_length=1, example="Buy milk")
    ]
    description: Annotated[str | None, Field(default=None)] = None


class TaskUpdate(BaseModel):
    title: Annotated[str | None, Field(min_length=1)] = None
    description: Annotated[str | None, Field()] = None
    completed: Annotated[bool | None, Field()] = None


class OperationStatus(BaseModel):
    operation_id: UUID = Field(default_factory=uuid4)
    status: Status = Field(
        default=Status.pending,
        description="Текущий статус операции"
    )
    progress: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Прогресс выполнения (0-100%)"
    )
    result: str | None = Field(
        default=None,
        description="Результат выполнения операции"
    )

    class Config:
        from_attributes = True

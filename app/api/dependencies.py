from typing import Annotated
from fastapi import Depends

from app.infrastructure.repositories.task_repository import TaskRepositoryImpl
from app.infrastructure.repositories.operation_repository import OperationRepositoryImpl
from app.services.task_service import TaskService
from app.services.operation_service import OperationService

# Создаем синглтоны репозиториев
task_repository = TaskRepositoryImpl()
operation_repository = OperationRepositoryImpl()

# Создаем синглтоны сервисов
task_service = TaskService(task_repository)
operation_service = OperationService(operation_repository)


def get_task_service() -> TaskService:
    return task_service


def get_operation_service() -> OperationService:
    return operation_service


# Типизированные зависимости для использования в маршрутах
TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
OperationServiceDep = Annotated[OperationService, Depends(get_operation_service)]

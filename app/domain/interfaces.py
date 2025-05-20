from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.models import Task, TaskCreate, TaskUpdate, OperationStatus

class TaskRepository(ABC):
    """Интерфейс репозитория для работы с задачами"""

    @abstractmethod
    async def create(self, task: TaskCreate) -> Task:
        """Создать новую задачу"""
        pass

    @abstractmethod
    async def get(self, task_id: UUID) -> Optional[Task]:
        """Получить задачу по ID"""
        pass

    @abstractmethod
    async def get_all(self) -> List[Task]:
        """Получить все задачи"""
        pass

    @abstractmethod
    async def update(self, task_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
        """Обновить задачу"""
        pass

    @abstractmethod
    async def delete(self, task_id: UUID) -> bool:
        """Удалить задачу"""
        pass


class OperationRepository(ABC):
    """Интерфейс репозитория для работы с операциями"""

    @abstractmethod
    async def create(self) -> OperationStatus:
        """Создать новую операцию"""
        pass

    @abstractmethod
    async def get(self, operation_id: UUID) -> Optional[OperationStatus]:
        """Получить статус операции по ID"""
        pass

    @abstractmethod
    async def get_all(self) -> List[Optional[OperationStatus]]:
        """Получить все операции """
        pass

    @abstractmethod
    async def update(self, operation_id: UUID, operation: OperationStatus) -> Optional[OperationStatus]:
        """Обновить статус операции"""
        pass

    @abstractmethod
    async def delete(self, operation_id: UUID) -> bool:
        """Удалить операцию"""
        pass

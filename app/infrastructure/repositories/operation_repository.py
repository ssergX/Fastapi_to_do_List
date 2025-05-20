from typing import Optional, List
from uuid import UUID

from domain.interfaces import OperationRepository
from domain.models import OperationStatus
from infrastructure.storage.in_memory_storage import operations_storage


class OperationRepositoryImpl(OperationRepository):
    """Реализация репозитория для работы с операциями в памяти"""

    async def create(self) -> OperationStatus:
        """Создать новую операцию"""
        operation = OperationStatus()
        operations_storage[operation.operation_id] = operation
        return operation

    async def get(self, operation_id: UUID | str) -> Optional[OperationStatus]:
        """Получить статус операции по ID"""
        if isinstance(operation_id, str):
            operation_id = UUID(operation_id)
        return operations_storage.get(operation_id)

    async def get_all(self) -> List[Optional[OperationStatus]]:
        """Получить список всех операций"""
        return list(operations_storage.values())

    async def update(self, operation_id: UUID | str, operation: OperationStatus) -> Optional[OperationStatus]:
        """Обновить статус операции"""
        if isinstance(operation_id, str):
            operation_id = UUID(operation_id)
        if operation_id not in operations_storage:
            return None

        operations_storage[operation_id] = operation
        return operation

    async def delete(self, operation_id: UUID | str) -> bool:
        """Удалить операцию"""
        if isinstance(operation_id, str):
            operation_id = UUID(operation_id)
        if operation_id not in operations_storage:
            return False

        del operations_storage[operation_id]
        return True

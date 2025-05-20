import asyncio
from typing import Optional, List
from uuid import UUID

from fastapi import BackgroundTasks

from domain.interfaces import OperationRepository
from domain.models import OperationStatus, Status


class OperationService:
    """Сервис для работы с длительными операциями"""

    # Конфигурация операции
    OPERATION_STEPS = 10  # Количество шагов
    STEP_DELAY = 1  # Задержка между шагами в секундах

    def __init__(self, operation_repository: OperationRepository):
        self.operation_repository = operation_repository

    async def start_operation(self, background_tasks: BackgroundTasks) -> OperationStatus:
        """Запустить новую длительную операцию"""
        # Создаем новую операцию
        operation = await self.operation_repository.create()

        # Добавляем задачу в фоновые задачи
        background_tasks.add_task(self._run_operation, operation.operation_id)

        return operation

    async def get_operation_status(self, operation_id: UUID) -> Optional[OperationStatus]:
        """Получить статус операции"""
        return await self.operation_repository.get(operation_id)

    async def get_all_operations(self) -> List[OperationStatus]:
        """Получить список всех операций"""
        return await self.operation_repository.get_all()

    async def cancel_operation(self, operation_id: UUID) -> bool:
        """Отменить операцию"""
        operation = await self.operation_repository.get(operation_id)
        if not operation:
            return False

        if operation.status in [Status.completed, Status.cancelled]:
            return False

        operation.status = Status.cancelled
        await self.operation_repository.update(operation_id, operation)
        return True

    async def _run_operation(self, operation_id: UUID) -> None:  # 10 сек ждем
        """Выполнить длительную операцию"""
        operation = await self.operation_repository.get(operation_id)
        if not operation:
            return

        # Обновляем статус на "в процессе"
        operation.status = Status.in_progress
        await self.operation_repository.update(operation_id, operation)

        try:
            # Симулируем длительную операцию
            for step in range(1, self.OPERATION_STEPS + 1):
                if operation.status == Status.cancelled:
                    return

                await asyncio.sleep(self.STEP_DELAY)  # Имитация работы
                operation.progress = (step * 100) // self.OPERATION_STEPS
                await self.operation_repository.update(operation_id, operation)

            # Отмечаем операцию как завершенную
            operation.status = Status.completed
            operation.result = "Операция успешно завершена"
            await self.operation_repository.update(operation_id, operation)

        except Exception as e:
            # В случае ошибки
            operation.status = Status.cancelled
            operation.result = f"Ошибка: {str(e)}"
            await self.operation_repository.update(operation_id, operation)

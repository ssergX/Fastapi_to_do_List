from typing import List, Optional
from uuid import UUID

from app.domain.interfaces import TaskRepository
from app.domain.models import Task, TaskCreate, TaskUpdate
from app.infrastructure.storage.in_memory_storage import tasks_storage


class TaskRepositoryImpl(TaskRepository):
    """Реализация репозитория для работы с задачами в памяти"""

    async def create(self, task_create: TaskCreate) -> Task:
        """Создать новую задачу"""
        task = Task(**task_create.dict())
        tasks_storage[task.id] = task
        return task

    async def get(self, task_id: UUID) -> Optional[Task]:
        """Получить задачу по ID"""
        return tasks_storage.get(task_id)

    async def get_all(self) -> List[Task]:
        """Получить все задачи"""
        return list(tasks_storage.values())

    async def update(self, task_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
        """Обновить задачу"""
        task = await self.get(task_id)
        if not task:
            return None

        # Обновляем только переданные поля
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        tasks_storage[task_id] = task
        return task

    async def delete(self, task_id: UUID) -> bool:
        """Удалить задачу"""
        if task_id not in tasks_storage:
            return False

        del tasks_storage[task_id]
        return True

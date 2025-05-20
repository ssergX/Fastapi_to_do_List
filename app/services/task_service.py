from typing import List, Optional
from uuid import UUID


from ..domain.interfaces import TaskRepository
from ..domain.models import Task, TaskCreate, TaskUpdate

class TaskService:

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def create_task(self, task_create: TaskCreate) -> Task:

        return await self.task_repository.create(task_create)

    async def get_task(self, task_id: UUID) -> Optional[Task]:

        return await self.task_repository.get(task_id)

    async def get_all_tasks(self) -> List[Task]:

        return await self.task_repository.get_all()

    async def update_task(self, task_id: UUID, task_update: TaskUpdate) -> Optional[Task]:

        task = await self.task_repository.get(task_id)
        if not task:
            return None

        # Обновляем задачу
        return await self.task_repository.update(task_id, task_update)

    async def delete_task(self, task_id: UUID) -> bool:

        task = await self.task_repository.get(task_id)
        if not task:
            return False

        return await self.task_repository.delete(task_id)

    async def complete_task(self, task_id: UUID) -> Optional[Task]:

        task = await self.task_repository.get(task_id)
        if not task:
            return None

        update = TaskUpdate(completed=True)
        return await self.task_repository.update(task_id, update)

    async def get_completed_tasks(self) -> List[Task]:

        all_tasks = await self.task_repository.get_all()
        return [task for task in all_tasks if task.completed]

    async def get_pending_tasks(self) -> List[Task]:

        all_tasks = await self.task_repository.get_all()
        return [task for task in all_tasks if not task.completed]

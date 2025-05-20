from typing import List
from fastapi import APIRouter, HTTPException, Path

from app.api.dependencies import TaskServiceDep
from app.domain.models import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=Task, status_code=201)
async def create_task(
        task: TaskCreate,
        task_service: TaskServiceDep
) -> Task:
    """Создать новую задачу"""
    return await task_service.create_task(task)


@router.get("/", response_model=List[Task])
async def list_tasks(
        task_service: TaskServiceDep
) -> List[Task]:

    return await task_service.get_all_tasks()


@router.get("/{task_id}", response_model=Task)
async def get_task(
        task_service: TaskServiceDep,
        task_id: str = Path(..., description="ID задачи")
) -> Task:

    task = await task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=Task)
async def update_task(
        task_service: TaskServiceDep,
        task_id: str = Path(..., description="ID задачи"),
        task_update: TaskUpdate = None,
) -> Task:

    task = await task_service.update_task(task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(
        task_service: TaskServiceDep,
        task_id: str = Path(..., description="ID задачи")
) -> None:

    success = await task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

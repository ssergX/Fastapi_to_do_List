from fastapi import APIRouter, BackgroundTasks, HTTPException, Path
from typing import List

from app.api.dependencies import OperationServiceDep
from app.domain.models import OperationStatus

router = APIRouter(prefix="/operations", tags=["operations"])


@router.post(
    "/",
    response_model=OperationStatus,
    status_code=202,
    summary="Запустить длительную операцию"
)
async def start_operation(
        background_tasks: BackgroundTasks,
        operation_service: OperationServiceDep
) -> OperationStatus:
    return await operation_service.start_operation(background_tasks)


@router.get(
    "/{operation_id}",
    response_model=OperationStatus,
    summary="Статус длительной операции"
)
async def get_operation_status(
        operation_service: OperationServiceDep,
        operation_id: str = Path(..., description="UUID операции")
) -> OperationStatus:
    operation = await operation_service.get_operation_status(operation_id)
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    return operation


@router.get(
    "/",
    response_model=List[OperationStatus],
    summary="Получить список всех операций"
)
async def get_all_operation_status(
        operation_service: OperationServiceDep,
) -> List[OperationStatus]:
    operations = await operation_service.get_all_operations()
    return operations


@router.delete(
    "/{operation_id}",
    status_code=204,
    summary="Отменить операцию"
)
async def cancel_operation(
        operation_service: OperationServiceDep,
        operation_id: str = Path(..., description="UUID операции")
) -> None:
    success = await operation_service.cancel_operation(operation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Operation not found")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.routes import api_router
from app.infrastructure.repositories.task_repository import TaskRepositoryImpl
from app.infrastructure.repositories.operation_repository import OperationRepositoryImpl
from app.services.task_service import TaskService
from app.services.operation_service import OperationService

app = FastAPI()

task_repository = TaskRepositoryImpl()
operation_repository = OperationRepositoryImpl()
task_service = TaskService(task_repository)
operation_service = OperationService(operation_repository)

app.dependency_overrides = {
    "get_task_service": lambda: task_service,
    "get_operation_service": lambda: operation_service
}

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="127.1.1.1", port=8001)

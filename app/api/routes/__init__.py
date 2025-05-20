from fastapi import APIRouter
from . import tasks, operations

api_router = APIRouter()
api_router.include_router(tasks.router)
api_router.include_router(operations.router)

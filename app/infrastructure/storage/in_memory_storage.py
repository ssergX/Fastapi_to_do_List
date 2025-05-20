from typing import Dict
from uuid import UUID

from app.domain.models import Task, OperationStatus

tasks_storage: Dict[UUID, Task] = {}

operations_storage: Dict[UUID, OperationStatus] = {}

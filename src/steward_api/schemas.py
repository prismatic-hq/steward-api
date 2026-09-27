import uuid
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class WorkOrderStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class WorkOrderCreate(BaseModel):
    site: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    priority: Priority = Priority.MEDIUM
    assigned_crew: str | None = Field(default=None, max_length=64)
    source_alert_id: uuid.UUID | None = None


class WorkOrderUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    priority: Priority | None = None
    status: WorkOrderStatus | None = None
    assigned_crew: str | None = Field(default=None, max_length=64)


class WorkOrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    site: str
    title: str
    description: str | None
    priority: Priority
    status: WorkOrderStatus
    assigned_crew: str | None
    source_alert_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime

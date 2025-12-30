from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class TaskState(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


# -------- Input --------
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskState = TaskState.pending


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskState] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskState
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

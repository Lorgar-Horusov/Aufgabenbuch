from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from rich.console import Console
from enum import Enum

console = Console()


class StatusEnum(str, Enum):
    todo = "new"
    in_progress = "in_progress"
    done = "done"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None

class TaskCreate(TaskBase):
    status: StatusEnum

class TaskUpdate(TaskBase):
    status: StatusEnum

class TaskOut(TaskBase):
    id: int
    user: str
    class Config:
        orm_mode = True

from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from . import models, schemas
from rich.console import Console

console = Console()


def create_task(db: Session, task: schemas.TaskCreate, username: str):
    try:
        db_task = task.model_dump()
        db_task["user"] = username

        db_task = models.Task(**db_task)

        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        console.print(f"Error: {e}")
        return None


def get_tasks(
    db: Session,
    user: str,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
):
    try:
        query = db.query(models.Task).filter(models.Task.user == user)
        if status:
            query = query.filter(models.Task.status == status)
        if date_from:
            query = query.filter(models.Task.due_date >= date_from)
        if date_to:
            query = query.filter(models.Task.due_date <= date_to)
        return query.offset(skip).limit(limit).all()
    except Exception:
        console.print_exception(show_locals=True)


def get_task(db: Session, task_id: int, user: str):
    try:
        return db.query(models.Task).filter(models.Task.id == task_id, models.Task.user == user).first()
    except Exception:
        console.print_exception(show_locals=True)


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate, user: str):
    try:
        db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user == user).first()
        if db_task:
            for key, value in task.model_dump().items():
                setattr(db_task, key, value)
            db.commit()
            db.refresh(db_task)
        return db_task
    except Exception:
        console.print_exception(show_locals=True)

def delete_task(db: Session, task_id: int, user: str):
    try:
        db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user == user).first()
        if db_task:
            db.delete(db_task)
            db.commit()
        return db_task
    except Exception:
        console.print_exception(show_locals=True)

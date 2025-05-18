from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from util import (
    crud,
    schemas,
)
from util.database import (
    init_db,
    SessionLocal,
)
from dotenv import load_dotenv
import os

import logging
from rich.logging import RichHandler
from rich.console import Console
from typing import Optional
from datetime import datetime

console = Console()
load_dotenv()
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

security = HTTPBearer()
app = FastAPI(
    title="Task Management API",
    description="API for managing tasks",
    version="1.0.0",
    contact={
        "name": "Lorgar Horusov",
        "url": "https://github.com/Lorgar-Horusov/",
    }
)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        for key, value in os.environ.items():
            if value == token:
                return key
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        console.print_exception(show_locals=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


init_db()


@app.post(
    "/tasks/", response_model=schemas.TaskOut, dependencies=[Depends(verify_token)]
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    username: str = Depends(verify_token),
):
    try:
        db_task = crud.create_task(db=db, task=task, username=username)
        if not db_task:
            raise HTTPException(status_code=400, detail="Task creation failed")
        return db_task
    except Exception:
        console.print_exception(show_locals=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get(
    "/task/{task_id}",
    response_model=schemas.TaskOut,
    dependencies=[Depends(verify_token)],
)
def get_task(
    task_id: int, db: Session = Depends(get_db), username: str = Depends(verify_token)
):
    task = crud.get_task(db=db, task_id=task_id, user=username)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get(
    "/tasks/",
    response_model=list[schemas.TaskOut],
    dependencies=[Depends(verify_token)],
)
def get_tasks(
    db: Session = Depends(get_db),
    username: str = Depends(verify_token),
    status: Optional[str] = Query(None, description="Filter by task status"),
    date_from: Optional[datetime] = Query(None, description="Start date (ISO format)"),
    date_to: Optional[datetime] = Query(None, description="End date (ISO format)"),
):
    try:
        return crud.get_tasks(
            db=db, user=username, status=status, date_from=date_from, date_to=date_to
        )
    except Exception:
        console.print_exception(show_locals=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve tasks")


@app.put(
    "/task/{task_id}",
    response_model=schemas.TaskOut,
    dependencies=[Depends(verify_token)],
)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    username: str = Depends(verify_token),
):
    try:
        return crud.update_task(db=db, task_id=task_id, task=task, user=username)
    except Exception:
        console.print_exception(show_locals=True)


@app.delete(
    "/task/{task_id}",
    response_model=schemas.TaskOut,
    dependencies=[Depends(verify_token)],
)
def delete_task(
    task_id: int, db: Session = Depends(get_db), username: str = Depends(verify_token)
):
    try:
        return crud.delete_task(db=db, task_id=task_id, user=username)
    except Exception:
        console.print_exception(show_locals=True)

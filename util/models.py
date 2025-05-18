from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    due_date = Column(DateTime)
    status = Column(String)
    user = Column(String, nullable=False)

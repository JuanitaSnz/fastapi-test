from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    @staticmethod
    def create_task(db: Session, task_data: TaskCreate, owner_id: int) -> Task:
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            owner_id=owner_id,
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    @staticmethod
    def get_user_tasks(db: Session, owner_id: int, page: int = 1, page_size: int = 10) -> List[Task]:
        if page < 1:
            raise HTTPException(status_code=400, detail="Page must be >= 1")
        if page_size < 1 or page_size > 100:
            raise HTTPException(status_code=400, detail="Page size must be between 1 and 100")
        
        offset = (page - 1) * page_size
        tasks = db.query(Task).filter(Task.owner_id == owner_id).offset(offset).limit(page_size).all()
        return tasks

    @staticmethod
    def get_task_by_id(db: Session, task_id: int, owner_id: int) -> Task:
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.owner_id == owner_id,
        ).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    @staticmethod
    def update_task(db: Session, task_id: int, updates: TaskUpdate, owner_id: int) -> Task:
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.owner_id == owner_id,
        ).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        for key, value in updates.dict(exclude_unset=True).items():
            setattr(task, key, value)

        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete_task(db: Session, task_id: int, owner_id: int) -> dict:
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.owner_id == owner_id,
        ).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully"}
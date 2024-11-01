from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session                       # сессия БД
from app.backend.db_depends import get_db                # функция подключения к БД
from typing import Annotated                             # аннотации, модели БД и pydantic
from sqlalchemy import select, insert, update, delete    # функции для работы с записями в таблице
from slugify import slugify                              # функция создания slug-строки

from app.models import *                          # модель таблиц User и Task, в которые заполнятся данные
from app.schemas import CreateTask, UpdateTask    # модель pydantic для создания и изменения данных


router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks_all = db.scalars(select(Task)).all()
    return tasks_all


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is not None:
        return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Task was not found'
    )


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task_model: CreateTask, user_id: int):
    user_search = db.scalar(select(User).where(User.id == user_id))
    if user_search is not None:
        db.execute(insert(Task).values(title=create_task_model.title,
                                       content=create_task_model.content,
                                       priority=create_task_model.priority,
                                       slug=slugify(create_task_model.title),
                                       user_id=user_id))
        db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User was not found'
    )


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task_model: UpdateTask):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is not None:
        db.execute(update(Task).where(Task.id == task_id).values(
            title=update_task_model.title,
            content=update_task_model.content,
            priority=update_task_model.priority,
            slug=slugify(update_task_model.title)))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Task update is successful!'
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Task was not found'
    )


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is not None:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Task delete is successful!'
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Task was not found'
    )

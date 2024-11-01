from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session                       # сессия БД
from app.backend.db_depends import get_db                # функция подключения к БД
from typing import Annotated                             # аннотации, модели БД и pydantic
from sqlalchemy import select, insert, update, delete    # функции для работы с записями в таблице
from slugify import slugify                              # функция создания slug-строки

from app.models import *                          # модель таблиц User и Task, в которые заполнятся данные
from app.schemas import CreateUser, UpdateUser    # модель pydantic для создания и изменения данных


router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users_all = db.scalars(select(User)).all()
    return users_all


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User was not found'
    )


@router.get('/user_id/tasks')
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_search = db.scalar(select(User).where(User.id == user_id))
    if user_search is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    tasks_for_user = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    if tasks_for_user:
        return tasks_for_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'No tasks found for a user with user_id={user_id}'
    )


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user_model: CreateUser):
    check_username = db.query(User).filter_by(username=create_user_model.username).first()
    if check_username is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Username already exists. Try entering a different username'
        )
    db.execute(insert(User).values(username=create_user_model.username,
                                   firstname=create_user_model.firstname,
                                   lastname=create_user_model.lastname,
                                   age=create_user_model.age,
                                   slug=slugify(create_user_model.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user_model: UpdateUser):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        db.execute(update(User).where(User.id == user_id).values(
            firstname=update_user_model.firstname,
            lastname=update_user_model.lastname,
            age=update_user_model.age))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User update is successful!'
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User was not found'
    )


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        db.execute(delete(User).where(User.id == user_id))
        db.execute(delete(Task).where(Task.user_id == user_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User and his tasks delete is successful!'
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User was not found'
    )

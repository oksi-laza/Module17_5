from fastapi import FastAPI
from app.routers import task, user


app = FastAPI()
# python -m uvicorn app.main:app - запуск из терминала в папке выше уровнем директории 'app'


@app.get('/')
async def welcome():
    return {'message': 'Welcome to Taskmanager'}


app.include_router(task.router)
app.include_router(user.router)

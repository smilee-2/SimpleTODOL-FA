from fastapi import APIRouter, Depends
from app.api.tasks.models_tasks import TaskModel
from app.database import crud
from typing import Annotated



router = APIRouter(prefix='/tasks',tags=['Task'])


@router.get('/get_one_task/{id_user}')
async def get_one_task(id_user: int) -> list[TaskModel]:
    return await crud.get_one_task(id_user=id_user)


@router.post('/add_task')
async def add_task(id_user, task: Annotated[TaskModel, Depends()]):
    return await crud.add_task(id_user=id_user, task=task)
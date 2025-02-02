from fastapi import APIRouter
from app.api.models import TaskModel
from app.database import crud



router = APIRouter(prefix='/tasks',tags=['Task'])


@router.get('/get_one_task/{id_user}')
async def get_one_task(id_user: int) -> list[TaskModel]:
    return await crud.get_one_task(id_user=id_user)


@router.post('/add_task')
async def add_task(id_user, task: TaskModel):
    return await crud.add_task(id_user=id_user, task=task)
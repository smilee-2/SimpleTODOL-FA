from fastapi import APIRouter, Depends
from app.api.tasks.models_tasks import TaskModel
from app.database import crud
from typing import Annotated
from typing import Annotated
from ..auth.depends import oauth2_scheme



router = APIRouter(prefix='/tasks',tags=['Task'])


@router.get('/get_one_task/{id_user}')
async def get_one_task(user_id: int, token: Annotated[str, Depends(oauth2_scheme)]) -> list[TaskModel]:
    return await crud.get_one_task(user_id=user_id)


@router.post('/add_task')
async def add_task(user_id, task: Annotated[TaskModel, Depends()], token: Annotated[str, Depends(oauth2_scheme)]):
    return await crud.add_task(user_id=user_id, task=task)
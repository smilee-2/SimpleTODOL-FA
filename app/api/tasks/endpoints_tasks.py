from fastapi import APIRouter, Depends
from app.api.tasks.models_tasks import TaskModel
from app.database import crud
from typing import Annotated
from typing import Annotated
from ..auth.depends import oauth2_scheme



router = APIRouter(prefix='/tasks',tags=['Task'])


@router.get('/get_one_task/{id_user}')
async def get_one_task(token: Annotated[str, Depends(oauth2_scheme)]) -> list[TaskModel]:
    user_id = await crud.get_user_id(token)
    return await crud.get_one_task_by_id(user_id=user_id)


@router.post('/add_task')
async def add_task(task: Annotated[TaskModel, Depends()],
                   token: Annotated[str, Depends(oauth2_scheme)]
                   ) -> dict[str,str]:
    user_id = await crud.get_user_id(token)
    return await crud.add_task(task=task, user_id=user_id)


@router.delete('/delete_one_task')
async def delete_one_task_by_id(task_id: int, token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
    return await crud.delete_one_task(task_id=task_id)
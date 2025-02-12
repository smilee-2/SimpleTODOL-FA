from fastapi import APIRouter, Depends, HTTPException, status
from app.api.tasks.models_tasks import TaskModel
from app.database.crud import TaskCrud, UserCrud
from typing import Annotated
from ..auth.depends import oauth2_scheme

router = APIRouter(prefix='/tasks', tags=['Task'])


# Эндпоинт получение всех задач пользователя
@router.get('/get_tasks')
async def get_all_tasks(token: Annotated[str, Depends(oauth2_scheme)]) -> list[TaskModel]:
    user_id = await UserCrud.get_user_id(token)
    return await TaskCrud.get_all_tasks_by_id(user_id=user_id)


# Энпоинт добавления задачи
@router.post('/add_task')
async def add_task(task: Annotated[TaskModel, Depends()],
                   token: Annotated[str, Depends(oauth2_scheme)]
                   ) -> dict[str, str]:
    user_id = await UserCrud.get_user_id(token)
    return await TaskCrud.add_task(task=task, user_id=user_id)


# Удаление задачи
@router.delete('/delete_one_task')
async def delete_one_task_by_id(task_id: int, token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
    try:
        return await TaskCrud.delete_one_task(task_id=task_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='task not found')


# Изменение задачи
@router.put('/update_task')
async def update_task(task_id: int,
                      new_description: str,
                      token: Annotated[str, Depends(oauth2_scheme)]
                      )-> dict[str, str] | None:
    try:
        user_id = await UserCrud.get_user_id(token)
        return await TaskCrud.update_task(new_description=new_description, task_id=task_id, user_id=user_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='task not found')


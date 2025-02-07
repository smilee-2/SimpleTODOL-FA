from fastapi import APIRouter, Depends
from app.api.users.models_users import UserModel
from app.database import crud


router = APIRouter(prefix='/users', tags=['Users'])


# Эндпоинт Получение пользователя
@router.get('/get_user')
async def get_user(username: str) -> UserModel | None:
    return await crud.get_user(username=username)


# Эндпоинт удаление пользователя
@router.delete('/delete_user')
async def delete_user(username: str) -> bool:
    return await crud.delete_user(username)



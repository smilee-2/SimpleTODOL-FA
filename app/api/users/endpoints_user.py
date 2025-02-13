from fastapi import APIRouter, HTTPException, status

from app.api.users.models_users import UserModel
from app.database.crud import UserCrud


router = APIRouter(prefix='/users', tags=['Users'])


# Эндпоинт Получение пользователя
@router.get('/get_user')
async def get_user(username: str) -> UserModel | None:
    try:
        return await UserCrud.get_user(username=username)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')


# Эндпоинт удаление пользователя
@router.delete('/delete_user')
async def delete_user(username: str) -> bool:
    return await UserCrud.delete_user(username)



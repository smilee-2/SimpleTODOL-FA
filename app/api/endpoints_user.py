from fastapi import APIRouter, Depends
from .models import UserModel
from app.database import crud

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/get_user/{user_id}')
async def get_user(user_id) -> UserModel:
    user_s = await crud.get_user(user_id=user_id)
    return user_s

@router.post('/create_user')
async def create_user(user: UserModel) -> dict[str, str]:
    await crud.create_user(user_input=user)
    return {'msg':'success'}


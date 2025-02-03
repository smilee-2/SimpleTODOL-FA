from fastapi import APIRouter, Depends
from app.api.users.models_users import UserModel
from app.database import crud
from typing import Annotated

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/get_user/{user_id}')
async def get_user(user_id: int) -> UserModel:
    user_s = await crud.get_user(user_id=user_id)
    return user_s

@router.post('/create_user')
async def create_user(user: Annotated[UserModel, Depends()]) -> dict[str, str]:
    await crud.create_user(user_input=user)
    return {'msg':'success'}


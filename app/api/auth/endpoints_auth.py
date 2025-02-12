from typing import Annotated
from app.database.crud import UserCrud
from ..users.models_users import UserModel
from .depends import get_password_hash, verify_password
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix='/auth', tags=['Auth'])


# Эндпоинт регистрация пользователя
@router.post('/register_user')
async def register_user(user: Annotated[UserModel, Depends()], request: Request):
    user.password = get_password_hash(user.password)
    await UserCrud.create_user(user_input=user)
    #return RedirectResponse('/auth/token', headers=request.headers)
    return {'msg': 'user created'}


# Эндпоинт проверки авторизации пользователя
@router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await UserCrud.get_user(form_data.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    check_password = verify_password(form_data.password, user.password)

    if not check_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

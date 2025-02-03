from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import HTTPBasicCredentials, HTTPBasic


router = APIRouter(prefix='/auth', tags=['auth'])

security = HTTPBasic()


@router.get('/auth')
async def auth_credentials(credentials: Annotated[HTTPBasicCredentials,Depends(security)]):
    return {'msg': 'hi', 'username': credentials.username, 'password': credentials.password}


@router.get('/auth')
async def auth_credentials(auth_username: str = Depends(security)):
    return
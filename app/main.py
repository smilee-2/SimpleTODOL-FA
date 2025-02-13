from pathlib import Path
from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
import uvicorn

from api import router_tasks, router_users, router_auth, router_files
from api.auth.depends import oauth2_scheme
from database import Base
from config import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        #await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield


BASE_DIR = Path(__file__).parent.parent

app = FastAPI(lifespan=lifespan)


app.include_router(router_tasks)
app.include_router(router_users)
app.include_router(router_auth)
app.include_router(router_files)


templates_auth = Jinja2Templates(directory=f'{BASE_DIR}/fronted/auth_page')
templates_main = Jinja2Templates(directory=f'{BASE_DIR}/fronted/main_page')


# Страница какая-то
@app.get('/main_page')
async def main_page(request: Request, token: Annotated[str, Depends(oauth2_scheme)]):
    context = {'request': request}
    return templates_main.TemplateResponse('index.html', context)


# Страница авторизации
@app.get('/')
async def main(request: Request):
    context = {'request': request}
    return templates_auth.TemplateResponse('index.html', context)


if __name__ == '__main__':
    uvicorn.run('main:app')
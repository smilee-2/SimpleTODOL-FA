from fastapi import FastAPI
from contextlib import asynccontextmanager
from config import engine
from database import Base
from api import router_tasks, router_users
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        #await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router_tasks)
app.include_router(router_users)

@app.get('/',tags=['main'])
async def main():
    return {'msg': 'Hello'}


if __name__ == '__main__':
    uvicorn.run('main:app')
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core import engine
from database import Base
from api import router as router_tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(
    router_tasks,
)

@app.get('/',tags=['main'])
async def main():
    return {'msg': 'Hello'}
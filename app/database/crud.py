from sqlalchemy import select
from sqlalchemy.util import await_only
from watchfiles import awatch

from .schemas import TaskSchemas, UserSchemas
from app.config.config import session_maker
from app.api.users.models_users import UserModel
from app.api.tasks.models_tasks import TaskModel


async def add_task(user_id: int, task: TaskModel) -> dict[str,str]:
    async with session_maker.begin() as session:
        task = TaskSchemas(**task.model_dump(), user_id=user_id)
        session.add(task)
        await session.commit()
        return {'msg':'Success'}


async def get_one_task(id_user: int) -> list[TaskModel]:
    async with session_maker.begin() as session:
        subquery = select(UserSchemas.id).where(UserSchemas.id == id_user).subquery()
        stmt = select(TaskSchemas).where(TaskSchemas.user_id == subquery)
        result = await session.execute(stmt)
        tasks = result.scalars().all()
        tasks_model =[TaskModel.model_validate(task) for task in tasks]
    return tasks_model


async def create_user(user_input: UserModel) -> UserSchemas:
    async with session_maker.begin() as session:
        user = UserSchemas(**user_input.model_dump())
        session.add(user)
        await session.commit()
    return user


async def get_user_by_id(user_id: int) -> UserSchemas|None:
    with session_maker.begin() as session:
        return await session.get(UserSchemas, user_id)


async def get_user(username: str) -> UserModel | None:
    async with session_maker.begin() as session:
        query = select(UserSchemas).where(UserSchemas.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return UserModel.model_validate(user)
        return None


async def delete_user(username: str) -> bool:
    async with session_maker.begin() as sess:
        user = await sess.get(UserSchemas, username)
        await sess.delete(user)
        await sess.commit()
        return True
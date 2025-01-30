from sqlalchemy import select
from .schemas import TaskSchemas, UserSchemas
from app.core.config import session
from app.api.models import TaskModel, UserModel


async def add_task(id_user: int, task: TaskModel) -> dict[str,str]:
    async with session.begin() as sess:
        task = TaskSchemas(**task.model_dump(), user_id=id_user)
        sess.add(task)
        await sess.commit()
        return {'msg':'Success'}

async def get_one_task(id_user: int) -> list[TaskModel]:
    async with session.begin() as sess:
        subquery = select(UserSchemas.id).where(UserSchemas.id == id_user).subquery()
        stmt = select(TaskSchemas).where(TaskSchemas.user_id == subquery)
        result = await sess.execute(stmt)
        tasks = result.scalars().all()
        print(tasks)
        tasks_model =[TaskModel.model_validate(task) for task in tasks]
    return tasks_model


async def create_user(user_input: UserModel) -> UserSchemas:
    async with session.begin() as sess:
        user = UserSchemas(**user_input.model_dump())
        sess.add(user)
        await sess.commit()
    return user


async def get_user(user_id: int) -> UserModel | None:
    async with session.begin() as sess:
        user = await sess.get(UserSchemas, user_id)
        return UserModel.model_validate(user)
from sqlalchemy import select
from schemas import TaskSchemas, UserSchemas
from app.core.config import session
from app.api.models import TaskModel


async def add_task(id_user: int, task: TaskModel) -> dict[str,str]:
    async with session.begin() as sess:
        task = TaskSchemas(**task.model_dump())
        sess.add(task)
        await sess.commit()
        return {'msg':'Success'}

async def get_one_task(id_user: int) -> list[TaskModel]:
    async with session.begin():
        subquery = select(UserSchemas.id).where(UserSchemas.id == id_user).subquery()
        stmt = select(TaskSchemas).where(TaskSchemas.user_id == subquery)
        result = await session.execute(stmt)
        tasks = result.scalars().all()
        tasks_model =[TaskModel.model_validate(task) for task in tasks]
    return tasks_model
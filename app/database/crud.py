from sqlalchemy import select
from .schemas import TaskSchemas, UserSchemas
from app.config.config import session_maker
from app.api.users.models_users import UserModel
from app.api.tasks.models_tasks import TaskModel


# Добавление задачи
async def add_task(task: TaskModel, user_id: int) -> dict[str,str]:
    async with session_maker.begin() as session:
        task = TaskSchemas(**task.model_dump(), user_id=user_id)
        session.add(task)
        await session.commit()
        return {'msg':'Success'}


# Получение всех задач пользователя
async def get_all_tasks_by_id(user_id: int) -> list[TaskModel]:
    async with session_maker.begin() as session:
        stmt = select(TaskSchemas).where(TaskSchemas.user_id == user_id)
        result = await session.execute(stmt)
        tasks = result.scalars().all()
        tasks_model =[TaskModel.model_validate(task) for task in tasks]
    return tasks_model


# Обновление задачи
async def update_task(new_description: str, task_id: int, user_id: int) -> dict[str, str]:
    async with session_maker.begin() as session:
        stmt = select(TaskSchemas).where(
            TaskSchemas.user_id == user_id,
            TaskSchemas.id == task_id
        )
        result = await session.execute(stmt)
        task = result.scalars().one()
        task.description = new_description
        return {'msg': 'success', 'new task': new_description}


# Удаление одной задачи
async def delete_one_task(task_id: int) -> bool:
    async with session_maker.begin() as session:
        task = await session.get(TaskSchemas, task_id)
        await session.delete(task)
        await session.commit()
        return True


# Создание нового пользователя
async def create_user(user_input: UserModel) -> UserSchemas:
    async with session_maker.begin() as session:
        user = UserSchemas(**user_input.model_dump())
        session.add(user)
        await session.commit()
        return user


# Получение пользователья по id
async def get_user_by_id(user_id: int) -> UserSchemas|None:
    with session_maker.begin() as session:
        return await session.get(UserSchemas, user_id)


# Получение пользователя по имени
async def get_user(username: str) -> UserModel | None:
    async with session_maker.begin() as session:
        query = select(UserSchemas).where(UserSchemas.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return UserModel.model_validate(user)
        return None


# Получение id пользователя
async def get_user_id(username: str) -> int | None:
    async with session_maker.begin() as session:
        query = select(UserSchemas).where(UserSchemas.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return user.id
        return None


# Удаление пользователя
async def delete_user(username: str) -> bool:
    async with session_maker.begin() as session:
        user = await session.get(UserSchemas, username)
        await session.delete(user)
        await session.commit()
        return True
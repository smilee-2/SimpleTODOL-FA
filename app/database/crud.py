from sqlalchemy import select, delete

from .schemas import TaskSchemas, UserSchemas, FileSchemas
from app.config.config import session_maker
from app.api.users.models_users import UserModel
from app.api.tasks.models_tasks import TaskModel
from app.api.files.models_files import FileModel


class TaskCrud:

    # Добавление задачи
    @staticmethod
    async def add_task(task: TaskModel, user_id: int) -> dict[str, str]:
        async with session_maker.begin() as session:
            task = TaskSchemas(**task.model_dump(), user_id=user_id)
            session.add(task)
            return {'msg': 'Success'}

    # Получение всех задач пользователя
    @staticmethod
    async def get_all_tasks_by_id(user_id: int) -> list[TaskModel]:
        async with session_maker.begin() as session:
            stmt = select(TaskSchemas).where(TaskSchemas.user_id == user_id)
            result = await session.execute(stmt)
            tasks = result.scalars().all()
            tasks_model = [TaskModel.model_validate(task) for task in tasks]
        return tasks_model

    # Обновление задачи
    @staticmethod
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
    @staticmethod
    async def delete_one_task(task_id: int) -> bool:
        async with session_maker.begin() as session:
            task = await session.get(TaskSchemas, task_id)
            await session.delete(task)
            await session.commit()
            return True


class UserCrud:

    # Создание нового пользователя
    @staticmethod
    async def create_user(user_input: UserModel) -> UserSchemas:
        async with session_maker.begin() as session:
            user = UserSchemas(**user_input.model_dump())
            session.add(user)
            await session.commit()
            return user

    # Получение пользователья по id
    @staticmethod
    async def get_user_by_id(user_id: int) -> UserSchemas | None:
        with session_maker.begin() as session:
            return await session.get(UserSchemas, user_id)

    # Получение пользователя по имени
    @staticmethod
    async def get_user(username: str) -> UserModel | None:
        async with session_maker.begin() as session:
            query = select(UserSchemas).where(UserSchemas.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return UserModel.model_validate(user)
            return None

    # Получение id пользователя
    @staticmethod
    async def get_user_id(username: str) -> int | None:
        async with session_maker.begin() as session:
            query = select(UserSchemas).where(UserSchemas.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return user.id
            return None

    # Удаление пользователя вместе со всеми задачами
    @staticmethod
    async def delete_user(username: str) -> bool:
        async with session_maker.begin() as session:
            query_user = select(UserSchemas).where(UserSchemas.username == username)
            result = await session.execute(query_user)
            user = result.scalar_one_or_none()
            if user:
                query_tasks = delete(TaskSchemas).where(TaskSchemas.user_id == user.id)
                result_tasks = await session.execute(query_tasks)
                await session.delete(user)
                return True
            return False


class FileCrud:
    # Добавление данных файла
    @staticmethod
    async def add_user_file(file: FileModel, username: str) -> None:
        async with session_maker.begin() as session:
            user_id = await UserCrud.get_user_id(username)
            user_file = FileSchemas(**file.model_dump(), user_id=user_id)
            session.add(user_file)

    # Получение данных файла
    @staticmethod
    async def get_user_file(file_id: int, username: str) -> FileSchemas | None:
        async with session_maker.begin() as session:
            user_id = await  UserCrud.get_user_id(username)
            query = select(FileSchemas).where(FileSchemas.id == file_id, FileSchemas.user_id == user_id)
            result = await session.execute(query)
            if result:
                return result.scalar_one_or_none()
            return None

    # Удаление данных файла
    @staticmethod
    async def delete_user_file(file_id: int) -> dict[str, str]:
        ...

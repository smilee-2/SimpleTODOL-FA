from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey


# Базовая таблица
class Base(DeclarativeBase):
    pass


# Таблица пользователей
class UserSchemas(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

# Таблица задач
class TaskSchemas(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))


class FileSchemas(Base):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[int] = mapped_column(nullable=False)
    directory: Mapped[str] = mapped_column(nullable=False)
    user_id:  Mapped[int] = mapped_column(ForeignKey('users.id'))


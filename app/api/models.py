from pydantic import BaseModel, EmailStr


class Base(BaseModel):
    id: int
    pass


class TaskModel(Base):
    status: bool
    description: str


class UserModel(Base):
    username: str
    email: EmailStr
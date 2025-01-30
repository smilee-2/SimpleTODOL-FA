from pydantic import BaseModel, EmailStr, ConfigDict


class Base(BaseModel):
    id: int
    pass


class TaskModel(Base):
    status: bool
    description: str
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class UserModel(Base):
    username: str
    model_config = ConfigDict(from_attributes=True)
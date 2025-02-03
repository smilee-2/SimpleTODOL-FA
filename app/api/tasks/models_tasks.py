from pydantic import BaseModel, EmailStr, ConfigDict


class BaseTaskModel(BaseModel):
    pass


class TaskModel(BaseTaskModel):
    status: bool
    description: str
    user_id: int
    model_config = ConfigDict(from_attributes=True)
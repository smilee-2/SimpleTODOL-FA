from pydantic import BaseModel, EmailStr, ConfigDict


class BaseTaskModel(BaseModel):
    pass


class TaskModel(BaseTaskModel):
    description: str
    model_config = ConfigDict(from_attributes=True)
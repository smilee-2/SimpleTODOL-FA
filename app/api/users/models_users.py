from pydantic import BaseModel, EmailStr, ConfigDict


class BaseUserModel(BaseModel):
    id: int
    pass


class UserModel(BaseUserModel):
    username: str
    model_config = ConfigDict(from_attributes=True)
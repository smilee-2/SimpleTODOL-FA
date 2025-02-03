from pydantic import BaseModel, EmailStr, ConfigDict


class BaseUserModel(BaseModel):
    pass


class UserModel(BaseUserModel):
    username: str
    password: str
    model_config = ConfigDict(from_attributes=True)
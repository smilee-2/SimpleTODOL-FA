from pydantic import BaseModel, ConfigDict


class BaseUserModel(BaseModel):
    pass


class UserModel(BaseUserModel):
    username: str
    password: str
    model_config = ConfigDict(from_attributes=True)

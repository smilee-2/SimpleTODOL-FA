from pydantic import BaseModel, ConfigDict


class BaseUserModel(BaseModel):
    pass


class UserModel(BaseUserModel):
    id: int
    username: str
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)

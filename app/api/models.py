from pydantic import BaseModel


class Base(BaseModel):
    pass


class TaskModel(Base):
    id: int
    status: bool
    description: str
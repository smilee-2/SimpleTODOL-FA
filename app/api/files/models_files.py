from pydantic import BaseModel


class BaseFileModel(BaseModel):
    pass


class FileModel(BaseFileModel):

    filename: str
    size: int
    directory: str


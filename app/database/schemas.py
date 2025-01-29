from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime




class Base(DeclarativeBase):
    pass


class TaskSchemas(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[bool]
    description: Mapped[str] = mapped_column(nullable=False)
    #datetime: datetime
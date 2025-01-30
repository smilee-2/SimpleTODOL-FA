from pathlib import Path
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

BASE_DIR = Path(__file__).parent.parent.parent


class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db/database.db"
    db_echo: bool = True


settings = Setting()

engine = create_async_engine(
    url=settings.db_url,
    echo=settings.db_echo
)

session = async_sessionmaker(engine, expire_on_commit=False)
print(BASE_DIR)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from settings import config

DATABASE_URL = f"postgresql+asyncpg://" \
               f"{config.POSTGRES_USER}:" \
               f"{config.POSTGRES_PASS}@" \
               f"{config.POSTGRES_HOST}:" \
               f"{config.POSTGRES_PORT}/" \
               f"{config.POSTGRES_DB}"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

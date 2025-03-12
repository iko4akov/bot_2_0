from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from database.config import bot_url_db, admin_url_db

engine = create_async_engine(bot_url_db, echo=True)
admin_engine = create_async_engine(admin_url_db, isolation_level="AUTOCOMMIT")

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

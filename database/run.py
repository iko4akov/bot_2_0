import asyncio

from database.services.services import initialize_database
from utils import logger
from database import admin_engine, engine


async def init_db():
    await initialize_database(admin_engine, engine)
    logger.info("База данных успешно развернута!")

if __name__ == "__main__":
    asyncio.run(init_db())

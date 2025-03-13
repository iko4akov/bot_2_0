import asyncio

from bot.run import start_bot
from database.run import init_db


async def main():

    await init_db()
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main())

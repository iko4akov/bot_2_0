import asyncio

from bot.run import start_bot
from database.run import init_db
from parser.run import start_parser

async def main():
    await init_db()
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(start_parser())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(start_parser())

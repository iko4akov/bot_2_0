import asyncio

from parser.run import start_parser
from bot.run import start_bot

async def main():
    await start_bot()
    # await start_parser()

if __name__ == "__main__":
    asyncio.run(main())

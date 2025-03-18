from telethon import events, TelegramClient
from parser.monitoring import forward_message


async def setup_handlers(client: TelegramClient, target_channel: str, list_channels: list[str]):
    """
    Настраивает обработчики событий для мониторинга каналов.
    """

    @client.on(events.NewMessage(chats=list_channels))
    async def handler(event):
        message = event.message
        await forward_message(message, target_channel=target_channel, client=client)

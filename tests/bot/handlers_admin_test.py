import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.types import Message

from database.models import Users
from settings.config import ADMINS


@pytest.mark.asyncio
async def test_show_user():

    mock_message = MagicMock(spec=Message)
    mock_message.text = "!123"
    mock_message.reply = AsyncMock()

    mock_user = MagicMock(spec=Users)
    mock_message.from_user = mock_user
    mock_user.id = 31
    mock_user.to_dict.return_value = {"id": mock_message.text, "name": "Test User"}
    get_user_mock = AsyncMock(return_value=mock_user)

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("bot.decorators.admin_required.is_admin", lambda x: True)
        mp.setattr("bot.decorators.admin_required.admin_required", lambda x: x)

        from bot.handlers.handlers_admin import show_user
        mp.setattr("settings.config.ADMINS", [31])
        with patch("database.services.crud_user.get_user", get_user_mock):
            await show_user(mock_message)


    get_user_mock.assert_awaited_once_with(123)

    mock_message.reply.assert_awaited_once_with('Пользователь найден{"id": 123, "name": "Test User"}')

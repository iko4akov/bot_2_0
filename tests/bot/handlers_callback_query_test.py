import pytest

from unittest.mock import MagicMock, AsyncMock, patch

from bot.handlers.handlers_callback_query import callback_user


@pytest.mark.asyncio
async def test_callback_user():

    mock_callback_query = MagicMock()
    mock_callback_query.from_user.id = 123456
    mock_callback_query.id = 1

    mock_user = MagicMock()
    mock_user.info.return_value = {
        "Ваш id": mock_callback_query.from_user.id,
        "Ваш ник": "qwerty"
    }

    get_user_mock = AsyncMock(return_value=mock_user)

    mock_bot = AsyncMock()

    with patch("database.services.crud_user.get_user", get_user_mock),\
            patch("bot.bot", mock_bot):

        # Вызываем тестируемую функцию
        callback_user(mock_callback_query)

        # Проверяем, что метод answer был вызван
        mock_callback_query.answer.assert_called_once()

        # Проверяем, что метод send_message был вызван с правильными аргументами
        mock_bot.send_message.assert_called_once_with(
            123456, {"Ваш id": 123456, "Ваш ник": "qwerty"}
        )

        get_user_mock.assert_awaited_once_with(123456)

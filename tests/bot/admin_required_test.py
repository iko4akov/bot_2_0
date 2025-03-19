import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message, User

from bot.decorators.admin_required import admin_required, is_admin


@pytest.mark.asyncio
async def test_admin_required_with_admin():
    # Создаем мок для сообщения от администратора
    mock_message = MagicMock(spec=Message)
    mock_message.from_user = MagicMock(spec=User)
    mock_message.from_user.id = 123
    mock_message.reply = AsyncMock()

    # Мокируем функцию is_admin, чтобы она возвращала True для этого ID
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("bot.decorators.admin_required.is_admin", lambda x: True)

        # Мокируем обработчик, который должен быть вызван для администратора
        mock_handler = AsyncMock()
        wrapped_handler = admin_required(mock_handler)

        # Вызываем обернутый обработчик
        await wrapped_handler(mock_message)

        # Проверяем, что обработчик был вызван
        mock_handler.assert_awaited_once_with(mock_message)
        # Проверяем, что reply не был вызван (так как пользователь - администратор)
        mock_message.reply.assert_not_called()


@pytest.mark.asyncio
async def test_admin_required_with_non_admin():
    # Создаем мок для сообщения от не-администратора
    mock_message = MagicMock(spec=Message)
    mock_message.from_user = MagicMock(spec=User)
    mock_message.from_user.id = 5  # ID не-администратора
    mock_message.reply = AsyncMock()

    # Мокируем функцию is_admin, чтобы она возвращала False для этого ID
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("bot.decorators.admin_required.is_admin", lambda x: False)

        # Мокируем обработчик, который не должен быть вызван для не-администратора
        mock_handler = AsyncMock()
        wrapped_handler = admin_required(mock_handler)

        # Вызываем обернутый обработчик
        await wrapped_handler(mock_message)

        # Проверяем, что обработчик не был вызван
        mock_handler.assert_not_called()
        # Проверяем, что reply был вызван с правильным сообщением
        mock_message.reply.assert_awaited_once_with("У вас нет прав администратора.")


def test_is_admin():
    """Тестируем функцию is_admin"""
    admins = [123, 456]
    assert True == is_admin(123, admins)
    assert True == is_admin(456, admins)
    assert False == is_admin(789, admins)

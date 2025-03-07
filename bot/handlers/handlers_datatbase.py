import asyncio
import logging

from aiogram import Router, types

from bot import bot
from bot.keyboard import kb, DBKeyboard
from bot.services.for_error import handle_value_error, handle_general_error
from bot.services.for_handlers import process_public_posts, send_post_to_user
from bot.services.utils import parse_post_id
from database.services.crud_post import get_posts, get_post, update_post
from database.services.crud_user import get_user, update_user

db_router = Router()


@db_router.callback_query(lambda c: c.data == 'db')
async def show_posts(callback_query: types.CallbackQuery):
    """Показывает кнопки со всеми постами"""
    await callback_query.answer()
    user = await get_user(callback_query.from_user.id)
    posts = await get_posts(callback_query.from_user.id)
    kb_db = DBKeyboard(posts, user)
    inline_keyboard = kb_db.get_keyboard()
    if posts:
        await bot.edit_message_reply_markup(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=inline_keyboard
        )
    else:
        await bot.send_message(callback_query.from_user.id, "Нет постов", reply_markup=kb.inline_markup)

@db_router.callback_query(lambda c: c.data in ["next_page", "back_page"])
async def handle_pagination(callback_query: types.CallbackQuery):
    """Добавляет вкнопки назад и дальше в клавиатуру"""
    await callback_query.answer()
    user = await get_user(callback_query.from_user.id)
    posts = await get_posts(callback_query.from_user.id)
    total_pages = len(posts) // user.on_pages + (1 if len(posts) % user.on_pages != 0 else 0)

    if callback_query.data == "next_page":
        new_page = user.current_page + 1
    elif callback_query.data == "back_page":
        new_page = user.current_page - 1

    if 0 <= new_page < total_pages and new_page != user.current_page:
        user.current_page = new_page
        await update_user(user)
        kb_db = DBKeyboard(posts, user)
        inline_keyboard = kb_db.get_keyboard()

        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=inline_keyboard
        )
    else:
        if new_page < 0:
            await callback_query.answer("Вы уже на первой странице")
        elif new_page >= total_pages:
            await callback_query.answer("Вы уже на последней странице")

@db_router.callback_query(lambda c: c.data.startswith("|"))
async def show_post(callback_query: types.CallbackQuery):
    """Показывает, в чате с ботом, как будет выглядеть пост """
    await callback_query.answer()
    post_id = parse_post_id(callback_query.data)
    try:
        post = await get_post(post_id)
        if not post:
            raise ValueError("Пост не найден")

        await send_post_to_user(post, post.owner.tg_id)

    except ValueError as ve:
        await handle_value_error(callback_query, str(ve))
    except Exception as e:
        await handle_general_error(callback_query, e)

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text="-" * 60,
        reply_markup=kb.markup_for_post(post_id)
    )

@db_router.callback_query(lambda c: c.data == "public_all")
async def public_all(callback_query: types.CallbackQuery):
    """Публикует все не опубликованные посты"""
    try:
        await callback_query.answer("Начинаем публиковать...")
        await process_public_posts(callback_query)

    except Exception as e:
        logging.error(f"Ошибка при обработке callback: {str(e)}")

    inline_keyboard = kb.inline_markup
    await bot.send_message(
        callback_query.message.chat.id,
        "-"*60,
        reply_markup=inline_keyboard
    )

@db_router.callback_query(lambda c: c.data.startswith(">"))
async def publish_post(callback_query: types.CallbackQuery):
    """"""
    await callback_query.answer()
    try:
        post_id = parse_post_id(callback_query.data)

        post = await get_post(post_id)
        if not post:
            raise ValueError("Пост не найден")

        await send_post_to_user(post, post.owner.target)
        post.public = True
        await update_post(post)
        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=kb.inline_markup
        )

    except ValueError as ve:
        await handle_value_error(callback_query, str(ve))
    except Exception as e:
        await handle_general_error(callback_query, e)

@db_router.callback_query(lambda c: c.data.startswith("d"))
async def delete_post(callback_query: types.CallbackQuery):
    post_id = parse_post_id(callback_query.data)
    post = await get_post(post_id)
    post.public = True
    await update_post(post)
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=kb.inline_markup
    )

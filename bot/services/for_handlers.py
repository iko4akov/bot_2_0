import asyncio
from typing import Union

from aiogram import types

from bot import bot
from bot.services.for_error import handle_value_error, handle_general_error
from bot.services.utils import send_media_files
from database.models.models import Media, Post
from database.services.crud_post import get_posts, update_post


async def process_public_posts(callback_query: types.CallbackQuery):
    """Публикация всех постов со статусом public=False"""
    posts = await get_posts(callback_query.from_user.id)

    for post in posts:
        try:
            if post.media:
                await send_media_files(post.owner.target, post.media)
                await bot.send_message(callback_query.from_user.id, f"Пост {post.text[:6]} уже в канале")
                post.public = True
                await update_post(post)
                await asyncio.sleep(5)
            await bot.send_message(chat_id=post.owner.target, text=f"{post.text}")

        except ValueError as ve:
            await handle_value_error(callback_query, str(ve))
            post.public = True
            await update_post(post)
        except Exception as e:
            await handle_general_error(callback_query, e)
            post.public = True
            await update_post(post)

async def send_post_to_user(post: Post, target: Union[int, str]):
    """
    Отправляет текст и медиафайлы поста пользователю.
    """
    await bot.send_message(chat_id=target, text=f"{post.text}")

    if post.media:
        await send_media_files(target, post.media)
    else:
        await bot.send_message(target, "У этого поста нет медиа.")

from config import bot
from aiogram import types, Dispatcher

from database import sql_commands


async def echo_ban(message: types.Message):
    ban_words = ["damn", "fuck", "bitch"]

    if message.chat.id == -871316677:
        for word in ban_words:
            if word in message.text.lower().replace(" ", ""):
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=message.message_id
                )
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f"вы подозрительны. предупреждаю вы в одном шаге от бана\n\n"
                         f'Пользователь {message.from_user.username}'
                )


def register_chat_actions_handlers(dp: Dispatcher):
    dp.register_message_handler(echo_ban)

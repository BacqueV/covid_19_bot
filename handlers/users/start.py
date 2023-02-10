import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    # adding user into db
    try:
        db.add_user(id=message.from_user.id,
                    name=name)
        await message.answer(f"Welcome! {name}. Send me name of some country")
        # Informing admins
        count = db.count_users()[0]
        msg = f"{message.from_user.full_name} joined into db.\nThere are {count} users in db."
        await bot.send_message(chat_id=ADMINS[0], text=msg)

    except sqlite3.IntegrityError as err:
        await bot.send_message(chat_id=ADMINS[0], text=f"{name} is already in db")
        await message.answer(f"Welcome! {name}")

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = "I can do search of covid info for last month.\n" \
           "Send me countries or continents name"
    
    await message.answer(text)

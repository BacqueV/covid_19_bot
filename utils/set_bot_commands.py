from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "just adds you into db, what you expected?"),
            types.BotCommand("help", "explains you how bot works, but I think you already know"),
        ]
    )

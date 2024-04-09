from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start"),
            types.BotCommand("help", "Yordam"),
            # types.BotCommand("register", "Register"),
            # types.BotCommand("reset_password", "Kodni qayta yuborish"),
        ]
    )

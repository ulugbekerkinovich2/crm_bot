from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start"),
            types.BotCommand("restart", "Restart"),
            # types.BotCommand("register", "Register"),
            # types.BotCommand("reset_password", "Kodni qayta yuborish"),
        ]
    )

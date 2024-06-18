from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start"),
            types.BotCommand("restart", "Restart"),
            types.BotCommand("admin", "admin"),
            # types.BotCommand("reset_password", "Kodni qayta yuborish"),
        ]
    )

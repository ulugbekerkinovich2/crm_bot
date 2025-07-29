# import threading
# from aiogram import executor
# from loader import dp
# import middlewares, filters, handlers
# from utils.notify_admins import on_startup_notify
# from utils.set_bot_commands import set_default_commands
# from handlers.users.web_server import start_web_server

# async def on_startup(dispatcher):
#     # Birlamchi komandalar (/start va /help)
#     await set_default_commands(dispatcher)

#     # Bot ishga tushgani haqida adminga xabar berish
#     await on_startup_notify(dispatcher)

# if __name__ == '__main__':
#     # Start the web server in a separate thread
#     web_server_thread = threading.Thread(target=start_web_server)
#     web_server_thread.start()
    
#     # Start the Telegram bot
#     executor.start_polling(dp, on_startup=on_startup)


import threading
from loader import dp
from aiogram import executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.users.web_server import start_web_server
from utils.set_bot_commands import set_default_commands
from utils.notify_admins import on_startup_notify

async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)



if __name__ == '__main__':
    web_server_thread = threading.Thread(target=start_web_server)
    web_server_thread.start()

    executor.start_polling(dp, on_startup=on_startup)

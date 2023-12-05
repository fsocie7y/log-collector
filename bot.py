import os

import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

from log_processor import display_all_logs_in_the_directory

load_dotenv()

bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"{message.from_user.first_name} wellcome to Log Collector bot!\n"
                         f"Please enter absolute path to directory that you want to check.\n"
                         f"Or separate path by spaces.")


@dp.message()
async def echo(message: Message):
    print(message.text)

    search_log_res = display_all_logs_in_the_directory(message.text)
    if isinstance(search_log_res, list):
        await message.answer("\n".join(search_log_res))
    elif isinstance(search_log_res, str):
        await message.answer(search_log_res)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

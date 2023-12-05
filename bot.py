import os

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv

from states import lc_router
from keyboards import main_kb

load_dotenv()

storage = MemoryStorage()
bot = Bot(os.getenv("BOT_TOKEN"), parse_mode="HTML")
dp = Dispatcher(bot=bot, storage=storage)
dp.include_router(lc_router)


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(
        f"{message.from_user.first_name} wellcome to Log Collector bot!\n"
        f"U can see what options i have by typing <b>'/menu'</b> or click button below!",
        reply_markup=main_kb
    )


@dp.message(Command("menu"))
async def menu(message: Message) -> None:
    await message.answer(
        "I have such options:\n"
        "Log collection by directory - /collect_logs\n"
        "Analyzing log-file - /analyze_logs\n"
        "Menu - /menu",
        reply_markup=main_kb
    )


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

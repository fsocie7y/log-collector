from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           Message)
from aiogram.filters import Command
from aiogram import Router, F

from log_processor import (display_all_logs_in_the_directory,
                           read_log_file,
                           google_helper)
from keyboards import y_n, main_kb

lc_router = Router()


class FSMLogCollector(StatesGroup):
    dir_path = State()


class FSMLogAnalyzer(StatesGroup):
    file_path = State()
    help = State()


@lc_router.message(Command("cancel"))
@lc_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Cancelled.")


@lc_router.message(Command("collect_logs"))
async def st_collecting(message: Message, state: FSMContext) -> None:
    await state.set_state(FSMLogCollector.dir_path)
    await message.answer(
        "Please enter absolute path to directory that you want to check.\n"
        "Or separate path by spaces."
    )


@lc_router.message(FSMLogCollector.dir_path)
async def collecting(message: Message, state: FSMContext) -> None:
    print(message.text)

    search_log_res = display_all_logs_in_the_directory(message.text)
    if isinstance(search_log_res, list):
        await message.answer("\n".join(search_log_res))
    elif isinstance(search_log_res, str):
        await message.answer(search_log_res)

    await state.clear()


@lc_router.message(Command("analyze_logs"))
async def st_analyzing(message: Message, state: FSMContext) -> None:
    await state.set_state(FSMLogAnalyzer.file_path)
    await message.answer(
        "Please enter absolute path to log-life that you want to analyze.\n"
    )


@lc_router.message(FSMLogAnalyzer.file_path)
async def analyzing(message: Message, state: FSMContext) -> None:
    print(message.text)

    analyze_log_res = read_log_file(message.text)
    if isinstance(analyze_log_res, list):
        report = "\n".join(analyze_log_res)
        await state.update_data(issue=report)
        await state.set_state(FSMLogAnalyzer.help)
        await message.answer(
            f'Such errors was found - {len(analyze_log_res)}:\n'
            f'{report}\n'
            f'Do u want get help with this issue?',
            reply_markup=y_n
        )
    elif isinstance(analyze_log_res, str):
        await message.answer(analyze_log_res)
        await state.clear()


@lc_router.message(FSMLogAnalyzer.help, F.text.casefold() == "no")
async def process_dont_need_help(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Not bad not terrible.\nSee you soon.",
    )


@lc_router.message(FSMLogAnalyzer.help, F.text.casefold() == "yes")
async def process_need_help(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    issue = data.get("issue")
    await state.clear()
    await message.answer(
        f"This will help u to solve issue)\n"
        f"{google_helper(issue)}"
    )


@lc_router.message()
async def echo(message: Message):
    await message.answer(
        "I dont understand what u want)\n"
        "U can choose one option from buttons!",
        reply_markup=main_kb
    )

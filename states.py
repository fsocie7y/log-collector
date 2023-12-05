from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, Message
from aiogram.filters import Command
from aiogram import Router, F

from log_processor import display_all_logs_in_the_directory, read_log_file


lc_router = Router()


class FSMLogCollector(StatesGroup):
    dir_path = State()


class FSMLogAnalyzer(StatesGroup):
    file_path = State()


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
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@lc_router.message(Command("collect_logs"))
async def st_collecting(message: Message, state: FSMContext) -> None:
    await state.set_state(FSMLogCollector.dir_path)
    await message.answer(
        "Please enter absolute path to directory that you want to check.\n"
        "Or separate path by spaces.",
        reply_markup=ReplyKeyboardRemove()
    )


@lc_router.message(FSMLogCollector.dir_path)
async def collecting(message: Message) -> None:
    print(message.text)

    search_log_res = display_all_logs_in_the_directory(message.text)
    if isinstance(search_log_res, list):
        await message.answer("\n".join(search_log_res), reply_markup=ReplyKeyboardRemove())
    elif isinstance(search_log_res, str):
        await message.answer(search_log_res, reply_markup=ReplyKeyboardRemove())


@lc_router.message(Command("analyze_logs"))
async def st_analyzing(message: Message, state: FSMContext) -> None:
    await state.set_state(FSMLogAnalyzer.file_path)
    await message.answer(
        "Please enter absolute path to log-life that you want to analyze.\n",
        reply_markup=ReplyKeyboardRemove()
    )


@lc_router.message(FSMLogAnalyzer.file_path)
async def analyzing(message: Message) -> None:
    print(message.text)

    analyze_log_res = read_log_file(message.text)
    if isinstance(analyze_log_res, list):
        await message.answer(
            f'Such errors was found - {len(analyze_log_res)}:\n'
            f'{"\n".join(analyze_log_res)}',
            reply_markup=ReplyKeyboardRemove()
        )
    elif isinstance(analyze_log_res, str):
        await message.answer(analyze_log_res, reply_markup=ReplyKeyboardRemove())

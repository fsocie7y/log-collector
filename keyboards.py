from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/collect_logs"),
            KeyboardButton(text="/analyze_logs")
        ],
        [
            KeyboardButton(text="/cancel"),
            KeyboardButton(text="/menu")
        ]

    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Choose one option below...",
    selective=True
)

y_n = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Yes"),
            KeyboardButton(text="No"),
        ]
    ],
    resize_keyboard=True,

)

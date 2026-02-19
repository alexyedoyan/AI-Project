from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from texts import TEXTS

def lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
        ]
    ])

def soil_type_keyboard(lang: str) -> InlineKeyboardMarkup:
    soil_types = TEXTS[lang]["soil_types"]
    buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"soil_{key}")]
        for key, label in soil_types.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def skip_keyboard(lang: str) -> InlineKeyboardMarkup:
    skip_text = TEXTS[lang]["skip"]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"⏭ {skip_text}", callback_data="skip")]
    ])

def location_keyboard(lang: str) -> ReplyKeyboardMarkup:
    btn_text = TEXTS[lang]["send_location"]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn_text, request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()

def result_keyboard(lang: str) -> InlineKeyboardMarkup:
    new_field_text = TEXTS[lang]["new_field"]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=new_field_text, callback_data="new_field")]
    ])

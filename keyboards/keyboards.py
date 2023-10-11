from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon_ru import LEXICON_RU

button_upload: KeyboardButton = KeyboardButton(text=LEXICON_RU['upload'])
main_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[button_upload]],
    resize_keyboard=True
)

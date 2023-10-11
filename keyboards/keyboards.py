from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon_ru import LEXICON_RU

button_upload: InlineKeyboardButton = InlineKeyboardButton(
    text=LEXICON_RU['upload'],
    callback_data='upload_file',
)
main_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_upload]],
)

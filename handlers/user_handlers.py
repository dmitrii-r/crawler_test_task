import sqlite3

import pandas as pd
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import File, Message

from keyboards.keyboards import main_keyboard
from lexicon.lexicon_ru import LEXICON_RU
from services.parser import parse_prices

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    """
    Обработчик запуска бота.
    Выводит приветственное сообщение и основную клавиатуру.

    :param message: Объект сообщения от пользователя.
    :type message: types.Message

    :return: None
    :rtype: None
    """
    user_name: str = message.from_user.first_name
    start_text: str = LEXICON_RU['/start_prefix'] + user_name + LEXICON_RU['/start_postfix']
    await message.answer(text=start_text, reply_markup=main_keyboard)


@router.message(F.document)
async def handle_file(message: Message) -> None:
    """
    Обработчик загрузки файла Excel с данными о продуктах.

    :param message: Объект сообщения от пользователя.
    :type message: types.Message

    :return: None
    :rtype: None
    """
    file_id: str = message.document.file_id
    file_info: File = await message.bot.get_file(file_id)
    file = await message.bot.download_file(file_info.file_path)
    with open('data.xlsx', 'wb') as f:
        f.write(file.read())

    df: pd.DataFrame = pd.read_excel('data.xlsx')
    parsed_df: pd.DataFrame = parse_prices(df)

    await message.reply(LEXICON_RU['answer_parsed_data'] + parsed_df.to_string())

    con = sqlite3.connect('db.sqlite3')
    parsed_df.to_sql('zuzublik_data', con, index=False, if_exists='append')
    con.close()

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

import asyncio

from random import *
from datetime import *

from config import bot_token
from database import *


async def main() -> None:
    bot = Bot(bot_token)
    await dp.start_polling(bot)


def random_num():
    win_nums = [1, 2, 3, 4]
    return randrange(1, 11) in win_nums


dp = Dispatcher()

TRI_TOPORA = [64]
VICTORY = [1, 22, 43]

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}!\n"
                         f"Ты зашел в казик 👹👹👹 буэээээээээээ\n"
                         f"Надеюсь ты оставишь тут все свои бабки 🤑🤑🤑")


@dp.message()
async def message_handler(message: Message) -> None:
    user_id = message.from_user.id
    user_message = message.text
    user_dice = message.dice
    user_username = message.from_user.username

    if user_dice:
        dice_type = user_dice.emoji
        score = user_dice.value
        current_time = datetime.utcnow()

        if dice_type == '🎰':
            print(current_time, user_id, user_username, score)
            '''
            1 - бары
            22 - виноградик
            43 - лимоны
            64 - топоры  # по тестам 1:300
            '''
            new_user(user_id, current_time)
            new_krutochka(user_id, score in VICTORY + TRI_TOPORA, current_time)

            if score in VICTORY:
                try:
                    await asyncio.sleep(1.5)
                    await message.reply('почти джекпот')
                except Exception as e:
                    print(f'пидорас на {user_id}, {user_username} все сломал!\n{e}')
            elif score in TRI_TOPORA:
                try:
                    await asyncio.sleep(1.5)
                    await message.reply('УРААААААААААААААААААА!!!!!!!!!!\nТЫ ВЫИГРАЛ ЖИЗНЬЬЬЬЬЬЬЬЬ')
                except Exception as e:
                    print(f'пидорас на {user_id}, {user_username} все сломал!\n{e}')
            else:
                try:
                    await asyncio.sleep(1.5)
                    await message.reply('ты просрал бабки(((')
                except Exception as e:
                    print(f'пидорас на {user_id}, {user_username} все сломал!\n{e}')
        else:
            pass

    if user_message:
        pass


if __name__ == "__main__":
    input('Если хочешь запустить не из main, нажми Enter')
    asyncio.run(main())

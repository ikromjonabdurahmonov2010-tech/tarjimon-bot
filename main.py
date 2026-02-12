from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


bot = Bot(token="8344603285:AAEmV_4Bm7UoYCfcvlWTvAhVUlxXgoYdQ7s")
dp = Dispatcher()

MOVIES = {}
movie_id = 1
ADMIN_ID = 8010711230

@dp.message(Command('start'))
async def start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        keyboards = ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text='Kino qoshish ➕'),
                KeyboardButton(text='Kino qidirish 🔎')
            ]
        ],
            resize_keyboard=True,
            input_field_placeholder="Menyudan tanlang..."
        )
        await message.answer(
            f"Assalomu alaykum {message.from_user.first_name}\n\n"
            "🎥 Kino botga xush kelibsiz!\n", reply_markup=keyboards)
    else:
        keyboards = ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text='Kino qidirish 🔎')
            ]
        ],
            resize_keyboard=True,
            input_field_placeholder="Menyudan tanlang..."
        )
        await message.answer(
            f"Assalomu alaykum {message.from_user.first_name}\n\n"
            "🎥 Kino botga xush kelibsiz!\n", reply_markup=keyboards)




@dp.message(F.text == "Kino qoshish ➕")
async def msg_video(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer('Iltimos kinoni yuboring ...')
    else:
        await message.answer('Bunday buyruq mavjud emas ...')


@dp.message(F.video)
async def add_video(message: types.Message):
    global movie_id
    if message.video:
        if message.from_user.id == ADMIN_ID:
            MOVIES[movie_id] = {
                'title': f'Kino #{movie_id}',
                'film_id': message.video.file_id
            }
            movie_id += 1
            await message.answer('Kino botga qoshildi !!!')
        else:
            await message.answer('Sizga ruxsat yoq !!!')
    else:
        await message.answer('Iltimos faqat video yuboring !!!')

@dp.message(F.text == "Kino qidirish 🔎")
async def search_video(message: types.Message):
    await message.answer('Kino raqamini kiriting ...')

@dp.message(F.text)
async def get_video(message: types.Message):
    global movie_id
    if message.text:
        if not message.text.isdigit():
            await message.answer('Iltimos faqat raqam kiriting !!!')
        raqam = int(message.text)
        movie = MOVIES.get(raqam)
        if movie:
            await message.answer_video(
                video=movie["film_id"],
                caption=f"🎬 {movie['title']}"
            )
        else:
            await message.answer('Bunday raqamli kino topilmadi 🔎')


async def start_bot():
    print('Bot starting...')
    await dp.start_polling(bot)


asyncio.run(start_bot())

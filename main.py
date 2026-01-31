import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from googletrans import Translator
from gtts import gTTS

TOKEN = "7355562290:AAETdSAKBnT2DuiswTDH9tkgDNrSayrf86Q"

dp = Dispatcher()
translator = Translator()


class TranslateState(StatesGroup):
    choosing_direction = State()
    translating = State()


# Tillar ro'yxati
LANGS = [
    ("🇬🇧", "Ingliz", "en"),
    ("🇷🇺", "Rus", "ru"),
    ("🇹🇷", "Turk", "tr"),
    ("🇩🇪", "Nemis", "de"),
    ("🇫🇷", "Fransuz", "fr"),
    ("🇰🇷", "Koreys", "ko"),
    ("🇨🇳", "Xitoy", "zh-cn"),
    ("🇦🇪", "Arab", "ar"),
    ("🇪🇸", "Ispan", "es"),
    ("🇯🇵", "Yapon", "ja")
]


# Pastda turadigan "Menuga qaytish" tugmasi
def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🔝 Menuga qaytish")
    return builder.as_markup(resize_keyboard=True)


# Inline til tanlash menyusi
def get_lang_keyboard():
    builder = InlineKeyboardBuilder()
    for flag, name, code in LANGS:
        builder.button(text=f"{flag}{name} - Uzb", callback_data=f"dir_{code}_uz")
        builder.button(text=f"Uzb - {flag}{name}", callback_data=f"dir_uz_{code}")
    builder.adjust(2)
    return builder.as_markup()


@dp.message(CommandStart())
@dp.message(F.text == "🔝 Menuga qaytish")  # Har qanday holatda menyuga qaytaradi
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(TranslateState.choosing_direction)
    await message.answer(
        "Assalomu alaykum! Yo'nalishni tanlang:",
        reply_markup=get_main_menu()  # Pastdagi tugmani chiqaradi
    )
    await message.answer(
        "Tillar ro'yxati:",
        reply_markup=get_lang_keyboard()
    )


@dp.callback_query(F.data.startswith("dir_"))
async def set_direction(callback: types.CallbackQuery, state: FSMContext):
    _, src, dest = callback.data.split("_")
    await state.update_data(src=src, dest=dest)
    await state.set_state(TranslateState.translating)
    await callback.message.edit_text(
        f"✅ <b>{src.upper()} - {dest.upper()}</b> tanlandi.\nMatn yuboring:",
        parse_mode="HTML"
    )
    await callback.answer()


@dp.message(TranslateState.translating)
async def translate_text(message: types.Message, state: FSMContext):
    if not message.text or message.text == "🔝 Menuga qaytish":
        return

    data = await state.get_data()
    src_l = data.get('src')
    dest_l = data.get('dest')

    try:
        # 1. Matnni tarjima qilish
        res = translator.translate(message.text, src=src_l, dest=dest_l)
        await message.reply(f"<b>Natija:</b>\n\n{res.text}", parse_mode="HTML")

        # 2. Ovozli fayl yaratish
        tts = gTTS(text=res.text, lang=dest_l)
        file_name = f"voice_{message.from_user.id}.mp3"
        tts.save(file_name)

        # 3. Ovozni yuborish
        voice_file = types.FSInputFile(file_name)
        await message.answer_voice(voice=voice_file)

        # 4. Faylni o'chirish
        os.remove(file_name)

    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.answer("Xatolik! Qayta urinib ko'ring.")


async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
import os
API_TOKEN = os.getenv("API_TOKEN")


ADMIN_ID = 416293512               # <-- твой Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Машина состояний для анкеты
class Anketa(StatesGroup):
    fio_child = State()
    age = State()
    fio_parent = State()
    phone = State()
    experience = State()
    medical = State()

# Главное меню
def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 О нас", callback_data="about")],
        [InlineKeyboardButton(text="📍 Как нас найти", callback_data="location")],
        [InlineKeyboardButton(text="🗓 Расписание", callback_data="schedule")],
        [InlineKeyboardButton(text="👩‍🏫 Наши педагоги", callback_data="teachers")],
        [InlineKeyboardButton(text="🛍 Товары", callback_data="products")],
        [InlineKeyboardButton(text="📝 Анкета для записи", callback_data="anketa")],
        [InlineKeyboardButton(text="🎁 Пробное занятие", callback_data="trial")],
        [InlineKeyboardButton(text="🏢 Наш зал", callback_data="hall")],
        [InlineKeyboardButton(text="⭐ Отзывы", callback_data="reviews")],
        [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")],
    ])
    return kb

# ============================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================
async def send_about(message: types.Message):
    await message.answer(
        "Танцевальная студия *Place of dance* открылась в 2023 году.\n"
        "Основное направление – Hip-Hop, также Dancehall, Waacking, Jazzfunk.\n"
        "У нас группы с 5 лет, начинающие и продолжающие.",
        parse_mode="Markdown"
    )

async def send_location(message: types.Message):
    await message.answer("📍 Как нас найти: https://vk.ru/clip-221829288_456239630")

async def send_schedule(message: types.Message):
    await message.answer(
        "🗓 *Расписание занятий:*\n"
        "Пн, Ср 5-8 лет (16.30-17.30), (17.30-18.30)\n"
        "Пн, Ср 9-12 лет (18.30-19.30)\n"
        "Пн, Ср 16+ (19.30-20.30)\n"
        "Вт, Чт 9-12 лет (16.30-17.30)\n"
        "Вт, Чт 5-8 лет (17.30-18.30)\n"
        "Вт, Чт 9-12 лет (19.30-19.30)\n"
        "Вт, Чт 16+ (19.30-20.30)",
        parse_mode="Markdown"
    )

async def send_teachers(target):
    photo = FSInputFile("D:/PythonProject3/julia.jpg")
    await target.answer_photo(
        photo,
        caption=(
            "👩‍🏫 *Мильшина Юлия Александровна* — руководитель и педагог студии.\n"
            "▪ Окончила МГИК (2018)\n"
            "▪ Участница Flyographers (чемпионы HHI 2014)\n"
            "▪ Шоу «Новые танцы» ТНТ 2 сезон\n"
            "▪ Педагог-хореограф студии Play (2016-2023)"
        ),
        parse_mode="Markdown"
    )

# ====== Товары ======
def products_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👕 Футболка", callback_data="product_tshirt")],
        [InlineKeyboardButton(text="🎨 Стикерпак", callback_data="product_stickers")],
        [InlineKeyboardButton(text="📱 3D наклейка на телефон", callback_data="product_3d")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="back_main")]
    ])
    return kb

async def send_products(message: types.Message):
    await message.answer("🛍 Наши товары:", reply_markup=products_menu())

async def send_product_tshirt(message: types.Message):
    photos = [FSInputFile("tshirt1.jpg"), FSInputFile("tshirt2.jpg")]
    media = [types.InputMediaPhoto(media=p) for p in photos]
    await message.answer_media_group(media)
    await message.answer("👕 Футболка — 1200₽")

async def send_product_stickers(message: types.Message):
    photo = FSInputFile("stickerpack.jpg")
    await message.answer_photo(photo, caption="🎨 Стикерпак — 200₽")

async def send_product_3d(message: types.Message):
    photo = FSInputFile("sticker3d.jpg")
    await message.answer_photo(photo, caption="📱 3D наклейка на телефон — 300₽")

# ====== Остальное ======
async def send_trial(message: types.Message):
    await message.answer(
        "🎁 Пробное занятие бесплатно!\n"
        "С собой: спортивная одежда, сменная обувь, вода 💧"
    )

async def send_hall(message: types.Message):
    photos = ["hall1.jpg", "hall2.jpg", "hall3.jpg", "hall4.jpg"]
    media = [types.InputMediaPhoto(media=FSInputFile(p)) for p in photos]
    await message.answer_media_group(media)

async def send_reviews(message: types.Message):
    await message.answer("⭐ Отзывы: https://vk.ru/reviews-221829288")

async def send_contacts(message: types.Message):
    await message.answer("📞 Мильшина Юлия Александровна\n☎ 8-919-269-05-85")

# ============================
# КОМАНДЫ
# ============================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет, мы танцевальная студия *Place of dance*!\n"
        "Здесь ты можешь узнать о нас и записаться на занятие!",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

@dp.message(Command("about"))
async def cmd_about(message: types.Message): await send_about(message)

@dp.message(Command("location"))
async def cmd_location(message: types.Message): await send_location(message)

@dp.message(Command("schedule"))
async def cmd_schedule(message: types.Message): await send_schedule(message)

@dp.message(Command("teachers"))
async def cmd_teachers(message: types.Message): await send_teachers(message)

@dp.message(Command("products"))
async def cmd_products(message: types.Message): await send_products(message)

@dp.message(Command("trial"))
async def cmd_trial(message: types.Message): await send_trial(message)

@dp.message(Command("hall"))
async def cmd_hall(message: types.Message): await send_hall(message)

@dp.message(Command("reviews"))
async def cmd_reviews(message: types.Message): await send_reviews(message)

@dp.message(Command("contacts"))
async def cmd_contacts(message: types.Message): await send_contacts(message)

# Анкета через команду
@dp.message(Command("anketa"))
async def cmd_anketa(message: types.Message, state: FSMContext):
    await message.answer("📝 Введите ФИО ребёнка:")
    await state.set_state(Anketa.fio_child)

# ============================
# КНОПКИ (callback)
# ============================
@dp.callback_query(F.data == "about")
async def cb_about(callback: types.CallbackQuery):
    await send_about(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "location")
async def cb_location(callback: types.CallbackQuery):
    await send_location(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "schedule")
async def cb_schedule(callback: types.CallbackQuery):
    await send_schedule(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "teachers")
async def cb_teachers(callback: types.CallbackQuery):
    await send_teachers(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "products")
async def cb_products(callback: types.CallbackQuery):
    await send_products(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "product_tshirt")
async def cb_product_tshirt(callback: types.CallbackQuery):
    await send_product_tshirt(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "product_stickers")
async def cb_product_stickers(callback: types.CallbackQuery):
    await send_product_stickers(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "product_3d")
async def cb_product_3d(callback: types.CallbackQuery):
    await send_product_3d(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "back_main")
async def cb_back_main(callback: types.CallbackQuery):
    await callback.message.answer("⬅ Возврат в меню", reply_markup=main_menu())
    await callback.answer()

@dp.callback_query(F.data == "trial")
async def cb_trial(callback: types.CallbackQuery):
    await send_trial(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "hall")
async def cb_hall(callback: types.CallbackQuery):
    await send_hall(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "reviews")
async def cb_reviews(callback: types.CallbackQuery):
    await send_reviews(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "contacts")
async def cb_contacts(callback: types.CallbackQuery):
    await send_contacts(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "anketa")
async def cb_anketa(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("📝 Введите ФИО ребёнка:")
    await state.set_state(Anketa.fio_child)
    await callback.answer()

# ============================
# АНКЕТА
# ============================
@dp.message(Anketa.fio_child)
async def anketa_name(message: types.Message, state: FSMContext):
    await state.update_data(fio_child=message.text)
    await message.answer("Возраст ребёнка:")
    await state.set_state(Anketa.age)

@dp.message(Anketa.age)
async def anketa_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("ФИО родителя:")
    await state.set_state(Anketa.fio_parent)

@dp.message(Anketa.fio_parent)
async def anketa_parent(message: types.Message, state: FSMContext):
    await state.update_data(fio_parent=message.text)
    await message.answer("Номер телефона родителя:")
    await state.set_state(Anketa.phone)

@dp.message(Anketa.phone)
async def anketa_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Есть ли опыт в танцах?")
    await state.set_state(Anketa.experience)

@dp.message(Anketa.experience)
async def anketa_exp(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer("Есть ли медицинские противопоказания?")
    await state.set_state(Anketa.medical)

@dp.message(Anketa.medical)
async def anketa_done(message: types.Message, state: FSMContext):
    await state.update_data(medical=message.text)
    data = await state.get_data()

    text = (
        f"📝 Новая анкета!\n\n"
        f"👶 Ребёнок: {data['fio_child']}\n"
        f"🎂 Возраст: {data['age']}\n"
        f"👩‍👦 Родитель: {data['fio_parent']}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"💃 Опыт: {data['experience']}\n"
        f"⚕ Противопоказания: {data['medical']}"
    )

    await message.answer("✅ Спасибо, заявка отправлена! Мы свяжемся с вами 📞")
    await bot.send_message(ADMIN_ID, text)
    await state.clear()

# ============================
# ЗАПУСК
# ============================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

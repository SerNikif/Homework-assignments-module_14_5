from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from crud_functions import *

api = '7938094703:AAGSdDlTimj7iYifQvLl9Ls3PYpS0aguXrY'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb0 = ReplyKeyboardMarkup(resize_keyboard=True)
button3 = KeyboardButton(text='Рассчитать')
button4 = KeyboardButton(text='Информация')
button5 = KeyboardButton(text='Купить')
button6 = KeyboardButton(text='Регистрация')
kb0.row(button3, button4)
kb0.add(button5)
kb0.add(button6)

kb = InlineKeyboardMarkup(resize_keyboard=True)
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb.row(button, button2)

kb1 = InlineKeyboardMarkup(resize_keyboard=True)
button6 = InlineKeyboardButton(text='Product 1', callback_data="product_buying")
button7 = InlineKeyboardButton(text='Product 2', callback_data="product_buying")
button8 = InlineKeyboardButton(text='Product 3', callback_data="product_buying")
button9 = InlineKeyboardButton(text='Product 4', callback_data="product_buying")
kb1.row(button6, button7, button8, button9)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb0)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о боте!')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    await message.answer('Название: Product 1 | Описание: Описание1 | Цена: 100')
    with open("file/1.png", 'rb') as img:
        await message.answer_photo(img, reply_markup=kb0)
    await message.answer('Название: Product 2 | Описание: Описание2 | Цена: 200')
    with open("file/2.png", 'rb') as img:
        await message.answer_photo(img, reply_markup=kb0)
    await message.answer('Название: Product 3 | Описание: Описание3 | Цена: 300')
    with open("file/3.png", 'rb') as img:
        await message.answer_photo(img, reply_markup=kb0)
    await message.answer('Название: Product 4 | Описание: Описание4 | Цена: 400')
    with open("file/4.png", 'rb') as img:
        await message.answer_photo(img, reply_markup=kb0)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb1)


@dp.callback_query_handler(text='Product 1')
async def get_buying_list(call):
    await call.message.answer()
    await call.answer()


@dp.callback_query_handler(text='Product 2')
async def get_buying_list(call):
    await call.message.answer()
    await call.answer()


@dp.callback_query_handler(text='Product 3')
async def get_buying_list(call):
    await call.message.answer()
    await call.answer()


@dp.callback_query_handler(text='Product 4')
async def get_buying_list(call):
    await call.message.answer()
    await call.answer()


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=float(message.text))
    await message.answer('Введите свой рост (см.):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=float(message.text))
    await message.answer('Введите свой вес (кг.):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=float(message.text))
    data = await state.get_data()
    norm_cal = (10.0 * data['weight']) + (6.25 * data['growth']) - (5.0 * data['age']) - 161.0
    await message.answer(f'Ваша норма калорий - {norm_cal}', reply_markup=kb0)
    await state.finish()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит): ")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    available = is_included(message.text)
    if available is True:
        await message.answer("Пользователь существует, введите другое имя")
    else:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email: ")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст: ")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer('Регистрация прошла успешно', reply_markup=kb0)
    await state.finish()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

api = ''

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button1)
kb.add(button2)

inline_kb = InlineKeyboardMarkup()
inline_b1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_b2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.add(inline_b1, inline_b2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands='start')
async def start_message(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    result = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] - 161
    await message.answer(f'Ваша норма калорий: {result}')
    await state.finish()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

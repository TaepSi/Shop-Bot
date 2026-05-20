from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    photo = State()

@router.message(F.text == "Админ-панель")
async def admin_panel(message: Message):
    await message.answer("Демо админ-панель\n\nКоманда: /add_product")

@router.message(F.text == "/add_product")
async def add_product_start(message: Message, state: FSMContext):
    await state.set_state(AddProduct.name)
    await message.answer("Введите название товара:")

@router.message(AddProduct.name)
async def add_product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProduct.description)
    await message.answer("Введите описание:")

@router.message(AddProduct.description)
async def add_product_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddProduct.price)
    await message.answer("Введите цену:")

@router.message(AddProduct.price)
async def add_product_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(AddProduct.photo)
    await message.answer("Отправьте фото товара:")

@router.message(AddProduct.photo, F.photo)
async def add_product_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
    text = (
        "Товар получен (демо-режим, не сохранён)\n\n"
        f"Название: {data['name']}\n"
        f"Описание: {data['description']}\n"
        f"Цена: {data['price']} ₽\n"
        f"Photo file_id:\n{photo_id}"
    )
    await message.answer(text)
    await state.clear()
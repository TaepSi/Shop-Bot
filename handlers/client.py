from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards import main_menu, product_keyboard
from database import get_products, add_to_cart, get_cart, clear_cart

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать в ShopBot!\n\n"
        "Это демо-версия бота-витрины. Вы можете посмотреть каталог, добавить товары в корзину и оформить заказ. "
        "Админ-панель доступна по кнопке \"Админ-панель\".\n\n"
        "Для заказа персонального бота обратитесь к разработчику.",
        reply_markup=main_menu
    )

@router.message(F.text == "Каталог")
async def catalog_handler(message: Message):
    products = await get_products()
    if not products:
        await message.answer("Каталог пуст.")
        return
    for p in products:
        pid, name, desc, price, photo = p
        text = f"<b>{name}</b>\n\n{desc}\n\nЦена: {price} ₽"
        await message.answer_photo(photo=photo, caption=text, reply_markup=product_keyboard(pid))

@router.callback_query(F.data.startswith("add_"))
async def add_cart_handler(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    await add_to_cart(callback.from_user.id, product_id)
    await callback.answer("Товар добавлен!")

@router.message(F.text == "Корзина")
async def cart_handler(message: Message):
    cart = await get_cart(message.from_user.id)
    if not cart:
        await message.answer("Корзина пуста.")
        return
    text = "<b>Ваша корзина:</b>\n\n"
    total = 0
    for name, price, qty in cart:
        item_total = price * qty
        total += item_total
        text += f"{name}\n{qty} x {price} ₽ = {item_total} ₽\n\n"
    text += f"<b>Итого:</b> {total} ₽"
    await message.answer(text)

@router.message(F.text == "Оформить заказ")
async def order_handler(message: Message):
    cart = await get_cart(message.from_user.id)
    if not cart:
        await message.answer("Корзина пуста.")
        return
    await clear_cart(message.from_user.id)
    await message.answer("Заказ оформлен! (демо-режим)")

@router.message(F.text == "Контакты")
async def contacts_handler(message: Message):
    await message.answer(
        "Это демо-версия бота.\n"
        "Для заказа персонального бота обратитесь к разработчику:\n"
        "https://kwork.ru/user/demurgas"
    )
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Каталог")],
        [KeyboardButton(text="Корзина"), KeyboardButton(text="Оформить заказ")],
        [KeyboardButton(text="Контакты"), KeyboardButton(text="Админ-панель")],
    ],
    resize_keyboard=True
)

def product_keyboard(product_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_{product_id}")]
    ])
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


# main keyboard
main_keyboard = [
    ["б’юті консьерж", "поділитись відгуком", "Q & A"]
]

main_keyboard_markup = ReplyKeyboardMarkup(
    keyboard=main_keyboard,
    resize_keyboard=True
)

# q&a keyboard
q_and_a_keyboard = [
    [
        InlineKeyboardButton(
            text="Магазин (адреса, номер, паркування, графік)",
            callback_data="shop_inline_button_click"
        ),
    ],
    [
        InlineKeyboardButton(
            text="Доставка",
            callback_data="delivery_inline_button_click"
        ),
    ],
    [
        InlineKeyboardButton(
            text="Оплата",
            callback_data="payment_inline_button_click"
        ),
    ],
    [
        InlineKeyboardButton(
            text="Сертифікат",
            callback_data="certificate_inline_button_click"
        ),
    ],
]

q_and_a_inline_keyboard_markup = InlineKeyboardMarkup(
    inline_keyboard=q_and_a_keyboard
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_add(username: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Добавить",
                callback_data=f"add:{username}"
            )
        ]
    ])


def edit_menu(username: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔴 Занят",
                callback_data=f"busy:{username}"
            ),
            InlineKeyboardButton(
                text="⭐ Отзыв",
                callback_data=f"review:{username}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🗑 Удалить",
                callback_data=f"delete:{username}"
            )
        ]
    ])

def confirm_bulk_add(usernames: list[str]):
    data = "|".join(usernames)
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"➕ Добавить {len(usernames)} пользователей",
                callback_data=f"bulk_add:{data}"
            )
        ]
    ])
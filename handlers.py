from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils import valid_username, is_admin
from keyboards import confirm_add, edit_menu
from sheets import (
    add_user, get_free_users,
    set_status, delete_user
)
from states import EditState

from states import AddState
from keyboards import confirm_bulk_add
from sheets import find_row


router = Router()

@router.message(Command("add"))
async def add_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AddState.collecting)
    await state.update_data(users=[])
    await message.answer(
        "Отправь usernames (по одному сообщению).\n"
        "Когда закончишь — напиши /done"
    )

@router.message(AddState.collecting)
async def collect_usernames(message: Message, state: FSMContext):
    text = message.text.strip()

    if text.startswith("/"):
        return

    if not valid_username(text):
        await message.answer(f"❌ Неверный username: {text}")
        return

    data = await state.get_data()
    users = data.get("users", [])

    if text in users:
        await message.answer(f"⚠️ {text} уже в списке")
        return

    users.append(text)
    await state.update_data(users=users)
    await message.answer(f"✅ {text} добавлен в список")

@router.message(Command("done"))
async def add_done(message: Message, state: FSMContext):
    data = await state.get_data()
    users = data.get("users", [])

    if not users:
        await message.answer("Список пуст")
        return

    await state.clear()
    await message.answer(
        "Добавить пользователей?\n\n" + "\n".join(users),
        reply_markup=confirm_bulk_add(users)
    )

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Бот управления исполнителями 🚀")


@router.message(Command("allfree"))
async def allfree(message: Message):
    free = get_free_users()
    if not free:
        await message.answer("Свободных исполнителей нет")
    else:
        await message.answer("\n".join(free))


@router.message(Command("edit"))
async def edit(message: Message, state: FSMContext):
    await message.answer("Отправь username исполнителя")
    await state.set_state(EditState.waiting_username)


@router.message(EditState.waiting_username)
async def process_edit_username(message: Message, state: FSMContext):
    username = message.text.strip()

    if not valid_username(username):
        await message.answer("❌ Неверный формат username")
        return

    if not find_row(username):
        await message.answer(
            f"❌ Пользователь {username} не найден в таблице"
        )
        return

    await state.clear()
    await message.answer(
        f"Выбери действие для {username}",
        reply_markup=edit_menu(username)
    )



@router.message(F.text)
async def add_candidate(message: Message):
    if not valid_username(message.text):
        return

    await message.answer(
        f"Добавить {message.text}?",
        reply_markup=confirm_add(message.text)
    )


@router.callback_query(F.data.startswith("add:"))
async def cb_add(call: CallbackQuery):
    username = call.data.split(":")[1]
    if add_user(username):
        await call.message.edit_text(f"{username} добавлен ✅")
    else:
        await call.message.edit_text("Пользователь уже существует")


@router.callback_query(F.data.startswith("busy:"))
async def cb_busy(call: CallbackQuery):
    username = call.data.split(":")[1]
    set_status(username, "занят")
    await call.message.edit_text(f"{username} отмечен как занят")


@router.callback_query(F.data.startswith("review:"))
async def cb_review(call: CallbackQuery):
    username = call.data.split(":")[1]
    set_status(username, "review")
    await call.message.edit_text(f"Отзыв для {username} отмечен")


@router.callback_query(F.data.startswith("delete:"))
async def cb_delete(call: CallbackQuery):
    username = call.data.split(":")[1]
    delete_user(username)
    await call.message.edit_text(f"{username} удалён ❌")

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from keyboars.buttons import get_remind, get_time
import asyncio
from aiogram.fsm.state import *
from aiogram.fsm.context import *
from aiogram.fsm.storage.base import (
    BaseEventIsolation,
    BaseStorage,
    StateType,
    StorageKey,
)


from datetime import datetime
router = Router()  # [1]
class on_off_reminder(StatesGroup):
    off = State()
    on = State()
    process = State()

@router.message(Command("start"))  # [2]
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Привет! Я бот, который может напоминать тебе о твоих делах! Напиши /new, чтобы создать новое напоминание.')
    await state.set_state(on_off_reminder.off)

@router.message(Command('new'))
async def new_reminder(message: Message, state: FSMContext):
    await message.answer('Введи в сообщение то, что хочешь записать в напоминание:')
    await state.set_state(on_off_reminder.process)

@router.message(F.text, on_off_reminder.off)
async def skip(message: Message):
    if message.text not in '/new/get':
        await message.answer('Неверная команда. Если вы хотите поменять напоминалку напишите /new')

@router.message(on_off_reminder.process)
async def work_reminder(message: Message, state: FSMContext):
    await state.update_data(reminder_choice = message.text)
    await message.answer('Готово! Напиши /get, чтобы вызвать')
    await state.set_state(on_off_reminder.on)

@router.message(Command('get'), on_off_reminder.on)
async def get_reminder(message: Message, state: FSMContext):
    user_reminder = await state.get_data()
    await message.answer(user_reminder['reminder_choice'])

@router.message(F.text, on_off_reminder.on)
async def skip(message: Message):
    if message.text not in '/new/get':
        await message.answer('Неверная команда. Если вы хотите поменять напоминалку напишите /new')

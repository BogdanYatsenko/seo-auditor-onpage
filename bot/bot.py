import os, asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import Lead
from app.notify import notify_manager

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
MANAGER_CHAT_ID = os.getenv('MANAGER_CHAT_ID', '')

class LeadForm(StatesGroup):
    name = State()
    phone = State()
    note = State()

async def start_handler(message: types.Message):
    await message.answer("Hi! Send /lead to leave your contacts.")

async def lead_start(message: types.Message, state: FSMContext):
    await state.set_state(LeadForm.name)
    await message.answer("Your name?")

async def lead_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(LeadForm.phone)
    await message.answer("Your phone?")

async def lead_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await state.set_state(LeadForm.note)
    await message.answer("Any note? (or type - )")

async def lead_note(message: types.Message, state: FSMContext):
    note = message.text.strip()
    if note == '-':
        note = ''
    data = await state.get_data()
    name = data.get('name', '')
    phone = data.get('phone', '')
    # Save to DB
    db: Session = SessionLocal()
    lead = Lead(name=name, phone=phone, note=note, source='bot')
    db.add(lead)
    db.commit()
    db.close()
    # Notify manager
    notify_manager(f"<b>New lead (bot)</b>\nName: {name}\nPhone: {phone}\nNote: {note}")
    await message.answer("Thanks! A manager will contact you soon.")
    await state.clear()

async def main():
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")
    init_db()  # ensure tables exist
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.register(start_handler, F.text == "/start")
    dp.message.register(lead_start, F.text == "/lead")
    dp.message.register(lead_name, LeadForm.name)
    dp.message.register(lead_phone, LeadForm.phone)
    dp.message.register(lead_note, LeadForm.note)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

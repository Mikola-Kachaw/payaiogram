import logging, asyncio, yookassa, uuid
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from yookassa import Payment

TOKEN = '7639956752:AAGITQf-wtLmtVNAO6JmFGorI3NuCkiP9Mk'
PRICE = '1.00'
ACCOUNT_ID = '466584'
SECRET_KEY = 'test_aAgJF29QR81io4GgAGr6A-YuXpqYlY29MmrcYd1fgUU'

bot = Bot(TOKEN)
db = Dispatcher()
router = Router()
db.include_router(router)

yookassa.Configuration.account_id = ACCOUNT_ID
yookassa.Configuration.secret_key = SECRET_KEY

def create(amount, chat_id):
    id_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            'value': amount,
            'currency': "RUB"
        },
        'payment_method_data': {
            'type': 'bank_card'
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': 'https://web.telegram.org/a/#7192210344'
        },
        'capture': True,
        'metadata': {
            'chat_id': chat_id
        },
        'description': 'Подписка бота на 1 месяц'
    }, id_key)

    return payment.confirmation.confirmation_url, payment.id


@router.message(Command(commands=['buy']))
async def buy_handler(message: Message):
    payments_url, payments_id = create(PRICE, message.chat.id)

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Оплатить',
        web_app=WebAppInfo(url=payments_url)
    ))

    await message.answer(f"Счёт сформирован", reply_markup=builder.as_markup())


async def main():
    await db.start_polling(bot, skip_updates=False)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

import telebot
from telebot import types

import main_menu as menu
import acquain as acq
from database import BotDB
import abonement as abon
import exerc
import progress as progr

db = BotDB()
db.setup()

bot = telebot.TeleBot('5202574376:AAFNTZQTljHdZulpE5C1FYgfPxy0j0izi6c')

@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    if db.is_user(message.from_user.id):
        menu.main_menu(message, bot)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('▶️ Начать'))
        
        bot.send_message(message.chat.id, f'Привет, я буду тебя контролировать и держать в памяти некоторые вещи:\
            \n*• Твои персональные веса*\n*• Динамику прогресса*\n*• Дни окончания срока абонементов*', \
            parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=["help"])
def help_bot(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Напиши в чат "Качок" и все увидишь')

@bot.message_handler(content_types=["text"])
def handle_text(message: telebot.types.Message):
    msg = message.text.lower()
    
    if msg in ['качок', 'в главное меню']:
        menu.main_menu(message, bot)
    elif msg == '▶️ начать':
        acq.start(message, bot)
    elif msg == '💶 абонемент':
        abon.abonement_menu(message, bot)
    elif msg == "🏋 веса":
        exerc.exerc_menu(message, bot)
    elif msg == "✔️ прогресс":
        progr.progress_menu(message, bot)
    
bot.polling(none_stop=True, interval=0)
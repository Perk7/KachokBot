import telebot
from telebot import types

import main_menu as menu

from database import BotDB

db = BotDB()
db.setup()

def progress_menu(msg: telebot.types.Message, bot: telebot.TeleBot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user = db.get_user(msg.from_user.id)
    
    exercs = list(user['exerc'].keys())

    btns = ['⬅️ В главное меню'] + exercs
    
    markup.add(*btns)
    
    message = bot.send_message(msg.chat.id, text='Выбери упражнение, прогресс по которому ты хочешь посмотреть' if exercs else 'У вас нет упражнений, чтобы смотреть по ним прогресс', reply_markup=markup)
    bot.register_next_step_handler(message, progress_handler, bot)
    
def progress_handler(msg: telebot.types.Message, bot: telebot.TeleBot):
    text = msg.text
    user = db.get_user(msg.from_user.id)
    
    btns = ['⬅️ В главное меню'] + list(user['exerc'].keys())
    
    
    if text == '⬅️ В главное меню':
        menu.main_menu(msg, bot)
    elif text in btns:
        get_progress_by_exerc(msg, bot, text)
    else:
        progress_menu(msg, bot)
        
def get_progress_by_exerc(msg: telebot.types.Message, bot: telebot.TeleBot, name: str):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Вернуться'))
    
    user = db.get_user(msg.from_user.id)
    
    exerc = user['exerc'][name]
    text = f'Твой прогресс весов по упражнению "{name}":\n\n' + ''.join((f'{i[1]} : *{i[0]} кг*\n' for i in exerc))
    
    message = bot.send_message(msg.chat.id, text=text, parse_mode='Markdown', reply_markup=markup)
    bot.register_next_step_handler(message, progress_menu, bot)

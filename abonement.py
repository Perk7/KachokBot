import telebot
from telebot import types

import main_menu as menu
import datetime

from database import BotDB

db = BotDB()
db.setup()

def abonement_menu(msg: telebot.types.Message, bot: telebot.TeleBot):
    now = datetime.datetime.now()
    user = db.get_user(msg.from_user.id)
    date_abon = tuple(map(int,user['abonement'].split('.')))
    
    if date_abon[0] < now.day and (1 <= now.month if date_abon[1] == 12 else date_abon[1] + 1 <= now.month):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Я обновил абонемент"))
        markup.add(types.KeyboardButton("⬅️ В главное меню"))
        
        message = bot.send_message(msg.chat.id, text="Твой абонемент закончился!", reply_markup=markup)
        bot.register_next_step_handler(message, update_abonement, bot)
    
    else:
        months = {
            1: 'января',
            2: 'февраля',
            3: 'марта',
            4: 'апреля',
            5: 'мая',
            6: 'июня',
            7: 'июля',
            8: 'августа',
            9: 'сентября',
            10: 'октября',
            11: 'ноября',
            12: 'декабря',
        }
        bot.send_message(msg.chat.id, text=f"Твой абонемент кончается {date_abon[0]} {months[date_abon[1]+1]}")
        menu.main_menu(msg, bot)
        
def update_abonement(msg: telebot.types.Message, bot: telebot.TeleBot):
    text = msg.text
     
    if text == "⬅️ В главное меню":
        menu.main_menu(msg, bot)
    elif text == "Я обновил абонемент":
        
        message = bot.send_message(msg.chat.id, text="В какой день месяца ты купил новый абонемент?")
        bot.register_next_step_handler(message, set_day_abonement, bot)
        
def set_day_abonement(msg: telebot.types.Message, bot: telebot.TeleBot):
    text = msg.text.lower()
    status = text.isdigit() and int(text) in tuple(range(1, 31))
    
    if status:
        user = db.get_user(msg.from_user.id)
        
        now = datetime.datetime.now()
        month = now.month if int(text) >= now.day else now.month - 1
        user['abonement'] = f'{int(text)}.{month}'
        db.update_user(msg.from_user.id, user)
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
        btns = []
        btns.append(types.KeyboardButton("💶 Абонемент"))
        btns.append(types.KeyboardButton("🏋 Веса"))
        btns.append(types.KeyboardButton("✔️ Прогресс"))
        
        markup.add(*btns)
        
        bot.send_message(msg.chat.id, text=f"Новая дата установлена. Твоя совесть чиста", reply_markup=markup)
        menu.main_menu(msg, bot)
    else:
        message = bot.send_message(msg.chat.id, text='День месяца должен быть числом от 1 до 31')
        bot.register_next_step_handler(message, set_day_abonement, bot)

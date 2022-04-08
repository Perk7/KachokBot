import telebot
from telebot import types

import main_menu as menu
import datetime

from database import BotDB

db = BotDB()
db.setup()

def exerc_menu(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = db.get_user(msg.from_user.id)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔃 Изменить"), types.KeyboardButton('➕ Добавить'))
    
    if user['exerc'].keys():
        markup.add(types.KeyboardButton('❌ Удалить'))
    
    markup.add(types.KeyboardButton("⬅️ В главное меню"))
    
    text = 'Твои упражнения:\n\n'+'\n'.join((f'*• {i}: {user["exerc"][i][-1][0]} кг*' for i in user["exerc"]) if user['exerc'].keys() else ['*...Пусто...*'.center(20)])
    
    message = bot.send_message(msg.chat.id, text=text, parse_mode='Markdown', reply_markup=markup)
    bot.register_next_step_handler(message, exerc_handler, bot)
    
def exerc_handler(msg: telebot.types.Message, bot: telebot.TeleBot):
    text = msg.text
    
    if text == "⬅️ В главное меню":
        menu.main_menu(msg, bot)
    elif text == '❌ Удалить':
        delete_exerc(msg, bot)
    elif text == '➕ Добавить':
        add_exerc(msg, bot)
    elif text == "🔃 Изменить":
        update_exerc(msg, bot)
                
def add_exerc(msg: telebot.types.Message, bot: telebot.TeleBot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('⬅️ Назад')
    
    message = bot.send_message(msg.chat.id, text='Скажи мне название упражнения', reply_markup=markup)
    bot.register_next_step_handler(message, add_exerc_name, bot)
    
def add_exerc_name(msg: telebot.types.Message, bot: telebot.TeleBot, name=None):
    text = name if name else msg.text
    
    if text == '⬅️ Назад':
        exerc_menu(msg, bot)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('⬅️ Назад')
        
        message = bot.send_message(msg.chat.id, text='Скажи твой рабочий вес (в кг)', reply_markup=markup)
        bot.register_next_step_handler(message, add_exerc_weight, bot, text)
    
def add_exerc_weight(msg: telebot.types.Message, bot: telebot.TeleBot, name: str):
    text = msg.text
    user = db.get_user(msg.from_user.id)
    
    if text == '⬅️ Назад':
        add_exerc(msg, bot)
    elif text.isdigit():
        now = datetime.datetime.now()
        if name in user['exerc'].keys():
            user['exerc'][name].append((int(text), f'{now.day:02}.{now.month:02}.{now.year}'))
        else:
            user['exerc'][name] = [(int(text), f'{now.day:02}.{now.month:02}.{now.year}')]
        db.update_user(msg.from_user.id, user)
        exerc_menu(msg, bot)
    else:
        message = bot.send_message(msg.chat.id, text='Рабочий вес должен быть числом (кг)')
        bot.register_next_step_handler(message, add_exerc_weight, bot, name)

def update_exerc(msg: telebot.types.Message, bot: telebot.TeleBot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user = db.get_user(msg.from_user.id)
    
    exercs = list(user['exerc'].keys())

    btns = ['⬅️ Назад'] + exercs
    
    markup.add(*btns)
    
    message = bot.send_message(msg.chat.id, text='Выбери упражнение, веса которого ты хочешь изменить:' if exercs else 'У тебя нет упражнений, чтобы их изменять', reply_markup=markup)
    bot.register_next_step_handler(message, update_exerc_select, bot)

def update_exerc_select(msg: telebot.types.Message, bot: telebot.TeleBot):
    text = msg.text
    user = db.get_user(msg.from_user.id)
    
    btns = ['⬅️ Назад'] + list(user['exerc'].keys())
    
    if text == '⬅️ Назад':
        exerc_menu(msg, bot)
    elif text in btns:
        add_exerc_name(msg, bot, text)
    else:
        update_exerc(msg, bot)
        
def delete_exerc(msg: telebot.types.Message, bot: telebot.TeleBot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user = db.get_user(msg.from_user.id)
    
    btns = ['⬅️ Назад'] + list(user['exerc'].keys())
    
    markup.add(*btns)
    
    message = bot.send_message(msg.chat.id, text='Выбери упражнение, которые ты хочешь удалить:', reply_markup=markup)
    bot.register_next_step_handler(message, delete_exerc_select, bot)
    
def delete_exerc_select(msg: telebot.types.Message, bot: telebot.TeleBot):
    text = msg.text
    user = db.get_user(msg.from_user.id)
    
    btns = ['⬅️ Назад'] + list(user['exerc'].keys())
    
    if text == '⬅️ Назад':
        exerc_menu(msg, bot)
    elif text in btns:
        del user['exerc'][text]
        db.update_user(msg.from_user.id, user)
        
        exerc_menu(msg, bot)
    else:
        delete_exerc(msg, bot)

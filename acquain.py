import datetime

import telebot
from telebot import types

import main_menu as menu
from database import BotDB

db = BotDB()
db.setup()

user = {'exerc': {}}

def get_all_exercs():
    return list(user['exerc'].keys())

def start(msg: telebot.types.Message, bot: telebot.TeleBot):
    markup = types.ReplyKeyboardRemove()
    message = bot.send_message(msg.chat.id, text="В какой день месяца начался твой абонемент?", reply_markup=markup)
    
    bot.register_next_step_handler(message, set_abonement, bot)

def set_abonement(msg: telebot.types.Message, bot: telebot.TeleBot):
    text = msg.text.lower()
    status = text.isdigit() and int(text) in tuple(range(1, 31))
    
    if status:
        now = datetime.datetime.now()
        month = now.month if int(text) <= now.day else now.month - 1
        user['abonement'] = f'{int(text)}.{month}'
        answer = 'Ок, теперь установим веса для тех упражнений, которые ты делаешь'
        handler = set_exerc
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('➡️ Далее'))  
    else:
        answer = 'День месяца должен быть числом от 1 до 31'
        handler = set_abonement
        markup = None
        
    message = bot.send_message(msg.chat.id, text=answer, reply_markup=markup)
    bot.register_next_step_handler(message, handler, bot)
    
def set_exerc(msg: telebot.types.Message, bot: telebot.TeleBot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('➡️ Далее'), types.KeyboardButton('➕ Добавить'))
    
    if get_all_exercs():
        markup.add(types.KeyboardButton('❌ Удалить'))
    
    text = 'Твои упражнения:\n\n'+'\n'.join((f'*• {i}: {user["exerc"][i][-1][0]} кг*' for i in user["exerc"]) if get_all_exercs() else ['*...Пусто...*'.center(20)])
    
    message = bot.send_message(msg.chat.id, text=text, parse_mode='Markdown', reply_markup=markup)
    bot.register_next_step_handler(message, handler_exerc, bot)
    
def handler_exerc(msg: telebot.types.Message, bot: telebot.TeleBot):
    text = msg.text
    
    if text == '➡️ Далее':
        user['id'] = msg.from_user.id
        db.add_user(user)
        menu.main_menu(msg, bot)
    elif text == '➕ Добавить':
        add_exerc(msg, bot)
    elif text == '❌ Удалить':
        delete_exerc(msg, bot)
    else:
        set_exerc(msg, bot)
        
def add_exerc(msg: telebot.types.Message, bot: telebot.TeleBot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('⬅️ Назад')
    
    message = bot.send_message(msg.chat.id, text='Скажи мне название упражнения', reply_markup=markup)
    bot.register_next_step_handler(message, add_exerc_name, bot)
    
def add_exerc_name(msg: telebot.types.Message, bot: telebot.TeleBot):
    text = msg.text
    
    if text == '⬅️ Назад':
        set_exerc(msg, bot)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add('⬅️ Назад')
        
        message = bot.send_message(msg.chat.id, text='Скажи твой рабочий вес (в кг)', reply_markup=markup)
        bot.register_next_step_handler(message, add_exerc_weight, bot, text)
    
def add_exerc_weight(msg: telebot.types.Message, bot: telebot.TeleBot, name: str):
    text = msg.text
    
    if text == '⬅️ Назад':
        add_exerc(msg, bot)
    elif text.isdigit():
        now = datetime.datetime.now()
        user['exerc'][name] = [(int(text), f'{now.day:02}.{now.month:02}.{now.year}')]
        set_exerc(msg, bot)
    else:
        message = bot.send_message(msg.chat.id, text='Рабочий вес должен быть числом (кг)')
        bot.register_next_step_handler(message, add_exerc_weight, bot, name)

def delete_exerc(msg: telebot.types.Message, bot: telebot.TeleBot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns = ['⬅️ Назад'] + get_all_exercs()
    
    markup.add(*btns)
    
    message = bot.send_message(msg.chat.id, text='Выбери упражнение, которые ты хочешь удалить:', reply_markup=markup)
    bot.register_next_step_handler(message, delete_exerc_select, bot)
    
def delete_exerc_select(msg: telebot.types.Message, bot: telebot.TeleBot):
    text = msg.text
    btns = ['⬅️ Назад'] + get_all_exercs()
    
    if text == '⬅️ Назад':
        set_exerc(msg, bot)
    elif text in btns:
        del user['exerc'][text]
        set_exerc(msg, bot)
    else:
        delete_exerc(msg, bot)
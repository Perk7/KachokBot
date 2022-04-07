import telebot
from telebot import types

def main_menu(msg: telebot.types.Message, bot: telebot.TeleBot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    btns = []
    btns.append(types.KeyboardButton("💶 Абонемент"))
    btns.append(types.KeyboardButton("🏋 Веса"))
    btns.append(types.KeyboardButton("✔️ Прогресс"))
    
    markup.add(*btns)
    bot.send_message(msg.chat.id, text="Что интересует?", reply_markup=markup)
def next_training(bot: telebot.TeleBot, msg: telebot.types.Message):
    form_days = {
        1: '1 день',
        2: '2 дня',
        3: '3 дня',
        4: '4 дня',
        5: '5 дней',
        6: '6 дней',
        7: '7 дней',
    }

    today = datetime.datetime.now()
    weekday = today.weekday()
    
    db.add_exerc(msg.from_user.id)
    print(msg.from_user.id, db.get_items())
    msg_new = db.get_items()
    
    if weekday in (1, 3):
        delta_day = 2 if weekday == 1 else 5
        value = 'сегодня' if today.hour < 20 else f'через {form_days[delta_day]}, {(today + datetime.timedelta(days=delta_day)).strftime("%d.%m.%y")}'
    elif weekday in (4,5,6,7):
        value = f'через {form_days[8-weekday]}, {(today + datetime.timedelta(days=8-weekday)).strftime("%d.%m.%y")}'
    elif weekday == 2:
        value = f'через {form_days[4-weekday]}, {(today + datetime.timedelta(days=4-weekday)).strftime("%d.%m.%y")}'
    
    #bot.send_message(msg.chat.id, f'Следующая тренировка {value}')
    bot.send_message(msg.chat.id, str(msg_new))
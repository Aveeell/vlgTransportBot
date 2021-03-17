import telebot
import main
import cfg
import config
from telebot import types
import os
os.environ['TOKEN']


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help'])
def welcomeMessage(message):
    bot.send_message(message.chat.id,
                     'Привет. Чтобы узнать расписание нужного тебе автобуса/троллейбуса просто введи его номер')


@bot.message_handler(func=lambda message: True)
def searchBus(message):
    busNumber = message.text
    try:
        main.getPageOfDirections(main.getPageOfBus(busNumber))
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=num, callback_data=num) for num in ['1', '2']])
        bot.send_message(message.chat.id,
                         'Выберите направление:\n1) ' + cfg.directions[0] + '\n2) ' + cfg.directions[1],
                         reply_markup=keyboard)
    except AttributeError:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=msg, callback_data=msg) for msg in ['Все автобусы',
                                                                                           'Все троллейбусы']])
        bot.send_message(message.chat.id,
                         'Вы ввели номер маршрута, который отсутствует на сайте ' + cfg.url + ', попробуйте заново',
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def inline(call):
    if call.data == '1':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=main.printSchedule(main.chooseDirection('1'))
        )
    elif call.data == '2':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=main.printSchedule(main.chooseDirection('2'))
        )
    elif call.data == 'Все автобусы':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=main.getAllBuses()
        )
    elif call.data == 'Все троллейбусы':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text= main.getAllTrolleybuses()
        )


if __name__ == '__main__':
    print('work')
    bot.polling(none_stop=True)

import sqlite3
import telebot
from telebot import types
from dotenv import dotenv_values

config = dotenv_values(".env")
bot = telebot.TeleBot(config.get("TELEGRAM_TOKEN"))


def executeAll(request):
    connection = sqlite3.connect(config.get('DB_NAME'))
    cursor = connection.cursor()
    cursor.execute(request)
    data = cursor.fetchall()
    connection.close()
    return data

def executeOne(request):
    connection = sqlite3.connect(config.get('DB_NAME'))
    cursor = connection.cursor()
    cursor.execute(request)
    data = cursor.fetchone()
    connection.close()
    return data




print("RABOTAET")
@bot.message_handler(commands=['menu'])
def handle_command(message):
    id  = message.from_user.id
    name  = message.from_user.first_name    
    print(f'{id}: {name} запросил меню')  
    items = executeAll('SELECT * FROM items')

    markup = types.InlineKeyboardMarkup()   
    for item in items:
        markup.add(types.InlineKeyboardButton(item[1], callback_data=f'abc{item[0]}'))

    bot.send_message(message.from_user.id, 'Наши товары' , reply_markup=markup) 


@bot.callback_query_handler(func=lambda call: True)
def test(call):
    if call.data.startswith("abc"):
         bot.send_message(call.message.chat.id, f"кнопка нажата {call.data}")




bot.polling(none_stop=True, interval=0)








import telebot
import extensions
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду бота в следующем формате: " \
           "\n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>" \
           "\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        check_parametrs = message.text.split(' ')
        if len(check_parametrs) < 3:
            raise Exception('Введено параметров меньше необходимого')
        if len(check_parametrs) > 3:
            raise Exception('Введено параметров больше необходимого')
    except Exception as e:
        text = e
    else:
        quote_k, base_k, amount_k = message.text.strip().lower().split(' ')
        text = extensions.RequestAPI.get_price(quote_k, base_k, amount_k)
    bot.send_message(message.chat.id, text)


bot.polling()

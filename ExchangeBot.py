import telebot

from config import TOKEN, keys
from exceptions import ConvertException, ExchangeRate

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = "Чтобы начать работу, введите сообщение в виде: \n <имя валюты> \
<имя валюты, в которую нужно перевести первую валюту> \
<количество валюты> \n \
Чтобы увидеть список доступных валют, введите команду /values "
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты: \n"
    text += '\n'.join(keys.keys())
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        parameters = message.text.split(" ")
        if len(parameters) < 3:
            raise ConvertException("Вы ввели недостаточно параметров.")

        if len(parameters) > 3:
            raise ConvertException("Вы ввели слишком много параметров.")

        base = parameters[0].lower()
        quote = parameters[1].lower()
        amount = parameters[2]
        res = ExchangeRate.convert(base, quote, amount)
    except ConvertException as e:
        bot.reply_to(message, f"Произошла ошибка:\n {e}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка сервера:\n {e}")
    else:
        text = f"Цена {amount} {base} в {quote} - {res['result']}"
        bot.reply_to(message, text)


bot.polling(none_stop=True)

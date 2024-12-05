import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter
import random
# import time

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ('Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n \
Пример: доллар рубль 1 \n \
Увидеть список всех доступных валют: /values \n \
/test')
    bot.reply_to(message, text)
    # text2 = 'спам'
    # announce_time = '18:10:00'
    # while True:
    #     if str(time.strftime('%X')) == announce_time:
    #         bot.send_message(message.chat.id, text2)
    #         time.sleep(1)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(commands=['test'])
def test(message: telebot.types.Message):
    quote, base = random.sample(list(keys.keys()), 2)
    amount = str(random.randint(1, 10))
    total_base = CryptoConverter.get_price(quote, base, amount)
    text = f'{quote} {base} {amount}\nЦена {amount} {quote} в {base} - {total_base * float(amount)}'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    # print(message.text, message.chat.id)
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров. (/help)')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base * float(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling()

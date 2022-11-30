import telebot
from config import keys,TOKEN
from classes import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def repeat(message: telebot.types.Massage):
    text = "Чтобы начать работу введите команду боту в следующем формате: \n <имя валюты> <в какую валюту перевести> < количество переводимой валюты> с маленькой буквы\n Увидеть список всех доступных валют: /values"
    bot.reply_to(message, text)
    pass

@bot.message_handler(content_types=['voice'])
def function_name(message):
    print(message.text)
    bot.send_message(message.chat.id, f"Слушать я ЭТО не буду. Пиши буквами!")

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Massage):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Massage):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConvertionException('Слишком много букв.... Ещё раз =)')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду \n{e}')
    else:
        text =  f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
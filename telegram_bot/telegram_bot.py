import telebot
from extensions import API
from extensions import APIException
from extensions import Token

# список доступных валют
currency = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB',
}


# создаём объект класса Телеграм-бот в контекстном менеджере с получением токена из файла конфигурации
with Token() as tg_token:
    bot = telebot.TeleBot(tg_token)


# обработчик сообщения START при начале работы с ботом
@bot.message_handler(commands=['start'])
def handle_welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - Бот-'конвертер валют'.\n\n "
                     "Как со мной работать: отправьте сообщение в виде "
                     "<имя валюты, цену которой вы хотите узнать> "
                     "<имя валюты, в которой надо узнать цену первой валюты> "
                     "<количество первой валюты>, разделяя всё пробелами.\n"
                     "Пример: рубль доллар 3000.\n\n"
                     "Для получения списка доступных валют введите команду /values.\n"
                     "Для получения помощи по работе со мной введите /help.\n".format(
                         message.from_user))


# обработчик команды VALUES
@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    text = 'Доступные валюты:'  # выдаём список доступных валют
    for key in currency.keys():
        text = '\n - '.join((text, key,))
    bot.reply_to(message, text)


# обработчик команды HELP
@bot.message_handler(commands=['help'])
def handle_help(message: telebot.types.Message):
    bot.send_message(message.chat.id,
                     "Как со мной работать: отправьте сообщение в виде "
                     "<имя валюты цену которой вы хотите узнать> "
                     "<имя валюты в которой надо узнать цену первой валюты> "
                     "<количество первой валюты>, разделяя всё пробелами.\n"
                     "Пример: рубль доллар 3000.\n\n"
                     "Для получения списка доступных валют введите команду /values.\n".format(
                         message.from_user, bot.get_me()))


# обработчик введённого текста в сообщении боту
@bot.message_handler(content_types=['text'])
def handle_chat(message: telebot.types.Message):
    if message.chat.type == 'private':

        try:  # анализируем введённый текст от пользователя
            print(message.text)
            text_cmd = message.text.lower()
            text_cmd = text_cmd.split(" ")
            # проверяем корректность ввода
            if len(text_cmd) != 3:
                raise APIException('Введено неверное количество данных.')
                # если значений больше или меньше 3, то вызываем исключение
            if not text_cmd[0].isalpha() or not text_cmd[1].isalpha():
                raise APIException('Введены неверные данные.')
                # если данные не похожи на буквы алфавита, то вызываем исключение
            if text_cmd[0] not in currency.keys() or text_cmd[1] not in currency.keys():
                raise APIException('Кажется, что вы неправильно ввели валюту или ввели валюту не из списка.')
                # если введённые данные не содержатся в списке доступных валют, то вызываем исключение
            if text_cmd[0] == text_cmd[1]:
                raise APIException('Кажется, вы ввели одинкаовые валюты.')
                # если данные совпадают, то вызываем исключение
            if not text_cmd[2].isdigit():
                raise APIException('Кажется, что вы ввели неверную сумму.')
                # если сумма обмена не цифра, то вызываем исключение

            base_currency, exchange_currency, base_amount = text_cmd

        except APIException as e:
            bot.send_message(message.chat.id, e)
        except Exception as e:
            bot.send_message(message.chat.id, f'Не удалось обработать запрос.\n'
                                              f'{e}')
        else:
            exchange_amount = API.get_price(currency.get(base_currency), currency.get(exchange_currency), base_amount)
            bot.send_message(message.chat.id, f'{base_amount} {currency.get(base_currency)} = '
                                              f'{exchange_amount} {currency.get(exchange_currency)}')


# запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)

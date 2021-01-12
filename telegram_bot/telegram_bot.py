import telebot
from extensions import my_API
from extensions import APIException_NotCorrectValueAmount, APIException_NotCorrectCurrency

# список доступных валют
currency = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB',
}


# функция получения токена бота из файла
def get_token():
    with open('token.conf', 'r') as file:  # в контекстном менеджере открываем файл и считываем токен
        name_t = file.read(8)
        if name_t == "TOKEN = ":  # находим токен
            TOKEN = file.read()  # считываем токен
            return TOKEN  # возвращаем токен


# создаём объект класса Телеграм-бот
bot = telebot.TeleBot(get_token())


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

            if text_cmd[0] not in currency.keys() or text_cmd[1] not in currency.keys():
                raise APIException_NotCorrectCurrency()
                # если введённые данные не содержатся в списке доступных валют, то вызываем исключение
            if not text_cmd[2].isdigit():
                raise APIException_NotCorrectValueAmount()  # если сумма обмена не цифра, то вызываем исключение
        except IndexError:  # исключение вызываемое при введении недостаточного количества значений
            bot.send_message(message.chat.id, 'Кажется, что вы не ввели одно или несколько значений.')
        except APIException_NotCorrectCurrency:
            bot.send_message(message.chat.id, 'Кажется, что вы неправильно ввели валюту или ввели валюту не из списка.')
        except APIException_NotCorrectValueAmount:
            bot.send_message(message.chat.id, 'Кажется, что вы ввели неверную сумму.')
        else:
            exchange_currency = currency.get(text_cmd[1])
            base_currency = currency.get(text_cmd[0])
            curr_amount = float(text_cmd[2])
            bot.send_message(message.chat.id, f'{text_cmd[2]} {base_currency} '
                                              f'это {my_API.get_price(base_currency, exchange_currency, curr_amount)} '
                                              f'{exchange_currency}')


# запуск бота
bot.polling(none_stop=True)

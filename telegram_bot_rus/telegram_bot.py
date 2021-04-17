import telebot  # модуль по созданию и работе с телеграм ботом
from telebot import types  # types для создания кнопок

# мои классы
from extensions import API
from extensions import Token


# создаём объект класса Телеграм-бот в контекстном менеджере с получением токена из файла конфигурации
with Token() as tg_token:
    bot = telebot.TeleBot(tg_token)


# обработчик команды START при начальной работе с ботом
@bot.message_handler(commands=['start'])
def welcome(message: telebot.types.Message):
    # клавиатура бота
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(api.get_list_phrases().get('keyboardButton1'))
    button_2 = types.KeyboardButton(api.get_list_phrases().get('keyboardButton2'))
    button_3 = types.KeyboardButton(api.get_list_phrases().get('keyboardButton3'))
    button_4 = types.KeyboardButton(api.get_list_phrases().get('keyboardButton4'))

    # добавляем клавиатуру
    markup.add(button_1, button_2, button_3, button_4, row_width=1)

    # отправляем сообщение и включаем клавиатуру
    bot.send_message(message.chat.id, "Welcome {0.first_name}!".format(message.from_user))
    bot.send_message(message.chat.id, api.get_list_phrases().get('start2'), parse_mode='html', reply_markup=markup)


# обработчик команды HELP
@bot.message_handler(commands=['help'])
def handle_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, api.get_list_phrases().get('help'))


# обработчик сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message: telebot.types.Message):
    if message.chat.type == 'private':
        if message.text == api.get_list_phrases().get('keyboardButton3'):
            bot.send_message(message.chat.id, api.get_available_list_currency())
        elif message.text == api.get_list_phrases().get('keyboardButton4'):
            handle_help(message)
        elif message.text == api.get_list_phrases().get('keyboardButton2'):
            markup = types.InlineKeyboardMarkup(row_width=3)
            buttons = {}
            index = 0

            for key in api.get_list_currency().keys():  # перебираем ключи валют и создаём инлайн кнопки с их названиями
                buttons[index] = types.InlineKeyboardButton(api.get_list_currency().get(key), callback_data=key+'_base')
                markup.add(buttons.get(index))
                index += 1

            # отсылаем сообщение и включаем инлайн кнопки
            bot.send_message(message.chat.id, api.get_list_phrases().get('phrase_kB2'), reply_markup=markup)

        elif message.text == api.get_list_phrases().get('keyboardButton1'):

            markup = types.InlineKeyboardMarkup(row_width=3)
            buttons = {}
            index = 0

            for key in api.get_list_currency().keys():  # перебираем ключи валют и создаём инлайн кнопки с их названиями
                buttons[index] = types.InlineKeyboardButton(api.get_list_currency().get(key), callback_data=key)
                markup.add(buttons.get(index))
                index += 1

            # отсылаем сообщение и включаем инлайн кнопки
            bot.send_message(message.chat.id, api.get_list_phrases().get('phrase_kB1'), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, api.get_list_phrases().get('phrase_wrong_text'))


# обработчик callback функций, которые срабатывают по нажатию на инлайн кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # обрабатываем сообщения callback
    try:
        if call.message:
            call_back = call.data.split('_')
            # обработка "Курс обмена валют"
            if len(call_back) == 1 and call_back[0] in api.get_list_currency().keys():
                base_currency = call_back[0]

                # удаление инлайн кнопок и изменение сообщения
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"{api.get_list_phrases().get('phrase_kB1_1')} {base_currency} "
                                           f"{api.get_list_currency().get(base_currency)} "
                                           f"{api.get_list_phrases().get('phrase_kB1_2')}", reply_markup=None)

                for exchange_currency in api.get_list_currency().keys():
                    if exchange_currency == base_currency:
                        continue
                    diff = API.get_rate(api.get_list_currency().get(base_currency),
                                        api.get_list_currency().get(exchange_currency))
                    bot.send_message(call.message.chat.id, f"1 {api.get_list_currency().get(base_currency)} = "
                                                           f"{diff} {api.get_list_currency().get(exchange_currency)}")

            # обработка "Конверсия валют" валютное основание
            if len(call_back) == 2 and call_back[0] in api.get_list_currency().keys() and call_back[1] == 'base':
                name_currency = call_back[0]
                api.set_base(api.get_list_currency().get(call_back[0]))

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"{api.get_list_phrases().get('phrase_kB2_1')} "
                                           f"{name_currency} ({api.get_base()})."
                                           f"", reply_markup=None)

                bot.send_message(call.message.chat.id, api.get_list_phrases().get('phrase_kB2_2'))
                bot.register_next_step_handler(call.message, set_amount)

            # обработка "Конверсия валют" валютная квота
            if len(call_back) == 2 and call_back[0] in api.get_list_currency().keys() and call_back[1] == 'exc':
                name_currency = call_back[0]
                api.set_quote(api.get_list_currency().get(call_back[0]))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"{api.get_list_phrases().get('phrase_kB2_3')} {name_currency} "
                                           f"({api.get_quote()}).", reply_markup=None)
                conv_amount = api.get_rate_self()
                bot.send_message(call.message.chat.id, f" {api.get_amount()} {api.get_base()} "
                                                       f"= {conv_amount} {api.get_quote()}")

            # show alert
            # bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
            #                           text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ")

    except Exception as e:
        print(repr(e))


# функция обработки сообщения о сумме конверсии валюты
# обработка "Курс обмена валют" сумма
def set_amount(message):
    api.set_amount(message.text)  # устанавливаем сумму в объект
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = {}
    index = 0

    for key in api.get_list_currency().keys():  # перебираем ключи и создаём кнопки
        buttons[index] = types.InlineKeyboardButton(api.get_list_currency().get(key), callback_data=key+'_exc')
        markup.add(buttons.get(index))  # добавляем кнопки
        index += 1

    bot.send_message(message.chat.id, f"{api.get_list_phrases().get('phrase_kB2_4')} {api.get_amount()}")
    bot.send_message(message.chat.id, api.get_list_phrases().get('phrase_kB2_5'), reply_markup=markup)


# запуск бота
if __name__ == '__main__':
    while True:
        try:
            api = API()
            bot.polling(none_stop=True)  # без этого бот не будет работать
        except:
            pass

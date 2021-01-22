import requests
import json
import lxml.html
from lxml import etree
import ast


# класс интерфейса приложения по конвертации валют
class API:
    def __init__(self, currencies=None, phrases=None, base=None, quote=None, amount=None):
        self.base = base
        self.quote = quote
        self.amount = amount
        self.currencies = currencies
        self.phrases = phrases
        self.set_list_currency()
        self.set_list_phrases()

    # @staticmethod
    # def get_rate(base, quote, amount=1):
    #     print(f'https://api.exchangeratesapi.io/latest?base={base}&symbols={quote}')
    #     req_curr = requests.get(f'https://api.exchangeratesapi.io/latest?base={base}&symbols={quote}')
    #     print(req_curr)
    #     req_curr_content = json.loads(req_curr.content)
    #     req_curr_content = req_curr_content["rates"]
    #     exchange_rate = req_curr_content[quote]
    #     result = float(amount) * exchange_rate
    #     result = format(float(result), '.2f')
    #     return result

    # @staticmethod
    # def get_rate(base, quote, amount=1):
    #     # print(f'https://www.vbr.ru/banki/kurs-valut/converter/{base.lower()}-{quote.lower()}/{amount}/')
    #     req_curr = requests.get(f'https://www.vbr.ru/banki/kurs-valut'
    #                             f'/converter/{base.lower()}-{quote.lower()}/{amount}/').content
    #     # print(req_curr)
    #     req_curr_content = lxml.html.document_fromstring(req_curr)
    #     # print(req_curr_content)
    #     exchange_rate = req_curr_content.xpath('/html/body/div[5]/div[3]/div[5]/b[2]/text()')
    #     exchange_rate = exchange_rate[0]
    #     exchange_rate = float(exchange_rate[2:])
    #     # print(type(exchange_rate))
    #     # print(exchange_rate)
    #     result = float(amount) * exchange_rate
    #     result = format(float(result), '.2f')
    #     return result

    # статический метод конвертации валют, полученных с сайта
    # входные параметры берутся из вне
    @staticmethod
    def get_rate(base, quote, amount=1):
        req_curr = requests.get(f'https://freecurrencyrates.com/ru/'
                                f'convert-{base}-{quote}#{amount}').content
        req_curr_content = lxml.html.document_fromstring(req_curr)
        exchange_rate = req_curr_content.xpath('/html/body/main/div/div[2]/div[1]/div[1]'
                                               '/div[2]/div[2]/input/@value')
        exchange_rate = float(exchange_rate[0])
        result = float(amount) * exchange_rate
        result = format(float(result), '.2f')
        return result

    # метод конвертации валют, полученных с сайта, записанные в класс
    # входные параметры берутся из объекта класса
    def get_rate_self(self):
        req_curr = requests.get(f'https://freecurrencyrates.com/ru/'
                                f'convert-{self.base}-{self.quote}#{self.amount}').content
        req_curr_content = lxml.html.document_fromstring(req_curr)
        exchange_rate = req_curr_content.xpath('/html/body/main/div/div[2]/div[1]/div[1]'
                                               '/div[2]/div[2]/input/@value')
        exchange_rate = float(exchange_rate[0])
        result = float(self.amount) * exchange_rate
        result = format(float(result), '.2f')
        return result

    # метод получения списка доступных валют
    def get_available_list_currency(self):
        phrase = self.get_list_phrases().get('phrase_available_currency')
        available_list_currency = phrase  # выдаём список доступных валют
        for key in self.currencies.keys():  # перебираем в цикле ключи словаря с валютами
            available_list_currency = '\n - '.join((available_list_currency, key,))  # соединяем их в строке
        return available_list_currency

    # метод получения списка доступных валют
    def get_list_currency(self):
        return self.currencies

    # метод установки списка доступных валют
    def set_list_currency(self):
        file = open('currencies.yaml', 'r', encoding='UTF-8')  # открываем файл для чтения
        currencies = file.read()  # читаем весь файл с валютами
        self.currencies = ast.literal_eval(currencies)  # переводим полученный данные в словарь
        file.close()

    # метод получения списка доступных валют
    def get_list_phrases(self):
        return self.phrases

    # метод установки списка доступных валют
    def set_list_phrases(self):
        file = open('phrases.yaml', 'r', encoding='UTF-8')  # открываем файл для чтения
        phrases = file.read()  # читаем весь файл с валютами
        self.phrases = ast.literal_eval(phrases)  # переводим полученный данные в словарь
        file.close()

    # установить основание конверсии
    def set_base(self, base):
        self.base = base

    # получить основание конверсии
    def get_base(self):
        return self.base

    # установить квоту конверсии
    def set_quote(self, quote):
        self.quote = quote

    # получить квоту конверсии
    def get_quote(self):
        return self.quote

    # установить сумму конверсии
    def set_amount(self, amount):
        self.amount = amount

    # получить сумму конверсии
    def get_amount(self):
        return self.amount


# класс исключений
class APIException(Exception):
    pass


# класс по работе с токеном
class Token:
    def __init__(self):
        pass

    def __enter__(self):  # обработчик входа в контекстный менеджер
        self.file = open('token.yaml', 'r')  # открываем файл для чтения
        self.name_t = self.file.read(8)  # читаем первые символы с названием конфигурации
        if self.name_t == "TOKEN = ":  # находим конфигурацию токена
            self.TOKEN = self.file.read()  # считываем токен
            return self.TOKEN

    def __exit__(self, exc_type, exc_val, exc_tb):  # обработчик выхода из контекстного менеджера
        self.file.close()

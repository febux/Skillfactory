import requests
import json


class API:
    def __init__(self, currencies):
        self.currencies = currencies

    @staticmethod
    def get_price(base, quote, amount):
        req_curr = requests.get(f'https://api.exchangeratesapi.io/latest?base={base}&symbols={quote}')
        req_curr_content = json.loads(req_curr.content)
        req_curr_content = req_curr_content["rates"]
        exchange_rate = req_curr_content[quote]
        result = float(amount) * exchange_rate
        result = format(float(result), '.2f')
        return result


class APIException(Exception):
    pass


class Token:
    def __init__(self):
        pass

    def __enter__(self):
        self.file = open('token.conf', 'r')  # открываем файл для чтения
        self.name_t = self.file.read(8)  # читаем первые символы с названием конфигурации
        if self.name_t == "TOKEN = ":  # находим конфигурацию токена
            self.TOKEN = self.file.read()  # считываем токен
            return self.TOKEN

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

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

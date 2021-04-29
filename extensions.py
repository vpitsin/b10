import requests
import json
from config import APITOKEN, keys, keys_b, keys_q


class APIException(Exception):
    pass


class RequestAPI:
    @staticmethod
    def get_price(quote_k, base_k, amount_k):
        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={APITOKEN}&symbols=RUB,USD')
        rub = json.loads(r.content)['rates']['RUB']
        usd = json.loads(r.content)['rates']['USD']
        eur = 1.00
        try:
            if quote_k not in keys.keys():
                raise APIException(f'Введенная валюта "{quote_k}" отлична от поддерживаемой')
            if base_k not in keys.keys():
                raise APIException(f'Введенная валюта "{base_k}" отлична от поддерживаемой')
            if not (amount_k.isdigit() or amount_k.replace('.', '', 1).isdigit() or amount_k.replace(',', '', 1).isdigit()):
                raise APIException(f'"{amount_k}" - не число')

        except APIException as e:
            return e

        else:
            if amount_k.replace(',', '', 1).isdigit():
                amount_k = amount_k.replace(',', '.', 1)
            quote, base, amount = keys[quote_k], keys[base_k], float(amount_k)
            if quote == 'EUR' and base == 'RUB':
                total = eur * rub * amount
            elif quote == 'EUR' and base == 'USD':
                total = eur * usd * amount
            elif quote == 'RUB' and base == 'EUR':
                total = eur / rub * amount
            elif quote == 'USD' and base == 'EUR':
                total = eur / usd * amount
            elif quote == 'RUB' and base == 'USD':
                total = usd / rub * amount
            elif quote == 'USD' and base == 'RUB':
                total = rub / usd * amount
            elif quote == base:
                total = amount
            else:
                total = "ошибка малех"
            return (f'{amount_k} {keys_q[quote]} в {keys_b[base]} = {round(total, 2)} {keys_q[base]}')

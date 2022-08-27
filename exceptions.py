import json
import requests

from config import headers, payload, keys


class ConvertException(Exception):
    pass


class ExchangeRate:
    @staticmethod
    def convert(base, quote, amount):
        if quote == base:
            raise ConvertException(f"Вы ввели одинаковую валюту {base}")
        try:
            quote_tick = keys[quote]
        except KeyError:
            raise ConvertException(f"Валюты {quote} нет в списке")
        try:
            base_tick = keys[base]
        except KeyError:
            raise ConvertException(f"Валюты {base} нет в списке")
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f"Не удалось обработать {amount}")

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={quote_tick}&from={base_tick}&amount={amount}"
        response = requests.request("GET", url, headers=headers, data=payload)
        d = json.loads(response.content)
        return d

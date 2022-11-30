import json
import requests
from config import keys

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Я для тебя шутка? Невозможно перевести одинаковые валюты  {base}  -_- ')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'ОшЫбка  {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'ОшЫбка {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'ОшЫбка,  это что за количество такое?=) -  {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] *float(amount)
        return total_base
import requests
import json


def get_crypto_price():
    try:
        key = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'


        data = requests.get(key)
        data = data.json()

        the_price = list({data['price']})
        final_price = float(the_price[0])
        return final_price

    except:
        pass
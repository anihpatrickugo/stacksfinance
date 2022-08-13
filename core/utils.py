import requests
import json
import uuid


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



def generate_ref_code():
    code = str(uuid.uuid4()).replace("-", "")[:6]
    return code



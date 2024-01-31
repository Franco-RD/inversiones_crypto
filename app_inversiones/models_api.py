from config import APIKEY
import requests


def get_exchange_rate(moneda_from, moneda_to):
    url = f"https://rest.coinapi.io/v1/exchangerate/{moneda_from}/{moneda_to}?apikey={APIKEY}"
    r = requests.get(url)
    data = r.json()
    # r.json() -> {"asset_id_base": "BTC", "asset_id_quote": "EUR", "rate": 36457.681033351495, "time": "2024-01-23T23:15:12.0000000Z"}
    # o -> {"error": "You requested specific single item that we don't have at this moment."}
    return data


     
def get_neto_valor_actual(moneda_from):
    url = f"https://rest.coinapi.io/v1/exchangerate/{moneda_from}/EUR?apikey={APIKEY}"
    r = requests.get(url)
    data = r.json()
    
    return data["rate"]


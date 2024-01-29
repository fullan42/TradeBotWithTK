import logging
import requests
import pprint

#binanceden datayı çektim yer
def get_contracts():
    response_object=requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")
    contracs=[]

    for contract in response_object.json()['symbols']:
        contracs.append(contract['pair'])
    return contracs
logger=logging.getLogger()


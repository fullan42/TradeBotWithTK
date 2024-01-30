import json
import logging
import urllib
from typing import Dict, Any
import time
import requests
import pprint
import hmac
import hashlib
logger = logging.getLogger()
import urllib.parse as urlparse
import websocket as websocket
import threading
class BinanceFuturesClient:
    def __init__(self,public_key,secret_key, testnet):
        if testnet:
            self.base_url = "https://testnet.binancefuture.com"
            self.wss_url = "wss://testnet.binance.vision/ws"
        else:
            self.base_url = "https://fapi.binance.com"
            self.wss_url = "wss://fstream.binance.com/ws"
        self.public_key = public_key
        self.secret_key = secret_key
        self.prices = dict()
        self.headers = {
            'X-MBX-APIKEY': self.public_key
        }
        self.ws=None
        self.id = 1
        t = threading.Thread(target=self.start_ws)
        t.start()

        logger.info("Binance Futures Client Initiated")

    def generate_signature(self, data):
        query_string = '&'.join([f"{k}={v}" for k, v in data.items()])
        signature = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        return signature

    def make_request(self, method, endpoint, data ):
        if method == "GET":
            response=requests.get(self.base_url + endpoint, params=data,headers=self.headers)
        elif method == "POST":
            response=requests.post(self.base_url + endpoint, params=data,headers=self.headers)
        elif method == "DELETE":
            response=requests.delete(self.base_url + endpoint, params=data,headers=self.headers)
        else:
            raise Exception("Invalid request method")

        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Request failed, status code %s, method: %s, endpoint: %s, response: %s",
                         response.status_code, method, endpoint, response.json())

    def get_contracts(self):
        exchange_info = self.make_request("GET", "/fapi/v1/exchangeInfo", None)
        contracts = dict()
        if exchange_info is not None:
            for contract_data in exchange_info['symbols']:
                contracts[contract_data['pair']] = contract_data
        return contracts

    def get_historical_candles(self, symbol, interval,  limit=1000):
        data = dict()
        data['symbol'] = symbol
        data['interval'] = interval
        data['limit'] = limit
        raw_candles = self.make_request("GET", "/fapi/v1/klines", data)
        candles = []
        if raw_candles is not None:
            for c in raw_candles:
                candles.append([
                    c[0],
                    float(c[1]),
                    float(c[2]),
                    float(c[3]),
                    float(c[4]),
                    float(c[5]),
                ])
        return candles

    def get_bid_ask(self, symbol):
        data = dict()
        data['symbol'] = symbol
        ob_data = self.make_request("GET", "/fapi/v1/ticker/bookTicker", data)
        if ob_data is not None:
            if symbol not in self.prices:
                self.prices[symbol] = {'bid': float(ob_data['bidPrice']), 'ask': float(ob_data['askPrice'])}
            else:
                self.prices[symbol]['bid'] = float(ob_data['bidPrice'])
                self.prices[symbol]['ask'] = float(ob_data['askPrice'])
        return self.prices[symbol]
    def get_balances(self):
        data = dict()
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)
        balances = dict()

        account_data= self.make_request("GET", "/fapi/v2/account", data)

        if account_data is not None:
            for b in account_data['assets']:
                balances[b['asset']] = b

        return balances

    def place_order(self, symbol, side, order_type, quantity, price=None ,tif=None):
        data = dict()
        data['symbol'] = symbol
        data['side'] = side
        data['type'] = order_type
        data['quantity'] = quantity
        if price is not None:
            data['price'] = price

        if tif is not None:
            data['timeInForce'] = tif
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)
        order_result = self.make_request("POST", "/fapi/v1/order", data)
        return order_result
    def cancel_order(self, symbol, order_id):
        data = dict()
        data['symbol'] = symbol
        data['orderId'] = order_id
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)
        order_result = self.make_request("DELETE", "/fapi/v1/order", data)
        return order_result
    def get_order_status(self, symbol, order_id):
        data = dict()
        data['symbol'] = symbol
        data['orderId'] = order_id
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)
        order_result = self.make_request("GET", "/fapi/v1/order", data)
        return order_result
    def start_ws(self):
        self.ws = websocket.WebSocketApp(self.wss_url, on_open=self.on_open , on_close=self.on_close, on_error=self.on_error,on_message=self.on_message, )
        self.ws.run_forever()

    def on_open(self, ws):
        logger.info("Connection opened")
        self.subscribe_channel("BTCUSDT")

    def on_close(self, ws, *args, **kwargs):
        logger.warning('Websocket connection closed')
        self.ws_connected = False
    def on_error(self, ws, error):
        logger.error("Connection error %s", error)
    def on_message(self, ws, message):
        data=json.loads(message)


        if data['s'] not in self.prices:
            self.prices[data['s']] = {'bid': float(data['b']), 'ask': float(data['a'])}
        else:
            self.prices[data['s']]['bid'] = float(data['b'])
            self.prices[data['s']]['ask'] = float(data['a'])
        print(self.prices[data['s']])
    def subscribe_channel(self,symbol):
        data = dict()
        data['method'] = "SUBSCRIBE"
        data['params'] = []
        data['params'].append(symbol.lower() + "@bookTicker")
        data['id'] = self.id
        self.ws.send(json.dumps(data))
        self.id += 1

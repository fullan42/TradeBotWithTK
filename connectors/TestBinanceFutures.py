import unittest
from unittest.mock import MagicMock, patch
from connectors.binance_futures import BinanceFuturesClient as bf
from models import Contract


class TestBinanceFuturesClient(unittest.TestCase):


    def test_get_contracts(self):
        # BinanceFuturesClient örneği oluşturun
        binance_client = bf("ad08cd0dca0ad5465e9b309259df0216931329d71422116937576e943c4352c0",
                                                 "b233aedcb230204d811f21efecf8714d5af13b8a992f00d024270c75f871132d",
                                                 True)
        contracts = binance_client.get_contracts()
        #is not None?
        self.assertIsNotNone(contracts)
        # is cont dict?
        self.assertIsInstance(contracts, dict)
        # is xrp inside
        self.assertEqual(Contract.get_symbol(contracts['XRPUSDT']), 'XRPUSDT')

    def test_get_balances(self):
        binance_client = bf("ad08cd0dca0ad5465e9b309259df0216931329d71422116937576e943c4352c0",
                            "b233aedcb230204d811f21efecf8714d5af13b8a992f00d024270c75f871132d", True)
        balances = binance_client.get_balances()
        self.assertIsNotNone(balances)
        self.assertIsInstance(balances, dict)
        self.assertIn('USDT', balances)

    def test_get_historical_candles(self):
        binance_client = bf("ad08cd0dca0ad5465e9b309259df0216931329d71422116937576e943c4352c0",
                            "b233aedcb230204d811f21efecf8714d5af13b8a992f00d024270c75f871132d", True)
        contract = Contract({'symbol': 'XRPUSDT', 'baseAsset': 'XRP', 'quoteAsset': 'USDT', 'pricePrecision': 4, 'quantityPrecision': 4, 'tickSize': 0.0001, 'lotSize': 0.1}, 'binance')
        candles = binance_client.get_historical_candles(contract, '1m')
        self.assertIsNotNone(candles)
        self.assertIsInstance(candles, list)
        self.assertEqual(len(candles), 500)

    def test_get_bid_ask(self):
        binance_client = bf("ad08cd0dca0ad5465e9b309259df0216931329d71422116937576e943c4352c0",
                            "b233aedcb230204d811f21efecf8714d5af13b8a992f00d024270c75f871132d", True)
        contract = Contract({'symbol': 'XRPUSDT', 'baseAsset': 'XRP', 'quoteAsset': 'USDT', 'pricePrecision': 4, 'quantityPrecision': 4, 'tickSize': 0.0001, 'lotSize': 0.1}, 'binance')
        bid_ask = binance_client.get_bid_ask(contract)
        self.assertIsNotNone(bid_ask)
        self.assertIsInstance(bid_ask, dict)
        self.assertIn('bid', bid_ask)
        self.assertIn('ask', bid_ask)

    def test_place_order(self):
        # BinanceFuturesClient örneği oluşturun
        binance_client = bf("ad08cd0dca0ad5465e9b309259df0216931329d71422116937576e943c4352c0",
                            "b233aedcb230204d811f21efecf8714d5af13b8a992f00d024270c75f871132d", True)

        contract_info = {
            'symbol': 'BTCUSDT',
            'baseAsset': 'BTC',
            'quoteAsset': 'USDT',
            'pricePrecision': 2,
            'quantityPrecision': 3
        }
        contract = Contract(contract_info, "binance")

        order_status =binance_client.place_order(contract, "BUY", 0.5, "limit", 10000.0, "GTC")
        isExist=order_status.order_id

        self.assertIsNotNone(isExist)

    def test_get_order_status(self):
        binance_client = bf("ad08cd0dca0ad5465e9b309259df0216931329d71422116937576e943c4352c0","b233aedcb230204d811f21efecf8714d5af13b8a992f00d024270c75f871132d", True)
        contract_info = {
            'symbol': 'BTCUSDT',
            'baseAsset': 'BTC',
            'quoteAsset': 'USDT',
            'pricePrecision': 2,
            'quantityPrecision': 3
        }
        contract = Contract(contract_info, "binance")
        order_status = binance_client.place_order(contract, "BUY", 0.5, "limit", 10000.0, "GTC")

        order_id = order_status.order_id

        # Şimdi, order_id ile get_order_status fonksiyonunu test edin
        fetched_order_status = binance_client.get_order_status(contract, order_id)

        # fetched_order_status'ün None olmadığını kontrol edin
        self.assertIsNotNone(fetched_order_status)

    def test_cancel_order(self):
        binance_client = bf("ad08cd0dca0ad5465e9b309259df0216931329d71422116937576e943c4352c0",
                                                 "b233aedcb230204d811f21efecf8714d5af13b8a992f00d024270c75f871132d",
                                                 True)
        contract_info = {
            'symbol': 'BTCUSDT',
            'baseAsset': 'BTC',
            'quoteAsset': 'USDT',
            'pricePrecision': 2,
            'quantityPrecision': 3
        }
        contract = Contract(contract_info, "binance")

        # Sipariş oluşturun
        order_status = binance_client.place_order(contract, "BUY", 0.5, "limit", 10000.0, "GTC")

        # Siparişin order_id bilgisini alın
        order_id = order_status.order_id

        # Şimdi, cancel_order fonksiyonunu test edin
        cancelled_order_status = binance_client.cancel_order(contract, order_id)

        # İptal edilen siparişin bilgisinin None olmadığını doğrulayın
        self.assertIsNotNone(cancelled_order_status)

if __name__ == '__main__':
    unittest.main()
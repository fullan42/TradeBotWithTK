import unittest
import pandas as pd
import KAMA
import numpy as np
import os


class TestKAMAIndicator(unittest.TestCase):

    def test_setUp(self):

        self.df = pd.read_csv('TQQQ.csv')
        price_series = self.df['Close']
        self.price_series = price_series
        self.period = 30
        self.period_fast = 2
        self.period_slow = 30
        self.assertIsNotNone(self.df)
        self.assertIsNotNone(self.price_series)
    def test_calculate_kama(self):
        self.df = pd.read_csv('TQQQ.csv')
        price_series = self.df['Close']
        self.price_series = price_series
        self.period = 30
        self.period_fast = 2
        self.period_slow = 30
        self.assertIsNotNone(self.df)
        self.assertIsNotNone(self.price_series)
        price_series = self.price_series
        kama_indicator = KAMA.KAMAIndicator(price_series)
        kama_values = kama_indicator.calculate_kama()
        self.assertIsNotNone(kama_values)



if __name__ == '__main__':
    unittest.main()


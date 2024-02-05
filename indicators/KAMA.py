import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import pandas as pd

# TQQQ.csv dosyasını oku
df = pd.read_csv('TQQQ.csv')

class KAMAIndicator:
    def __init__(self, price_series, period=30, period_fast=2, period_slow=30):
        self.price_series = price_series
        self.period = period
        self.period_fast = period_fast
        self.period_slow = period_slow

    def calculate_kama(self):
        close = self.price_series

        # Efficiency Ratio
        change = abs(close - close.shift(self.period))
        volatility = (abs(close - close.shift())).rolling(self.period).sum()
        er = change / volatility

        # Smoothing Constant
        sc_fastest = 2 / (self.period_fast + 1)
        sc_slowest = 2 / (self.period_slow + 1)
        sc = (er * (sc_fastest - sc_slowest) + sc_slowest) ** 2

        # KAMA Calculation
        kama = pd.Series(index=close.index)
        kama[self.period - 1] = close.iloc[self.period - 1]
        for i in range(self.period, len(close)):
            kama[i] = kama[i - 1] + sc[i] * (close[i] - kama[i - 1])
        kama[kama == 0] = np.nan

        return kama

    def isKamaBullish(self):
        kama_values = self.calculate_kama()
        last_kama = kama_values.iloc[-1]
        last_close = self.price_series.iloc[-1]

        if last_close > last_kama:
            return True
        else:
            return False

# Veriyi incele
print(df.head())

# 'Close' sütununu kullanarak KAMA hesapla
price_series = df['Close']

# KAMAIndicator sınıfını kullanarak bir örnek oluştur
kama_indicator = KAMAIndicator(price_series)

# isKamaBullish yöntemini kullanarak KAMA'nın boğa eğiliminde olup olmadığını kontrol et
is_bullish = kama_indicator.isKamaBullish()
print("Is KAMA Bullish?", is_bullish)

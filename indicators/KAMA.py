import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set()

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
        kama = np.zeros_like(close)
        kama[self.period - 1] = close[self.period - 1]
        for i in range(self.period, len(close)):
            kama[i] = kama[i - 1] + sc[i] * (close[i] - kama[i - 1])
        kama[kama == 0] = np.nan

        return kama

    def plot_kama(self):
        kama_values = self.calculate_kama()

        df = pd.DataFrame({
            'Close': self.price_series,
            'KAMA': kama_values,
            'SMA_10days': self.price_series.rolling(self.period).mean()
        })

        figsize = (12, 6)
        df[['KAMA', 'Close']].plot(figsize=figsize)
        df['SMA_10days'].plot(linestyle="-")
        plt.legend(['KAMA', 'Close', 'SMA_10day'])
        plt.title("KAMA ({0},{1},{2})".format(self.period, self.period_fast, self.period_slow))
        plt.show()


if __name__ == "__main__":
    # CSV dosyasının yolu
    dosya_yolu = "TQQQ.csv"

    # CSV dosyasını oku ve veri çerçevesine dönüştür
    df = pd.read_csv(dosya_yolu)

    # Veri çerçevesinin ilk birkaç satırını yazdır
    print(df.head())

    close_prices = df['Adj Close']
    kama_indicator = KAMAIndicator(close_prices)
    kama_indicator.plot_kama()
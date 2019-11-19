import numpy as np
import pandas as pd


class Alpha:

    def __init__(self, ohlc):
        df = ohlc
        self.open = df['Open'].values
        self.close = df['Close'].values
        self.high = df['High'].values
        self.low = df['Low'].values
        self.vol = df['Volume'].values
        self.upper = np.max([self.open, self.close], axis=0)
        self.lower = np.min([self.open, self.close], axis=0)
        self.T = len(self.close)

    # alpha should have the same length with the data.

    def close_return(self):
        signal = np.concatenate([[np.nan], (self.close[1:]-self.close[:-1])/self.close[:-1]])
        return signal

    def open_return(self):
        signal = np.concatenate([[np.nan], (self.open[1:]-self.open[:-1])/self.open[:-1]])
        return signal

    def close_open_diff(self):
        signal = (self.close - self.open) / self.close
        return signal

    def upper_lower_diff(self):
        signal = (self.upper - self.lower) / self.close
        return signal

    def high_low_diff(self):
        signal = (self.high - self.low) / self.close
        return signal

    def high_upper_diff(self):
        signal = (self.high - self.upper) / self.close
        return signal

    def lower_low_diff(self):
        signal = (self.lower - self.low)/self.close
        return signal

    def moving_average(self, window=10):
        signal = pd.DataFrame({'signal': self.close}).rolling(window=window).mean().values.reshape(-1)
        return signal

    def moving_std(self, window=10):
        signal = pd.DataFrame({'signal': self.close}).rolling(window=window).std().values.reshape(-1)
        return signal

    def moving_var(self, window=10):
        signal = pd.DataFrame({'signal': self.close}).rolling(window=window).var().values.reshape(-1)
        return signal

    def moving_med(self, window=10):
        signal = pd.DataFrame({'signal': self.close}).rolling(window=window).median().values.reshape(-1)
        return signal

    def moving_max(self, window=10):
        signal = pd.DataFrame({'signal': self.close}).rolling(window=window).max().values.reshape(-1)
        return signal

    def moving_min(self, window=10):
        signal = pd.DataFrame({'signal': self.close}).rolling(window=window).min().values.reshape(-1)
        return signal

    def moving_average_diff(self, window1=10, window2=20):
        signal1 = pd.DataFrame({'signal': self.close}).rolling(window=window1).mean().values.reshape(-1)
        signal2 = pd.DataFrame({'signal': self.close}).rolling(window=window2).mean().values.reshape(-1)
        signal = signal1-signal2
        return signal

    def bollinger_upper_bound(self, window=10, width=2):
        signal = self.moving_average(window=window) + width*self.moving_std(window=window)
        return signal

    def bollinger_lower_bound(self, window=10, width=2):
        signal = self.moving_average(window=window) - width * self.moving_std(window=window)
        return signal














if __name__ == '__main__':
    df = pd.read_csv('./data/ZIV.csv')
    alpha = Alpha(df)
    print(alpha.alpha10(window1=10, window2=20))


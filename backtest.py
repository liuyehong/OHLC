import numpy as np
from alpha import Alpha
import pandas as pd
from strategy import *

class Backtest:

    def __init__(self, df):
        self.alpha = Alpha(df)
        self.strategy = Strategy(df)
        self.cost = 0.001

    def run(self, strategy):
        self.history_asset = []
        self.buy_time = []
        self.sell_time = []
        self.history_inventory = []
        cash = 1
        stock = 0

        cond_b, cond_s, price_b, price_s = strategy

        for t in range(1, self.alpha.T-1):
            if cond_b[t] and stock == 0 and price_b[t]>self.alpha.low[t+1]:
                stock = cash / price_b[t] * (1 - self.cost)
                cash = 0
                self.buy_time.append(t)

            elif cond_s[t] and cash == 0 and price_s[t]<self.alpha.high[t+1]:
                cash = stock * price_s[t] * (1 - self.cost)
                stock = 0
                self.sell_time.append(t)

            asset = stock * self.alpha.close[t] + cash
            self.history_asset.append(asset)
            self.history_inventory.append(stock > 0)

        self.r = np.diff(self.history_asset)/self.history_asset[:-1]
        self.sharpe_ratio = np.average(self.r)/np.std(self.r)
        self.sharpe_ratio_year = self.sharpe_ratio*np.sqrt(240)


        if np.isnan(self.sharpe_ratio):
            self.sharpe_ratio = -np.inf
            self.sharpe_ratio_year = -np.inf


        df_close = pd.DataFrame({'asset': self.history_asset})['asset']
        rollmax = df_close.cummax()
        daily_drawdown = df_close/rollmax - 1
        self.max_drawdown = np.min(daily_drawdown)

        #print(self.sharpe_ratio_year, self.max_drawdown)



if __name__ == '__main__':
    df = pd.read_csv('./data/BTC-USD.csv')
    backtest = Backtest(df)
    backtest.run(backtest.strategy.strategy2())
    print(backtest.sharpe_ratio_year)







from backtest import Backtest
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from strategy import Strategy
import traceback


class Optimization:

    def __init__(self, df):
        self.backtest = Backtest(df)

    def optimize(self, strategy, n_iters=10, method='Powell'):
        self.strategy = strategy
        self.strategy()
        self.bound = self.backtest.strategy.bound
        self.type = self.backtest.strategy.type

        list_yopt = []
        list_xopt = []
        i = 0
        while i < n_iters:

            try:
                # uniform random initial points
                x0 = [np.random.random()*(self.bound[k, 1]-self.bound[k, 0])+self.bound[k, 0] for k in range(len(self.bound))]
                self.x = x0
                self.x = [int(round(self.x[i])) if self.type[i] == 'int' else self.x[i] for i in range(len(self.x))]
                res = minimize(self.f, x0=x0, method=method) # Powell
                y_opt = self.f(res.x)
                x_opt = [int(round(res.x[i])) if self.type[i] == 'int' else res.x[i] for i in range(len(res.x))]
                list_yopt.append(y_opt)
                list_xopt.append(x_opt)
                i += 1
                print(i)
                print(x_opt, -y_opt)
            except:
                print(traceback.format_exc())

        global_xopt = list_xopt[np.argmin(list_yopt)]
        global_sr = -np.min(list_yopt)

        return global_xopt, global_sr

    def f(self, x):
        x = [int(round(x[i])) if self.type[i] == 'int' else x[i] for i in range(len(x))]
        self.backtest.run(self.strategy(x))
        sr = -self.backtest.sharpe_ratio_year
        return sr


if __name__ == '__main__':
    df = pd.read_csv('./data/BTC-USD.csv')
    opt = Optimization(df)
    global_xopt, global_sr = opt.optimize(opt.backtest.strategy.strategy2, method='Powell')
    print(global_xopt, global_sr)


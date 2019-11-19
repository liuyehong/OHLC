from alpha import Alpha
import numpy as np
import pandas as pd
np.seterr(divide='ignore', invalid='ignore')

class Strategy:

    def __init__(self, df):
        self.alpha = Alpha(df)

    def strategy1(self, parameters=(29, 14, 21, 3.0)):
        self.bound = np.array([[5, 30],[5, 30],[5,30],[0.5, 3]])
        self.type =['int','int','int','float']

        window1 = parameters[0]
        window2 = parameters[1]
        window = parameters[2]
        width = parameters[3]

        moving_average_diff = self.alpha.moving_average_diff(window1=window1, window2=window2)
        bollinger_upper_bound = self.alpha.bollinger_upper_bound(window=window, width=width)
        bollinger_lower_bound = self.alpha.bollinger_lower_bound(window=window, width=width)

        cond_b = [np.nan] + \
                 [moving_average_diff[t-1]<0 and moving_average_diff[t]>0 for t in range(1, self.alpha.T)]

        cond_s = [np.nan] + \
                 [moving_average_diff[t-1]>0 and moving_average_diff[t]<0 for t in range(1, self.alpha.T)]

        price_b = bollinger_lower_bound
        price_s = bollinger_upper_bound

        return cond_b, cond_s, price_b, price_s

    def strategy2(self, parameters=(8, 0.7768753434085348)):
        self.bound = np.array([[5, 15], [1, 2]])
        self.type = ['int', 'float']

        window = parameters[0]
        width = parameters[1]

        bollinger_upper_bound = self.alpha.bollinger_upper_bound(window=window, width=width)
        bollinger_lower_bound = self.alpha.bollinger_lower_bound(window=window, width=width)

        cond_b = [np.nan] + \
                 [self.alpha.close[t-1]< bollinger_upper_bound[t-1]
                  and self.alpha.close[t]> bollinger_upper_bound[t] for t in range(1, self.alpha.T)]

        cond_s = [np.nan] + \
                 [self.alpha.close[t-1]> bollinger_lower_bound[t-1]
                  and self.alpha.close[t]< bollinger_lower_bound[t] for t in range(1, self.alpha.T)]

        price_b = bollinger_lower_bound
        price_s = bollinger_upper_bound
        return cond_b, cond_s, price_b, price_s


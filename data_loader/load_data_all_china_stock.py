from single_load_data_tushare import *
import pandas as pd
import os
def load_data_all_tickers():
    df = pd.read_csv('./Tickers/china_tickers.csv')
    for ticker in df['code']:
        ticker = str('0')*(6-len(str(ticker)))+str(ticker)
        print (ticker)
        if ticker + '.csv' not in os.listdir('../data/tick_level/'):
            load_data_tick_level(str(ticker))


if __name__ == '__main__':
    load_data_all_tickers()


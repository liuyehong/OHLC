import pandas as pd
import numpy as np
from datetime import datetime
import os


def tick_to_ohlc(df):

    list_time = df['time'].astype('str').values
    list_date = df['date'].astype('str').values
    df['datetime'] = [datetime.strptime(list_date[i] + ' ' + list_time[i], '%Y%m%d %H:%M:%S') for i in range(len(df))]
    df = df.set_index(pd.DatetimeIndex(df['datetime']))
    df_ohlc = df['price'].resample('1Min').ohlc()
    df_ohlc['volume'] = df['volume'].resample('1Min').sum()
    df_ohlc = df_ohlc.dropna()
    df_ohlc = df_ohlc.rename(columns={"open": "Open", "close": "Close", "low": "Low", "high": "High", "volume": "Volume"})
    return df_ohlc


def all_tick_to_ohlc(freq='1Min'):

    root_dir = '../data/tick_level/'
    target_dir = '../data/' + freq + '/'
    list_dir = os.listdir(root_dir)
    for d in list_dir:
        print(d)
        if '.csv' in d:
            df = pd.read_csv(root_dir + d)
            df_ohlc = tick_to_ohlc(df)
            df_ohlc.to_csv(target_dir + d)


if __name__ == '__main__':
    df = pd.read_csv('../data/tick_level/600008.csv')
    #ohlc = tick_to_ohlc(df)
    #ohlc.to_csv('../data/1Min/600008.csv')
    all_tick_to_ohlc(freq='1Min')
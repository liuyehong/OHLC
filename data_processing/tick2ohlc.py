import pandas as pd
import numpy as np
from datetime import datetime


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




if __name__ == '__main__':
    df = pd.read_csv('../data/600006.csv')
    ohlc = tick_to_ohlc(df)
    ohlc.to_csv('../data/600006_ohlc.csv')
import tushare as ts
import pandas as pd

def get_ticker():
    df = ts.get_zz500s()

    df.to_csv('./Tickers/china_tickers.csv', index=False)


if __name__ == '__main__':
    get_ticker()
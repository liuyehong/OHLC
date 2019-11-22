import tushare as ts

import datetime
import traceback

# 5minute
def load_data_day_level(symbol):
    df = ts.get_hist_data(symbol)
    try:
        df.to_csv('../data/tick_level/' + symbol + '.csv', index=False)
    except:
        print (traceback.format_exc())

def load_data_tick_level(symbol):
    base = datetime.datetime.today().date()
    date_list = [str(base - datetime.timedelta(days=x)) for x in range(365)]
    print('Downloading ' + symbol)
    I = 0
    for idx in range(len(date_list)):
        d = date_list[idx]
        print(symbol + ': ' + d)
        df_day = ts.get_tick_data(symbol, date=d.replace('-', ''), src='tt')

        if df_day is not None and I == 0:
            I = 1
            df_day['date'] = [d.replace('-', '')] * len(df_day)
            df = df_day

        if df_day is not None and I == 1:
            df_day['date'] = [d.replace('-', '')] * len(df_day)
            df = df.append(df_day)


    try:
        df.to_csv('../data/tick_level/' + symbol + '.csv', index=False)
        print ('Tick Level Data Downloaded: ' + symbol)
    except:
        print (traceback.format_exc())


if __name__ == '__main__':
    symbol = '000001'

    #load_data_day_level(symbol)
    load_data_tick_level(symbol)

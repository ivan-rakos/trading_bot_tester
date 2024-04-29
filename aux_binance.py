from binance.client import Client
import configparser
import pandas as pd


config = configparser.ConfigParser()
config.read("config.ini")

APIKEY = config['BINANCE']['API_KEY']
SECRETKEY = config['BINANCE']['SECRET_KEY']

client = Client(APIKEY, SECRETKEY)


def get_data_market(symbol, temporality, startTime):
    symbol_binance = symbol.replace('-', '')
    columns_names = ['time', 'open', 'high', 'low', 'Close', 'Volume', 'Close Time', 'Quote asset volume',
                     'Number of Trades', 'Taker Volume', 'Maker Volume', 'Nothing']
    candles = client.get_klines(symbol=symbol_binance, interval=temporality, limit=1000, startTime=startTime)
    data = pd.DataFrame(candles, columns=columns_names)
    data['time'] = pd.DatetimeIndex(pd.to_datetime(data['time'], unit='ms'))
    data['open'] = data['open'].astype('float')
    data['high'] = data['high'].astype('float')
    data['low'] = data['low'].astype('float')
    data['Close'] = data['Close'].astype('float')
    data['open'] = data['open'].astype('float')
    data.reset_index(drop=True, inplace=True)
    #data.set_index('time')
    return data[::-1]
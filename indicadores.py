from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.trend import SMAIndicator


def calculate_rsi(data, length):
    dataCloseAux = data.Close.astype(float)
    dataClose = dataCloseAux[::-1].reset_index(drop=True)
    result = RSIIndicator(dataClose, length)
    rsi = result.rsi()
    rsiAct = rsi.get(len(data)-1)
    return round(rsiAct, 2)


def calculate_ema(data, periods):
    dataResult = data[::-1].reset_index(drop=True)
    dataEma = EMAIndicator(dataResult, int(periods)).ema_indicator()
    return round(dataEma.get(dataEma.size-2), 3)


def calculate_sma(data, periods):
    dataResult = data[::-1].reset_index(drop=True)
    dataEma = SMAIndicator(dataResult, int(periods)).sma_indicator()
    a = 1
    return round(dataEma.get(dataEma.size-2), 3)


def calculate_ssl_channel(data, period, ema):
    sslHigh = calculate_sma(data.high, period)
    sslLow = calculate_sma(data.low, period)
    ema = calculate_ema(data.Close, ema)

    return {'sslHigh': sslHigh, 'sslLow': sslLow, 'ema': ema}


def cruce_alza(price1, price2, sslHigh):
    return price1 > sslHigh and price2 < sslHigh
def cruce_baja(price1, price2, sslLow):
    return price1 < sslLow and price2 > sslLow
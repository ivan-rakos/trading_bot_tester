from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator


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
    a = 1
    return round(dataEma.get(dataEma.size-2), 3)

import bingx
import json
import time


def calculate_size_position(percent, leverage, symbol):
    balance = bingx.get_balance()
    quantity_position_aux = balance * (percent / 100)
    data_symbol = json.loads(bingx.get_ticker(symbol))['data']
    ask_price = float(data_symbol['askPrice'])
    quantity_position = int((round(quantity_position_aux, 2) * leverage) / ask_price)
    return quantity_position


def calculate_tp_sl(side, profit, stop, price):
    sl = 0
    tp = 0
    if side == "SELL":
        sl = price + (price * (stop/100))
        tp = price - (price * (profit/100))

    elif side == "BUY":
        sl = price - (price * (stop/100))
        tp = price + (price * (profit/100))

    return {"takeProfitPrice": str(tp), "stopLossPrice": str(sl)}


def convertDates(strDate):
    tiempo_segundos = time.mktime(time.strptime(strDate, "%Y/%m/%d"))
    # Convertir los segundos a milisegundos
    milisegundos = tiempo_segundos * 1000
    return int(milisegundos)
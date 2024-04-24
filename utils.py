import bingx
import json
import time
from datetime import datetime



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
    fecha_hora = time.strptime(strDate, "%Y-%m-%d %H:%M:%S")
    fecha_hora_datetime = datetime.fromtimestamp(time.mktime(fecha_hora))
    tiempo_segundos = (fecha_hora_datetime - datetime(1970, 1, 1)).total_seconds()
    # Convertir los segundos a milisegundos
    milisegundos = tiempo_segundos * 1000
    return int(milisegundos)

def timestampToDate(time):
    return datetime.fromtimestamp(time/1000)

def calculate_percent_stop(initialPrice, finalPrice):
    return abs(100 - (finalPrice * 100)/initialPrice) * -1

def check_if_stop(data, stop, capital, percent_stop, mode):
    takeStop = False
    if (mode == "sell" and float(data.high) >= stop) or (mode == "buy" and float(data.low) <= stop):
        capital = capital + (capital * percent_stop/100)
        takeStop = True
    return {"initialCapital": capital, "takeStop": takeStop}

def check_result(data, priceOpened, priceClosed, mode, capital, op_winners, op_losers):
    new_capital = 0.0
    operation_winner = False
    diff_price = abs(100 - (priceClosed * 100)/priceOpened)
    if mode == "buy" and priceClosed > priceOpened:
        new_capital = capital + (capital * diff_price/100)
    if mode == "buy" and priceClosed <= priceOpened:
        new_capital = capital - (capital * diff_price / 100)
    if mode == "sell" and priceClosed < priceOpened:
        new_capital = capital + (capital * diff_price / 100)
    if mode == "sell" and priceClosed >= priceOpened:
        new_capital = capital - (capital * diff_price / 100)

    if new_capital > capital:
        op_winners = op_winners +1
    else:
        op_losers = op_losers +1

    return [new_capital, op_winners, op_losers]

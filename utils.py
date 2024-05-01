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
def calculate_percent_profit(initialPrice, takeProfitPercent, mode):
    gap_price = (initialPrice * (takeProfitPercent/100))
    price_take_profit = 0.0
    if mode == "buy":
        price_take_profit = initialPrice + gap_price
    else:
        price_take_profit = initialPrice - gap_price
    return price_take_profit


def check_if_stop_profit(data, stop, profit,  capital, percent_stop, percent_profit, mode, fee):
    takeStop = False
    takeProfit = False
    if (mode == "sell" and float(data.high) >= stop) or (mode == "buy" and float(data.low) <= stop):
        lost_capital = (capital * percent_stop/100)
        lost_capital_fee = apply_fees(lost_capital, fee)
        capital = capital + lost_capital_fee
        takeStop = True
    elif(mode == "sell" and float(data.low) <= profit) or (mode == "buy" and float(data.high) >= profit):
        won_capital = (capital * (percent_profit/100))
        won_capital_fee = apply_fees(won_capital, fee)
        capital = capital + won_capital_fee
        takeProfit = True
    return {"initialCapital": capital, "takeStop": takeStop, "takeProfit": takeProfit}


def check_result(data, priceOpened, priceClosed, mode, capital, op_winners, op_losers, fee):
    new_capital = 0.0
    operation_winner = False
    diff_price = abs(100 - (priceClosed * 100)/priceOpened)
    won_lost_capital = (capital * diff_price/100)
    won_lost_capital_fee = apply_fees(won_lost_capital, fee)
    if mode == "buy" and priceClosed > priceOpened:

        new_capital = capital + won_lost_capital_fee
    if mode == "buy" and priceClosed <= priceOpened:
        new_capital = capital - won_lost_capital_fee
    if mode == "sell" and priceClosed < priceOpened:
        new_capital = capital + won_lost_capital_fee
    if mode == "sell" and priceClosed >= priceOpened:
        new_capital = capital - won_lost_capital_fee

    if new_capital > capital:
        op_winners = op_winners +1
    else:
        op_losers = op_losers +1

    return [new_capital, op_winners, op_losers]

def apply_fees(capital, fee):
    fee_calculated = capital * fee
    return capital-fee_calculated

def change_exchange(date):
    exchange = "bingx"
    if "2022-01" in date or "2022-02" in date or "2022-03" in date or "2020" in date or "2021" in date:
        exchange = "binance"
    return exchange

def print_results(dataResults):
    print(json.dumps(dataResults, indent=4))

def generate_all_results(op_winners, op_losers, capital, initialCapital, smaValue, emaValue, takeProfitPercent, date, dict):
    op_total = op_winners + op_losers
    winner_percent = (op_winners * 100) / op_total
    loser_percent = (op_losers * 100) / op_total
    capital_percent = ((capital * 100) / initialCapital) - 100
    result = {'beneficio': capital, 'beneficio_porcentaje': round(capital_percent, 2), 'op_total': op_total,
              'op_winner': op_winners, 'winner_percent': winner_percent
        , 'op_losers': op_losers, 'loser_percent': loser_percent}
    key = str(smaValue) + "-" + str(emaValue) + "-" + str(takeProfitPercent)
    resumeDate = {date: result}
    if key in dict:
        dict[key].update(resumeDate)
    else:
        dict[key] = resumeDate

    return dict

def generate_profit(capital, initialCapital, smaValue, emaValue, takeProfitPercent, date, dict):
    capital_percent = ((capital * 100) / initialCapital) - 100
    result = {'beneficio_porcentaje': round(capital_percent, 2)}
    key = str(smaValue) + "-" + str(emaValue) + "-" + str(takeProfitPercent)
    resumeDate = {date: result}
    if key in dict:
        dict[key].update(resumeDate)
    else:
        dict[key] = resumeDate

    return dict

def calculate_avg_profit(result):
    medias_por_clave = {}

    for clave, subdiccionario in result.items():
        # Inicializamos la suma y el contador para cada clave
        suma_valores = 0
        contador_valores = 0

        # Iteramos sobre los valores del subdiccionario
        for valor in subdiccionario.values():
            suma_valores += valor["beneficio_porcentaje"]
            contador_valores += 1

        # Calculamos la media para la clave actual
        media = suma_valores / contador_valores

        # Guardamos la media para la clave actual
        medias_por_clave[clave] = media
    return medias_por_clave
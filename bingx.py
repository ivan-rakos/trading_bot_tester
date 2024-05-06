import utils
from aux_bingx import *
import pandas as pd
import json
import time


def get_data_market(symbol, temporality, limit):
    payload = {}
    path = '/openApi/swap/v3/quote/klines'
    method = "GET"
    paramsMap = {
        "symbol": symbol,
        "interval": temporality,
        "limit": limit
    }
    paramsStr = parseParam(paramsMap)
    dataCandles = send_request(method, path, paramsStr, payload)
    json_candles = json.loads(dataCandles)
    candles_string = json.dumps(json_candles['data'])
    df = pd.DataFrame(json.loads(candles_string))
    df['high'] = df['high'].astype(float)
    df['close'] = df['close'].astype(float)
    df['low'] = df['low'].astype(float)
    df.set_index('time')
    return df


def set_leverage(mode, leverage, symbol):
    payload = {}
    path = '/openApi/swap/v2/trade/leverage'
    method = "POST"
    paramsMap = {
        "leverage": leverage,
        "side": mode,
        "symbol": symbol,
        "timestamp": str(int(time.time() * 1000))
    }
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)


def open_position(symbol, side, position_side, profit, stop, price, leverage, percent_position):
    tp_sl = utils.calculate_tp_sl(side, profit, stop, price)
    take_profit = tp_sl['takeProfitPrice']
    stop_loss = tp_sl['stopLossPrice']
    take_profit_json = "{\"type\": \"TAKE_PROFIT_MARKET\", \"stopPrice\":" + take_profit + " ,\"price\": " + take_profit + ",\"workingType\":\"MARK_PRICE\"}"
    stop_loss_json = "{\"type\": \"STOP_MARKET\", \"stopPrice\":" + stop_loss + " ,\"price\": " + stop_loss + ",\"workingType\":\"MARK_PRICE\"}"

    size_position = utils.calculate_size_position(percent_position, int(leverage), symbol)
    payload = {}
    path = '/openApi/swap/v2/trade/order'
    method = "POST"
    paramsMap = {
        "symbol": symbol,
        "side": side,
        "positionSide": position_side,
        "type": "MARKET",
        "quantity": size_position,
        "takeProfit": take_profit_json,
        "stopLoss": stop_loss_json
    }
    paramsStr = parseParam(paramsMap)
    result_request = send_request(method, path, paramsStr, payload)
    return result_request


def close_all_positions(symbol):
    payload = {}
    path = '/openApi/swap/v2/trade/closeAllPositions'
    method = "POST"
    paramsMap = {
        "timestamp": str(int(time.time() * 1000)),
        "symbol": symbol
    }
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)


def get_balance():
    payload = {}
    path = '/openApi/swap/v2/user/balance'
    method = "GET"
    paramsMap = {
        "timestamp": str(int(time.time() * 1000))
    }
    paramsStr = parseParam(paramsMap)
    response = send_request(method, path, paramsStr, payload)
    json_response = json.loads(response)
    balance = json.dumps(json_response['data'])
    return float(json.loads(balance)['balance']['balance'])


def get_ticker(symbol):
    payload = {}
    path = '/openApi/swap/v2/quote/ticker'
    method = "GET"
    paramsMap = {
        "symbol": symbol,
        "timestamp": str(int(time.time() * 1000))
    }
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)


def check_position_opened(symbol):
    payload = {}
    path = '/openApi/swap/v2/user/positions'
    method = "GET"
    paramsMap = {
        "symbol": symbol,
        "timestamp": str(int(time.time() * 1000))
    }
    paramsStr = parseParam(paramsMap)
    response = send_request(method, path, paramsStr, payload)
    response_json = json.loads(response)['data']
    pos_quantity = len(response_json)
    return pos_quantity > 0



def open_position_mock(initialPrice, priceStop):
    stopPercent =  utils.calculate_percent_stop(initialPrice, priceStop)
    a = 1
    return stopPercent

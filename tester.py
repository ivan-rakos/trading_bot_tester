import bingx as bingx
import json
import pandas as pd
import utils
import indicadores


def tester(symbol, temporality, periodsRSI, overBoughtValues, overSoldValues, emaFastValues, emaSlowValues,
           takeProfitValues, startTime, endTime):
    startTimeMilis = utils.convertDates(startTime)
    endTimeMilis = utils.convertDates(endTime)
    data = get_data_market(symbol, temporality, "200", startTimeMilis, endTimeMilis)
    for periodRsi in periodsRSI:
        for overBought in overBoughtValues:
            for overSold in overSoldValues:
                for emaFast in emaFastValues:
                    for emaSlow in emaSlowValues:
                        for takeProfit in takeProfitValues:
                            strategy(data, periodRsi, overBought, overSold, emaFast, emaSlow, takeProfit)


def strategy(data, periodRsiValue, overBoughtValue, overSoldValue, emaFastValue, emaSlowValue, takeProfitValue):
    totalLength = len(data)
    maxValue = max(periodRsiValue, emaFastValue, emaSlowValue)
    try:
        for indice in range(len(data) - 1, -1, -1):
            if (totalLength - indice) > maxValue:
                fila = data.iloc[indice]
                print(f'Precio actual: {fila.Close}')
                dataRecorrida = data.tail(totalLength - indice)
                rsi = indicadores.calculate_rsi(dataRecorrida, periodRsiValue)
                #emaFast = indicadores.calculate_ema(dataRecorrida, emaFastValue)
                #emaSlow = indicadores.calculate_ema(dataRecorrida, emaSlowValue)
    except Exception as error:
        print("An exception ocurred: ", error)


def get_data_market(symbol, temporality, limit, startDate, endDate):
    payload = {}
    path = '/openApi/swap/v3/quote/klines'
    method = "GET"
    paramsMap = {
        "symbol": symbol,
        "interval": temporality,
        "limit": limit,
        "startTime": str(startDate),
        "endTime": str(endDate)
    }
    paramsStr = bingx.parseParam(paramsMap)
    dataCandles = bingx.send_request(method, path, paramsStr, payload)
    json_candles = json.loads(dataCandles)
    candles_string = json.dumps(json_candles['data'])
    df = pd.DataFrame(json.loads(candles_string))
    df.rename(columns={'close': 'Close'}, inplace=True)
    df.set_index('time')
    return df

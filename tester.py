import aux_binance
import bingx as bingx
import json
import pandas as pd
import utils
import indicadores


def tester(symbol, temporality, smaValues, emaValues, takeProfitValues, dates, initialCapital):
    resultTest = dict()
    for date in dates:
        data = pd.DataFrame()
        try:
            data = pd.read_csv("resources/"+date+"_"+temporality+".csv", sep=',')
        except Exception as error:
            startDate = date+"-01 00:00:00"
            endDate = ""
            if "-02" in date:
                endDate = date + "-28 00:00:00"
            else:
                endDate = date + "-30 00:00:00"
            startTimeMilis = utils.convertDates(startDate)
            endTimeMilis = utils.convertDates(endDate)
            exchange = utils.change_exchange(startDate)
            data = get_all_data_market(symbol, temporality, "1440", startTimeMilis, endTimeMilis, exchange)
            data.to_csv("resources/"+startDate.split("-01 ")[0]+"_"+temporality+".csv", index = False)

        for smaValue in smaValues:
            for emaValue in emaValues:
                for takeProfitPercent in takeProfitValues:
                    [capital, op_winners, op_losers] = strategy(data, smaValue, emaValue, takeProfitPercent, initialCapital)
                    op_total = op_winners + op_losers
                    winner_percent = (op_winners * 100) / op_total
                    loser_percent = (op_losers * 100) / op_total
                    capital_percent = ((capital*100)/initialCapital) - 100
                    result = {'beneficio': capital, 'beneficio_porcentaje': round(capital_percent,2), 'op_total': op_total, 'op_winner': op_winners, 'winner_percent': winner_percent
                              , 'op_losers': op_losers, 'loser_percent': loser_percent}
                    key = date+"--"+str(smaValue) + "-" + str(emaValue) + "-" + str(takeProfitPercent)
                    resultTest[key] = result
    str_profits_resume = ""
    for result in resultTest:
        data = resultTest[result]
        beneficio = data['beneficio']
        capital_percent = data['beneficio_porcentaje']
        op_total = data['op_total']
        op_winners = data['op_winner']
        winner_percent = data['winner_percent']
        op_losers = data['op_losers']
        loser_percent = data['loser_percent']
        key = result.split("--")[0]
        str_profits_resume = str_profits_resume + key +": "+str(capital_percent) + "\n"
        print("###################### RESULTADOS ##################")
        print(f'Resultados del test realizado con ema: {result}')
        print(f'Beneficio final: {beneficio} --> {capital_percent}%')
        print(f'Operaciones totales : {op_total}')
        print(f'Operaciones ganadoras : {op_winners} - {winner_percent}%')
        print(f'Operaciones perdedoras : {op_losers} - {loser_percent}%')
        print("###################### FIN RESULTADOS ##################")
    print(str_profits_resume)




def strategy(data, smaValue, emaValue, takeProfitPercent, initialCapital):
    totalLength = len(data)
    order_open = False
    mode = ""
    stop_percent = 0.0
    stopLoss = 0.0
    takeProfit = 0.0
    priceOpened = 0.0
    op_winners = 0
    op_losers = 0
    fee = 0.0005
    fee_limit = 0.0002
    try:
        for indice in range(len(data) - 1, -1, -1):
            maxValue = max(smaValue,emaValue)
            if (totalLength - indice) > maxValue:
                fila = data.iloc[indice + 1]
                filaAnt = data.iloc[indice + 2]
                tiempo_actual = fila.time
                if order_open == True:
                    resultCheckStop = utils.check_if_stop_profit(fila, stopLoss, takeProfit, initialCapital, stop_percent, takeProfitPercent, mode, fee_limit)
                    initialCapital = resultCheckStop["initialCapital"]
                    takeStop = resultCheckStop["takeStop"]
                    takeProfitR = resultCheckStop["takeProfit"]
                    if takeStop or takeProfitR:
                        order_open = False
                        mode = ""
                        if takeProfitR:
                            print("Operacion toca TAKE PROFIT y se CIERRA")
                            op_winners = op_winners +1
                        else:
                            print("Operacion toca STOP LOSS y se CIERRA")
                            op_losers = op_losers + 1

                print(f'Precio actual: {tiempo_actual} - {fila.Close}')
                price1 = float(fila.Close)
                price2 = float(filaAnt.Close)
                dataRecorrida = data.tail(totalLength - indice)
                #adx = indicadores.calculate_adx(dataRecorrida, 14)
                ssl_channel = indicadores.calculate_ssl_channel(dataRecorrida, smaValue, emaValue)
                sslHigh = ssl_channel['sslHigh']
                sslLow = ssl_channel['sslLow']

                long_condition = indicadores.cruce_alza(price1, price2, sslHigh) and price1 > ssl_channel['ema']
                long_close_condition = indicadores.cruce_baja(price1, price2, sslLow)
                short_condition = indicadores.cruce_baja(price1, price2, sslLow) and price1 < ssl_channel['ema']
                short_close_condition = indicadores.cruce_alza(price1, price2, sslHigh)

                if long_close_condition:
                    if order_open and mode != "sell":
                        print("CIERRO LONG PREVIOO")
                        [initialCapital, op_winners, op_losers] = utils.check_result(fila, priceOpened, price1, mode,
                                                                                     initialCapital, op_winners,
                                                                                     op_losers, fee)
                        order_open = False
                        mode = ""
                if short_close_condition:
                    if order_open and mode != "buy":
                        print("CIERRO SHORT PREVIO")
                        [initialCapital, op_winners, op_losers] = utils.check_result(fila, priceOpened, price1, mode,
                                                                                     initialCapital, op_winners,
                                                                                     op_losers, fee)
                        order_open = False
                        mode = ""

                if long_condition and not order_open:
                    calculateRisk = ((price1 * 100) / sslLow) - 100
                    if calculateRisk <= 4:
                        mode = "buy"
                        print("ABRO LONG")
                        order_open = True
                        stopLoss = sslLow
                        stop_percent = bingx.open_position_mock(price1, sslLow)
                        takeProfit = utils.calculate_percent_profit(price1, takeProfitPercent, mode)
                        initialCapital = utils.apply_fees(initialCapital, fee)
                        priceOpened = price1
                    else:
                        print("DEMASIADO RIESGO PARA ABRIR LONG")
                elif short_condition and not order_open:
                    calculateRisk = 100 - ((price1 * 100) / sslHigh)
                    if calculateRisk <= 4:
                        mode = "sell"
                        print("ABRO SHORT")
                        order_open = True
                        stopLoss = sslHigh
                        stop_percent = bingx.open_position_mock(price1, sslHigh)
                        takeProfit = utils.calculate_percent_profit(price1, takeProfitPercent, mode)
                        initialCapital = utils.apply_fees(initialCapital, fee)
                        priceOpened = price1

                    else:
                        print("DEMASIADO RIESGO PARA ABRIR UN SHORT")
        return [initialCapital, op_winners, op_losers]
    except Exception as error:
        print("An exception ocurred: ", error)




def get_data_market(symbol, temporality, limit, startDate):
    payload = {}
    path = '/openApi/swap/v3/quote/klines'
    method = "GET"
    paramsMap = {
        "symbol": symbol,
        "interval": temporality,
        "limit": limit,
        "startTime": str(startDate)
    }
    paramsStr = bingx.parseParam(paramsMap)
    dataCandles = bingx.send_request(method, path, paramsStr, payload)
    json_candles = json.loads(dataCandles)
    candles_string = json.dumps(json_candles['data'])
    df = pd.DataFrame(json.loads(candles_string))
    df.rename(columns={'close': 'Close'}, inplace=True)
    df['time'] = pd.to_datetime(df['time'], utc=True, unit='ms')
    df.set_index('time')
    return df

def get_all_data_market(symbol, temporality, limit, startDate, endDate, bingx_binance):
    finalDataFrame = pd.DataFrame()
    finalDate = 0
    while finalDate < endDate:
        if bingx_binance == "bingx":
            data = get_data_market(symbol, temporality,limit, startDate)
            lastDate = str(data.iloc[0].time).split('+')[0]
        elif bingx_binance == "binance":
            data = aux_binance.get_data_market(symbol, temporality, startDate)
            lastDate = str(data.iloc[0].time)

        if data.shape[0] == 1:
            finalDate = endDate
        else:
            finalDate = utils.convertDates(lastDate)
        startDate = finalDate
        if finalDate != endDate:
            finalDataFrame = pd.concat([data, finalDataFrame])

    df_filtrado = pd.DataFrame()
    if bingx_binance == "binance":
        df_filtrado = finalDataFrame[finalDataFrame['time'] <= utils.timestampToDate(endDate)]
        df_filtrado.drop_duplicates()
    elif bingx_binance == "bingx":
        df_filtrado = finalDataFrame.drop_duplicates()
    return df_filtrado

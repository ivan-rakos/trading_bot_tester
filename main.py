import pandas as pd

import dates
import indicadores
import tester

if __name__ == '__main__':
    symbol = "RUNE-USDT"
    temporality = "30m"
    smaValues = [25]
    emaValues = [34]
    takeProfitValues = [8]

    fechas = dates.get_all_data()
    initialCapital = 1000
    #tester.tester(symbol, temporality, smaValues, emaValues, takeProfitValues, fechas, initialCapital)
    data = pd.read_csv("resources/RUNE-USDT/all_data.csv", sep=',')
    totalLength = len(data)
    for indice in range(len(data) - 1, -1, -1):
        if (totalLength - indice) > 27:
            dataRecorrida = data.tail(totalLength - indice)
            adx = indicadores.calculate_adx(dataRecorrida, 14)
    a = 1

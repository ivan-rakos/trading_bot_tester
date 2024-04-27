import tester
import numpy as np

if __name__ == '__main__':
    symbol = "RUNE-USDT"
    temporality = "5m"
    smaValues = [6]
    emaValues = [37]
    takeProfitValues = [1.5, 2]
    startDate = "2024-04-01 00:00:00"
    endDate = "2024-04-26 00:00:00"
    initialCapital = 1000
    tester.tester(symbol, temporality, smaValues, emaValues, takeProfitValues, startDate, endDate, initialCapital)

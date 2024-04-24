import tester
import numpy as np

if __name__ == '__main__':
    symbol = "RUNE-USDT"
    temporality = "15m"
    smaValues = [14]
    takeProfitValues = np.arange(0.5, 3)
    startDate = "2022-04-01 00:00:00"
    endDate = "2024-04-01 00:00:00"
    initialCapital = 1000
    tester.tester(symbol, temporality, smaValues, takeProfitValues, startDate, endDate, initialCapital)

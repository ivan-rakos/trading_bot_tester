import tester
import numpy as np

if __name__ == '__main__':
    symbol = "RUNE-USDT"
    temporality = "15m"
    smaValues = [7,14,15,16,55]
    takeProfitValues = np.arange(0.5, 3)
    startDate = "2024/04/01"
    endDate = "2024/04/02"
    initialCapital = 1000
    tester.tester(symbol, temporality, smaValues, takeProfitValues, startDate, endDate, initialCapital)

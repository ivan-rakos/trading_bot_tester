import tester
import numpy as np

if __name__ == '__main__':
    symbol = "BTC-USDT"
    temporality = "1h"
    periodsRSI = np.arange(9, 16)
    overBoughtValues = np.arange(60, 91)
    overSoldValues = np.arange(10, 41)
    emaFastValues = np.arange(2, 6)
    emaSlowValues = np.arange(15, 31)
    takeProfitValues = np.arange(0.5, 3)
    startDate = "2024/03/24"
    endDate = "2024/03/27"
    tester.tester(symbol, temporality, periodsRSI, overBoughtValues, overSoldValues, emaFastValues, emaSlowValues,
                  takeProfitValues, startDate, endDate)

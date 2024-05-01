import dates
import tester

if __name__ == '__main__':
    symbol = "RUNE-USDT"
    temporality = "15m"
    smaValues = [18,19,20,21,22,23,24,25,26,27]
    emaValues = [30,31,32,33,34,35,36,37,38,39,40]
    takeProfitValues = [4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5]

    fechas = dates.get_all_data()
    initialCapital = 1000
    tester.tester(symbol, temporality, smaValues, emaValues, takeProfitValues, fechas, initialCapital)

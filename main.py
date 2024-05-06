import dates
import tester

if __name__ == '__main__':
    symbol = "RUNE-USDT"
    temporality = "5m"
    smaValues = [14]
    emaValues = [2]
    takeProfitValues = [8]

    fechas = dates.get_post_bullrun()
    initialCapital = 1000
    tester.tester(symbol, temporality, smaValues, emaValues, takeProfitValues, fechas, initialCapital)

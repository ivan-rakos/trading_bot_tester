import tester

if __name__ == '__main__':
    symbol = "RUNE-USDT"
    temporality = "30m"
    smaValues = [21]
    emaValues = [37]
    takeProfitValues = [200]

    single_month = ["2024-04"]
    dates = ["2022-04", "2022-05", "2022-06"]
    last_year = ["2024-01", "2024-02", "2024-03", "2024-04"]
    dates_bullrun = ["2021-01", "2021-02", "2021-03", "2021-04", "2021-05", "2021-06", "2021-07", "2021-08", "2021-09",
                     "2021-10", "2021-11", "2021-12", "2022-01", "2022-02", "2022-03"]
    dates_2022_2024 = ["2022-04", "2022-05", "2022-06", "2022-07", "2022-08", "2022-09", "2022-10", "2022-11",
                       "2022-12", "2023-01", "2023-02", "2023-03", "2023-04", "2023-05", "2023-06", "2023-07",
                       "2023-08", "2023-09", "2023-10", "2023-11", "2023-12", "2024-01", "2024-02", "2024-03",
                       "2024-04"]

    dates_all = dates_bullrun + dates_2022_2024
    initialCapital = 1000
    tester.tester(symbol, temporality, smaValues, emaValues, takeProfitValues, single_month, initialCapital)

import pandas


def get_data():
    csv_data = pandas.read_csv('./nasdaq_tickers.csv')
    symbols = csv_data['Symbol']
    return symbols


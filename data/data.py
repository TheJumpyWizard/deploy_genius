import requests
import pandas as pd

def get_historical_prices(symbol, api_key):
    """
    Retrieves historical price data for a given symbol from the Alpha Vantage API.

    Args:
        symbol (str): The symbol to retrieve price data for.
        api_key (str): The API key to use for authentication.

    Returns:
        pandas.DataFrame: A DataFrame containing the historical price data.
    """
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()['Time Series (Daily)']
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.astype('float')
    df = df.sort_index(ascending=True)
    return df


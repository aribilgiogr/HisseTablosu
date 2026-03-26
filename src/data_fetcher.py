import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker_symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """ Belirtilen hisse senedi ve tarih aralığı için yfinance (Yahoo Finance) üzerinden geçmiş fiyat verilerini indirir. """
    try:
        df = yf.download(ticker_symbol, start_date, end_date, multi_level_index=False)
        return df
    except Exception as ex:
        print(f"Veri çekme hatası: {ex}")
        return pd.DataFrame()

import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose


def calculate_moving_average(df: pd.DataFrame, window: int = 20):
    """ Belirtilen pencere (window) değerine göre Basit Hareketli Ortalama (SMA) hesaplar. """
    if 'Close' in df.columns:
        df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
    return df


def decompose_time_series(df: pd.DataFrame, period: int = 30):
   """ Kapanış fiyatları üzerinden trend ve mevsimsellik ayrıştırması yapar. """
   if 'Close' not in df.columns or df.empty:
       return None

   ts_data = df['Close'].dropna()

   try:
       result = seasonal_decompose(ts_data,model='additive', period=period)
       return result
   except Exception as ex:
       print(f"Ayrıştırma hatası: {ex}")
       return None
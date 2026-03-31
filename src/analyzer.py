import pandas as pd
from pmdarima import auto_arima
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
        result = seasonal_decompose(ts_data, model='additive', period=period)
        return result
    except Exception as ex:
        print(f"Ayrıştırma hatası: {ex}")
        return None


def predict_next_day(df: pd.DataFrame):
    """ Kapanış fiyatları üzerinden (ARIMA) kullanarak en uygun modeli bulup bir sonraki işlem adımını tahmin eder. """
    if 'Close' not in df.columns or len(df) < 30:
        return None

    try:
        ts_data = df['Close'].dropna()
        model = auto_arima(
            ts_data,
            seasonal=False,
            stepwise=False,
            approximation=False,
            information_criterion='aic',
            max_p=5,
            max_q=5,
            suppress_warnings=True,
            error_action='ignore'
        )
        forecast = model.predict(n_periods=1)
        return forecast.iloc[0]
    except Exception as ex:
        print(f"Tahmin hatası: {ex}")
        return None

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_time_series(df: pd.DataFrame, symbol: str):
    """ Kapanış fiyatı ve hesaplanmış hareketli ortalamaları gösteren ana grafik. """
    fig = go.Figure()
    if 'Close' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=f'{symbol} Kapanış'))

    sma_cols = [col for col in df.columns if 'SMA_' in col]
    for col in sma_cols:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=col))
    fig.update_layout(title=f'{symbol} Fiyat Grafiği', xaxis_title='Tarih', yaxis_title='Fiyat')
    return fig


def plot_decomposition(decompose_result):
    """ Zaman serisinin trend, mevsimsellik ve kalıntı bileşenlerini çizer. """
    if decompose_result is None:
        return go.Figure()

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                        subplot_titles=('Gözlem', 'Trend', 'Mevsimsellik', 'Kalıntı'))

    x_values = decompose_result.observed.index

    fig.add_trace(go.Scatter(x=x_values, y=decompose_result.observed, mode='lines', name='Gözlem'), row=1, col=1)
    fig.add_trace(go.Scatter(x=x_values, y=decompose_result.trend, mode='lines', name='Trend'), row=2, col=1)
    fig.add_trace(go.Scatter(x=x_values, y=decompose_result.seasonal, mode='lines', name='Mevsimsellik'), row=3, col=1)
    fig.add_trace(go.Scatter(x=x_values, y=decompose_result.resid, mode='lines', name='Kalıntı'), row=4, col=1)

    fig.update_layout(height=800, title_text='Zaman Serisi Ayrıştırması')
    return fig

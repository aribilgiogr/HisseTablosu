from datetime import date, timedelta

import streamlit as st
from scipy.constants import year

from src.analyzer import calculate_moving_average, decompose_time_series, predict_next_day
from src.data_fetcher import fetch_stock_data
from src.utils import load_symbols, save_symbols
from src.visualizer import plot_time_series, plot_decomposition

st.set_page_config(page_title="Finansal Zaman Serisi Analizi", layout="wide")

with st.sidebar:
    st.header("Hisse Sembol Yönetimi:")
    symbols = load_symbols()

    with st.form(key="ekle_form", clear_on_submit=True):
        new_symbol = st.text_input("Yeni Sembol Ekle (Örn: AAPL):")
        if st.form_submit_button('Ekle') and new_symbol:
            if new_symbol.upper() not in symbols:
                symbols.append(new_symbol.upper())
                save_symbols(symbols)
                st.rerun()

    with st.form(key="sil_form"):
        remove_symbol = st.selectbox("Sembol Sil:", ["Seçiniz"] + symbols)
        if st.form_submit_button('Sil') and remove_symbol != "Seçiniz":
            symbols.remove(remove_symbol)
            save_symbols(symbols)
            st.rerun()

st.title("Finansal Zaman Serisi Analizi ve Gelecek Tahmini")

tab1, tab2 = st.tabs(["Seçilen Sembol", "Tüm Semboller"])
with tab1:
    selected_symbol = st.selectbox("Analiz Edilecek Sembol:", symbols)

    col1, col2, col3 = st.columns((2, 2, 1))
    start_date = col1.date_input("Başlangıç Tarihi:", date.today() - timedelta(days=2*365), key='start_1')
    end_date = col2.date_input("Bitiş Tarihi:", date.today(), key='end_1')
    if col3.button("Analizi Başlat", width='stretch', key='analyze_1'):
        if selected_symbol:
            data = fetch_stock_data(selected_symbol, str(start_date), str(end_date + timedelta(days=1)))
            if not data.empty:
                last_price = data['Close'].iloc[-1]
                prediction = predict_next_day(data)
                if prediction is not None:
                    delta = prediction - last_price
                    delta_perc = delta * 100 / last_price
                    st.metric(label="Tahmini Kapanış Fiyatı", value=f"{prediction:.2f}",
                              delta=f"%{delta_perc:.2f}")
                else:
                    st.warning("Tahmin yapılamadı. Yeterli veri olmayabilir.")

                st.subheader(f"{selected_symbol} Fiyat ve Hareketli Ortalama (20 Gün)")
                data_with_sma = calculate_moving_average(data)
                fig_ts = plot_time_series(data_with_sma, selected_symbol)
                c1, c2 = st.columns(2)
                c1.plotly_chart(fig_ts, width='stretch')
                c2.dataframe(data_with_sma, width='stretch')

                st.subheader(f"{selected_symbol} Zaman Serisi Ayrıştırması")
                decomposition = decompose_time_series(data_with_sma)
                if decomposition:
                    fig_decomp = plot_decomposition(decomposition)
                    st.plotly_chart(fig_decomp, width='stretch')
                else:
                    st.warning("Ayrıştırma için yeterli veri noktası bulunamadı.")
            else:
                st.error("Veri çekilemedi, sembol adını veya tarih aralığını kontrol edin.")
        else:
            st.warning("Analiz için önce bir sembol eklemelisiniz!")

with tab2:
    c1, c2, c3 = st.columns((2, 2, 1))
    start_date = c1.date_input("Başlangıç Tarihi:",  date.today() - timedelta(days=2*365), key='start_2')
    end_date = c2.date_input("Bitiş Tarihi:", date.today(), key='end_2')
    if c3.button("Analizi Başlat", width='stretch', key='analyze_2'):
        cols = st.columns(3)
        for i, symbol in enumerate(symbols):
            with cols[i % 3]:
                d = fetch_stock_data(symbol, str(start_date), str(end_date + timedelta(days=1)))
                if not d.empty:
                    last = d['Close'].iloc[-1]
                    pred = predict_next_day(d)
                    if pred is not None:
                        delta = pred - last
                        delta_perc = delta * 100 / last
                        print(delta, delta_perc, pred, last)
                        st.metric(
                            label=symbol,
                            value=f"{pred:.2f}",
                            delta=f"%{delta_perc:.2f} - ${delta:.2f}",
                            format="dollar"
                        )
                    else:
                        st.warning("Tahmin yapılamadı. Yeterli veri olmayabilir.")
                else:
                    st.error("Veri çekilemedi, sembol adını veya tarih aralığını kontrol edin.")

from datetime import UTC, datetime, date

import streamlit as st

from src.analyzer import calculate_moving_average, decompose_time_series
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

st.title("Finansal Zaman Serisi Analizi")
selected_symbol = st.selectbox("Analiz Edilecek Sembol:", symbols)

col1, col2, col3 = st.columns((2, 2, 1))
start_date = col1.date_input("Başlangıç Tarihi:", date(2020, 1, 1))
end_date = col2.date_input("Bitiş Tarihi:", date.today())
if col3.button("Analizi Başlat", width='stretch'):
    if selected_symbol:
        data = fetch_stock_data(selected_symbol, str(start_date), str(end_date))
        if not data.empty:
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
                st.plotly_chart(fig_decomp,width='stretch')
            else:
                st.warning("Ayrıştırma için yeterli veri noktası bulunamadı.")
        else:
            st.error("Veri çekilemedi, sembol adını veya tarih aralığını kontrol edin.")
    else:
        st.warning("Analiz için önce bir sembol eklemelisiniz!")
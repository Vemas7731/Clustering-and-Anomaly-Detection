import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from datetime import datetime

st.set_page_config(page_title="Wisata Forecasting", layout="centered")
st.title("🎢 Input Data Pengunjung Wisata")


# Inisialisasi penyimpanan data di session_state
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Bulan', 'Tahun', 'Jumlah'])

# Form input
with st.form("input_form"):
    col1, col2 = st.columns(2)
    bulan = col1.selectbox("Bulan", list(range(1, 13)), format_func=lambda x: datetime(2000, x, 1).strftime('%B'))
    tahun = col2.number_input("Tahun", min_value=2000, max_value=2100, value=datetime.now().year)
    jumlah = st.number_input("Jumlah Pengunjung", min_value=0)
    submitted = st.form_submit_button("Tambah Data / Perbarui")
    if submitted:
        # Cek apakah kombinasi bulan & tahun sudah ada
        existing = (st.session_state.data['Bulan'] == bulan) & (st.session_state.data['Tahun'] == tahun)
        if existing.any():
            st.session_state.data.loc[existing, 'Jumlah'] = jumlah
            st.info("✏️ Data untuk bulan & tahun tersebut telah diperbarui.")
        else:
            new_row = {'Bulan': bulan, 'Tahun': tahun, 'Jumlah': jumlah}
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
            st.success("✅ Data baru berhasil ditambahkan!")

# Tampilkan data
st.subheader("📋 Data Pengunjung")
data = st.session_state.data
data_sorted = data.sort_values(by=['Tahun', 'Bulan'])
st.dataframe(data_sorted, use_container_width=True)

# Ubah ke format time series
if len(data_sorted) > 0:
    # Konversi Tahun & Bulan ke Tanggal
    data_sorted['Tanggal'] = pd.to_datetime(dict(year=data_sorted['Tahun'], month=data_sorted['Bulan'], day=1))
    ts = data_sorted.set_index('Tanggal')['Jumlah'].asfreq('MS')  # MS = month start

    # Plot grafik pengunjung
    st.subheader("📈 Grafik Pengunjung Bulanan")
    fig, ax = plt.subplots()
    ts.plot(ax=ax, marker='o', label='Data Historis')

    # Forecast jika data ≥ 50
    if len(ts.dropna()) >= 50:
        st.success("🔮 Forecasting Aktif (Data ≥ 50)")

        # Model ARIMA otomatis
        model = auto_arima(ts, seasonal=True, m=12, suppress_warnings=True)
        n_periods = st.slider("Jumlah Bulan ke Depan untuk Prediksi", 1, 12, 6)
        forecast = model.predict(n_periods=n_periods)
        future_index = pd.date_range(ts.index[-1] + pd.offsets.MonthBegin(), periods=n_periods, freq='MS')
        forecast_series = pd.Series(forecast, index=future_index)

        # Gabungkan dan plot
        forecast_series.plot(ax=ax, style='--', color='orange', label='Forecast')
        ax.fill_between(forecast_series.index, forecast_series * 0.9, forecast_series * 1.1,
                        color='orange', alpha=0.3, label='Bayangan Prediksi')

    ax.set_title("Grafik Pengunjung Wisata Bulanan")
    ax.set_ylabel("Jumlah Pengunjung")
    ax.legend()
    st.pyplot(fig)

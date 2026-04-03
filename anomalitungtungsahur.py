import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("💰 Sistem Manajemen Dana Desa")

# Inisialisasi session state
if "transaksi" not in st.session_state:
    st.session_state.transaksi = []

# Form transaksi
st.header("📝 Input Transaksi Dana Desa")
with st.form("form_transaksi"):
    tipe = st.selectbox("Jenis Transaksi", ["Pemasukan", "Pengeluaran"])
    nama = st.text_input("Nama")
    kategori = st.text_input("Kategori")
    jumlah = st.number_input("Jumlah", min_value=0)
    deskripsi = st.text_area("Deskripsi")
    bulan = st.selectbox("Bulan", list(range(1, 13)))
    tahun = st.selectbox("Tahun", [2024, 2025])
    submit = st.form_submit_button("Simpan")

# Simpan input
if submit:
    st.session_state.transaksi.append({
        "tipe": tipe,
        "nama": nama,
        "kategori": kategori,
        "jumlah": jumlah,
        "deskripsi": deskripsi,
        "bulan": bulan,
        "tahun": tahun,
        "status": "✅ Aman"
    })

# DataFrame transaksi
df = pd.DataFrame(st.session_state.transaksi)

# Deteksi Anomali hanya untuk pengeluaran
def deteksi_anomali(df):
    df = df.copy()
    df.loc[df["tipe"] == "Pengeluaran", "status"] = "✅ Aman"

    df_pengeluaran = df[df["tipe"] == "Pengeluaran"]

    # Aturan global
    df.loc[(df["tipe"] == "Pengeluaran") & (df["jumlah"] < 10_000), "status"] = "🧐 Perlu Diaudit"
    df.loc[(df["tipe"] == "Pengeluaran") & (df["jumlah"] > 10_000_000), "status"] = "⚠️ Warning"

    for kategori in df_pengeluaran["kategori"].unique():
        group = df_pengeluaran[
            (df_pengeluaran["kategori"] == kategori) & 
            (df_pengeluaran["jumlah"] >= 10_000) & 
            (df_pengeluaran["jumlah"] <= 10_000_000)
        ]
        if len(group) < 4:
            continue

        Q1 = group["jumlah"].quantile(0.25)
        Q3 = group["jumlah"].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        idx = group[(group["jumlah"] < lower) | (group["jumlah"] > upper)].index
        df.loc[idx, "status"] = "🧐 Perlu Diaudit"

    return df

df = deteksi_anomali(df)

# Saldo
total_masuk = df[df["tipe"] == "Pemasukan"]["jumlah"].sum()
total_keluar = df[df["tipe"] == "Pengeluaran"]["jumlah"].sum()
saldo = total_masuk - total_keluar

# Tampilkan saldo
st.header("💼 Informasi Dana Desa")
col1, col2, col3 = st.columns(3)
col1.metric("Total Pemasukan", f"Rp {total_masuk:,.0f}")
col2.metric("Total Pengeluaran", f"Rp {total_keluar:,.0f}")
col3.metric("💰 Saldo Saat Ini", f"Rp {saldo:,.0f}")

# Tabel transaksi
st.header("📊 Tabel Transaksi")
st.dataframe(df, use_container_width=True)

# Visualisasi
if not df.empty:
    st.header("📌 Visualisasi Pengeluaran (IQR per Kategori)")
    kategori_pilih = st.selectbox("Pilih Kategori", df[df["tipe"] == "Pengeluaran"]["kategori"].unique())
    data_kat = df[(df["tipe"] == "Pengeluaran") & (df["kategori"] == kategori_pilih)]
    
    if len(data_kat) >= 4:
        Q1 = data_kat["jumlah"].quantile(0.25)
        Q3 = data_kat["jumlah"].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        fig, ax = plt.subplots()
        sns.boxplot(x=data_kat["jumlah"], ax=ax, color="lightgreen")
        ax.axvline(lower, color="red", linestyle="--", label="Batas Bawah")
        ax.axvline(upper, color="orange", linestyle="--", label="Batas Atas")
        ax.set_title(f"IQR - {kategori_pilih}")
        ax.legend()
        st.pyplot(fig)
    else:
        st.info("Data kategori ini belum cukup untuk divisualisasikan.")

# Grafik pemasukan & pengeluaran
if not df.empty:
    st.header("📈 Grafik Bulanan")
    df_group = df.groupby(["tahun", "bulan", "tipe"])["jumlah"].sum().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=df_group, x="bulan", y="jumlah", hue="tipe", ax=ax)
    ax.set_ylabel("Jumlah")
    ax.set_title("Pemasukan vs Pengeluaran per Bulan")
    st.pyplot(fig)

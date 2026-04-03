# 📊 DesaGo - Sistem Manajemen Dana Desa & Prediksi Wisata

## 📌 Deskripsi

DesaGo adalah aplikasi berbasis Streamlit yang digunakan untuk:

* Mengelola transaksi dana desa secara transparan
* Mendeteksi anomali pada pengeluaran dana desa
* Memprediksi jumlah pengunjung wisata desa berdasarkan data historis

Aplikasi ini dirancang untuk kondisi data yang relatif terbatas dan bersifat bulanan.

---

## 💰 Deteksi Anomali Dana Desa

Pendekatan yang digunakan adalah kombinasi rule-based dan metode statistik sederhana (IQR), karena data transaksi cenderung tidak besar dan perlu mudah dijelaskan.

### ⚙️ Mekanisme Deteksi

#### 1. Rule Global (Hard Threshold)

* Pengeluaran < 10.000 → 🧐 Perlu Diaudit
* Pengeluaran > 10.000.000 → ⚠️ Warning

#### 2. Deteksi Anomali per Kategori (IQR Method)

Menggunakan:

* Q1 (25th percentile)
* Q3 (75th percentile)
* IQR = Q3 - Q1

Batas:

* Lower Bound = Q1 - 1.5 × IQR
* Upper Bound = Q3 + 1.5 × IQR

Data di luar batas akan ditandai sebagai:

* 🧐 Perlu Diaudit

#### 3. Minimum Data Constraint

Deteksi IQR hanya dilakukan jika jumlah data ≥ 4 per kategori.

### 🎯 Output Status

* ✅ Aman
* 🧐 Perlu Diaudit
* ⚠️ Warning

---

## 🎢 Prediksi Pengunjung Wisata

### 📌 Alasan Menggunakan ARIMA

Model yang digunakan adalah ARIMA (Auto ARIMA) karena:

* Data berbentuk time series bulanan
* Jumlah data terbatas (sekitar 50 data)
* Cocok untuk data kecil dan pola musiman

### ⚙️ Implementasi

* Data input:

  * Bulan
  * Tahun
  * Jumlah pengunjung

* Data diubah menjadi time series dengan frekuensi bulanan (Month Start / MS)

### 🚀 Aktivasi Forecast

Forecast hanya dilakukan jika:

```
Jumlah data ≥ 50
```

Jika kurang dari itu, model dianggap belum cukup untuk menangkap pola.

### 🔮 Proses Forecasting

* Menggunakan `auto_arima`
* Seasonal = True (m = 12)
* Prediksi 1–12 bulan ke depan

### 📊 Output

* Grafik data historis
* Garis prediksi (forecast)
* Area bayangan ±10% sebagai indikasi ketidakpastian

---

## 🧠 Insight Desain

* Mengutamakan interpretasi dibanding kompleksitas
* Cocok untuk skenario data kecil
* Fokus pada transparansi dan kemudahan penggunaan

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Pandas
* Matplotlib
* Seaborn
* pmdarima

---

## ⚠️ Limitasi

* Belum menggunakan metode anomaly detection berbasis machine learning
* Sensitif terhadap data yang tidak stabil
* Belum menangani missing value secara kompleks
* Data belum disimpan ke database (masih session state)

---

## 🚀 Future Improvement

* Integrasi database
* Anomaly detection berbasis machine learning
* Dashboard interaktif yang lebih advanced
* Integrasi API

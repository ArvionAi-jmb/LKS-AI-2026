<div align="center">
  <img src="logo.jpg" alt="Sistem Prediksi Stunting" width="120" style="border-radius: 20px;"/>
  <h1 align="center">Sistem Monitoring & Prediksi Stunting</h1>
  <p align="center">
    Platform berbasis <strong>Artificial Intelligence</strong> untuk deteksi dini,
    pemantauan tren, dan analisis spasial kasus stunting pada anak di Indonesia.
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python" alt="Python">
    <img src="https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B?style=flat-square&logo=streamlit" alt="Streamlit">
    <img src="https://img.shields.io/badge/XGBoost-2.0%2B-FF6600?style=flat-square&logo=xgboost" alt="XGBoost">
    <img src="https://img.shields.io/badge/SHAP-Explainable%20AI-5C5CFF?style=flat-square" alt="SHAP">
    <img src="https://img.shields.io/badge/Plotly-Interactive-3B4BA0?style=flat-square&logo=plotly" alt="Plotly">
    <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
  </p>
</div>

---

## 📋 Daftar Isi

- [Tentang](#-tentang)
- [Fitur Utama](#-fitur-utama)
- [Tech Stack](#-tech-stack)
- [Screenshot](#-screenshot)
- [Cara Menjalankan](#-cara-menjalankan)
- [Struktur Proyek](#-struktur-proyek)
- [Cara Kerja Sistem](#-cara-kerja-sistem)
- [Fitur Explainable AI (SHAP)](#-fitur-explainable-ai-shap)
- [Dataset](#-dataset)
- [Deploy](#-deploy)
- [Lisensi](#-lisensi)

---

## 🎯 Tentang

**Stunting** adalah kondisi gagal tumbuh pada anak balita akibat kekurangan gizi kronis,
terutama pada periode **1.000 Hari Pertama Kehidupan (HPK)**. Indonesia masih menghadapi
tantangan serius dalam penurunan prevalensi stunting.

Aplikasi ini menggunakan **algoritma XGBoost** yang telah dilatih pada dataset sintetis
untuk memprediksi risiko stunting berdasarkan **25+ fitur** — mencakup antropometri,
riwayat kesehatan, kondisi sosial-ekonomi, dan faktor lingkungan.

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| **🔮 Prediksi Stunting** | Input data anak → prediksi risiko stunting dengan probabilitas |
| **📊 Dashboard Monitoring** | Tren temporal, prevalensi per provinsi, analisis faktor risiko |
| **🗺️ Peta GIS Interaktif** | Sebaran kasus stunting per Kabupaten/Kota + heatmap |
| **🧠 Explainable AI (SHAP)** | Analisis kontribusi setiap faktor terhadap hasil prediksi individu |
| **📱 Responsif** | Antarmuka modern dengan tema kustom dan navigasi sidebar |

---

## 🛠 Tech Stack

| Teknologi | Kegunaan |
|-----------|----------|
| [Streamlit](https://streamlit.io) | Web framework Python untuk dashboard interaktif |
| [XGBoost](https://xgboost.readthedocs.io) | Algoritma gradient boosting untuk klasifikasi |
| [SHAP](https://shap.readthedocs.io) | Explainable AI — interpretasi prediksi model |
| [scikit-learn](https://scikit-learn.org) | OneHotEncoder & pipeline preprocessing |
| [Plotly](https://plotly.com/python/) | Visualisasi interaktif (chart, map, gauge) |
| [Pandas](https://pandas.pydata.org) | Manipulasi & agregasi data |
| [NumPy](https://numpy.org) | Komputasi numerik |

---

## 🌐 Demo Langsung

Kunjungi aplikasi yang sudah di-deploy di **[lks.arvionai.web.id](https://lks.arvionai.web.id)**.

---

## 🚀 Cara Menjalankan

### Prasyarat

- Python **3.10+**
- pip (package manager)

### Instalasi

```bash
# 1. Clone repository
git clone https://github.com/username/sistem_prediksi_stunting.git
cd sistem_prediksi_stunting

# 2. (Opsional) Buat virtual environment
python -m venv venv

# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 3. Install dependensi
pip install -r requirements.txt
```

### Menjalankan Aplikasi

```bash
streamlit run app.py
```

Buka browser di **http://localhost:8501**.

---

## 📁 Struktur Proyek

```
├── app.py                          # Halaman Beranda — ringkasan & statistik
├── logo.jpg                        # Logo aplikasi
├── requirements.txt                # Dependensi Python
│
├── pages/
│   ├── 1_Prediksi_Stunting.py      # Form input + prediksi + SHAP analysis
│   ├── 2_Dashboard_Monitoring.py   # Dashboard tren & faktor risiko
│   └── 3_Peta_GIS.py               # Peta interaktif sebaran stunting
│
├── utils/
│   ├── core.py                     # Load data/model, preprocessing, SHAP, geohierarchy
│   └── ui.py                       # CSS kustom, branding (ArvionAi)
│
├── model/
│   └── model_stunting.pkl          # Model XGBoost terlatih
│
├── data/
│   └── dataset_stunting_sintetis.csv  # Dataset sintetis (simulasi)
│
└── .streamlit/
    └── config.toml                 # Tema Streamlit
```

---

## 🧠 Cara Kerja Sistem

### Alur Prediksi

```
Input Data Anak (25+ fitur)
        │
        ▼
  Preprocessing Pipeline
  ├── OneHotEncoder → 12 kolom kategorikal
  └── Passthrough   → 13 kolom numerik
        │
        ▼
  XGBoost Classifier
  ├── predict()      → Status (0 = Normal / 1 = Stunting)
  └── predict_proba()→ Probabilitas risiko (%)
        │
        ▼
  SHAP TreeExplainer
  └── Kontribusi per fitur → Naratif Bahasa Indonesia
```

### Fitur Model

**12 Kategorikal** (one-hot encoded):
`Jenis_Kelamin`, `Provinsi`, `Kabupaten_Kota`, `Kecamatan`, `Desa_Kelurahan`,
`Tempat_Pemeriksaan`, `Status_Imunisasi`, `Kebiasaan_Cuci_Tangan`,
`Pendidikan_Ibu`, `Pendidikan_Ayah`, `Pekerjaan_Ibu`, `Pekerjaan_Ayah`

**13 Numerik** (passthrough):
`Tahun`, `Bulan`, `Usia_Bulan`, `Latitude`, `Longitude`, `Berat_Badan_kg`,
`Tinggi_Badan_cm`, `Lingkar_Kepala_cm`, `LiLA_cm`, `BB_Lahir_gram`,
`PB_Lahir_cm`, `Usia_Kehamilan_Minggu`, `Prematur`, `ASI_Eksklusif`,
`Usia_MPASI_Bulan`, `Protein_Hewani_per_Minggu`, `Skor_Keragaman_Pangan`,
`Riwayat_Diare`, `Riwayat_ISPA`, `Riwayat_TBC`, `Air_Bersih`, `Jamban_Sehat`,
`Tinggi_Ibu_cm`, `Tinggi_Ayah_cm`, `Pendapatan_Keluarga`

---

## 🔬 Fitur Explainable AI (SHAP

Setiap prediksi dilengkapi analisis kontribusi faktor menggunakan **SHAP
(Shapley Additive Explanations)** — metode dari game theory yang secara adil
mendistribusikan kontribusi setiap fitur terhadap hasil prediksi.

### Output Analisis

1. **Bar Chart Vertikal** — 10 faktor dengan kontribusi terbesar
   - 🟢 Hijau = menurunkan risiko stunting
   - 🔴 Merah = meningkatkan risiko stunting

2. **Ringkasan Naratif** — faktor risiko & faktor protektif utama dalam
   Bahasa Indonesia yang mudah dipahami.

### Contoh Interpretasi

| Faktor | Kontribusi | Arti |
|--------|-----------|------|
| TB anak 85 cm vs standar usia | +0.32 | Meningkatkan risiko (tinggi di bawah standar) |
| ASI Eksklusif 6 bulan | -0.18 | Menurunkan risiko |
| Pendapatan Rp 1,5 jt/bln | +0.12 | Meningkatkan risiko |

---

## 📊 Dataset

Dataset yang digunakan bersifat **sintetis** (`dataset_stunting_sintetis.csv`),
dibuat untuk keperluan simulasi dan pengembangan model.

| Atribut | Detail |
|---------|--------|
| Jumlah sampel | ~10.000 baris |
| Fitur | 25+ (kategorikal + numerik) |
| Target | `Status_Stunting` (0 = Normal, 1 = Stunting) |
| Akurasi model | ~98% (pada dataset sintetis) |

> ⚠️ **Catatan:** Koordinat lokasi (Latitude/Longitude) tidak mencerminkan
> posisi geografis riil secara presisi. Untuk produksi nyata, gunakan data
> riil seperti e-PPGBM / SSGI Kemenkes beserta koordinat wilayah administratif
> yang valid.

---

## 🌐 Deploy ke Streamlit Cloud

```bash
# 1. Push ke GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/sistem_prediksi_stunting.git
git push -u origin main

# 2. Buka https://share.streamlit.io
# 3. Hubungkan repository GitHub
# 4. Set entry point: app.py
# 5. Pastikan requirements.txt terunggah
```

Atau deploy manual dengan Docker:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License** — silakan gunakan, modifikasi,
dan distribusikan sesuai kebutuhan.

---

<div align="center">
  <sub>Dibuat untuk keperluan Lomba Kompetensi Siswa (LKS) — Bidang <strong>Artificial Intelligence</strong></sub>
  <br>
  <sub>© 2026 ArvionAi</sub>
</div>

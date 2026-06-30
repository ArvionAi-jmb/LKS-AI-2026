"""
Modul inti: pemuatan data & model, preprocessing manual (mereplikasi
ColumnTransformer asli: OneHotEncoder untuk kolom kategorikal + passthrough
untuk kolom numerik), prediksi, dan explainability berbasis SHAP.
"""

import pickle
import warnings

# Fix Python 3.10 + joblib atexit conflict
import threading
import concurrent.futures.process
try:
    threading._register_atexit(concurrent.futures.process._python_exit)
except (RuntimeError, AttributeError):
    pass

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.preprocessing import OneHotEncoder

warnings.filterwarnings("ignore")

import os
_BASE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(_BASE, "..", "data", "dataset_stunting_sintetis.csv")
MODEL_PATH = os.path.join(_BASE, "..", "model", "model_stunting.pkl")

# Urutan kolom HARUS sama dengan urutan saat model dilatih.
CAT_COLS = [
    "Jenis_Kelamin", "Provinsi", "Kabupaten_Kota", "Kecamatan", "Desa_Kelurahan",
    "Tempat_Pemeriksaan", "Status_Imunisasi", "Kebiasaan_Cuci_Tangan",
    "Pendidikan_Ibu", "Pendidikan_Ayah", "Pekerjaan_Ibu", "Pekerjaan_Ayah",
]

NUM_COLS = [
    "Tahun", "Bulan", "Usia_Bulan", "Latitude", "Longitude", "Berat_Badan_kg",
    "Tinggi_Badan_cm", "Lingkar_Kepala_cm", "LiLA_cm", "BB_Lahir_gram",
    "PB_Lahir_cm", "Usia_Kehamilan_Minggu", "Prematur", "ASI_Eksklusif",
    "Usia_MPASI_Bulan", "Protein_Hewani_per_Minggu", "Skor_Keragaman_Pangan",
    "Riwayat_Diare", "Riwayat_ISPA", "Riwayat_TBC", "Air_Bersih", "Jamban_Sehat",
    "Tinggi_Ibu_cm", "Tinggi_Ayah_cm", "Pendapatan_Keluarga",
]

BINARY_COLS = ["Prematur", "ASI_Eksklusif", "Riwayat_Diare", "Riwayat_ISPA",
               "Riwayat_TBC", "Air_Bersih", "Jamban_Sehat"]

FEATURE_LABELS = {
    "Jenis_Kelamin": "Jenis Kelamin", "Provinsi": "Provinsi",
    "Kabupaten_Kota": "Kabupaten/Kota", "Kecamatan": "Kecamatan",
    "Desa_Kelurahan": "Desa/Kelurahan", "Tempat_Pemeriksaan": "Tempat Pemeriksaan",
    "Status_Imunisasi": "Status Imunisasi", "Kebiasaan_Cuci_Tangan": "Kebiasaan Cuci Tangan",
    "Pendidikan_Ibu": "Pendidikan Ibu", "Pendidikan_Ayah": "Pendidikan Ayah",
    "Pekerjaan_Ibu": "Pekerjaan Ibu", "Pekerjaan_Ayah": "Pekerjaan Ayah",
    "Tahun": "Tahun Pemeriksaan", "Bulan": "Bulan Pemeriksaan",
    "Usia_Bulan": "Usia Anak (bulan)", "Latitude": "Latitude Lokasi",
    "Longitude": "Longitude Lokasi", "Berat_Badan_kg": "Berat Badan (kg)",
    "Tinggi_Badan_cm": "Tinggi Badan (cm)", "Lingkar_Kepala_cm": "Lingkar Kepala (cm)",
    "LiLA_cm": "Lingkar Lengan Atas / LiLA (cm)", "BB_Lahir_gram": "Berat Badan Lahir (gram)",
    "PB_Lahir_cm": "Panjang Badan Lahir (cm)", "Usia_Kehamilan_Minggu": "Usia Kehamilan saat Lahir (minggu)",
    "Prematur": "Riwayat Kelahiran Prematur", "ASI_Eksklusif": "Pemberian ASI Eksklusif",
    "Usia_MPASI_Bulan": "Usia Mulai MPASI (bulan)",
    "Protein_Hewani_per_Minggu": "Frekuensi Protein Hewani / Minggu",
    "Skor_Keragaman_Pangan": "Skor Keragaman Pangan",
    "Riwayat_Diare": "Riwayat Diare", "Riwayat_ISPA": "Riwayat ISPA",
    "Riwayat_TBC": "Riwayat TBC", "Air_Bersih": "Akses Air Bersih",
    "Jamban_Sehat": "Akses Jamban Sehat", "Tinggi_Ibu_cm": "Tinggi Badan Ibu (cm)",
    "Tinggi_Ayah_cm": "Tinggi Badan Ayah (cm)",
    "Pendapatan_Keluarga": "Pendapatan Keluarga (Rp/bulan)",
}


@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Tanggal_Pemeriksaan"] = pd.to_datetime(df["Tanggal_Pemeriksaan"], errors="coerce")
    return df


@st.cache_resource(show_spinner=False)
def load_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model


@st.cache_resource(show_spinner=False)
def get_encoder(_df):
    """Fit OneHotEncoder pada kategori yang ada di dataset training agar
    konsisten dengan kolom yang diharapkan model."""
    enc = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    enc.fit(_df[CAT_COLS])
    return enc


@st.cache_data(show_spinner=False)
def get_geo_hierarchy(_df):
    """Bangun struktur Provinsi -> Kabupaten/Kota -> Kecamatan -> Desa, plus
    titik koordinat rata-rata per Kabupaten/Kota untuk peta."""
    hierarchy = {}
    for prov, g in _df.groupby("Provinsi"):
        kabs = {}
        for kab, g2 in g.groupby("Kabupaten_Kota"):
            kabs[kab] = {
                "kecamatan": sorted(g2["Kecamatan"].unique().tolist()),
                "desa": sorted(g2["Desa_Kelurahan"].unique().tolist()),
                "lat": float(g2["Latitude"].mean()),
                "lon": float(g2["Longitude"].mean()),
            }
        hierarchy[prov] = kabs
    return hierarchy


def encode_input(raw_row: dict, model, encoder) -> pd.DataFrame:
    """Mengubah satu baris input mentah (dict) menjadi DataFrame terenkode
    sesuai urutan & nama kolom yang diharapkan model."""
    expected_cols = model.get_booster().feature_names

    cat_df = pd.DataFrame([{c: raw_row[c] for c in CAT_COLS}])
    cat_encoded = encoder.transform(cat_df)
    cat_names = ["cat__" + n for n in encoder.get_feature_names_out(CAT_COLS)]
    cat_part = pd.DataFrame(cat_encoded, columns=cat_names)

    num_part = pd.DataFrame([{("remainder__" + c): raw_row[c] for c in NUM_COLS}])

    X = pd.concat([cat_part, num_part], axis=1)
    X = X[expected_cols]
    return X


def predict_one(raw_row: dict, model, encoder):
    X = encode_input(raw_row, model, encoder)
    proba = model.predict_proba(X)[0]
    pred = int(model.predict(X)[0])
    return pred, proba, X


@st.cache_resource(show_spinner=False)
def get_shap_explainer(_model):
    import shap
    return shap.TreeExplainer(_model)


def explain_one(_model, X_row: pd.DataFrame):
    """Hitung SHAP values untuk satu baris prediksi, lalu kembalikan
    DataFrame ringkasan kontribusi per fitur mentah (human-readable)."""
    explainer = get_shap_explainer(_model)
    shap_values = explainer.shap_values(X_row)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
    sv = np.array(shap_values)[0]
    base_value = explainer.expected_value
    if isinstance(base_value, (list, np.ndarray)):
        base_value = base_value[-1] if np.ndim(base_value) > 0 else base_value

    rows = []
    cols = X_row.columns.tolist()
    for col, val, shapv in zip(cols, X_row.iloc[0].tolist(), sv):
        if col.startswith("cat__"):
            raw_name = col[len("cat__"):]
            # cari nama kolom kategorikal asal (bisa mengandung underscore di nilainya)
            matched_group, matched_value = None, None
            for c in CAT_COLS:
                prefix = c + "_"
                if raw_name.startswith(prefix):
                    matched_group, matched_value = c, raw_name[len(prefix):]
            if matched_group is None:
                matched_group, matched_value = raw_name, ""
            is_active = val == 1
            label = FEATURE_LABELS.get(matched_group, matched_group)
            display = f"{label}: {matched_value}"
            rows.append({
                "group": matched_group, "label": label, "value_display": matched_value,
                "full_display": display, "is_active": is_active, "shap": float(shapv),
                "raw_value": val,
            })
        else:
            raw_name = col[len("remainder__"):]
            label = FEATURE_LABELS.get(raw_name, raw_name)
            if raw_name in BINARY_COLS:
                value_display = "Ya" if val == 1 else "Tidak"
            else:
                value_display = val
            rows.append({
                "group": raw_name, "label": label, "value_display": value_display,
                "full_display": f"{label}: {value_display}", "is_active": True,
                "shap": float(shapv), "raw_value": val,
            })

    explain_df = pd.DataFrame(rows)
    return explain_df, float(base_value)


@st.cache_data(show_spinner=False)
def get_global_feature_importance(_model):
    """Agregasi feature_importances_ dari XGBoost ke level kolom mentah
    (menggabungkan semua dummy one-hot dari kolom kategorikal yang sama)."""
    importances = _model.feature_importances_
    cols = _model.get_booster().feature_names
    agg = {}
    for col, imp in zip(cols, importances):
        if col.startswith("cat__"):
            raw_name = col[len("cat__"):]
            group = raw_name
            for c in CAT_COLS:
                if raw_name.startswith(c + "_"):
                    group = c
                    break
        else:
            group = col[len("remainder__"):]
        agg[group] = agg.get(group, 0) + imp
    out = pd.DataFrame(
        [{"Faktor": FEATURE_LABELS.get(k, k), "Importance": v} for k, v in agg.items()]
    ).sort_values("Importance", ascending=False).reset_index(drop=True)
    return out

import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.core import (
    load_data, load_model, get_encoder, get_geo_hierarchy,
    predict_one, explain_one, FEATURE_LABELS,
)
from utils.ui import inject_css, section_label, render_sidebar_header

st.set_page_config(page_title="Prediksi Stunting", page_icon="▣", layout="wide", initial_sidebar_state="collapsed")

inject_css()
render_sidebar_header()
df = load_data()
model = load_model()
encoder = get_encoder(df)
geo = get_geo_hierarchy(df)

st.markdown("## Prediksi Risiko Stunting")
st.markdown(
    '<p style="color:#64748b;margin-top:-0.5rem;margin-bottom:1.5rem;">'
    "Masukkan data pemeriksaan anak untuk mendapatkan prediksi status gizi "
    "beserta faktor-faktor yang memengaruhinya.</p>",
    unsafe_allow_html=True,
)

section_label("Lokasi Pemeriksaan")
loc1, loc2, loc3, loc4 = st.columns(4)
with loc1:
    provinsi = st.selectbox("Provinsi", sorted(geo.keys()), key="sel_prov")
with loc2:
    kab_options = sorted(geo[provinsi].keys())
    kabupaten = st.selectbox("Kabupaten/Kota", kab_options, key="sel_kab")
with loc3:
    kec_options = geo[provinsi][kabupaten]["kecamatan"]
    kecamatan = st.selectbox("Kecamatan", kec_options, key="sel_kec")
with loc4:
    desa_options = geo[provinsi][kabupaten]["desa"]
    desa = st.selectbox("Desa/Kelurahan", desa_options, key="sel_desa")

default_lat = geo[provinsi][kabupaten]["lat"]
default_lon = geo[provinsi][kabupaten]["lon"]

st.divider()

with st.form("form_prediksi"):

    section_label("Identitas & Antropometri Anak")
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        jenis_kelamin = st.radio("Jenis Kelamin", ["L", "P"], horizontal=True,
                                  format_func=lambda x: "Laki-laki" if x == "L" else "Perempuan")
        usia_bulan = st.number_input("Usia (bulan)", 0, 59, 24)
    with a2:
        berat_badan = st.number_input("Berat Badan (kg)", 2.0, 25.0, 10.5, step=0.1)
        tinggi_badan = st.number_input("Tinggi Badan (cm)", 40.0, 130.0, 80.0, step=0.1)
    with a3:
        lingkar_kepala = st.number_input("Lingkar Kepala (cm)", 30.0, 55.0, 45.0, step=0.1)
        lila = st.number_input("LiLA (cm)", 8.0, 22.0, 14.0, step=0.1)
    with a4:
        tempat_periksa = st.selectbox("Tempat Pemeriksaan", sorted(df["Tempat_Pemeriksaan"].unique()))
        tgl_periksa = st.date_input("Tanggal Periksa", datetime.date.today())

    section_label("Riwayat Kelahiran & Pemberian Makan")
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        bb_lahir = st.number_input("BB Lahir (gram)", 1000, 5000, 3000, step=50)
        pb_lahir = st.number_input("PB Lahir (cm)", 35, 60, 49)
    with b2:
        usia_kehamilan = st.number_input("Usia Kehamilan (minggu)", 24, 42, 39)
        prematur = st.radio("Lahir Prematur?", ["Tidak", "Ya"], horizontal=True)
    with b3:
        asi_eksklusif = st.radio("ASI Eksklusif (0-6 bln)?", ["Ya", "Tidak"], horizontal=True)
        usia_mpasi = st.number_input("Mulai MPASI (bulan)", 0, 12, 6)
    with b4:
        protein_hewani = st.number_input("Protein Hewani/minggu", 0, 21, 7)
        skor_keragaman = st.slider("Keragaman Pangan (1-9)", 1, 9, 4)

    section_label("Riwayat Kesehatan & Imunisasi")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        riwayat_diare = st.radio("Diare (3 bln terakhir)", ["Tidak", "Ya"], horizontal=True)
    with c2:
        riwayat_ispa = st.radio("ISPA (3 bln terakhir)", ["Tidak", "Ya"], horizontal=True)
    with c3:
        riwayat_tbc = st.radio("Riwayat TBC", ["Tidak", "Ya"], horizontal=True)
    with c4:
        status_imunisasi = st.selectbox("Status Imunisasi", sorted(df["Status_Imunisasi"].unique()))

    section_label("Sanitasi & Lingkungan")
    d1, d2, d3 = st.columns(3)
    with d1:
        air_bersih = st.radio("Akses Air Bersih?", ["Ya", "Tidak"], horizontal=True)
    with d2:
        jamban_sehat = st.radio("Akses Jamban Sehat?", ["Ya", "Tidak"], horizontal=True)
    with d3:
        cuci_tangan = st.selectbox("Kebiasaan Cuci Tangan", sorted(df["Kebiasaan_Cuci_Tangan"].unique()))

    section_label("Data Orang Tua & Sosial-Ekonomi")
    e1, e2, e3, e4 = st.columns(4)
    with e1:
        tinggi_ibu = st.number_input("Tinggi Ibu (cm)", 130, 180, 155)
        pendidikan_ibu = st.selectbox("Pendidikan Ibu", sorted(df["Pendidikan_Ibu"].unique()))
    with e2:
        tinggi_ayah = st.number_input("Tinggi Ayah (cm)", 140, 195, 165)
        pendidikan_ayah = st.selectbox("Pendidikan Ayah", sorted(df["Pendidikan_Ayah"].unique()))
    with e3:
        pekerjaan_ibu = st.selectbox("Pekerjaan Ibu", sorted(df["Pekerjaan_Ibu"].unique()))
        pekerjaan_ayah = st.selectbox("Pekerjaan Ayah", sorted(df["Pekerjaan_Ayah"].unique()))
    with e4:
        pendapatan = st.number_input("Pendapatan Keluarga (Rp/bulan)", 500_000, 30_000_000, 3_000_000, step=100_000)

    submitted = st.form_submit_button("Prediksi Status Stunting", use_container_width=True, type="primary")

if submitted:
    raw_row = {
        "Jenis_Kelamin": jenis_kelamin, "Provinsi": provinsi, "Kabupaten_Kota": kabupaten,
        "Kecamatan": kecamatan, "Desa_Kelurahan": desa, "Tempat_Pemeriksaan": tempat_periksa,
        "Status_Imunisasi": status_imunisasi, "Kebiasaan_Cuci_Tangan": cuci_tangan,
        "Pendidikan_Ibu": pendidikan_ibu, "Pendidikan_Ayah": pendidikan_ayah,
        "Pekerjaan_Ibu": pekerjaan_ibu, "Pekerjaan_Ayah": pekerjaan_ayah,
        "Tahun": tgl_periksa.year, "Bulan": tgl_periksa.month, "Usia_Bulan": usia_bulan,
        "Latitude": default_lat, "Longitude": default_lon, "Berat_Badan_kg": berat_badan,
        "Tinggi_Badan_cm": tinggi_badan, "Lingkar_Kepala_cm": lingkar_kepala, "LiLA_cm": lila,
        "BB_Lahir_gram": bb_lahir, "PB_Lahir_cm": pb_lahir, "Usia_Kehamilan_Minggu": usia_kehamilan,
        "Prematur": 1 if prematur == "Ya" else 0,
        "ASI_Eksklusif": 1 if asi_eksklusif == "Ya" else 0,
        "Usia_MPASI_Bulan": usia_mpasi, "Protein_Hewani_per_Minggu": protein_hewani,
        "Skor_Keragaman_Pangan": skor_keragaman,
        "Riwayat_Diare": 1 if riwayat_diare == "Ya" else 0,
        "Riwayat_ISPA": 1 if riwayat_ispa == "Ya" else 0,
        "Riwayat_TBC": 1 if riwayat_tbc == "Ya" else 0,
        "Air_Bersih": 1 if air_bersih == "Ya" else 0,
        "Jamban_Sehat": 1 if jamban_sehat == "Ya" else 0,
        "Tinggi_Ibu_cm": tinggi_ibu, "Tinggi_Ayah_cm": tinggi_ayah,
        "Pendapatan_Keluarga": pendapatan,
    }

    pred, proba, X_enc = predict_one(raw_row, model, encoder)
    prob_stunting = proba[1] * 100

    st.divider()
    st.markdown("## Hasil Prediksi")

    res_col, gauge_col = st.columns([1, 1.2])
    with res_col:
        if pred == 1:
            st.markdown(
                f'<div class="result-card danger">'
                f'<h3 style="color:#dc2626;">Terindikasi Stunting</h3>'
                f'<p>Probabilitas risiko: <strong>{prob_stunting:.1f}%</strong></p>'
                f'<p style="margin-top:0.75rem;">Disarankan segera berkonsultasi dengan tenaga kesehatan '
                f"atau ahli gizi di Puskesmas/Posyandu terdekat untuk pemeriksaan "
                f"dan intervensi gizi lanjutan.</p>"
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="result-card success">'
                f'<h3 style="color:#059669;">Tidak Terindikasi Stunting</h3>'
                f'<p>Probabilitas risiko stunting: <strong>{prob_stunting:.1f}%</strong></p>'
                f'<p style="margin-top:0.75rem;">Pertahankan pola asuh, gizi, dan sanitasi yang baik '
                f"untuk menjaga tumbuh kembang anak.</p>"
                f'</div>',
                unsafe_allow_html=True,
            )

    with gauge_col:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob_stunting,
            number={"suffix": "%", "font": {"size": 28, "color": "#0f172a"}},
            title={"text": "Probabilitas Risiko", "font": {"size": 14}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94a3b8"},
                "bar": {"color": "#dc2626" if pred == 1 else "#059669", "thickness": 0.6},
                "bgcolor": "#f1f5f9",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 33], "color": "#f0fdf4"},
                    {"range": [33, 66], "color": "#fffbeb"},
                    {"range": [66, 100], "color": "#fef2f2"},
                ],
                "threshold": {
                    "line": {"color": "#dc2626" if pred == 1 else "#059669", "width": 3},
                    "thickness": 0.75,
                    "value": prob_stunting,
                },
            },
        ))
        fig_gauge.update_layout(height=240, margin=dict(t=30, b=0, l=20, r=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("### Faktor yang Memengaruhi Prediksi")
    st.caption(
        "Analisis kontribusi setiap faktor terhadap hasil prediksi risiko stunting anak ini. "
        "Nilai positif (merah) meningkatkan risiko, nilai negatif (hijau) menurunkan risiko."
    )

    with st.spinner("Menghitung kontribusi setiap faktor..."):
        explain_df, base_value = explain_one(model, X_enc)

    shown = explain_df[explain_df["is_active"]].copy()
    shown["arah"] = shown["shap"].apply(lambda x: "Meningkatkan Risiko" if x > 0 else "Menurunkan Risiko")
    shown = shown.reindex(shown["shap"].abs().sort_values(ascending=False).index)
    top_n = shown.head(10).iloc[::-1]

    fig_bar = px.bar(
        top_n, x="shap", y="full_display", orientation="h",
        color="arah",
        color_discrete_map={"Meningkatkan Risiko": "#dc2626", "Menurunkan Risiko": "#059669"},
        labels={"shap": "Kontribusi terhadap Risiko Stunting", "full_display": ""},
    )
    fig_bar.update_layout(
        height=400,
        margin=dict(t=10, b=10, l=10, r=10),
        legend_title_text="",
        xaxis={"gridcolor": "#f1f5f9"},
        yaxis={"gridcolor": "#f1f5f9"},
        plot_bgcolor="#ffffff",
    )
    fig_bar.update_traces(marker_line_width=0)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### Ringkasan Faktor Utama")

    risk_factors = shown[shown["shap"] > 0].head(3)
    protective_factors = shown[shown["shap"] < 0].head(3)

    def narrative(row):
        g, v = row["group"], row["value_display"]
        templates = {
            "Tinggi_Badan_cm": f"Tinggi badan anak ({v} cm) terhadap standar usianya",
            "Berat_Badan_kg": f"Berat badan anak ({v} kg)",
            "LiLA_cm": f"Lingkar lengan atas ({v} cm)",
            "BB_Lahir_gram": f"Berat badan lahir ({v} gram)",
            "PB_Lahir_cm": f"Panjang badan lahir ({v} cm)",
            "Usia_Kehamilan_Minggu": f"Usia kehamilan saat lahir ({v} minggu)",
            "Prematur": "Riwayat kelahiran prematur" if v == "Ya" else "Anak tidak lahir prematur",
            "ASI_Eksklusif": "Tidak mendapat ASI eksklusif" if v == "Tidak" else "Mendapat ASI eksklusif",
            "Usia_MPASI_Bulan": f"Usia mulai MPASI ({v} bulan)",
            "Protein_Hewani_per_Minggu": f"Frekuensi protein hewani ({v}x/minggu)",
            "Skor_Keragaman_Pangan": f"Skor keragaman pangan ({v})",
            "Riwayat_Diare": "Riwayat diare" if v == "Ya" else "Tidak ada riwayat diare",
            "Riwayat_ISPA": "Riwayat ISPA" if v == "Ya" else "Tidak ada riwayat ISPA",
            "Riwayat_TBC": "Riwayat TBC" if v == "Ya" else "Tidak ada riwayat TBC",
            "Air_Bersih": "Tidak memiliki akses air bersih" if v == "Tidak" else "Memiliki akses air bersih",
            "Jamban_Sehat": "Tidak memiliki akses jamban sehat" if v == "Tidak" else "Memiliki akses jamban sehat",
            "Status_Imunisasi": f"Status imunisasi: {v}",
            "Kebiasaan_Cuci_Tangan": f"Kebiasaan cuci tangan: {v}",
            "Tinggi_Ibu_cm": f"Tinggi badan ibu ({v} cm)",
            "Tinggi_Ayah_cm": f"Tinggi badan ayah ({v} cm)",
            "Pendidikan_Ibu": f"Pendidikan ibu: {v}",
            "Pendidikan_Ayah": f"Pendidikan ayah: {v}",
            "Pendapatan_Keluarga": f"Pendapatan keluarga (Rp {int(row['raw_value']):,})".replace(",", "."),
            "Usia_Bulan": f"Usia anak ({v} bulan)",
        }
        return templates.get(g, f"{row['full_display']}")

    if len(risk_factors) > 0:
        st.markdown("**Meningkatkan Risiko**")
        for _, row in risk_factors.iterrows():
            st.markdown(f"- {narrative(row)}")
    if len(protective_factors) > 0:
        st.markdown("**Menurunkan Risiko**")
        for _, row in protective_factors.iterrows():
            st.markdown(f"- {narrative(row)}")

    st.caption(
        "Analisis ini bersifat sebagai pendukung keputusan dan bukan diagnosis medis final. "
        "Diagnosis klinis stunting tetap perlu dikonfirmasi oleh tenaga kesehatan profesional "
        "menggunakan standar antropometri WHO/Kemenkes."
    )

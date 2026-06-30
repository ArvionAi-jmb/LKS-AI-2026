import pandas as pd
import plotly.express as px
import streamlit as st

from utils.core import load_data
from utils.ui import inject_css, render_sidebar_header

st.set_page_config(page_title="Peta Sebaran Stunting", page_icon="▣", layout="wide", initial_sidebar_state="collapsed")

inject_css()
render_sidebar_header()
df = load_data()

st.markdown("## Peta Sebaran Stunting")
st.markdown(
    '<p style="color:#64748b;margin-top:-0.5rem;margin-bottom:1.5rem;">'
    "Peta interaktif persebaran dan intensitas kasus stunting berdasarkan lokasi "
    "Kabupaten/Kota. Ukuran titik menunjukkan jumlah anak terdata, warna menunjukkan "
    "prevalensi stunting.</p>",
    unsafe_allow_html=True,
)

st.caption(
    "Koordinat lokasi pada dataset ini bersifat sintetis dan tidak merepresentasikan "
    "posisi geografis riil secara presisi — digunakan untuk simulasi sistem."
)

with st.sidebar:
    st.markdown("### Filter Peta")
    tahun_sel = st.multiselect("Tahun", sorted(df["Tahun"].unique()), default=sorted(df["Tahun"].unique()))
    prov_sel = st.multiselect("Provinsi", sorted(df["Provinsi"].unique()), default=sorted(df["Provinsi"].unique()))
    mode = st.radio("Mode Tampilan", ["Titik per Kabupaten/Kota", "Peta Kepadatan (Heatmap)"])

f = df[df["Tahun"].isin(tahun_sel) & df["Provinsi"].isin(prov_sel)]
if f.empty:
    st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
    st.stop()

agg = f.groupby(["Provinsi", "Kabupaten_Kota"]).agg(
    Latitude=("Latitude", "mean"), Longitude=("Longitude", "mean"),
    Jumlah_Anak=("Status_Stunting", "size"), Jumlah_Stunting=("Status_Stunting", "sum"),
).reset_index()
agg["Prevalensi (%)"] = (agg["Jumlah_Stunting"] / agg["Jumlah_Anak"] * 100).round(1)

center_lat, center_lon = agg["Latitude"].mean(), agg["Longitude"].mean()

if mode == "Titik per Kabupaten/Kota":
    fig_map = px.scatter_mapbox(
        agg, lat="Latitude", lon="Longitude", size="Jumlah_Anak", color="Prevalensi (%)",
        color_continuous_scale="YlOrRd", size_max=40, zoom=4.2,
        center={"lat": center_lat, "lon": center_lon},
        hover_name="Kabupaten_Kota",
        hover_data={"Provinsi": True, "Jumlah_Anak": True, "Jumlah_Stunting": True, "Prevalensi (%)": True,
                    "Latitude": False, "Longitude": False},
        mapbox_style="carto-positron",
    )
else:
    fig_map = px.density_mapbox(
        f, lat="Latitude", lon="Longitude", z="Status_Stunting", radius=25,
        zoom=4.2, center={"lat": center_lat, "lon": center_lon},
        color_continuous_scale="YlOrRd", mapbox_style="carto-positron",
    )

fig_map.update_layout(height=520, margin=dict(t=10, b=10, l=10, r=10))
st.plotly_chart(fig_map, use_container_width=True)

st.divider()

col1, col2 = st.columns([1.3, 1])
with col1:
    st.markdown("### Rekap per Kabupaten/Kota")
    st.dataframe(
        agg.sort_values("Prevalensi (%)", ascending=False)
           .reset_index(drop=True)[["Provinsi", "Kabupaten_Kota", "Jumlah_Anak", "Jumlah_Stunting", "Prevalensi (%)"]],
        use_container_width=True, height=400,
    )

with col2:
    st.markdown("### 10 Wilayah Tertinggi")
    top10 = agg.sort_values("Prevalensi (%)", ascending=False).head(10).iloc[::-1]
    fig_top = px.bar(top10, x="Prevalensi (%)", y="Kabupaten_Kota", orientation="h",
                      color="Prevalensi (%)", color_continuous_scale="YlOrRd")
    fig_top.update_layout(
        height=400, margin=dict(t=10, b=10), coloraxis_showscale=False,
        plot_bgcolor="#ffffff", xaxis={"gridcolor": "#f1f5f9"},
    )
    fig_top.update_traces(marker_line_width=0)
    st.plotly_chart(fig_top, use_container_width=True)

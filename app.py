import streamlit as st
from utils.core import load_data
from utils.ui import inject_css, section_label, render_sidebar_header

st.set_page_config(
    page_title="Sistem Monitoring & Prediksi Stunting",
    page_icon="▣",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()
render_sidebar_header()
df = load_data()

st.markdown("""
<div class="hero">
    <h1>Sistem Monitoring & Prediksi Stunting</h1>
    <p>Platform berbasis data untuk membantu tenaga kesehatan dan pemangku kebijakan dalam
    deteksi dini, pemantauan tren, dan analisis spasial kasus stunting pada anak di Indonesia.</p>
</div>
""", unsafe_allow_html=True)

total_anak = len(df)
total_stunting = int(df["Status_Stunting"].sum())
persen_stunting = total_stunting / total_anak * 100
jumlah_provinsi = df["Provinsi"].nunique()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Data Anak", f"{total_anak:,}".replace(",", "."))
c2.metric("Terindikasi Stunting", f"{total_stunting:,}".replace(",", "."), help="Jumlah anak dengan status stunting = 1")
c3.metric("Prevalensi Stunting", f"{persen_stunting:.1f}%")
c4.metric("Provinsi Tercakup", jumlah_provinsi)

st.divider()

col1, col2 = st.columns([1.3, 1])
with col1:
    st.markdown("### Tentang Stunting")
    st.markdown(
        "**Stunting** adalah kondisi gagal tumbuh pada anak balita akibat kekurangan gizi kronis, "
        "terutama pada periode 1.000 Hari Pertama Kehidupan (HPK), yang ditandai dengan "
        "tinggi badan anak lebih rendah dibanding standar usianya (WHO Child Growth Standards).\n\n"
        "Stunting bersifat multidimensi — dipengaruhi oleh faktor gizi, kesehatan, "
        "pola asuh, sanitasi, hingga kondisi sosial-ekonomi keluarga. Deteksi dini "
        "berbasis data dapat membantu intervensi dilakukan lebih cepat dan tepat sasaran."
    )
    st.markdown("### Fitur Utama")
    st.markdown("""
    - **Prediksi & Analisis Faktor** — input data anak, sistem memberikan prediksi risiko stunting beserta faktor-faktor yang memengaruhinya.
    - **Dashboard Monitoring** — tren, distribusi, dan faktor risiko stunting secara interaktif.
    - **Visualisasi Spasial** — peta persebaran dan intensitas stunting berdasarkan lokasi.
    """)

with col2:
    st.markdown("### Distribusi Status Gizi")
    import plotly.express as px
    pie_df = df["Status_Stunting"].map({0: "Normal", 1: "Stunting"}).value_counts().reset_index()
    pie_df.columns = ["Status", "Jumlah"]
    fig = px.pie(
        pie_df, names="Status", values="Jumlah", hole=0.55,
        color="Status", color_discrete_map={"Normal": "#059669", "Stunting": "#dc2626"},
    )
    fig.update_traces(textinfo="percent+label", textfont_size=13)
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

st.info(
    "Gunakan menu navigasi di sidebar untuk membuka halaman "
    "**Prediksi Stunting**, **Dashboard Monitoring**, atau **Peta Sebaran**.",
)

st.caption(
    "Dataset yang digunakan bersifat sintetis (dibuat untuk simulasi/pengembangan model) "
    "dan koordinat lokasi tidak merepresentasikan posisi geografis riil secara presisi."
)

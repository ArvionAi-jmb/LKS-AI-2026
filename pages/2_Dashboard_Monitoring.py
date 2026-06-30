import pandas as pd
import plotly.express as px
import streamlit as st

from utils.core import load_data, load_model, get_global_feature_importance
from utils.ui import inject_css, section_label, render_sidebar_header

st.set_page_config(page_title="Dashboard Monitoring", page_icon="▣", layout="wide", initial_sidebar_state="collapsed")

inject_css()
render_sidebar_header()
df = load_data()
model = load_model()

st.markdown("## Dashboard Monitoring Stunting")
st.markdown(
    '<p style="color:#64748b;margin-top:-0.5rem;margin-bottom:1.5rem;">'
    "Pantau tren, distribusi, dan faktor risiko stunting secara interaktif.</p>",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Filter Data")
    tahun_sel = st.multiselect("Tahun", sorted(df["Tahun"].unique()), default=sorted(df["Tahun"].unique()))
    prov_sel = st.multiselect("Provinsi", sorted(df["Provinsi"].unique()), default=sorted(df["Provinsi"].unique()))
    gender_sel = st.multiselect("Jenis Kelamin", ["L", "P"], default=["L", "P"],
                                 format_func=lambda x: "Laki-laki" if x == "L" else "Perempuan")

f = df[df["Tahun"].isin(tahun_sel) & df["Provinsi"].isin(prov_sel) & df["Jenis_Kelamin"].isin(gender_sel)]

if f.empty:
    st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
    st.stop()

total = len(f)
stunting = int(f["Status_Stunting"].sum())
persen = stunting / total * 100 if total else 0
rerata_usia = f["Usia_Bulan"].mean()
rerata_pendapatan = f["Pendapatan_Keluarga"].mean()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Anak", f"{total:,}".replace(",", "."))
k2.metric("Stunting", f"{stunting:,}".replace(",", "."))
k3.metric("Prevalensi", f"{persen:.1f}%")
k4.metric("Rata-rata Usia", f"{rerata_usia:.0f} bln")
k5.metric("Rata-rata Pendapatan", f"Rp {rerata_pendapatan/1_000_000:.1f} jt")

st.divider()

st.markdown("### Tren Prevalensi per Waktu")
trend = f.groupby(["Tahun", "Bulan"]).agg(
    jumlah=("Status_Stunting", "size"), stunting=("Status_Stunting", "sum")
).reset_index()
trend["prevalensi"] = trend["stunting"] / trend["jumlah"] * 100
trend["periode"] = pd.to_datetime(trend["Tahun"].astype(str) + "-" + trend["Bulan"].astype(str) + "-01")
trend = trend.sort_values("periode")

fig_trend = px.line(trend, x="periode", y="prevalensi", markers=True,
                     labels={"periode": "Periode", "prevalensi": "Prevalensi (%)"})
fig_trend.update_traces(line_color="#dc2626", line_width=2.5, marker_size=5)
fig_trend.update_layout(
    height=320, margin=dict(t=10, b=10),
    plot_bgcolor="#ffffff", xaxis={"gridcolor": "#f1f5f9"}, yaxis={"gridcolor": "#f1f5f9"},
)
st.plotly_chart(fig_trend, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Prevalensi per Provinsi")
    prov_stat = f.groupby("Provinsi").agg(
        jumlah=("Status_Stunting", "size"), stunting=("Status_Stunting", "sum")
    ).reset_index()
    prov_stat["prevalensi"] = prov_stat["stunting"] / prov_stat["jumlah"] * 100
    prov_stat = prov_stat.sort_values("prevalensi", ascending=True)
    fig_prov = px.bar(prov_stat, x="prevalensi", y="Provinsi", orientation="h",
                       color="prevalensi", color_continuous_scale="Reds")
    fig_prov.update_layout(
        height=360, margin=dict(t=10, b=10), coloraxis_showscale=False,
        plot_bgcolor="#ffffff", xaxis={"gridcolor": "#f1f5f9"},
    )
    fig_prov.update_traces(marker_line_width=0)
    st.plotly_chart(fig_prov, use_container_width=True)

with col2:
    st.markdown("### Stunting per Jenis Kelamin")
    gender_stat = f.copy()
    gender_stat["Jenis_Kelamin"] = gender_stat["Jenis_Kelamin"].map({"L": "Laki-laki", "P": "Perempuan"})
    gender_stat["Status"] = gender_stat["Status_Stunting"].map({0: "Normal", 1: "Stunting"})
    fig_gender = px.histogram(gender_stat, x="Jenis_Kelamin", color="Status", barmode="group",
                               color_discrete_map={"Normal": "#059669", "Stunting": "#dc2626"})
    fig_gender.update_layout(
        height=360, margin=dict(t=10, b=10), xaxis_title="", yaxis_title="Jumlah Anak",
        plot_bgcolor="#ffffff", xaxis={"gridcolor": "#f1f5f9"}, yaxis={"gridcolor": "#f1f5f9"},
        legend_title_text="",
    )
    st.plotly_chart(fig_gender, use_container_width=True)

st.markdown("### Faktor Sosial, Sanitasi & Kesehatan")
fc1, fc2, fc3 = st.columns(3)

def stacked_rate_chart(data, col, title, order=None):
    tmp = data.copy()
    tmp["Status"] = tmp["Status_Stunting"].map({0: "Normal", 1: "Stunting"})
    rate = tmp.groupby(col)["Status_Stunting"].mean().reset_index()
    rate["Status_Stunting"] *= 100
    if order:
        rate[col] = pd.Categorical(rate[col], categories=order, ordered=True)
        rate = rate.sort_values(col)
    fig = px.bar(rate, x=col, y="Status_Stunting", text_auto=".1f",
                  labels={"Status_Stunting": "Prevalensi (%)", col: ""}, title=title)
    fig.update_traces(marker_color="#0f172a", marker_line_width=0)
    fig.update_layout(
        height=300, margin=dict(t=40, b=10),
        plot_bgcolor="#ffffff", xaxis={"gridcolor": "#f1f5f9"}, yaxis={"gridcolor": "#f1f5f9"},
    )
    return fig

with fc1:
    st.plotly_chart(stacked_rate_chart(f, "Status_Imunisasi", "Status Imunisasi"), use_container_width=True)
with fc2:
    st.plotly_chart(stacked_rate_chart(f, "Air_Bersih", "Akses Air Bersih"), use_container_width=True)
with fc3:
    st.plotly_chart(stacked_rate_chart(f, "Jamban_Sehat", "Akses Jamban Sehat"), use_container_width=True)

fc4, fc5, fc6 = st.columns(3)
with fc4:
    st.plotly_chart(
        stacked_rate_chart(f, "Pendidikan_Ibu", "Pendidikan Ibu",
                            order=["Tidak Sekolah", "SD", "SMP", "SMA", "Diploma", "Sarjana"]),
        use_container_width=True)
with fc5:
    st.plotly_chart(stacked_rate_chart(f, "ASI_Eksklusif", "ASI Eksklusif"), use_container_width=True)
with fc6:
    st.plotly_chart(stacked_rate_chart(f, "Kebiasaan_Cuci_Tangan", "Kebiasaan Cuci Tangan",
                                        order=["Kurang", "Cukup", "Baik"]), use_container_width=True)

st.divider()
st.markdown("### Faktor Paling Berpengaruh")
st.caption("Tingkat kepentingan setiap faktor terhadap prediksi stunting secara global.")
imp_df = get_global_feature_importance(model).head(12).iloc[::-1]
fig_imp = px.bar(imp_df, x="Importance", y="Faktor", orientation="h", color_discrete_sequence=["#0f172a"])
fig_imp.update_layout(
    height=420, margin=dict(t=10, b=10),
    plot_bgcolor="#ffffff", xaxis={"gridcolor": "#f1f5f9"},
)
fig_imp.update_traces(marker_line_width=0)
st.plotly_chart(fig_imp, use_container_width=True)

with st.expander("Lihat Data Mentah"):
    st.dataframe(f, use_container_width=True, height=300)

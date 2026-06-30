import base64
from pathlib import Path

import streamlit as st

_logo_path = Path(__file__).resolve().parent.parent / "logo.jpg"
LOGO_B64 = base64.b64encode(_logo_path.read_bytes()).decode() if _logo_path.exists() else None
LOGO_DATA_URL = f"data:image/jpeg;base64,{LOGO_B64}" if LOGO_B64 else None

CUSTOM_CSS_TEMPLATE = """
<style>
    footer {display: none !important;}
    div[data-testid="stDecoration"] {display: none;}

    header {
        background: #ffffff !important;
        border-bottom: 1px solid #e2e8f0 !important;
        box-shadow: none !important;
    }
    header [data-testid="stStatusWidget"] {display: none !important;}

    /* Brand in top navbar */
    header > div:first-child {
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        padding-left: 12px !important;
    }
    header > div:first-child::before {
        content: '';
        display: inline-flex;
        width: 26px;
        height: 26px;
        background: url('__LOGO_URL__') center/contain no-repeat;
        border-radius: 6px;
        flex-shrink: 0;
    }
    header > div:first-child::after {
        content: 'ArvionAi';
        font-size: 0.85rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.01em;
    }

    .stApp { background-color: #f8fafc; }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    section[data-testid="stSidebar"] > div:first-child { padding-top: 0; }

    /* Logo + brand at top of sidebar nav */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"]::before {
        content: 'ArvionAi';
        display: flex;
        align-items: center;
        padding: 0.6rem 0.75rem 0.6rem 3rem;
        margin: 0 0.5rem 0.75rem 0.5rem;
        background: #f8fafc __LOGO_BG__ 0.75rem center/32px no-repeat;
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.9rem;
        color: #0f172a;
        white-space: nowrap;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul {
        margin-top: 0;
        padding: 0 0.5rem;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li {
        list-style: none;
        margin: 0.1rem 0;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li a {
        border-radius: 8px;
        padding: 0.4rem 0.75rem;
        font-size: 0.85rem;
        color: #475569 !important;
        display: flex;
        align-items: center;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li a:hover {
        background: #f8fafc;
        color: #0f172a !important;
    }

    /* SVG icon base */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li a::before {
        content: "";
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        margin-right: 10px;
        flex-shrink: 0;

        border-radius: 9px;
        background-color: #f1f5f9;
        background-repeat: no-repeat;
        background-position: center;
        background-size: 17px 17px;

        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.8),
            0 2px 6px rgba(15, 23, 42, 0.08);

        transition: all 0.25s ease;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li a:hover::before {
        transform: scale(1.08) rotate(-3deg);
        background-color: #e0f2fe;
        box-shadow:
            0 4px 12px rgba(14, 165, 233, 0.22),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }

    /* 1. App */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li:nth-child(1) a::before {
        background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Crect x='4' y='4' width='16' height='16' rx='4' stroke='%230f172a' stroke-width='2'/%3E%3Cpath d='M8 9H16M8 13H13M8 17H11' stroke='%230ea5e9' stroke-width='2' stroke-linecap='round'/%3E%3Ccircle cx='16.5' cy='16.5' r='1.5' fill='%230ea5e9'/%3E%3C/svg%3E");
    }

    /* 2. Prediksi Stunting */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li:nth-child(2) a::before {
        background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M12 3L14.4 8.6L20.5 9.2L15.9 13.2L17.3 19.2L12 16.1L6.7 19.2L8.1 13.2L3.5 9.2L9.6 8.6L12 3Z' stroke='%237c3aed' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M12 8V12L14.5 14.5' stroke='%230f172a' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
    }

    /* 3. Dashboard Monitoring */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li:nth-child(3) a::before {
        background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Crect x='4' y='5' width='16' height='14' rx='3' stroke='%230f172a' stroke-width='2'/%3E%3Cpath d='M8 15V12' stroke='%2322c55e' stroke-width='2' stroke-linecap='round'/%3E%3Cpath d='M12 15V9' stroke='%2322c55e' stroke-width='2' stroke-linecap='round'/%3E%3Cpath d='M16 15V11' stroke='%2322c55e' stroke-width='2' stroke-linecap='round'/%3E%3Cpath d='M7 19H17' stroke='%230f172a' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
    }

    /* 4. Peta GIS */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li:nth-child(4) a::before {
        background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M9 18L4 20V6L9 4M9 18L15 20M9 18V4M15 20L20 18V4L15 6M15 20V6M15 6L9 4' stroke='%230f172a' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M12 8.5C12 8.5 14.5 10.6 14.5 13C14.5 14.4 13.4 15.5 12 15.5C10.6 15.5 9.5 14.4 9.5 13C9.5 10.6 12 8.5 12 8.5Z' fill='%23f97316'/%3E%3C/svg%3E");
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li a[data-testid*="active"] {
        background: #f8fafc;
        color: #0f172a !important;
        font-weight: 600;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li a[data-testid*="active"]::before {
        background-color: #e0f2fe;
        box-shadow:
            0 4px 12px rgba(14, 165, 233, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 0.8rem; font-weight: 500; color: #475569;
    }

    .card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    div[data-testid="stMetric"] label {
        color: #64748b !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
    }

    .stButton button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.15s ease !important;
    }
    .stButton button[kind="primary"] {
        background: #0f172a !important;
        color: #ffffff !important;
        border: none !important;
    }
    .stButton button[kind="primary"]:hover {
        background: #1e293b !important;
        box-shadow: 0 4px 12px rgba(15,23,42,0.15) !important;
    }
    .stButton button[kind="secondary"] {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #e2e8f0 !important;
    }
    .stButton button[kind="secondary"]:hover {
        border-color: #94a3b8 !important;
        background: #f8fafc !important;
    }

    div[data-testid="stForm"] {
        border: none !important; padding: 0 !important; background: transparent !important;
    }
    div[data-testid="stForm"] > div:first-child {
        border: none !important; padding: 0 !important; background: transparent !important;
    }
    .stTextInput input, .stNumberInput input, .stSelectbox > div, .stDateInput input {
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox > div:focus-within, .stDateInput input:focus {
        border-color: #0f172a !important;
        box-shadow: 0 0 0 2px rgba(15,23,42,0.08) !important;
    }

    div[data-testid="stRadio"] > div { gap: 0.25rem; }
    div[data-testid="stRadio"] label {
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 0.35rem 1rem;
        font-size: 0.85rem;
        transition: all 0.15s ease;
    }
    div[data-testid="stRadio"] label:hover { border-color: #94a3b8; }
    div[data-testid="stRadio"] label[data-selected="true"] {
        background: #0f172a; color: #ffffff; border-color: #0f172a;
    }
    div[data-testid="stRadio"] label[data-selected="true"]:hover {
        background: #1e293b; border-color: #1e293b;
    }

    hr { margin: 1.5rem 0 !important; border-color: #e2e8f0 !important; opacity: 0.6; }

    h1, h2, h3 { font-weight: 600 !important; color: #0f172a !important; letter-spacing: -0.01em; }
    h1 { font-size: 1.4rem !important; }
    h2 { font-size: 1.1rem !important; }

    .stCaption, .stCaption p { color: #64748b !important; font-size: 0.85rem !important; }

    .section-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.75rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid #e2e8f0;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px !important;
        border-left: 4px solid !important;
    }
    div[data-testid="stAlert"] > div:first-child { padding: 0.75rem 1rem !important; }

    .hero {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .hero h1 {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        margin-bottom: 0.35rem;
    }
    .hero p {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 0.25rem;
        line-height: 1.6;
    }

    .result-card {
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
    }
    .result-card.danger {
        background: #fef2f2;
        border: 1px solid #fecaca;
    }
    .result-card.success {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
    }
    .result-card h3 { margin-bottom: 0.25rem; }
    .result-card p {
        font-size: 0.9rem;
        color: #475569;
        margin-top: 0.25rem;
    }
</style>
"""


def inject_css():
    logo_bg = f"url('{LOGO_DATA_URL}')" if LOGO_DATA_URL else "none"
    css = CUSTOM_CSS_TEMPLATE.replace("__LOGO_URL__", LOGO_DATA_URL or "").replace("__LOGO_BG__", logo_bg)
    st.markdown(css, unsafe_allow_html=True)


def section_label(text):
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def render_sidebar_header():
    pass

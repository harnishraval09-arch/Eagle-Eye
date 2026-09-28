"""Visual system for the Eagle Eye Streamlit app."""

import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&display=swap');
        :root { --navy:#0b1828; --ink:#142338; --muted:#6b7a8d; --line:#dbe3ea; --panel:#ffffff; --wash:#f4f7f9; --teal:#087f83; --gold:#c88b2e; --red:#c44949; }
        .stApp { background:var(--wash); color:var(--ink); font-family:'DM Sans',sans-serif; }
        [data-testid='stHeader'] { background:transparent; }
        [data-testid='stSidebar'] { background:var(--navy); border-right:0; }
        [data-testid='stSidebar'] * { color:#dce6ef !important; }
        [data-testid='stSidebar'] .stRadio label { padding:9px 8px; border-radius:6px; }
        [data-testid='stSidebar'] .stRadio label:hover { background:#172b43; }
        .brand { padding:14px 8px 22px; border-bottom:1px solid #24384d; margin-bottom:20px; }
        .brand-mark { display:inline-flex; width:30px; height:30px; border:1px solid #9cc8c6; border-radius:50%; align-items:center; justify-content:center; color:#b8e7e3; font-weight:700; margin-right:9px; }
        .brand-name { font-weight:700; letter-spacing:.08em; color:white; }
        .brand-sub { color:#93a9bd; font-size:11px; margin-top:7px; letter-spacing:.08em; text-transform:uppercase; }
        .topline { display:flex; justify-content:space-between; align-items:center; padding:2px 0 24px; }
        .eyebrow { color:var(--teal); font-family:'DM Mono'; text-transform:uppercase; letter-spacing:.12em; font-size:11px; font-weight:500; }
        h1,h2,h3 { color:var(--ink); letter-spacing:-.025em; }
        h1 { font-size:30px; margin:4px 0 2px; } h2 { font-size:19px; margin:0; } h3 { font-size:14px; }
        .muted { color:var(--muted); font-size:13px; }
        .panel { background:var(--panel); border:1px solid var(--line); border-radius:9px; padding:20px; box-shadow:0 1px 2px rgba(19,42,64,.03); }
        .panel-title { display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; }
        .badge { display:inline-flex; align-items:center; gap:5px; border-radius:999px; padding:5px 9px; font-size:11px; font-weight:600; letter-spacing:.04em; }
        .badge-teal { color:#086b6e; background:#e3f4f2; } .badge-gold { color:#8c5c13; background:#fff2d8; } .badge-red { color:#9b3636; background:#fde7e7; } .badge-gray { color:#526375; background:#edf1f4; }
        .metric { padding:12px 14px; border-left:3px solid var(--teal); background:#f7fbfb; border-radius:4px; }
        .metric-value { font-size:25px; font-weight:700; color:var(--ink); } .metric-label { color:var(--muted); font-size:11px; text-transform:uppercase; letter-spacing:.08em; }
        .step { position:relative; display:grid; grid-template-columns:28px 1fr auto; gap:12px; align-items:center; padding:11px 0; border-bottom:1px solid #edf1f4; }
        .step:last-child { border-bottom:0; } .step-dot { width:24px; height:24px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; background:var(--teal); font:11px 'DM Mono'; }
        .step-dot.self { background:#6a7890; } .step-dot.mcp { background:var(--gold); } .step-dot.report { background:#283e59; }
        .step-name { font-weight:600; font-size:13px; } .step-detail { color:var(--muted); font-size:12px; margin-top:3px; }
        .flag-row { display:grid; grid-template-columns:1.3fr .6fr 2fr; gap:12px; padding:12px 0; border-bottom:1px solid #edf1f4; align-items:center; font-size:13px; }
        .flag-row:last-child { border-bottom:0; } .flag-detail { color:var(--muted); font-size:12px; }
        .section-space { margin-top:18px; }
        .note { background:#fff8e9; border:1px solid #f1ddb1; border-radius:7px; padding:12px 14px; color:#6c4c16; font-size:12px; }
        .mono { font-family:'DM Mono',monospace; font-size:12px; }
        .footer-note { color:#8090a0; font-size:11px; padding-top:16px; border-top:1px solid var(--line); margin-top:22px; }
        div[data-testid='stFileUploader'] section { border:1px dashed #9eb1bf; background:#fbfcfd; }
        .stButton > button { border-radius:6px; font-weight:600; }
        </style>
        """, unsafe_allow_html=True,
    )

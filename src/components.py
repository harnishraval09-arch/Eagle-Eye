"""Reusable Streamlit presentation components."""

import streamlit as st


def badge(text, tone="gray"):
    return f'<span class="badge badge-{tone}">{text}</span>'


def panel(title, body, right=""):
    st.markdown(f'<div class="panel"><div class="panel-title"><h2>{title}</h2>{right}</div>{body}</div>', unsafe_allow_html=True)


def metric_row(metrics):
    cols = st.columns(len(metrics))
    for col, (value, label) in zip(cols, metrics):
        with col:
            st.markdown(f'<div class="metric"><div class="metric-value">{value}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)


def render_pipeline(steps, active=6):
    rows = []
    for i, step in enumerate(steps):
        state = "Complete" if i < active else "Ready"
        rows.append(f'<div class="step"><div class="step-dot {step["kind"]}">{i+1}</div><div><div class="step-name">{step["label"]}</div><div class="step-detail">{step["detail"]}</div></div>{badge(state, "teal" if i < active else "gray")}</div>')
    st.markdown("".join(rows), unsafe_allow_html=True)

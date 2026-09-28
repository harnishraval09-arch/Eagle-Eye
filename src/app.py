"""Eagle Eye — AI-assisted forensic document examination workspace."""

import streamlit as st

from ui.components import badge, metric_row, panel, render_pipeline
from ui.mcp_client import classify_anomaly, fetch_case_precedents, generate_expert_report, map_to_standards, run_engine, score_forgery_confidence
from ui.mock_data import demo_case, default_observations
from ui.report_export import build_report
from ui.theme import inject_css


st.set_page_config(page_title="Eagle Eye · Forensic Workspace", page_icon="◉", layout="wide", initial_sidebar_state="expanded")
inject_css()


def init_state():
    if "case" not in st.session_state:
        st.session_state.case = demo_case()
    if "page" not in st.session_state:
        st.session_state.page = "Case workspace"


def sidebar():
    with st.sidebar:
        st.markdown('<div class="brand"><span class="brand-mark">◉</span><span class="brand-name">EAGLE EYE</span><div class="brand-sub">Forensic document intelligence</div></div>', unsafe_allow_html=True)
        choice = st.radio("Workspace", ["Case workspace", "Bob orchestration", "Findings & standards", "Report review"], label_visibility="collapsed", index=["Case workspace", "Bob orchestration", "Findings & standards", "Report review"].index(st.session_state.page))
        st.session_state.page = choice
        st.markdown('<div style="height:28px"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="muted">ACTIVE CASE</div><div style="color:white;font-weight:600;margin-top:5px">{st.session_state.case["observations"]["case_number"]}</div><div class="muted" style="margin-top:4px">COVID Certificate · {st.session_state.case["observations"]["examiner"]}</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="note" style="background:#13283e;border-color:#27445e;color:#c7d9e6">Decision support only.<br><br>Final interpretation, signature and admissibility decisions remain with the examiner.</div>', unsafe_allow_html=True)


def header(kicker, title, subtitle):
    st.markdown(f'<div class="topline"><div><div class="eyebrow">{kicker}</div><h1>{title}</h1><div class="muted">{subtitle}</div></div><div>{badge("BOB ONLINE", "teal")} &nbsp; {badge("MOCK DATA", "gold")}</div></div>', unsafe_allow_html=True)


def workspace():
    case = st.session_state.case
    header("Case workspace / Intake", "Examination console", "A controlled workspace for document observations, automated checks and examiner review.")
    left, right = st.columns([1.05, 1.45], gap="large")
    with left:
        with st.container(border=True):
            st.markdown('<div class="panel-title"><h2>Questioned item</h2><span class="badge badge-gray">STEP 01 · INTAKE</span></div>', unsafe_allow_html=True)
            uploaded = st.file_uploader("Upload case file", type=["pdf", "png", "jpg", "jpeg", "tif", "tiff"], help="Mock mode accepts any file; the engine response remains deterministic.")
            if uploaded:
                st.session_state.case["observations"]["filename"] = uploaded.name
                st.success(f"Queued: {uploaded.name}")
            st.markdown('<div class="muted" style="margin:12px 0 7px">Evidence handling</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mono">SHA-256 · {case["engine"]["hash"]}</div><div class="muted" style="margin-top:5px">{case["observations"]["chain_of_custody"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
        with st.form("observations"):
            st.markdown('<div class="panel-title"><h2>Structured observations</h2><span class="badge badge-teal">EXAMINER INPUT</span></div>', unsafe_allow_html=True)
            obs = case["observations"]
            obs["document_type"] = st.text_input("Document type", obs["document_type"])
            obs["issuing_body"] = st.text_input("Issuing body", obs["issuing_body"])
            obs["case_number"] = st.text_input("Case number", obs["case_number"])
            obs["examiner"] = st.text_input("Examiner", obs["examiner"])
            obs["observations"] = st.text_area("Observations", obs["observations"], height=90)
            if st.form_submit_button("Save observations", use_container_width=True):
                st.success("Observations saved to active case.")
    with right:
        panel("Automated forensic checks", f'<div class="muted" style="margin-bottom:8px">Python engine output · {case["engine"]["processed_at"]}</div>' + "".join([f'<div class="flag-row"><b>{f["name"]}</b>{badge(f["status"], "red" if f["status"]=="High" else "gold" if f["status"]=="Medium" else "gray")}<span class="flag-detail">{f["detail"]}</span></div>' for f in case["engine"]["flags"]]), badge("5 checks complete", "teal"))
        st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
        metric_row([("87 / 100", "Bob confidence"), ("5", "Checks run"), ("0.42", "Integrity signal")])
        st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
        st.markdown('<div class="note"><b>Interpretation guardrail.</b> High-severity flags are indicators for examiner review. They do not independently establish alteration or intent.</div>', unsafe_allow_html=True)
        if st.button("Run / refresh Bob analysis", type="primary", use_container_width=True):
            st.session_state.case["engine"] = run_engine(st.session_state.case["observations"].get("filename", "mock-case"))
            st.session_state.page = "Bob orchestration"
            st.rerun()


def orchestration():
    case = st.session_state.case
    header("Bob / EagleEye Mode", "Visible orchestration trace", "The pipeline is explicit: Bob activates the examiner skillset, calls MCP tools, then hands the full case to Report Engine.")
    left, right = st.columns([1.25, .75], gap="large")
    with left:
        panel("Bob execution trace", '<div class="muted" style="margin-bottom:12px">Run ID · <span class="mono">ee-0041-bob-20260928</span></div>')
        render_pipeline(case["steps"], 7)
    with right:
        panel("MCP return · classify_anomaly", f'<div class="mono">{case["outputs"]["classification"]["type"]}</div><div class="muted" style="margin-top:7px">Category · {case["outputs"]["classification"]["category"]}</div>', badge("RETURNED", "teal"))
        st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
        panel("MCP return · score_forgery_confidence", f'<div class="metric-value">{case["outputs"]["confidence"]["score"]}<span class="muted"> / 100</span></div>' + "".join([f'<div class="muted" style="margin-top:8px">• {x}</div>' for x in case["outputs"]["confidence"]["reasoning"]]), badge("RETURNED", "teal"))
        st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
        panel("MCP return · fetch_case_precedents", '<b>State v. Sharma 2022</b><div class="muted">Relevance · 0.91</div>', badge("1 MATCH", "gold"))
    st.markdown('<div class="footer-note">Integration status: demo uses deterministic mock adapters in <span class="mono">src/ui/mcp_client.py</span>. Each adapter is isolated for replacement with the real Bob/MCP implementation.</div>', unsafe_allow_html=True)


def findings():
    case = st.session_state.case
    header("Review / Standards", "Findings and reference mapping", "Separate observed signals, machine interpretation and standards-oriented documentation prompts.")
    left, right = st.columns([1, 1], gap="large")
    with left:
        panel("Classification", f'<div class="eyebrow">ANOMALY TYPE</div><h2 style="margin-top:7px">{case["outputs"]["classification"]["type"]}</h2><div class="muted" style="margin-top:6px">Category · {case["outputs"]["classification"]["category"]}</div>')
        st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
        panel("Standards mapping · ASTM E2388", "".join([f'<div class="step"><div class="step-dot self">✓</div><div><div class="step-name">{x}</div></div></div>' for x in case["outputs"]["standards"]["ASTM_E2388"]]))
    with right:
        panel("FSL checklist prompts", "".join([f'<div class="step"><div class="step-dot self">✓</div><div><div class="step-name">{x}</div></div></div>' for x in case["outputs"]["standards"]["FSL_checklist"]]))
        st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
        panel("Examiner note", '<div class="muted">Use the standards mapping as a documentation aid. Confirm the applicable laboratory SOP, jurisdictional requirements and the original evidence condition before signing.</div>')


def report_review():
    case = st.session_state.case
    header("Report Engine / Examiner review", "Court-style report package", "The report is generated for review, amendment and signature — not automatic submission.")
    left, right = st.columns([1.15, .85], gap="large")
    with left:
        panel("Report preview", '<div class="eyebrow">GENERATED ARTIFACT</div><h2 style="margin-top:7px">Expert report · EE-2026-0041</h2><div class="muted" style="margin-top:8px">Includes case identification, automated findings, Bob orchestration trace, standards prompts, and examiner sign-off block.</div>')
        st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
        st.markdown('<div class="note"><b>Required review.</b> Read the interpretive statement, verify the evidence hash and amend any finding that does not reflect your professional judgment.</div>', unsafe_allow_html=True)
        report = build_report(case)
        st.download_button("Download court-style PDF", data=report, file_name="eagle_eye_expert_report.pdf", mime="application/pdf", type="primary", use_container_width=True)
    with right:
        panel("Sign-off gate", '<div class="muted">The examiner owns the final opinion.</div>')
        reviewed = st.checkbox("I reviewed the automated findings and orchestration trace.")
        amended = st.checkbox("I confirmed or amended the interpretive statement.")
        signed = st.text_input("Examiner signature / initials", placeholder="Type to acknowledge review")
        if reviewed and amended and signed:
            st.success("Review gate satisfied. Report is ready for examiner-controlled use.")
        else:
            st.warning("Complete all review fields before treating the report as signed.")
        st.markdown('<div class="footer-note">Report Engine status · ready<br>Precedent source · mock return for demonstration</div>', unsafe_allow_html=True)


def main():
    init_state()
    sidebar()
    page = st.session_state.page
    if page == "Case workspace": workspace()
    elif page == "Bob orchestration": orchestration()
    elif page == "Findings & standards": findings()
    else: report_review()


if __name__ == "__main__":
    main()

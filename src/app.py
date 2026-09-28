"""Eagle Eye: Streamlit UI. Run with: streamlit run src/app.py"""
import time
from datetime import date

import streamlit as st

from ui import mcp_client as mc, report as R, theme as T
from ui.mock_data import SCENARIOS

st.set_page_config(page_title="Eagle Eye", page_icon="🦅", layout="wide")
st.markdown(T.CSS, unsafe_allow_html=True)
S = st.session_state
for k, v in {"step": 0, "case": {}, "obs": {}, "file": None, "engine": None, "bob": None,
             "scenario": "Forged COVID certificate"}.items():
    S.setdefault(k, v)

DOC_TYPES = ["Degree or marksheet", "Certificate", "ID card", "Property document", "FIR",
             "COVID vaccination certificate", "Other"]
SIG = ["Not applicable", "Consistent", "Minor variation", "Clearly different"]
SEAL = ["Not applicable", "Consistent", "Faint or smudged", "Missing", "Different from reference"]
PAPER = ["Different texture", "Tinted or off-white", "Missing watermark", "Uneven wear", "Trimmed edges"]
INK = ["Ink spread", "Feathering", "Different ink shades", "Toner and inkjet mixed", "Overwriting"]
SKILLS = ["Typography analysis", "Metadata analysis", "Standards mapping", "Report drafting"]


def go(n):
    S.step = n
    st.rerun()


def reset():
    for k in ("case", "obs", "file", "engine", "bob"):
        S.pop(k, None)
    S.step = 0
    st.rerun()


def stale():
    S.engine, S.bob = None, None


def pick(options, value, default=0):
    return options.index(value) if value in options else default


# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown("### Case console")
    st.selectbox("Demo scenario", list(SCENARIOS), key="scenario", on_change=stale,
                 help="Switches the mock data used for analysis.")
    if st.button("Load demo case", use_container_width=True):
        S.case = {"no": "FSL/2026/0417", "examiner": "Dr. A. Mehta",
                  "type": "COVID vaccination certificate", "date": date.today()}
        S.obs = {"sig": "Minor variation", "seal": "Consistent", "paper": ["Tinted or off-white"],
                 "ink": ["Different ink shades"], "notes": "Name line looks re-typed under magnification.",
                 "sig_n": ""}
        S.file = ("demo_certificate.jpg", None)
        stale()
        go(1)
    if S.case:
        st.caption(f"Case {S.case.get('no', '-')}")
        st.caption(f"File: {S.file[0] if S.file else 'none'}")
    if st.button("Start new case", use_container_width=True):
        reset()
    with st.expander("About and limitations"):
        st.caption("Eagle Eye supports the examiner and does not replace them. Scores come from "
                   "rule-based checks. Standards, precedents and legal sections are demo data until verified.")

st.markdown(T.header(), unsafe_allow_html=True)
st.markdown(T.stepper(S.step), unsafe_allow_html=True)


# ---------------------------------------------------------------- step 1
def intake():
    st.subheader("Case intake")
    c, (a, b) = S.case, st.columns(2)
    no = a.text_input("Case number", c.get("no", ""), placeholder="FSL/2026/0417")
    ex = b.text_input("Examiner name", c.get("examiner", ""))
    dt = a.selectbox("Document type", DOC_TYPES, index=pick(DOC_TYPES, c.get("type")))
    rec = b.date_input("Date received", c.get("date", date.today()))
    up = st.file_uploader("Suspected document", type=["jpg", "jpeg", "png", "pdf"])
    if up:
        S.file = (up.name, up.getvalue())
    if S.file and S.file[1] and S.file[0].lower().endswith((".jpg", ".jpeg", ".png")):
        st.image(S.file[1], caption=S.file[0], width=360)
    elif S.file:
        st.caption(f"Selected: {S.file[0]}")
    if st.button("Continue", type="primary"):
        if not no.strip() or not S.file:
            st.error("Enter a case number and upload the document to continue.")
        else:
            S.case = {"no": no.strip(), "examiner": ex, "type": dt, "date": rec}
            stale()
            go(1)


# ---------------------------------------------------------------- step 2
def observations():
    o = S.obs
    st.subheader("Examiner observations")
    st.caption("Record what the software cannot see.")
    a, b = st.columns(2)
    sig = a.selectbox("Signature comparison", SIG, index=pick(SIG, o.get("sig")))
    sig_n = a.text_area("Signature notes", o.get("sig_n", ""), height=90)
    seal = a.selectbox("Stamps and seals", SEAL, index=pick(SEAL, o.get("seal")))
    paper = b.multiselect("Paper anomalies", PAPER, default=o.get("paper", []))
    ink = b.multiselect("Ink and printing", INK, default=o.get("ink", []))
    notes = b.text_area("Examiner notes", o.get("notes", ""), height=110)
    x, y, _ = st.columns([1, 2, 6])
    if x.button("Back"):
        go(0)
    if y.button("Run analysis", type="primary"):
        S.obs = {"sig": sig, "sig_n": sig_n, "seal": seal, "paper": paper, "ink": ink, "notes": notes}
        stale()
        go(2)


# ---------------------------------------------------------------- step 3
def analysis():
    st.subheader("Automated checks")
    if S.engine is None:
        with st.status("Running forensic checks", expanded=True) as stt:
            for m in SCENARIOS[S.scenario]["modules"]:
                st.write(f"{m['title']}")
                time.sleep(0.4)
            S.engine = mc.run_engine(S.scenario, S.file)
            stt.update(label="Checks complete", state="complete", expanded=False)
    if S.engine["status"] != "ok":
        st.error(f"The analysis engine failed: {S.engine['result']}")
        return
    mods = S.engine["result"]
    checks = [c for m in mods for c in m["checks"]]
    n = {k: sum(c["status"] == k for c in checks) for k in ("fail", "warn", "pass")}
    cols = st.columns(4)
    for col, (lab, val, clr) in zip(cols, [("Checks run", len(checks), "#14182B"), ("Failed", n["fail"], T.STATUS_COL["fail"]),
                                           ("Warnings", n["warn"], T.STATUS_COL["warn"]), ("Passed", n["pass"], T.STATUS_COL["pass"])]):
        col.markdown(T.metric(lab, val, clr), unsafe_allow_html=True)
    left, right = st.columns([3, 2])
    with left:
        for tab, m in zip(st.tabs([m["title"] for m in mods]), mods):
            with tab:
                st.markdown("".join(T.check_row(c) for c in m["checks"]), unsafe_allow_html=True)
    with right:
        st.markdown(T.card("Suspicion by module", T.module_bars(mods)), unsafe_allow_html=True)
        if S.file and S.file[1] and S.file[0].lower().endswith((".jpg", ".jpeg", ".png")):
            st.image(S.file[1], caption="Document under examination")
    st.info("Automated indicators support, and do not replace, examiner judgement.")
    x, y, _ = st.columns([1, 2, 6])
    if x.button("Back"):
        go(1)
    if y.button("Hand over to Bob", type="primary"):
        go(3)


# ---------------------------------------------------------------- step 4
def run_pipeline(mods):
    flags = [c for m in mods for c in m["checks"]]
    sc, box, calls = S.scenario, st.empty(), []
    steps = [("classify_anomaly", "Classify anomaly type", lambda: mc.classify_anomaly(sc, S.obs)),
             ("score_forgery_confidence", "Score forgery confidence", lambda: mc.score_forgery_confidence(sc, flags)),
             ("map_to_standards", "Map findings to standards", lambda: mc.map_to_standards(sc, mods)),
             ("fetch_case_precedents", "Find similar cases", lambda: mc.fetch_case_precedents(sc, S.case.get("type", "")))]
    for tool, label, fn in steps:
        box.markdown(T.card("Bob is working", T.timeline(calls, (tool, label))), unsafe_allow_html=True)
        calls.append(fn())
        if calls[-1]["status"] != "ok":
            box.markdown(T.card("Bob stopped", T.timeline(calls)), unsafe_allow_html=True)
            st.error(f"{tool} failed: {calls[-1]['result']}")
            st.button("Retry")
            return
    r = [c["result"] for c in calls]
    ctx = {"case": S.case, "obs": S.obs, "file": S.file[0], "modules": mods,
           "cls": r[0], "score": r[1], "std": r[2], "prec": r[3]}
    box.markdown(T.card("Bob is working", T.timeline(calls, ("generate_expert_report", "Draft expert report"))), unsafe_allow_html=True)
    calls.append(mc.generate_expert_report(ctx))
    S.bob = {"calls": calls, "ctx": ctx}
    st.rerun()


def bob():
    st.subheader("Bob in forensic examiner mode")
    st.caption("Active skills: " + ", ".join(SKILLS))
    if S.bob is None:
        run_pipeline(S.engine["result"])
        return
    calls, ctx = S.bob["calls"], S.bob["ctx"]
    sc, cl = ctx["score"], ctx["cls"]
    left, right = st.columns([2, 3])
    with left:
        st.markdown(T.card("What Bob did", T.timeline(calls)), unsafe_allow_html=True)
    with right:
        st.markdown(T.card("Forgery confidence",
                           f'<div class="ee-big">{sc["score"]} <span class="ee-mut">out of 100</span> &nbsp;{T.pill(sc["level"])}</div>'
                           + T.scale(sc["score"])), unsafe_allow_html=True)
        st.markdown(T.card("Classification", f'<div class="ee-big">{cl["type"]}</div><div class="ee-mut">{cl["category"]}</div>'),
                    unsafe_allow_html=True)
        st.markdown(T.card("Why this score", "<ul>" + "".join(f"<li>{x}</li>" for x in sc["reasoning"]) + "</ul>"),
                    unsafe_allow_html=True)
    a, b = st.columns(2)
    with a:
        st.markdown(T.card("Standards (demo data, verify before citing)",
                           "<ul>" + "".join(f"<li>{x}</li>" for x in ctx["std"]["ASTM_E2388"]) + "</ul>"), unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("**Lab checklist**")
            for i, it in enumerate(ctx["std"]["FSL_checklist"]):
                st.checkbox(it["item"], value=it["done"], key=f"fsl{i}")
    with b:
        rows = "".join(f'<div style="margin-bottom:10px"><b>{p["case"]}</b> <span class="ee-mut">relevance {p["relevance"]:.2f}</span>'
                       f'<div class="ee-bar" style="margin:4px 0"><i style="width:{int(p["relevance"]*100)}%;background:#5B3FD6"></i></div>'
                       f'<div class="ee-mut">{p["summary"]}</div></div>' for p in ctx["prec"]) or '<div class="ee-mut">No similar cases found.</div>'
        st.markdown(T.card("Similar cases (demo data, verify before citing)", rows), unsafe_allow_html=True)
    st.markdown("### Expert opinion report")
    lines = R.build(ctx)
    d1, d2, d3, _ = st.columns([1, 1, 1, 3])
    d1.download_button("Download PDF", calls[-1]["result"], "eagle_eye_expert_report.pdf", "application/pdf", type="primary")
    d2.download_button("Download Markdown", R.to_markdown(lines), "eagle_eye_expert_report.md")
    if d3.button("Start new case"):
        reset()
    st.markdown(R.to_html(lines), unsafe_allow_html=True)


[intake, observations, analysis, bob][S.step]()

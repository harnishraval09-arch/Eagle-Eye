"""Visual theme: cool paper background, ink text, one UV-violet accent."""
LEVEL_COL = {"Low": "#1F9D6B", "Moderate": "#C98A00", "High": "#E0702B", "Very High": "#D64545"}
STATUS_COL = {"pass": "#1F9D6B", "warn": "#C98A00", "fail": "#D64545"}
ICON = {"pass": "✓", "warn": "!", "fail": "✕"}

CSS = """<style>
.stApp{background:#F5F6FA;color:#14182B}
header[data-testid=stHeader]{background:transparent}
.block-container{padding-top:1.2rem;max-width:1180px}
h1,h2,h3,h4{font-family:Georgia,'Times New Roman',serif;color:#14182B;letter-spacing:-.01em}
.ee-brand{display:flex;justify-content:space-between;align-items:baseline;padding:4px 0 16px}
.ee-brand b{font:700 32px Georgia,serif}.ee-brand span{color:#5F6884;font-size:15px;margin-left:12px}
.ee-by{border:1px solid #DDE1EC;border-radius:99px;padding:3px 12px;font-size:13px;color:#5B3FD6;background:#fff}
.ee-steps{display:flex;gap:30px;border-bottom:1px solid #DDE1EC;margin-bottom:22px}
.ee-steps div{padding:8px 0;color:#8A93AD;font-size:15px;border-bottom:3px solid transparent;margin-bottom:-1px}
.ee-steps .on{color:#14182B;font-weight:600;border-color:#5B3FD6}.ee-steps .done{color:#1F9D6B}
.ee-card{background:#fff;border:1px solid #DDE1EC;border-radius:10px;padding:16px 18px;margin-bottom:14px}
.ee-h{font:600 16px Georgia,serif;margin-bottom:10px}
.ee-mut{color:#5F6884;font-size:13px}.ee-big{font:700 26px Georgia,serif}
.ee-pill{border:1.5px solid;border-radius:99px;padding:2px 12px;font-size:13px;font-weight:600}
.ee-chk{display:grid;grid-template-columns:22px 1fr 110px 34px;gap:12px;align-items:center;padding:10px 0;border-bottom:1px solid #EEF0F6}
.ee-dot{width:20px;height:20px;border-radius:50%;color:#fff;font-size:12px;display:flex;align-items:center;justify-content:center;font-weight:700}
.ee-bar{height:6px;background:#E8EBF3;border-radius:9px;overflow:hidden}.ee-bar i{display:block;height:100%}
.ee-scale{position:relative;height:12px;border-radius:9px;background:linear-gradient(90deg,#1F9D6B 25%,#C98A00 25% 50%,#E0702B 50% 80%,#D64545 80%);margin:30px 0 8px}
.ee-scale u{position:absolute;top:-9px;width:4px;height:30px;background:#14182B;border-radius:2px;text-decoration:none}
.ee-scale-l{display:flex;justify-content:space-between;color:#5F6884;font-size:12px}
.ee-tl-row{display:grid;grid-template-columns:22px 1fr auto;gap:12px;padding:9px 0;border-bottom:1px solid #EEF0F6;align-items:center}
.ee-tl code{font-size:13px;color:#5B3FD6;background:none}
.ee-page{background:#fff;border:1px solid #DDE1EC;border-radius:4px;padding:40px 52px;font-family:Georgia,serif;line-height:1.65;max-width:820px;margin:8px auto}
.ee-page,.ee-page *{color:#1B2033!important}.ee-page h1{font-size:26px}.ee-page h3{font-size:18px;margin-top:22px}
</style>"""


def level_for(s):
    return "Low" if s <= 25 else "Moderate" if s <= 50 else "High" if s <= 80 else "Very High"

def header():
    return '<div class="ee-brand"><div><b>Eagle Eye</b><span>Document forgery examination</span></div><div class="ee-by">Powered by IBM Bob</div></div>'

def stepper(cur):
    names = ["Intake", "Observations", "Analysis", "Bob and report"]
    return '<div class="ee-steps">' + "".join(
        f'<div class="{"done" if i < cur else "on" if i == cur else ""}">{"✓ " if i < cur else ""}{n}</div>' for i, n in enumerate(names)) + "</div>"

def card(title, body):
    return f'<div class="ee-card"><div class="ee-h">{title}</div>{body}</div>'

def metric(label, value, color="#14182B"):
    return f'<div class="ee-card"><div class="ee-mut">{label}</div><div class="ee-big" style="color:{color}">{value}</div></div>'

def pill(level):
    c = LEVEL_COL[level]
    return f'<span class="ee-pill" style="color:{c};border-color:{c}">{level}</span>'

def scale(score):
    return (f'<div class="ee-scale"><u style="left:calc({score}% - 2px)"></u></div>'
            '<div class="ee-scale-l"><span>Low</span><span>Moderate</span><span>High</span><span>Very high</span></div>')

def check_row(c):
    col, w = STATUS_COL[c["status"]], int(c["score"] * 100)
    return (f'<div class="ee-chk"><span class="ee-dot" style="background:{col}">{ICON[c["status"]]}</span>'
            f'<div><b>{c["name"]}</b><div class="ee-mut">{c["detail"]}</div></div>'
            f'<div class="ee-bar"><i style="width:{w}%;background:{col}"></i></div><span class="ee-mut">{w}</span></div>')

def module_bars(mods):
    rows = ""
    for m in mods:
        s = max(c["score"] for c in m["checks"])
        col = STATUS_COL["fail" if s >= .7 else "warn" if s >= .4 else "pass"]
        rows += (f'<div style="margin-bottom:12px"><div class="ee-mut" style="margin-bottom:4px">{m["title"]}</div>'
                 f'<div class="ee-bar"><i style="width:{int(s*100)}%;background:{col}"></i></div></div>')
    return rows

def timeline(calls, running=None):
    rows = ""
    for c in calls:
        ok = c["status"] == "ok"
        rows += (f'<div class="ee-tl-row"><span class="ee-dot" style="background:{"#1F9D6B" if ok else "#D64545"}">{"✓" if ok else "✕"}</span>'
                 f'<div><code>{c["tool"]}()</code><div class="ee-mut">{c["label"]}</div></div><span class="ee-mut">{c["duration_s"]} s</span></div>')
    if running:
        rows += (f'<div class="ee-tl-row"><span class="ee-dot" style="background:#5B3FD6">…</span>'
                 f'<div><code>{running[0]}()</code><div class="ee-mut">{running[1]}</div></div><span class="ee-mut">running</span></div>')
    return f'<div class="ee-tl">{rows}</div>'

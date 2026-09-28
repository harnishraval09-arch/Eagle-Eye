"""Adapter between the UI and the real engine / Bob MCP tools.

Each function tries the real implementation first (src/engine/tools.py, same
function name) and falls back to mock data. TODO: implement these in engine/tools.py.
"""
import importlib
import time
from ui import mock_data as md, report


def _call(tool, label, args, mock, pause=0.7):
    t0, status = time.time(), "ok"
    try:
        result = getattr(importlib.import_module("engine.tools"), tool)(*args)
    except (ImportError, AttributeError):
        time.sleep(pause)
        result = mock() if callable(mock) else mock
    except Exception as e:  # real tool failed
        status, result = "error", str(e)
    return {"tool": tool, "label": label, "result": result,
            "duration_s": round(time.time() - t0, 2), "status": status}


def run_engine(scenario, file):
    return _call("run_engine", "Automated forensic checks", (file,), md.SCENARIOS[scenario]["modules"], 0.2)

def classify_anomaly(scenario, obs):
    return _call("classify_anomaly", "Classify anomaly type", (obs,), md.SCENARIOS[scenario]["classification"])

def score_forgery_confidence(scenario, flags):
    return _call("score_forgery_confidence", "Score forgery confidence", (flags,), md.SCENARIOS[scenario]["score"])

def map_to_standards(scenario, findings):
    return _call("map_to_standards", "Map findings to standards", (findings,), md.SCENARIOS[scenario]["standards"])

def fetch_case_precedents(scenario, doc_type):
    return _call("fetch_case_precedents", "Find similar cases", (doc_type,), md.SCENARIOS[scenario]["precedents"])

def generate_expert_report(ctx):
    return _call("generate_expert_report", "Draft expert report", (ctx,), lambda: report.build_pdf(ctx))

"""Integration boundary for Bob / MCP / Report Engine with mock fallback."""

from .mock_data import engine_result, pipeline_outputs


def _real_or_mock(real_import, fallback):
    try:
        module = __import__(real_import[0], fromlist=[real_import[1]])
        return getattr(module, real_import[1])
    except Exception:
        return fallback


def run_engine(file_path):
    # TODO: Replace with the forensic Python engine import/API.
    try:
        fn = _real_or_mock(("forensic_engine", "run_engine"), None)
        if fn:
            return fn(file_path)
    except Exception:
        pass
    return engine_result()


def classify_anomaly(observations):
    # TODO: Replace with the real MCP client call to classify_anomaly.
    try:
        fn = _real_or_mock(("mcp_tools", "classify_anomaly"), None)
        if fn:
            return fn(observations)
    except Exception:
        pass
    return pipeline_outputs()["classification"]


def score_forgery_confidence(all_flags):
    # TODO: Replace with the real MCP client call to score_forgery_confidence.
    try:
        fn = _real_or_mock(("mcp_tools", "score_forgery_confidence"), None)
        if fn:
            return fn(all_flags)
    except Exception:
        pass
    return pipeline_outputs()["confidence"]


def map_to_standards(findings):
    # TODO: Replace with the real MCP client call to map_to_standards.
    try:
        fn = _real_or_mock(("mcp_tools", "map_to_standards"), None)
        if fn:
            return fn(findings)
    except Exception:
        pass
    return pipeline_outputs()["standards"]


def fetch_case_precedents(query):
    # TODO: Replace with the real MCP client call to fetch_case_precedents.
    try:
        fn = _real_or_mock(("mcp_tools", "fetch_case_precedents"), None)
        if fn:
            return fn(query)
    except Exception:
        pass
    return pipeline_outputs()["precedents"]


def generate_expert_report(full_case):
    # TODO: Replace with the real Report Engine / MCP call.
    try:
        fn = _real_or_mock(("report_engine", "generate_expert_report"), None)
        if fn:
            return fn(full_case)
    except Exception:
        pass
    return {"status": "ready", "message": "Mock report payload ready for export."}

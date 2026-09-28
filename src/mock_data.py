"""Deterministic mock payloads for the standalone Eagle Eye demo."""

from datetime import datetime, timezone


def default_observations():
    return {
        "document_type": "COVID Certificate",
        "issuing_body": "Ministry of Health",
        "case_number": "EE-2026-0041",
        "examiner": "A. Morgan",
        "observations": "Uneven baseline on recipient name; QR block appears resampled.",
        "chain_of_custody": "Received sealed from submitting agency; SHA-256 recorded.",
    }


def engine_result():
    return {
        "flags": [
            {"name": "Error Level Analysis", "status": "High", "detail": "Localized compression mismatch around recipient name."},
            {"name": "Copy-move detection", "status": "Medium", "detail": "Repeated texture pattern detected near certificate ID."},
            {"name": "Metadata", "status": "Low", "detail": "Editing application marker present; not independently conclusive."},
            {"name": "Typography", "status": "High", "detail": "Baseline and glyph rasterization differ from surrounding text."},
            {"name": "Layout / QR", "status": "Medium", "detail": "QR quiet zone is inconsistent with issuer template."},
        ],
        "integrity": 0.42,
        "hash": "9f0d…a81c",
        "processed_at": "2026-09-28 14:32 UTC",
    }


def bob_steps():
    return [
        {"id": "intake", "label": "Intake routed to Bob", "kind": "input", "detail": "Case file + structured observations"},
        {"id": "mode", "label": "Activate forensic-examiner mode", "kind": "self", "detail": "Relevant skills loaded"},
        {"id": "classify", "label": "classify_anomaly(observations)", "kind": "mcp", "detail": "Typography Forgery · Cut-and-paste"},
        {"id": "score", "label": "score_forgery_confidence(all_flags)", "kind": "mcp", "detail": "87 / 100 · reasoning attached"},
        {"id": "standards", "label": "map_to_standards(findings)", "kind": "mcp", "detail": "ASTM E2388 · FSL checklist"},
        {"id": "precedents", "label": "fetch_case_precedents(\"COVID Certificate\")", "kind": "mcp", "detail": "State v. Sharma 2022 · 0.91 relevance"},
        {"id": "report", "label": "Report Engine: generate_expert_report(full_case)", "kind": "report", "detail": "Court-style PDF queued for examiner review"},
    ]


def pipeline_outputs():
    return {
        "classification": {"type": "Typography Forgery", "category": "Cut-and-paste"},
        "confidence": {"score": 87, "reasoning": ["Two high-severity image/typography flags converge.", "QR/layout anomaly is corroborative, not determinative.", "Metadata is treated as contextual only."]},
        "standards": {"ASTM_E2388": ["Record questioned-item condition", "Document image-processing limitations", "Separate observations from interpretation"], "FSL_checklist": ["Preserve original media", "Record hash and chain of custody", "Identify examiner and date"]},
        "precedents": [{"case": "State v. Sharma 2022", "relevance": 0.91}],
    }


def demo_case():
    return {"observations": default_observations(), "engine": engine_result(), "steps": bob_steps(), "outputs": pipeline_outputs(), "created_at": datetime.now(timezone.utc).isoformat()}

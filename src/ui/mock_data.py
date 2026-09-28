"""Mock scenarios so the UI runs before the real engine is connected."""

def _c(name, status, score, detail):
    return {"name": name, "status": status, "score": score, "detail": detail}

FORGED = {
    "modules": [
        {"module": "ela", "title": "Error level analysis", "checks": [
            _c("Compression hotspot", "fail", .82, "Name field was saved at a different compression level than the page."),
            _c("Uniform compression elsewhere", "warn", .48, "Date block shows mild variation."),
            _c("Signature region", "pass", .12, "Consistent with surrounding area.")]},
        {"module": "copy_move", "title": "Copy-move detection", "checks": [
            _c("Duplicated texture blocks", "pass", .10, "No repeated regions found."),
            _c("Cloned background near text", "warn", .35, "One small patch resembles its neighbour.")]},
        {"module": "metadata", "title": "Metadata", "checks": [
            _c("Producer software", "fail", .78, "Created by a PDF editor, not a scanner."),
            _c("Modified after creation", "fail", .71, "Modification date is later than creation date."),
            _c("Incremental saves", "warn", .55, "Two save revisions in the file structure.")]},
        {"module": "typography", "title": "Typography", "checks": [
            _c("Font in Name field", "fail", .91, "Different typeface and weight from the rest of the line."),
            _c("Baseline alignment", "fail", .74, "Name sits 3 px above the line baseline."),
            _c("Character spacing", "warn", .52, "Tracking differs in the edited field."),
            _c("Text orientation", "pass", .08, "No skew detected.")]},
        {"module": "layout_qr", "title": "Layout and QR", "checks": [
            _c("QR content vs printed name", "fail", .80, "QR decodes to a different name than the one printed."),
            _c("Logo position", "warn", .40, "Logo is 2 mm off the reference template."),
            _c("Footer margin", "pass", .14, "Matches the reference.")]},
    ],
    "classification": {"type": "Typography forgery", "category": "Cut-and-paste"},
    "score": {"score": 87, "level": "Very High", "reasoning": [
        "Typeface, weight and baseline of the Name field differ from the surrounding text.",
        "The same region shows a compression level unlike the rest of the page.",
        "The file was last saved by an editing tool, not a scanner.",
        "The QR code does not match the printed name."]},
    "standards": {"ASTM_E2388": [
        "Examine printed text for alteration, addition and substitution.",
        "Record the basis for each conclusion and the limits of the examination."],
        "FSL_checklist": [
            {"item": "Original document requested for physical examination", "done": False},
            {"item": "Source file and hash preserved", "done": True},
            {"item": "Specimen of the issuing authority's template obtained", "done": False}]},
    "precedents": [{"case": "State v. Sharma 2022", "relevance": .91,
                    "summary": "Altered vaccination certificate; typography and metadata evidence accepted."}],
}

GENUINE = {
    "modules": [
        {"module": m, "title": t, "checks": [_c(n, "pass", s, d) for n, s, d in cs]} for m, t, cs in [
            ("ela", "Error level analysis", [("Compression hotspot", .09, "Uniform across the page."), ("Signature region", .11, "Consistent.")]),
            ("copy_move", "Copy-move detection", [("Duplicated texture blocks", .06, "None found.")]),
            ("metadata", "Metadata", [("Producer software", .10, "Scanner firmware."), ("Dates", .08, "Creation and modification match.")]),
            ("typography", "Typography", [("Font consistency", .07, "One family and weight per field."), ("Baseline alignment", .09, "Within tolerance.")]),
            ("layout_qr", "Layout and QR", [("QR content vs printed name", .05, "Match."), ("Logo position", .10, "Matches the reference.")])]],
    "classification": {"type": "No significant anomaly", "category": "None"},
    "score": {"score": 12, "level": "Low", "reasoning": ["No check exceeded the warning threshold.", "Metadata and layout match a scanned original."]},
    "standards": {"ASTM_E2388": ["No alteration indicators recorded."], "FSL_checklist": [{"item": "Source file and hash preserved", "done": True}]},
    "precedents": [],
}

SCENARIOS = {"Forged COVID certificate": FORGED, "Genuine document": GENUINE}

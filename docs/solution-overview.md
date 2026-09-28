# Solution Overview — EagleEye

## What EagleEye Does

EagleEye is an **AI-powered guided examination workflow** built on IBM Bob. It transforms
a forensic document examiner's structured observations into a complete, court-admissible
expert opinion report — consistently, rapidly, and in compliance with Indian legal standards.

---

## The Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        EXAMINER INPUT                           │
│  Structured observations in JSON or via web form / file upload  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   EAGLEEYE FORENSIC ENGINE                      │
│                                                                 │
│  Step 1: classify_anomaly                                       │
│    → Each observation → TYP / SIG / PAP / INK / DIG / SEA      │
│    → Severity: Critical / High / Medium / Low                   │
│    → Standards: ASTM E2388 section + FSL Protocol reference     │
│                                                                 │
│  Step 2: score_forgery_confidence                               │
│    → Weighted scoring formula (severity multipliers)            │
│    → 0–100% → Likely Genuine / Inconclusive /                   │
│               Probable Forgery / High Confidence Forgery        │
│                                                                 │
│  Step 3: map_to_standards                                       │
│    → Full ASTM E2388 checklists for each anomaly type           │
│    → FSL Protocol examination steps                             │
│                                                                 │
│  Step 4: fetch_case_precedents                                  │
│    → 5 indexed Indian court decisions                           │
│    → Matched by document type + forgery pattern                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXPERT OPINION REPORT                        │
│                                                                 │
│  Section 1: Brief Facts                                         │
│  Section 2: Documents Received for Examination                  │
│  Section 3: Examination Conducted                               │
│  Section 4: Findings (anomaly table with standards)             │
│  Section 5: Opinion (score + classification + narrative)        │
│  Section 6: Relevant Case Precedents                            │
│  Section 7: Expert Declaration (IEA §45 compliant)              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Design Decisions

### Why Bob as the AI backbone?
Bob's custom mode system lets us define a specialised persona (the QD Examiner) with
domain-specific rules, skills, and MCP tool access. The examiner gets structured guidance
without requiring any AI prompt engineering knowledge.

### Why an MCP server?
The forensic engine (classification logic, scoring formula, standards database, case
precedents) runs as a Bob MCP tool server. This means Bob can call these tools natively
during a conversation — the AI retrieves authoritative forensic standards from the local
engine rather than hallucinating from training data.

### Why ASTM E2388 + FSL Protocols?
These are the two most widely cited standards in Indian forensic science labs and courts.
ASTM E2388 is the international standard for questioned document examination; FSL Protocols
are India-specific operating procedures followed by state Forensic Science Laboratories.
Mapping to these standards is what makes the report court-admissible.

### Why a weighted confidence score?
Different anomaly types carry different evidential weight. A mismatched PDF Creator field
(DIG/Critical) is more definitively probative than a font inconsistency (TYP/High). The
scoring formula applies severity multipliers (Critical: 1.5x, High: 1.2x, Medium: 1.0x,
Low: 0.7x) to each anomaly's base weight, summing to a normalised 0–100% score. This
mirrors how courts evaluate convergent forensic evidence.

---

## Bob Features Used

| Feature | How Used |
|---------|----------|
| Custom Mode | `forensic-examiner` — QD Examiner persona with domain rules and permissions |
| MCP Server | `eagleeye-forensics` — 4 forensic tools callable by Bob during conversation |
| Skills (×4) | `questioned-documents`, `digital-forgery-patterns`, `indian-evidence-act`, `court-report-format` |
| Mode Rules (×2) | `01-examination-protocol.md` (anomaly rubric), `02-report-format.md` (7-section template) |

---

## Anomaly Classification System

| Code | Category | Base Weight | Description |
|------|----------|-------------|-------------|
| TYP | Typography / Printing | 15 | Font mismatches, kerning, baseline, DPI anomalies |
| SIG | Signature / Handwriting | 25 | Pen pressure, tremor, stroke order, tracing evidence |
| PAP | Paper / Substrate | 10 | GSM weight, watermark, UV fluorescence, security thread |
| INK | Ink / Printing Process | 20 | Ink type mismatch, age testing, toner vs inkjet |
| DIG | Digital Metadata / PDF | 30 | Creator/Producer, ModDate, XMP history, digital signatures |
| SEA | Seal / Stamp | 20 | Ink distribution, font, dimensions vs reference specimen |

---

## Confidence Score Classification

| Score Range | Classification |
|-------------|----------------|
| 0–25% | Likely Genuine |
| 26–50% | Inconclusive — Further Examination Recommended |
| 51–75% | Probable Forgery |
| 76–100% | High Confidence Forgery |

---

## What Makes This Production-Ready

- **Real signals** — PDF upload extracts actual metadata from the raw buffer (Creator, Producer, ModDate, XMP history, digital signatures, font declarations)
- **Live connections** — all frontend pages make real `fetch()` calls to the API; zero hardcoded demo data
- **Standards-compliant output** — reports cite specific ASTM E2388 sections and FSL Protocol numbers
- **Legal declarations** — every report ends with an Indian Evidence Act §45 Expert Declaration
- **Reproducible** — runs on Node.js 24, no cloud dependencies, no paid APIs

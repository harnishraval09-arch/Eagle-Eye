# Architecture — EagleEye

## System Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         IBM BOB (AI LAYER)                              │
│                                                                         │
│   ┌──────────────────────────┐    ┌─────────────────────────────────┐   │
│   │  forensic-examiner Mode  │    │  4 Domain Skills                │   │
│   │  (.bob/custom_modes.yaml)│    │  · questioned-documents         │   │
│   │                          │    │  · digital-forgery-patterns     │   │
│   │  Role: QD Examiner       │    │  · indian-evidence-act          │   │
│   │  Rules: protocol +       │    │  · court-report-format          │   │
│   │         report format    │    └─────────────────────────────────┘   │
│   └──────────────────────────┘                                          │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ STDIO transport
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     MCP SERVER (server.js)                              │
│                     eagleeye-forensics                                  │
│                                                                         │
│   classify_anomaly  │  score_forgery_confidence                         │
│   map_to_standards  │  fetch_case_precedents                            │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ imports
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   FORENSIC ENGINE (forensics.js)                        │
│                                                                         │
│   Category Map (6 types × keyword lists)                                │
│   Weighted Scoring Formula (severity multipliers)                       │
│   Standards DB (ASTM E2388 §6.1–6.7 + FSL Protocols 2.1–7.2)          │
│   Case DB (5 Indian court decisions)                                    │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ also imports
                                 │
┌────────────────────────────────┴────────────────────────────────────────┐
│                    EXPRESS HTTP API (api.js)                            │
│                    http://localhost:3001                                 │
│                                                                         │
│   POST /api/examine  — PDF upload → buffer scan → forensics engine      │
│   POST /api/case     — structured JSON → forensics engine               │
│   GET  /api/health   — service health check                             │
│   GET  /*            — serves ui/index.html                             │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ fetch() REST calls
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   WEB DASHBOARD (ui/index.html)                         │
│                                                                         │
│   Page 1: Overview     — forgery gauge, breakdown chart, case stats     │
│   Page 2: Findings     — 18-row table, filterable by severity/category  │
│   Page 3: Expert Report — full FSL report + Export Court PDF            │
│   Page 4: Upload & Detect — real file upload → live analysis results    │
│   Page 5: New Case     — structured form → API → result card            │
└─────────────────────────────────────────────────────────────────────────┘
          ↑
    Examiner (Browser)              Bob Conversation
```

---

## Component Descriptions

### 1. IBM Bob — AI Layer

**Custom Mode** ([`.bob/custom_modes.yaml`](.bob/custom_modes.yaml))
Defines the `forensic-examiner` persona. Bob's role is a certified QD Examiner trained in
ASTM E2388 and FSL protocols. The mode restricts file editing to `.json`, `.md`, and `.txt`
files — case files and reports only.

**Skills** (`.bob/skills/`)
Four skills provide Bob with deep domain knowledge:
- `questioned-documents` — physical examination methods (signature, ink, paper, seal)
- `digital-forgery-patterns` — PDF metadata, manipulation patterns, exiftool usage
- `indian-evidence-act` — IEA §45 admissibility, IPC sections 463–471
- `court-report-format` — 7-section FSL report template with fill-in blocks

**Mode Rules** (`.bob/rules-forensic-examiner/`)
Two rule files Bob follows when in forensic-examiner mode:
- `01-examination-protocol.md` — anomaly classification rubric, confidence scoring table
- `02-report-format.md` — exact 7-section court report template with field markers

---

### 2. MCP Server (`mcp-server/server.js`)

Runs as a STDIO MCP server, registered in `.bob/mcp.json`. Bob auto-starts it when
the `forensic-examiner` mode is active. Exposes 4 tools:

| Tool | Input | Output |
|------|-------|--------|
| `classify_anomaly` | observation text, field name | type code, severity, standards reference |
| `score_forgery_confidence` | array of classified anomalies | 0–100% score + classification label |
| `map_to_standards` | array of type codes | ASTM + FSL checklists per type |
| `fetch_case_precedents` | document type, forgery type | up to 3 relevant court decisions |

---

### 3. Forensic Engine (`mcp-server/forensics.js`)

Pure functions, no side effects. Shared by both the MCP server and the HTTP API.

**Category Map** — 6 categories × keyword lists → anomaly type + severity classification

**Scoring Formula**
```
score = min(100, round(weightedSum / maxPossible × 100))

where:
  weightedSum = Σ (base_weight × severity_multiplier) for each anomaly
  severity_multipliers: Critical=1.5, High=1.2, Medium=1.0, Low=0.7
  maxPossible = count × 45 (max base weight × max multiplier)
```

**Standards DB** — Full ASTM E2388 §6.1–6.7 examination checklists + FSL Protocols 2.1–7.2

**Case DB** — 5 indexed Indian court decisions from Supreme Court and High Courts

---

### 4. HTTP API (`mcp-server/api.js`)

Express server on port 3001. Three endpoints + static file serving:

```
POST /api/examine
  Accepts: multipart/form-data (file + document_type)
  Process: reads PDF raw buffer (latin1) → scans for:
           /Creator, /Producer, /ModDate, /CreationDate
           Adobe Acrobat string, /JavaScript, XMP history
           /Sig + /ByteRange, /FontName declarations
           filename suspicious terms, MIME vs extension mismatch
  Returns: full examination JSON with classified anomalies + score

POST /api/case
  Accepts: JSON { case_id, document_type, observations[], ... }
  Returns: full examination JSON + case metadata

GET /api/health
  Returns: { status: "ok", service: "eagleeye-forensics-api", version: "1.0.0" }
```

---

### 5. Web Dashboard (`ui/index.html`)

Single self-contained HTML file. Five pages, all with live API connections:

| Page | Key Feature |
|------|-------------|
| Overview | SVG forgery gauge, anomaly breakdown bar chart, case fact cards |
| Findings | 18-row table filterable by severity and category |
| Expert Report | Full FSL-format report, Export Court PDF via `window.print()` |
| Upload & Detect | Drag-and-drop file upload, step-by-step animation, live result render |
| New Case | Validated form with dynamic observation rows, result card injection |

---

## Data Flows

### Path A — PDF Upload

```
User drops PDF on Upload & Detect page
  → POST /api/examine (multipart/form-data)
  → api.js reads buffer as latin1
  → Regex scans for metadata keywords in raw bytes
  → observations[] array built from real extracted signals
  → runFullExamination(document_type, observations)
  → JSON result rendered in browser
```

### Path B — Bob Conversation

```
Examiner switches to forensic-examiner mode in Bob
  → Bob auto-starts eagleeye-forensics MCP server (STDIO)
  → Bob loads 4 skills + 2 rule files
  → Examiner pastes case JSON or describes observations verbally
  → Bob calls classify_anomaly for each finding
  → Bob calls score_forgery_confidence
  → Bob calls map_to_standards
  → Bob calls fetch_case_precedents
  → Bob drafts 7-section court report using report-format.md rules
```

### Path C — New Case Form

```
Examiner fills New Case form in dashboard
  → POST /api/case (JSON body)
  → api.js validates required fields
  → runFullExamination(document_type, observations)
  → Result card injected below the form with score + findings summary
```

---

## Technology Choices

| Decision | Choice | Reason |
|----------|--------|--------|
| Runtime | Node.js v24 | Bundled in repo (node.exe) — zero install friction |
| Module system | ES Modules | Clean import/export, aligns with MCP SDK requirements |
| HTTP framework | Express 4 | Minimal, stable, zero config needed |
| File parsing | Raw buffer (latin1) | No native binary dependencies (exiftool, poppler) needed |
| Frontend | Vanilla JS | No build step, single file, works offline |
| PDF export | window.print() | Browser-native, no server-side library required |
| MCP transport | STDIO | Bob default; no port conflicts, auto-managed lifecycle |

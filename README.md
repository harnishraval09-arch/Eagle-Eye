# 🦅 EagleEye — AI-Powered Document Forgery Detection Assistant

> **IBM Bob Hackathon Submission**
> _Powered by IBM Bob · ASTM E2388 · Indian Evidence Act Section 45_

---

## The Problem

Document forgery is a public safety and judicial crisis in India:

| Year | Incident |
|------|----------|
| 2021 | Fake COVID vaccination certificates sold across Telangana & UP |
| 2022 | 3,000+ fake university degree cases (Education Ministry) |
| Ongoing | Forged property deeds and altered FIRs presented in courts |

Forensic document examiners work without AI assistance — examinations are manual, inconsistent across labs, and reports vary in format, creating uncertainty around court admissibility.

---

## The Solution: EagleEye

EagleEye is a **Bob-powered guided forensic examination workflow** that turns structured examiner observations into court-admissible expert opinion reports in minutes.

```
Examiner inputs observations
        ↓
Bob (forensic-examiner mode)
        ↓
classify_anomaly × N findings
        ↓
score_forgery_confidence (0–100%)
        ↓
map_to_standards (ASTM E2388 / FSL)
        ↓
fetch_case_precedents (Indian courts)
        ↓
7-section Expert Opinion Report
(Indian Evidence Act §45 compliant)
```

---

## Features

- 🔬 **6 anomaly categories**: Typography · Signature · Paper · Ink · Digital Metadata · Seal
- 📊 **Forgery confidence scoring**: 0–100% with weighted per-category breakdown
- 📚 **Standards mapping**: ASTM E2388 §6.1–6.7 + FSL Protocols 2.1–7.2
- ⚖️ **Case precedents**: 5 indexed Indian court decisions (Supreme Court to High Courts)
- 📄 **PDF upload & detect**: Real metadata extraction from PDF raw buffers
- 📝 **Court-admissible reports**: 7-section FSL format with Expert Declaration
- 🤖 **Bob integration**: Custom mode + MCP server + 4 skills + mode rules

---

## Quick Start

```powershell
# Step 1 — Install dependencies (uses bundled npm.cmd if node not on PATH)
cd mcp-server
.\npm.cmd install --prefix .. --cache "$env:TEMP\npm-cache"

# Step 2 — Start the API server
node api.js

# Step 3 — Open the dashboard
# http://localhost:3001
```

Full instructions: [`docs/setup-guide.md`](docs/setup-guide.md)

---

## Bob Integration

Switch to the **🦅 EagleEye Forensic Examiner** mode in Bob. It automatically loads:

- **Custom Mode** — QD Examiner persona with domain rules ([`.bob/custom_modes.yaml`](.bob/custom_modes.yaml))
- **MCP Server** — 4 forensic tools available to Bob in conversation ([`.bob/mcp.json`](.bob/mcp.json))
- **4 Skills** — physical exam · digital patterns · Indian Evidence Act · court report format
- **Mode Rules** — examination protocol + 7-section report template

---

## Project Structure

```
.bob/                          ← Bob AI configuration
├── custom_modes.yaml          ← forensic-examiner mode definition
├── mcp.json                   ← MCP server registration
├── rules-forensic-examiner/   ← Examination protocol + report format rules
└── skills/                    ← 4 domain knowledge skills

mcp-server/                    ← Backend source (src/)
├── forensics.js               ← Core engine: classify · score · map · precedents
├── server.js                  ← MCP STDIO server (Bob tool integration)
├── api.js                     ← Express HTTP API (frontend + REST endpoints)
└── package.json

ui/
└── index.html                 ← Dark-themed 5-page forensic dashboard

cases/
└── sample-case.json           ← Full COVID certificate forgery case (EE-2024-001)

reports/
└── EE-2024-001-report.md      ← Generated court-admissible report (92% confidence)

docs/                          ← Full documentation
demo/                          ← Screenshots and demo links
```

---

## Sample Output

**Case EE-2024-001** — Fake COVID Vaccination Certificate, Telangana Cybercrime Unit

```
Forgery Confidence Score : 92%
Classification           : HIGH CONFIDENCE FORGERY
Anomalies found          : 18 across all 6 categories
Critical findings        : Adobe Acrobat PDF creator (not NIC CoWIN backend)
                           3 XMP post-creation edit events
                           Invalid self-signed digital signature
                           Signature tracing (pen lift + no tremor)
IPC Sections             : §465 · §468 · §471
Precedent match          : State of Telangana v. Raju & Ors (2022)
```

Full report: [`reports/EE-2024-001-report.md`](reports/EE-2024-001-report.md)

---

## Standards & Legal Compliance

| Standard | Coverage |
|----------|----------|
| ASTM E2388 §6.1 | Handwriting & Signature Examination |
| ASTM E2388 §6.3 | Typography & Printing |
| ASTM E2388 §6.4 | Ink Examination |
| ASTM E2388 §6.5 | Paper & Substrate |
| ASTM E2388 §6.6 | Stamp & Seal |
| ASTM E2388 §6.7 | Digital Document |
| FSL Protocols 2.1–7.2 | Full physical + digital examination coverage |
| Indian Evidence Act §45 | Expert opinion admissibility |

---

## Documentation

| Document | Description |
|----------|-------------|
| [`docs/problem-statement.md`](docs/problem-statement.md) | What problem we're solving and why it matters |
| [`docs/solution-overview.md`](docs/solution-overview.md) | How EagleEye works end-to-end |
| [`docs/architecture.md`](docs/architecture.md) | Technical architecture with diagram |
| [`docs/setup-guide.md`](docs/setup-guide.md) | Step-by-step setup and run instructions |

---

_Built for the IBM Bob Hackathon · EagleEye Forensic Unit_

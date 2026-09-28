# Demo — EagleEye

## Live Demo

See [`live-demo-url.txt`](live-demo-url.txt) for the hosted demo URL.

To run locally: `cd mcp-server && node api.js` then open **http://localhost:3001**

---

## Demo Video

See [`demo-video-link.txt`](demo-video-link.txt) for the walkthrough video link.

Suggested video structure (~5 minutes):
1. **Problem** (30s) — real COVID certificate forgery case from Telangana 2021
2. **Bob mode demo** (90s) — paste sample case JSON, watch Bob call MCP tools live
3. **Dashboard demo** (90s) — Upload & Detect → New Case → Expert Report → PDF export
4. **Architecture** (60s) — system diagram walkthrough
5. **Standards** (30s) — ASTM E2388 + Indian Evidence Act §45 compliance callout

---

## Screenshots

Place screenshots in the `screenshots/` folder. Suggested filenames:

| Filename | Content |
|----------|---------|
| `01-overview.png` | Dashboard Overview — forgery gauge at 92%, anomaly breakdown chart |
| `02-findings.png` | Findings table — 18 anomalies with severity filter active |
| `03-report.png` | Expert Opinion Report — full 7-section FSL format |
| `04-upload.png` | Upload & Detect — PDF analysis step animation |
| `05-new-case.png` | New Case form — structured observation submission |
| `06-bob-mode.png` | Bob in forensic-examiner mode — MCP tool calls visible |
| `07-bob-report.png` | Bob generating the 7-section court report in conversation |

---

## Sample Case Walkthrough

**Case EE-2024-001** — Fake COVID Vaccination Certificate
Submitted by: Telangana Cybercrime Unit (Inspector R. Naidu)

### Key Findings

| # | Code | Observation | Severity |
|---|------|-------------|----------|
| 13 | DIG | PDF Creator: Adobe Acrobat 2021 — genuine CoWIN certificates use NIC backend | Critical |
| 14 | DIG | 3 XMP post-creation edit events — genuine certificates have zero modification events | Critical |
| 15 | DIG | Digital signature self-signed, ByteRange incomplete — modified after signing | Critical |
| 5  | SIG | Uniform pen pressure — no downstroke variation — indicates traced signature | Critical |
| 6  | SIG | Pen lift detected mid-stroke in 'S' character — tracing behaviour | Critical |
| 11 | INK | Laser toner on variable data fields — genuine uses inkjet per NIC specification | High |
| 12 | INK | Ink age test: printed within 30 days; certificate claims 14 months ago | High |

### Result

```
Forgery Confidence Score : 92%
Classification           : HIGH CONFIDENCE FORGERY
Total Anomalies          : 18 across all 6 examination categories
IPC Sections             : §465 (Forgery), §468 (Forgery for cheating), §471 (Using as genuine)
Precedent                : State of Telangana v. Raju & Ors (2022) — identical Adobe Acrobat creator pattern
```

Full input: [`../cases/sample-case.json`](../cases/sample-case.json)
Full report: [`../reports/EE-2024-001-report.md`](../reports/EE-2024-001-report.md)

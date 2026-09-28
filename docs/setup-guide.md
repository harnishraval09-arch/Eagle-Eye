# Setup Guide — EagleEye

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Node.js | v18+ (v24 bundled) | `node.exe` is bundled inside `mcp-server/` |
| npm | v9+ (v11 bundled) | `npm.cmd` is bundled inside `mcp-server/` |
| IBM Bob | Latest | For the guided AI examination workflow |
| Modern browser | Chrome / Edge / Firefox | For the web dashboard |

---

## Step 1 — Install Dependencies

### Option A — Using bundled executables (Windows, no PATH setup needed)

```powershell
# From the project root
cd mcp-server

# Install to project root (avoids permission issues on the bundled node_modules folder)
.\npm.cmd install --prefix "C:\projects\IBM hackathon" --cache "$env:TEMP\npm-cache"
```

### Option B — Using system Node.js (if node/npm are on your PATH)

```powershell
cd mcp-server
npm install
```

---

## Step 2 — Start the API Server

```powershell
# From the mcp-server/ directory
node api.js

# Expected output:
# EagleEye Forensics API running on http://localhost:3001
# Frontend: http://localhost:3001
# Health:   http://localhost:3001/api/health
```

---

## Step 3 — Open the Dashboard

Open **http://localhost:3001** in your browser.

You should see the EagleEye dark-themed dashboard with 5 pages:
- **Overview** — forgery gauge, anomaly breakdown, case facts
- **Findings** — 18-row findings table (filterable)
- **Expert Report** — full FSL court report + PDF export
- **Upload & Detect** — upload a real document for analysis
- **New Case** — submit structured observations via form

---

## Step 4 — Verify the Installation

```powershell
# Health check
Invoke-WebRequest http://localhost:3001/api/health | Select-Object -ExpandProperty Content
# Expected: {"status":"ok","service":"eagleeye-forensics-api","version":"1.0.0"}
```

---

## Setting Up Bob Integration

### Step 1 — Open Bob in this workspace

Open Bob and navigate to `C:\projects\IBM hackathon` (or wherever you cloned the repo).

### Step 2 — Bob detects the MCP server automatically

Bob reads `.bob/mcp.json` and registers the `eagleeye-forensics` MCP server on startup.

### Step 3 — Switch to the forensic-examiner mode

In Bob's mode selector, choose **🦅 EagleEye Forensic Examiner**.

Bob will automatically load:
- The QD Examiner custom mode definition
- 4 domain skills (questioned-documents, digital-forgery-patterns, indian-evidence-act, court-report-format)
- 2 mode rules (examination protocol + report format)
- The eagleeye-forensics MCP server (4 tools)

### Step 4 — Run your first examination

Paste the contents of `cases/sample-case.json` into Bob and say:
> "Examine this case and generate a court-admissible expert opinion report."

Bob will call `classify_anomaly`, `score_forgery_confidence`, `map_to_standards`, and
`fetch_case_precedents` in sequence, then draft the 7-section FSL report.

---

## MCP Server Configuration

The MCP server is registered in `.bob/mcp.json`:

```json
{
  "mcpServers": {
    "eagleeye-forensics": {
      "command": "node",
      "args": ["mcp-server/server.js"],
      "cwd": "."
    }
  }
}
```

**If `node` is not on your PATH**, update the command to the full path:

```json
{
  "mcpServers": {
    "eagleeye-forensics": {
      "command": "C:\\projects\\IBM hackathon\\mcp-server\\node.exe",
      "args": ["mcp-server/server.js"],
      "cwd": "C:\\projects\\IBM hackathon"
    }
  }
}
```

---

## Running with a Custom Port

```powershell
# PowerShell
$env:PORT = 3002
node api.js
# Open http://localhost:3002
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `npm not recognized` | npm not on system PATH | Use `.\npm.cmd` from `mcp-server/` |
| `EPERM on node_modules` | Read-only permissions on bundled folder | Use `--prefix ..` flag: `.\npm.cmd install --prefix ..` |
| `Cannot find package 'express'` | node_modules in wrong location | Run install with `--prefix "C:\projects\IBM hackathon"` |
| Port 3001 already in use | Another process on the port | Set `$env:PORT=3002` before starting |
| MCP server not connecting | `node` not on PATH for Bob | Use full path to `node.exe` in `.bob/mcp.json` |
| PDF metadata not extracted | Image-only PDF (scanned) | Only PDFs with embedded text/metadata are analysed; image PDFs require OCR tools |
| Bob skills not loading | Skill SKILL.md missing `name` field | Check `.bob/skills/*/SKILL.md` frontmatter |

---

## API Reference

### POST /api/examine

Upload a document for automatic forensic analysis.

**Request**: `multipart/form-data`
- `file` (required) — document file (.pdf, .jpg, .png, .tiff, .docx)
- `document_type` (optional, default: "Unknown Document") — e.g. "COVID Vaccination Certificate"

**Response**: Full examination JSON including `classified_anomalies`, `score`, `standards`, `precedents`

---

### POST /api/case

Submit structured case observations for forensic analysis.

**Request**: `application/json`
```json
{
  "case_id": "EE-2024-001",
  "document_type": "COVID Vaccination Certificate",
  "submitted_by": "Inspector R. Naidu",
  "examiner": "Dr. A. Sharma",
  "purpose": "Determine if certificate is genuine",
  "observations": [
    { "field": "typography font", "text": "Arial used in header; Times New Roman in patient name" },
    { "field": "digital metadata creator", "text": "PDF Creator: Adobe Acrobat 2021" }
  ]
}
```

**Response**: Full examination JSON + case metadata

---

### GET /api/health

Service health check. Returns `{"status":"ok","service":"eagleeye-forensics-api","version":"1.0.0"}`.

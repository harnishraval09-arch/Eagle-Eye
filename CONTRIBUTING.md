# Contributing to EagleEye

Thank you for your interest in EagleEye. This is an IBM Bob Hackathon project.

---

## Development Setup

Follow the [Setup Guide](docs/setup-guide.md) to get the project running locally.

---

## Project Structure

```
.bob/               — Bob AI configuration (modes, skills, rules, MCP registration)
mcp-server/         — Node.js backend (forensic engine + MCP server + REST API)
ui/                 — Web dashboard (single-file HTML/CSS/JS)
cases/              — Sample case JSON files
reports/            — Generated court report output files
docs/               — Written documentation
demo/               — Screenshots, video link, live demo link
```

---

## Adding a New Anomaly Category

1. Add a new entry to `CATEGORY_MAP` in [`mcp-server/forensics.js`](mcp-server/forensics.js):
```js
{
  keywords: ["keyword1", "keyword2"],
  type: "XXX",
  label: "New Category Label",
  baseWeight: 15,
  astm: "ASTM E2388 §6.X — Section Title",
  fsl:  "FSL Protocol X.X — Protocol Title"
}
```

2. Add the corresponding entry to `STANDARDS` in `forensics.js`:
```js
XXX: {
  full_name: "Full Category Name",
  astm: { section: "ASTM E2388 §6.X", title: "...", checklist: ["..."] },
  fsl:  { section: "FSL Protocol X.X", title: "...", checklist: ["..."] }
}
```

3. Update `.bob/skills/questioned-documents/SKILL.md` with the examination method
4. Update `.bob/rules-forensic-examiner/01-examination-protocol.md` with the new type code

---

## Adding a New Case Precedent

Add a new entry to `CASE_DATABASE` in [`mcp-server/forensics.js`](mcp-server/forensics.js):

```js
{
  case_name: "Party v. Party",
  court: "Court Name",
  year: YYYY,
  tags: ["keyword1", "keyword2"],   // used for relevance matching
  ipc_sections: ["IPC §XXX"],
  relevance: "Why this case is relevant to document forgery",
  qd_role: "What the QD examiner's contribution was",
  outcome: "Court outcome and sentence"
}
```

---

## Code Style

- ES Modules (`import`/`export`) throughout the codebase
- No TypeScript — plain JavaScript
- No build step — run directly with `node`
- Pure functions in `forensics.js` — no side effects, no external API calls
- Follow existing naming conventions (camelCase for functions/variables)

---

## Submitting a Case File

Case input files live in `cases/`. Format:

```json
{
  "case_id": "EE-YYYY-NNN",
  "document_type": "Document Type",
  "date_received": "DD/MM/YYYY",
  "submitted_by": "Name and designation",
  "reference_no": "Reference number",
  "examiner": "Dr. Name",
  "purpose": "Examination purpose",
  "observations": [
    { "field": "anomaly field", "text": "Observed anomaly description" }
  ]
}
```

---

## Reporting Issues

Open an issue with:
1. What you were doing
2. What you expected to happen
3. What actually happened
4. Your Node.js version (`node --version`)
5. Your operating system

---
name: court-report-format
description: Activate when generating the final expert opinion report. Provides the exact FSL-standard 7-section report structure, table formats, confidence score language, and declaration conventions used in Indian forensic labs.
---

# FSL Expert Opinion Report — Complete Format Guide

## Full Report Template

Copy and fill in this exact structure for every generated report:

---

```
================================================================
                    EXPERT OPINION REPORT
================================================================
Organization : EagleEye Forensic Unit / [FSL Name]
Case No      : [CASE_ID]
Ref No       : [REF_NO]
Date of Report: [DD/MM/YYYY]
----------------------------------------------------------------
Document Type : [e.g. COVID Vaccination Certificate]
Submitted by  : [Authority Name and Designation]
Date Received : [DD/MM/YYYY]
Examined by   : [Examiner Name], [Credentials]
================================================================
```

---

## SECTION 1 — BRIEF FACTS

State in 2–3 sentences:
- Who submitted the document and why
- What offence or dispute it relates to
- What question the examination is meant to answer

*Example:*
> "The document was submitted by the Telangana Cybercrime Unit in connection with
> Case No. CR-2024/TG/001 relating to suspected use of a forged COVID vaccination
> certificate. The examination was requested to determine whether the certificate
> is genuine or fabricated."

---

## SECTION 2 — DOCUMENTS RECEIVED FOR EXAMINATION

Numbered list format:
```
1. One (1) printed COVID Vaccination Certificate, A4 size, bearing name [REDACTED],
   received in a sealed envelope, condition: fair.
2. One (1) reference specimen — genuine CoWIN certificate, provided by NIC for comparison.
```

---

## SECTION 3 — EXAMINATION CONDUCTED

List all methods used:
```
The following examinations were conducted:
(a) Visual examination under white light (naked eye and 10x loupe)
(b) UV/Ultraviolet light examination (365nm and 254nm)
(c) Infrared examination using VSC6000
(d) Microscopic examination at 20x and 40x magnification
(e) Digital metadata analysis using ExifTool v12.6 and PDFInfo
(f) PDF structural analysis using MuPDF tools
(g) Comparison with genuine reference specimen provided by [authority]
```

---

## SECTION 4 — FINDINGS TABLE

Use this exact table format. List EVERY anomaly on its own row.

| # | Code | Anomaly Type | Observation | Severity | Standard Reference |
|---|------|-------------|-------------|----------|--------------------|
| 1 | TYP | Typography | Font family inconsistency in patient name field (Arial vs Times New Roman) | High | ASTM E2388 §6.3 |
| 2 | DIG | Digital Metadata | Creator field shows Adobe Acrobat 2021; genuine CoWIN certificates show NIC portal | Critical | FSL Protocol 7.2 |
| 3 | PAP | Paper | UV fluorescence absent; genuine CoWIN certificates exhibit specific fluorescence pattern | Medium | ASTM E2388 §6.5 |

**Severity scale:**
- **Low**: Minor anomaly, likely explainable
- **Medium**: Notable anomaly, warrants attention
- **High**: Significant anomaly, strong indicator
- **Critical**: Definitive indicator of tampering/fabrication

---

## SECTION 5 — OPINION

### Confidence Score Block
```
Forgery Confidence Score: [XX]%
Classification          : [Likely Genuine / Inconclusive / Probable Forgery / High Confidence Forgery]

Anomaly Breakdown:
  Typography (TYP)       : [X] anomalies — Weight: [X]%
  Digital Metadata (DIG) : [X] anomalies — Weight: [X]%
  Paper (PAP)            : [X] anomalies — Weight: [X]%
  Ink (INK)              : [X] anomalies — Weight: [X]%
  Signature (SIG)        : [X] anomalies — Weight: [X]%
  Seal/Stamp (SEA)       : [X] anomalies — Weight: [X]%
```

### Opinion Paragraph (use this language)
> "Based on the examination conducted, it is my opinion that the submitted [document type]
> bearing [identifiers] shows [X] anomalies across [Y] categories as detailed in Section 4.
> The cumulative forgery confidence score is [Z]%, placing it in the '[classification]' range.
> The document is [likely / probably / in all probability] [forged / tampered with / fabricated],
> and is NOT consistent with documents issued by [issuing authority] through [portal/process]."

---

## SECTION 6 — RELEVANT CASE PRECEDENTS

Format each precedent as:
> **[Case Name, Court, Year]**
> *IPC Sections*: [list]
> *Relevance*: [1 sentence]
> *Outcome*: [1 sentence]

---

## SECTION 7 — EXPERT DECLARATION

(See `indian-evidence-act` skill for the full declaration template.)
Always include: Full name, designation, organization, signature line, date, place.

---

## Formatting Rules
- Use Markdown for the report file (`.md` extension)
- Headings use `##` for sections, `###` for subsections
- Tables must be pipe-delimited Markdown tables
- Case IDs, names, and identifying information go in `[BRACKETS]` as placeholders
- Dates always in `DD/MM/YYYY` format
- Confidence score always as a percentage with one decimal place (e.g. `87.0%`)

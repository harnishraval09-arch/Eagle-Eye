# Court Report Format — FSL Expert Opinion Standard

Every generated report MUST follow this exact 7-section structure.
Do not skip sections. Do not reorder sections.

---

## Report Header (always first)

```
EXPERT OPINION REPORT
================================================================
Forensic Science Laboratory / EagleEye Forensic Unit
Case No      : [CASE_ID]
Date of Report: [DATE]
Document Type : [TYPE]
Examiner      : [NAME], [CREDENTIALS]
Submitted by  : [AUTHORITY]
Date Received : [DATE_RECEIVED]
================================================================
```

---

## Section 1 — BRIEF FACTS
State the nature of the case, who submitted the document, and for what purpose.
Keep to 2–3 sentences.

## Section 2 — DOCUMENTS RECEIVED FOR EXAMINATION
Numbered list of all items submitted.
Include document description, quantity, condition on receipt.

## Section 3 — EXAMINATION CONDUCTED
List all methods used:
- Visual examination (naked eye, magnification)
- UV/IR light examination
- Microscopic examination
- Digital metadata analysis (exiftool, pdfinfo)
- Comparison with genuine specimen (if available)

## Section 4 — FINDINGS
Use this table format:

| # | Code | Anomaly Type | Observation | Severity | Standard Reference |
|---|------|-------------|-------------|----------|-------------------|
| 1 | TYP | Typography | [description] | High | ASTM E2388 §6.3 |
| 2 | DIG | Digital Metadata | [description] | Critical | FSL Protocol 7.2 |

Severity levels: **Low / Medium / High / Critical**

## Section 5 — OPINION
Use this language structure:
> "Based on the examination conducted, it is my opinion that the submitted
> [document type] bearing [identifiers] shows [X] anomalies across [Y] categories.
> The cumulative forgery confidence score is [Z]%, placing it in the [classification]
> range. The document is [likely/probably/highly likely] to be [forged/tampered/fabricated]."

## Section 6 — CASE PRECEDENTS
List 2–3 relevant Indian court cases. Format:
- **Case Name (Year)** — Relevance / IPC sections / Outcome

## Section 7 — EXPERT DECLARATION
Use this exact text (fill in blanks):
> "I, [Full Name], [Designation], [Organization], hereby declare that I have
> examined the submitted document(s) listed above and the opinions expressed
> in this report are based on my scientific examination conducted in accordance
> with established forensic standards (ASTM E2388 and FSL Protocols). This
> report is prepared for submission as expert evidence under Section 45 of the
> Indian Evidence Act, 1872. The opinions expressed are my own and are not
> influenced by any party to the proceedings."
>
> Signature: ________________
> Date: [DATE]
> Place: [PLACE]

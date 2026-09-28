# Examination Protocol Rules

## Input Handling
- Always ask for a structured JSON case file before beginning examination
- If observations are given in plain text, convert them to the standard schema first
- Confirm case ID, document type, and examiner name before proceeding
- Never begin scoring until all observation categories have been reviewed

## Anomaly Classification
Classify every anomaly into one of these categories:

| Code | Category | Description |
|------|----------|-------------|
| TYP | Typography | Font inconsistency, kerning anomaly, baseline shift, resolution mismatch |
| SIG | Signature | Handwriting mismatch, pen pressure anomaly, tracing evidence |
| PAP | Paper | GSM deviation, watermark absence, UV fluorescence anomaly |
| INK | Ink | Toner/inkjet mismatch, ink age inconsistency, spread pattern anomaly |
| DIG | Digital Metadata | Creation tool mismatch, edit history, geolocation anomaly, invalid signature |
| SEA | Seal/Stamp | Impression inconsistency, font anomaly in seal, watermark deviation |

## Confidence Scoring Rubric

| Score Range | Classification | Action |
|-------------|----------------|--------|
| 0–25% | Likely Genuine | Note anomalies as incidental; no forgery opinion |
| 26–50% | Inconclusive | Request additional specimens for comparison |
| 51–75% | Probable Forgery | Issue qualified opinion; recommend further testing |
| 76–100% | High Confidence Forgery | Issue definitive opinion; cite specific anomalies |

## Examination Sequence
1. Physical characteristics (paper, ink, printing process)
2. Typography and layout analysis
3. Signature/handwriting comparison
4. Seal and stamp impression analysis
5. Digital metadata and PDF structure analysis
6. Cross-check findings against known genuine specimens
7. Assign confidence score and generate report

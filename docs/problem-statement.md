# Problem Statement — Document Forgery in India

## Context

Document forgery is not a fringe crime in India — it is systemic, high-volume, and
increasingly sophisticated. Three real categories define the scope:

---

### 1. Health Document Forgery

**Fake COVID vaccination certificates** were sold in bulk across Telangana and Uttar Pradesh
in 2021. Sellers charged ₹500–2,000 per certificate. The certificates were passed at
workplaces, airports, and government offices. The Telangana Cybercrime Unit alone registered
dozens of FIRs. The forgeries were identified when digital metadata revealed Adobe Acrobat
as the PDF creator instead of the NIC CoWIN portal — a discrepancy a forensic examiner can
spot in seconds but an untrained official cannot.

### 2. Educational Credential Forgery

The Education Ministry's 2022 report recorded **3,000+ fake degree cases**. Forged degrees
from IITs, IIMs, and central universities have been used to secure government jobs, bank
loans, and professional licences. Fake universities (degree mills) also sell UGC-style
certificates indistinguishable from genuine documents to the untrained eye.

### 3. Property and Legal Document Forgery

Courts regularly receive forged property sale deeds, altered FIRs, and fabricated affidavits.
These cases are particularly damaging because they can result in wrongful property transfers
and miscarriages of justice. The Supreme Court's ruling in Ram Prasad v. State of UP (2019)
sentenced a forger to life imprisonment — yet the case required 12 handwriting specimens and
months of expert analysis.

---

## The Forensic Examiner's Problem

A **Questioned Documents (QD) Examiner** must:

1. Examine the physical document across 6 categories:
   - Typography / Printing
   - Signature / Handwriting
   - Paper / Substrate
   - Ink / Printing Process
   - Digital Metadata / PDF Structure
   - Seal / Stamp / Impression

2. Record structured observations about each anomaly
3. Classify each finding to an anomaly type and severity
4. Map findings to ASTM E2388 or FSL Protocol examination standards
5. Calculate an overall forgery confidence level
6. Retrieve relevant legal precedents
7. Draft a court-admissible 7-section expert opinion report under Indian Evidence Act §45

This process is **entirely manual** today. It is slow (days to weeks per case), inconsistent
across different examiners and labs, and produces reports of varying quality. A poorly
structured report can be challenged in court and excluded as evidence.

---

## The Gap

| Problem | Current State |
|---------|--------------|
| Anomaly classification | Manual, based on individual examiner experience |
| Confidence scoring | Subjective, no standardised formula |
| Standards mapping | Examiner must know ASTM/FSL sections from memory |
| Case precedents | Manual legal research, often skipped |
| Report generation | Word-processed individually, inconsistent format |
| Admissibility | Varies; challenged when format deviates from FSL standard |

**EagleEye addresses every row in this table.**

---

## Impact Potential

If deployed to India's ~200 state Forensic Science Laboratories and courts:

- Examination time reduced from **days to minutes** per case
- Report format standardised across all FSLs — consistent court admissibility
- Junior examiners guided by the same AI-backed protocol as senior experts
- Digital forgeries (metadata, PDF structure) detectable without specialised tooling
- Case precedents surfaced automatically, strengthening legal arguments

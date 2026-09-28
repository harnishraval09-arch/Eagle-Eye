---
name: digital-forgery-patterns
description: Activate when analyzing PDF or digital document metadata for signs of tampering, unauthorized editing, or fabrication. Covers metadata analysis, PDF structure forensics, and common tool-based manipulation patterns.
---

# Digital Document Forgery Patterns

## PDF Metadata Fields to Inspect

| Field | Location | What to Check |
|-------|----------|---------------|
| `Creator` | DocInfo / XMP | Should match the issuing system (e.g. CoWIN portal, DigiLocker) |
| `Producer` | DocInfo | PDF generator library — Adobe, iText, pdflatex, etc. |
| `CreationDate` | DocInfo | When the PDF was first created |
| `ModDate` | DocInfo | When the PDF was last modified — should not exist post-signing |
| `xmp:ModifyDate` | XMP | Should match DocInfo ModDate; conflict = tampering |
| `dc:creator` | XMP | Author field — should match issuing authority |

## Critical Red Flags in Metadata

1. **Creator mismatch**: `Adobe Acrobat 2021` on a document claimed to be from a government portal
2. **Post-signing modification**: `ModDate` timestamp after `CreationDate` + digital signature date
3. **Multiple edit cycles**: `ModDate` list with 3+ entries on a document that should be generated once
4. **Tool fingerprint**: GIMP, Photoshop, or Inkscape in Producer field of an "official" document
5. **Geolocation mismatch**: GPS or timezone metadata inconsistent with issuing authority location
6. **Invalid certificate chain**: Digital signature present but certificate unverifiable or self-signed

## Common Manipulation Techniques

### Layer Tampering
- PDF retains hidden content layers with original text beneath modified text
- Check: Open in PDF reader → View → Show All Layers
- Tool: `mutool show file.pdf trailer` to inspect object structure

### Object Injection
- New content objects inserted into the existing PDF stream
- Injected objects often have higher object numbers than surrounding content
- Reveals as visual artifacts when cross-reference table is inspected

### Font Substitution
- Original font unavailable on forger's system — substituted automatically
- Substituted fonts have different metrics, causing text reflow
- Check: `pdffonts file.pdf` — embedded vs non-embedded fonts

### Image Region Replacement
- Name/date/signature fields replaced with image patches
- Original text still present in PDF stream beneath the image overlay
- Detectable with `pdfimages -list file.pdf`

### Signature Field Manipulation
- Digital signature fields repurposed or visual-only signatures added
- Check `ByteRange` in signature dictionary — must cover entire file
- `/SubFilter` should be `adbe.pkcs7.detached` for genuine Adobe signatures

## Command-Line Forensic Tools

```bash
# Extract all metadata
exiftool document.pdf

# List all PDF objects
mutool show document.pdf trailer

# Extract embedded images
pdfimages -list document.pdf

# Check fonts
pdffonts document.pdf

# Get document info
pdfinfo document.pdf

# Check for JavaScript (injection vector)
pdfextract --javascript document.pdf
```

## Government Portal Fingerprints (India)

| Portal | Expected Creator/Producer |
|--------|--------------------------|
| CoWIN (COVID certificates) | `CoWIN` or `NIC` in creator field |
| DigiLocker | `DigiLocker` or NIC-issued certificate |
| CBSE | `CBSE` document management system |
| State RTO | Vahan portal, state-specific generator |
| Income Tax | `ITD-CPC` or TRACES in producer |

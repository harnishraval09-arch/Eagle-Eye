// ─────────────────────────────────────────────────────────────────────────────
// forensics.js — Shared forensic logic used by both the MCP server (server.js)
// and the HTTP API (api.js). Pure functions, no side effects.
// ─────────────────────────────────────────────────────────────────────────────

const CATEGORY_MAP = [
  {
    keywords: ["font", "typography", "kerning", "baseline", "typeface", "character", "spacing", "resolution", "dpi", "alignment", "toner", "inkjet", "printing"],
    type: "TYP", label: "Typography / Printing Anomaly", baseWeight: 15,
    astm: "ASTM E2388 §6.3 — Typewriting and Printing Examination",
    fsl:  "FSL Protocol 3.1 — Typography Analysis"
  },
  {
    keywords: ["signature", "handwriting", "pen", "pressure", "tremor", "stroke", "cursive", "autograph", "sign", "initials", "pen lift", "tracing"],
    type: "SIG", label: "Signature / Handwriting Mismatch", baseWeight: 25,
    astm: "ASTM E2388 §6.1 — Handwriting Examination",
    fsl:  "FSL Protocol 2.1 — Signature Verification"
  },
  {
    keywords: ["paper", "gsm", "substrate", "watermark", "fiber", "fluorescence", "uv", "grain", "weight", "texture", "security thread"],
    type: "PAP", label: "Paper / Substrate Anomaly", baseWeight: 10,
    astm: "ASTM E2388 §6.5 — Paper and Substrate Examination",
    fsl:  "FSL Protocol 5.1 — Physical Substrate Analysis"
  },
  {
    keywords: ["ink", "toner", "age", "spread", "bleed", "chromatography", "solvent", "carbon", "gel", "ballpoint", "laser", "printing process"],
    type: "INK", label: "Ink / Printing Process Anomaly", baseWeight: 20,
    astm: "ASTM E2388 §6.4 — Ink Examination",
    fsl:  "FSL Protocol 4.1 — Ink Dating and Comparison"
  },
  {
    keywords: ["metadata", "creator", "producer", "moddate", "creation", "adobe", "acrobat", "pdf", "digital", "certificate", "geolocation", "timestamp", "edit", "modification", "cowin", "portal", "invalid", "signature valid", "byterange", "xmp"],
    type: "DIG", label: "Digital Metadata / PDF Structure Anomaly", baseWeight: 30,
    astm: "ASTM E2388 §6.7 — Digital Document Examination",
    fsl:  "FSL Protocol 7.2 — Metadata Forensics"
  },
  {
    keywords: ["seal", "stamp", "impression", "emboss", "rubber", "wax", "hallmark", "official mark", "notary", "dimension", "diameter"],
    type: "SEA", label: "Seal / Stamp / Impression Anomaly", baseWeight: 20,
    astm: "ASTM E2388 §6.6 — Stamp and Seal Examination",
    fsl:  "FSL Protocol 6.1 — Impression Evidence"
  }
];

const STANDARDS = {
  TYP: {
    full_name: "Typography / Printing Process Examination",
    astm: { section: "ASTM E2388 §6.3", title: "Typewriting and Printing Examination", checklist: ["Compare font metrics with reference specimen", "Check printing process (offset/laser/inkjet)", "Examine baseline alignment", "Measure kerning intervals"] },
    fsl:  { section: "FSL Protocol 3.1", title: "Typography Analysis", checklist: ["Document font inconsistencies with scale", "Photograph under oblique lighting", "Compare with known-genuine document"] }
  },
  SIG: {
    full_name: "Handwriting and Signature Examination",
    astm: { section: "ASTM E2388 §6.1", title: "Handwriting Examination", checklist: ["Obtain minimum 12 request writing samples", "Compare pen pressure patterns", "Examine stroke direction and order", "Check for tremor and retouching"] },
    fsl:  { section: "FSL Protocol 2.1", title: "Signature Verification", checklist: ["Examine under 20x stereomicroscope", "ESDA test for tracing evidence", "Compare letter proportions"] }
  },
  PAP: {
    full_name: "Paper and Substrate Examination",
    astm: { section: "ASTM E2388 §6.5", title: "Paper and Substrate Examination", checklist: ["Measure GSM and caliper thickness", "UV fluorescence test", "Check watermark (transmitted light)", "Examine security threads"] },
    fsl:  { section: "FSL Protocol 5.1", title: "Physical Substrate Analysis", checklist: ["Compare paper grade with genuine specimen", "Document fluorescence anomalies", "Microscopic fiber analysis"] }
  },
  INK: {
    full_name: "Ink and Printing Material Examination",
    astm: { section: "ASTM E2388 §6.4", title: "Ink Examination", checklist: ["Identify ink type (ballpoint/gel/inkjet/toner)", "IR examination for ink differentiation", "Check ink spread pattern under magnification", "Note any erasure or obliteration"] },
    fsl:  { section: "FSL Protocol 4.1", title: "Ink Dating and Comparison", checklist: ["TLC chromatography if required", "Compare ink formulation with dated samples", "Document toner fusion characteristics"] }
  },
  DIG: {
    full_name: "Digital Document and Metadata Examination",
    astm: { section: "ASTM E2388 §6.7", title: "Digital Document Examination", checklist: ["Extract and document all metadata fields", "Check Creator/Producer against issuing system", "Verify digital signature certificate chain", "Examine PDF object structure for injections"] },
    fsl:  { section: "FSL Protocol 7.2", title: "Metadata Forensics", checklist: ["Run exiftool — document all fields", "Check ModDate against known timeline", "Inspect PDF cross-reference table", "List all embedded objects and fonts"] }
  },
  SEA: {
    full_name: "Seal, Stamp, and Impression Examination",
    astm: { section: "ASTM E2388 §6.6", title: "Stamp and Seal Examination", checklist: ["Photograph impression under oblique light", "Measure seal dimensions and compare", "Check ink distribution pattern", "Verify embossing depth if applicable"] },
    fsl:  { section: "FSL Protocol 6.1", title: "Impression Evidence", checklist: ["Cast or photograph seal impression", "Compare with genuine specimen", "Examine rubber/metal die characteristics"] }
  }
};

const CASE_DATABASE = [
  {
    case_name: "State of Telangana v. Raju & Ors", court: "Telangana High Court", year: 2022,
    tags: ["covid certificate", "vaccination", "digital tampering", "metadata", "adobe", "creator"],
    ipc_sections: ["IPC §465", "IPC §468", "IPC §471"],
    relevance: "Accused sold forged COVID vaccination certificates; digital metadata showed Adobe Acrobat as creator instead of CoWIN portal.",
    qd_role: "QD examiner's digital metadata analysis was primary evidence establishing fabrication.",
    outcome: "Conviction — 2 years rigorous imprisonment + fine."
  },
  {
    case_name: "University Grants Commission v. Fake Degree Syndicate", court: "Delhi High Court", year: 2022,
    tags: ["university degree", "education", "typography", "seal", "stamp", "font"],
    ipc_sections: ["IPC §420", "IPC §468", "IPC §471"],
    relevance: "Typography analysis and seal impression mismatches decisive in establishing forgery.",
    qd_role: "Expert report under Evidence Act S.45 accepted as primary evidence.",
    outcome: "Conviction of 7 accused."
  },
  {
    case_name: "Ram Prasad v. State of Uttar Pradesh", court: "Supreme Court of India", year: 2019,
    tags: ["property paper", "property document", "signature forgery", "handwriting", "pen pressure"],
    ipc_sections: ["IPC §467", "IPC §468", "IPC §420"],
    relevance: "Property sale deed forged through signature fabrication; QD examiner identified mismatch using 12 comparison specimens.",
    qd_role: "Handwriting examination per ASTM E2388 §6.1 — pen pressure and stroke analysis conclusive.",
    outcome: "Life imprisonment — property forgery under §467."
  },
  {
    case_name: "State of Maharashtra v. Pradeep Kumar Sharma", court: "Bombay High Court", year: 2021,
    tags: ["fir", "police record", "alteration", "ink", "age", "toner"],
    ipc_sections: ["IPC §463", "IPC §466", "IPC §471"],
    relevance: "FIR document altered post-registration; ink age analysis revealed additions made months after original recording.",
    qd_role: "Ink dating via TLC chromatography established timeline of alterations.",
    outcome: "7 years — forgery of public register under §466."
  },
  {
    case_name: "Shashi Kumar Banerjee v. Subodh Kumar Banerjee", court: "Supreme Court of India", year: 1964,
    tags: ["handwriting", "signature", "expert opinion", "evidence"],
    ipc_sections: ["Indian Evidence Act §45"],
    relevance: "Landmark: expert QD opinion must be corroborated and is not conclusive in isolation.",
    qd_role: "Sets the legal standard for how QD expert evidence is weighed by courts.",
    outcome: "Precedent: Court must independently assess comparison; expert opinion is one piece of evidence."
  }
];

// ─── TOOL IMPLEMENTATIONS ─────────────────────────────────────────────────────

/**
 * Classify a single observation into a forensic anomaly category.
 */
export function classifyAnomaly(observation, field) {
  const combined = (observation + " " + field).toLowerCase();
  let best = null;
  let bestScore = 0;
  for (const cat of CATEGORY_MAP) {
    const score = cat.keywords.filter(kw => combined.includes(kw)).length;
    if (score > bestScore) { bestScore = score; best = cat; }
  }
  if (!best) {
    best = { type: "UNK", label: "Unclassified Anomaly", baseWeight: 5,
      astm: "ASTM E2388 §6.0 — General Document Examination",
      fsl:  "FSL Protocol 1.0 — General Examination" };
  }
  const severity =
    best.baseWeight >= 25 ? "Critical" :
    best.baseWeight >= 20 ? "High" :
    best.baseWeight >= 10 ? "Medium" : "Low";
  return {
    anomaly_type: best.type, category_label: best.label,
    severity, confidence_weight: best.baseWeight,
    observation, field,
    standards: { astm: best.astm, fsl: best.fsl }
  };
}

/**
 * Score overall forgery confidence from an array of classified anomalies.
 */
export function scoreForgeryConfidence(anomalies, document_type) {
  if (!anomalies.length) return { confidence_score: 0, classification: "Likely Genuine", anomaly_count: 0, category_summary: {}, detailed_breakdown: [] };
  const MULT = { Critical: 1.5, High: 1.2, Medium: 1.0, Low: 0.7 };
  let weightedSum = 0, maxPossible = 0;
  const breakdown = anomalies.map(a => {
    const m = MULT[a.severity] || 1.0;
    const w = a.confidence_weight * m;
    weightedSum += w; maxPossible += 45;
    return { type: a.anomaly_type, label: a.category_label, severity: a.severity,
      base_weight: a.confidence_weight, weighted_contribution: Math.round(w),
      observation: a.observation };
  });
  const score = Math.min(100, Math.round((weightedSum / maxPossible) * 100));
  const classification =
    score <= 25 ? "Likely Genuine" :
    score <= 50 ? "Inconclusive — Further Examination Recommended" :
    score <= 75 ? "Probable Forgery" : "High Confidence Forgery";
  const byType = {};
  for (const b of breakdown) {
    if (!byType[b.type]) byType[b.type] = { label: b.label, count: 0, total_weight: 0 };
    byType[b.type].count++;
    byType[b.type].total_weight += b.weighted_contribution;
  }
  return { document_type, confidence_score: score, classification, anomaly_count: anomalies.length, category_summary: byType, detailed_breakdown: breakdown };
}

/**
 * Map anomaly type codes to ASTM E2388 and FSL Protocol standards.
 */
export function mapToStandards(anomaly_types) {
  const unique = [...new Set(anomaly_types)];
  const mapped = unique.map(type => ({
    type,
    ...(STANDARDS[type] || {
      full_name: "General Document Examination",
      astm: { section: "ASTM E2388 §6.0", title: "General Examination", checklist: ["Document all visible anomalies"] },
      fsl:  { section: "FSL Protocol 1.0", title: "General Examination Protocol", checklist: ["Standard visual examination"] }
    })
  }));
  return { standards_mapping: mapped, total_standards_referenced: mapped.length };
}

/**
 * Fetch relevant Indian court case precedents.
 */
export function fetchCasePrecedents(document_type, forgery_type) {
  const combined = (document_type + " " + forgery_type).toLowerCase();
  const scored = CASE_DATABASE.map(c => ({
    ...c, _score: c.tags.filter(t => combined.includes(t)).length
  }));
  scored.sort((a, b) => b._score - a._score);
  return scored.slice(0, 3).map(({ _score, ...c }) => c);
}

/**
 * Run the full examination pipeline on a list of raw observations.
 * Each observation: { field: string, text: string }
 */
export function runFullExamination(document_type, observations) {
  // Step 1: Classify each observation
  const classified = observations
    .filter(o => o.text && o.text.trim())
    .map(o => classifyAnomaly(o.text, o.field));

  // Step 2: Score
  const scoreResult = scoreForgeryConfidence(classified, document_type);

  // Step 3: Map standards
  const types = [...new Set(classified.map(c => c.anomaly_type))];
  const standards = mapToStandards(types);

  // Step 4: Precedents
  const forgery_type = types.join(" ");
  const precedents = fetchCasePrecedents(document_type, forgery_type);

  return {
    document_type,
    classified_anomalies: classified,
    score: scoreResult,
    standards: standards.standards_mapping,
    precedents
  };
}

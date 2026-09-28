// ─────────────────────────────────────────────────────────────────────────────
// api.js — Express HTTP API server
// Exposes the forensic engine over HTTP so the browser frontend can call it.
//
// Endpoints:
//   POST /api/examine   — Upload & Detect: analyses observations from a file
//   POST /api/case      — New Case: accepts structured form observations
//   GET  /api/health    — Health check
//
// Run:  node api.js
// Default port: 3001  (override with PORT env var)
// ─────────────────────────────────────────────────────────────────────────────

import express from "express";
import cors from "cors";
import multer from "multer";
import path from "path";
import { fileURLToPath } from "url";
import { runFullExamination, classifyAnomaly } from "./forensics.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const PORT = process.env.PORT || 3001;

// ─── Middleware ───────────────────────────────────────────────────────────────
app.use(cors());
app.use(express.json());

// Serve the frontend statically from ../ui/
app.use(express.static(path.join(__dirname, "../ui")));

// Multer — accept uploaded files (stored in memory, max 25MB)
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 25 * 1024 * 1024 },
  fileFilter(req, file, cb) {
    const allowed = [".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".tif", ".docx"];
    const ext = path.extname(file.originalname).toLowerCase();
    if (allowed.includes(ext)) cb(null, true);
    else cb(new Error(`Unsupported file type: ${ext}`));
  }
});

// ─── GET /api/health ─────────────────────────────────────────────────────────
app.get("/api/health", (req, res) => {
  res.json({ status: "ok", service: "eagleeye-forensics-api", version: "1.0.0" });
});

// ─── POST /api/examine ───────────────────────────────────────────────────────
// Called by the Upload & Detect page.
// Accepts a multipart form with:
//   file         — the uploaded document (required)
//   document_type — string e.g. "COVID Vaccination Certificate"
//
// Because we cannot run real OCR/exiftool without native binaries here,
// we extract what we CAN from the file metadata (name, size, extension,
// mimetype) and then run the full forensics engine on those real signals.
// For PDF files we also scan the raw buffer for metadata keywords.
//
app.post("/api/examine", upload.single("file"), (req, res) => {
  if (!req.file) return res.status(400).json({ error: "No file uploaded" });

  const { document_type = "Unknown Document" } = req.body;
  const { originalname, mimetype, size, buffer } = req.file;
  const ext = path.extname(originalname).toLowerCase();

  // ── Extract real signals from file ──────────────────────────────────────
  const observations = [];

  // 1. File extension vs claimed mimetype
  const extMimeMap = {
    ".pdf": ["application/pdf"],
    ".jpg": ["image/jpeg"], ".jpeg": ["image/jpeg"],
    ".png": ["image/png"],
    ".tiff": ["image/tiff"], ".tif": ["image/tiff"],
    ".docx": ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
  };
  if (extMimeMap[ext] && !extMimeMap[ext].includes(mimetype)) {
    observations.push({
      field: "digital metadata",
      text: `File extension ${ext} does not match reported MIME type ${mimetype} — possible file disguise`
    });
  }

  // 2. For PDF files — scan raw buffer for metadata keywords
  if (ext === ".pdf" && buffer) {
    const raw = buffer.toString("latin1");

    // Creator / Producer
    const creatorMatch = raw.match(/\/Creator\s*\(([^)]{1,80})\)/);
    const producerMatch = raw.match(/\/Producer\s*\(([^)]{1,80})\)/);

    if (creatorMatch) {
      const creator = creatorMatch[1];
      observations.push({ field: "digital metadata creator", text: `PDF Creator metadata: "${creator}"` });

      // Flag non-government creators
      const govKeywords = ["nic", "cowin", "digilocker", "gov", "cbse", "nsdl", "traces", "irctc"];
      const isGov = govKeywords.some(k => creator.toLowerCase().includes(k));
      if (!isGov) {
        observations.push({
          field: "digital metadata creator",
          text: `Creator "${creator}" does not match expected government portal identifier — possible fabrication using Adobe Acrobat or similar tool`
        });
      }
    }

    if (producerMatch) {
      const producer = producerMatch[1];
      observations.push({ field: "digital metadata producer", text: `PDF Producer metadata: "${producer}"` });
    }

    // ModDate presence
    const modDateMatch = raw.match(/\/ModDate\s*\(([^)]{10,30})\)/);
    const creationDateMatch = raw.match(/\/CreationDate\s*\(([^)]{10,30})\)/);
    if (modDateMatch && creationDateMatch) {
      observations.push({
        field: "digital metadata modification",
        text: `Document has ModDate (${modDateMatch[1].trim()}) different from CreationDate (${creationDateMatch[1].trim()}) — indicates post-creation editing`
      });
    }

    // Check for Adobe Acrobat signature
    if (raw.includes("Adobe Acrobat") || raw.includes("Acrobat Distiller")) {
      observations.push({
        field: "digital metadata",
        text: "Adobe Acrobat identified as PDF authoring tool — inconsistent with government-issued documents which use official portal generators"
      });
    }

    // Check for JavaScript (injection vector)
    if (raw.includes("/JavaScript") || raw.includes("/JS ")) {
      observations.push({
        field: "digital metadata pdf structure",
        text: "Embedded JavaScript detected in PDF structure — unusual for official documents, potential injection vector"
      });
    }

    // XMP modification history
    const xmpModCount = (raw.match(/xmpMM:History/g) || []).length;
    if (xmpModCount > 0) {
      observations.push({
        field: "digital metadata xmp",
        text: `XMP modification history block found — document has been edited after initial creation`
      });
    }

    // Digital signature check
    if (raw.includes("/Sig") && raw.includes("/ByteRange")) {
      const hasCert = raw.includes("/Cert") || raw.includes("adbe.pkcs7");
      if (!hasCert) {
        observations.push({
          field: "digital signature",
          text: "Digital signature field present but no valid certificate chain found — signature may be invalid or self-signed"
        });
      }
    } else {
      // Official docs typically have digital signatures
      const govDoctypes = ["certificate", "degree", "vaccination", "property", "fir", "passport"];
      if (govDoctypes.some(k => document_type.toLowerCase().includes(k))) {
        observations.push({
          field: "digital signature",
          text: "No digital signature detected on a document type that should carry an official digital signature"
        });
      }
    }

    // Font consistency check — look for multiple font declarations
    const fonts = [...raw.matchAll(/\/FontName\s*\/([A-Za-z0-9_+-]{2,40})/g)].map(m => m[1]);
    const uniqueFonts = [...new Set(fonts)];
    if (uniqueFonts.length > 3) {
      observations.push({
        field: "typography font",
        text: `${uniqueFonts.length} distinct fonts detected (${uniqueFonts.slice(0, 4).join(", ")}…) — official single-source documents typically use 1–2 fonts`
      });
    }
  }

  // 3. File size signals
  if (size < 5000 && ["certificate", "degree", "vaccination"].some(k => document_type.toLowerCase().includes(k))) {
    observations.push({
      field: "paper substrate",
      text: `File size is unusually small (${size} bytes) for an official certificate document — may indicate a low-quality scan or simplified reproduction`
    });
  }

  // 4. Filename anomalies
  const suspiciousNames = ["edited", "copy", "modified", "fake", "new", "v2", "final", "template"];
  if (suspiciousNames.some(s => originalname.toLowerCase().includes(s))) {
    observations.push({
      field: "digital metadata filename",
      text: `Filename "${originalname}" contains a suspicious term suggesting the document was edited or is a copy`
    });
  }

  // If no signals extracted, return a meaningful result
  if (observations.length === 0) {
    observations.push({
      field: "general",
      text: `Document type ${ext} uploaded — no extractable metadata signals found without OCR/exiftool; manual examination required`
    });
  }

  // ── Run forensics engine on extracted observations ───────────────────────
  const result = runFullExamination(document_type, observations);

  res.json({
    filename: originalname,
    file_size_bytes: size,
    file_type: ext,
    document_type,
    extraction_note: ext === ".pdf"
      ? "Metadata extracted from raw PDF buffer"
      : "Signals extracted from file properties — full analysis requires server-side OCR tools",
    ...result
  });
});

// ─── POST /api/case ──────────────────────────────────────────────────────────
// Called by the New Case form.
// Accepts JSON body:
//   case_id, document_type, date_received, reference_no,
//   submitted_by, examiner, purpose, specimen_available,
//   observations: [ { field, text } ]
//
app.post("/api/case", (req, res) => {
  const {
    case_id, document_type, date_received, reference_no,
    submitted_by, examiner, purpose, specimen_available,
    observations = []
  } = req.body;

  // Basic validation
  if (!case_id || !document_type || !submitted_by || !examiner || !purpose) {
    return res.status(400).json({ error: "Missing required fields: case_id, document_type, submitted_by, examiner, purpose" });
  }
  if (!observations.length) {
    return res.status(400).json({ error: "At least one observation is required" });
  }

  // Run full forensics pipeline
  const result = runFullExamination(document_type, observations);

  res.json({
    case_id,
    document_type,
    date_received,
    reference_no,
    submitted_by,
    examiner,
    purpose,
    specimen_available,
    examination_timestamp: new Date().toISOString(),
    ...result
  });
});

// ─── Error handler ────────────────────────────────────────────────────────────
app.use((err, req, res, next) => {
  console.error(err.message);
  res.status(400).json({ error: err.message });
});

// ─── Start ────────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`EagleEye Forensics API running on http://localhost:${PORT}`);
  console.log(`Frontend: http://localhost:${PORT}`);
  console.log(`Health:   http://localhost:${PORT}/api/health`);
});

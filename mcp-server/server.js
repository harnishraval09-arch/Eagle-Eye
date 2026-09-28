import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { classifyAnomaly, scoreForgeryConfidence, mapToStandards, fetchCasePrecedents } from "./forensics.js";

const server = new McpServer({ name: "eagleeye-forensics", version: "1.0.0" });

// ─── TOOL 1 — classify_anomaly ───────────────────────────────────────────────
server.registerTool(
  "classify_anomaly",
  {
    description: "Classifies a single document observation into a forensic anomaly category. Returns the anomaly type code (TYP/SIG/PAP/INK/DIG/SEA), category label, severity level, and applicable standard reference.",
    inputSchema: {
      observation: z.string().describe("The raw observation text describing what was found"),
      field: z.string().describe("The document field or area where the anomaly was observed")
    }
  },
  async ({ observation, field }) => {
    const result = classifyAnomaly(observation, field);
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// ─── TOOL 2 — score_forgery_confidence ──────────────────────────────────────
server.registerTool(
  "score_forgery_confidence",
  {
    description: "Calculates an overall forgery confidence score (0–100%) from an array of classified anomaly objects.",
    inputSchema: {
      anomalies: z.array(z.object({
        anomaly_type: z.string(), category_label: z.string(),
        confidence_weight: z.number(), severity: z.string(), observation: z.string()
      })).describe("Array of anomaly objects returned by classify_anomaly"),
      document_type: z.string().describe("Type of document being examined")
    }
  },
  async ({ anomalies, document_type }) => {
    const result = scoreForgeryConfidence(anomalies, document_type);
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// ─── TOOL 3 — map_to_standards ───────────────────────────────────────────────
server.registerTool(
  "map_to_standards",
  {
    description: "Maps anomaly type codes (TYP, SIG, PAP, INK, DIG, SEA) to their ASTM E2388 and FSL Protocol sections.",
    inputSchema: {
      anomaly_types: z.array(z.string()).describe("Array of anomaly type codes, e.g. ['TYP', 'DIG', 'SIG']")
    }
  },
  async ({ anomaly_types }) => {
    const result = mapToStandards(anomaly_types);
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// ─── TOOL 4 — fetch_case_precedents ─────────────────────────────────────────
server.registerTool(
  "fetch_case_precedents",
  {
    description: "Returns relevant Indian court case precedents for a given document type and forgery pattern.",
    inputSchema: {
      document_type: z.string().describe("Type of document e.g. 'COVID certificate', 'university degree'"),
      forgery_type: z.string().describe("Type of forgery detected e.g. 'digital tampering', 'signature forgery'")
    }
  },
  async ({ document_type, forgery_type }) => {
    const result = fetchCasePrecedents(document_type, forgery_type);
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// ─── Start MCP server on STDIO ───────────────────────────────────────────────
const transport = new StdioServerTransport();
await server.connect(transport);

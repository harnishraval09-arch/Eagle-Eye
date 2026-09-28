# src/ — Source Code

All EagleEye backend source code lives in [`../mcp-server/`](../mcp-server/).

| File | Purpose |
|------|---------|
| [`../mcp-server/forensics.js`](../mcp-server/forensics.js) | Core forensic engine — classify, score, map, precedents |
| [`../mcp-server/server.js`](../mcp-server/server.js) | MCP STDIO server — exposes 4 tools to Bob |
| [`../mcp-server/api.js`](../mcp-server/api.js) | Express HTTP API — serves frontend + REST endpoints |
| [`../mcp-server/package.json`](../mcp-server/package.json) | Node.js project manifest |

The frontend is a single-file dashboard: [`../ui/index.html`](../ui/index.html)

Bob configuration (mode, skills, rules, MCP registration) is in [`../.bob/`](../.bob/).

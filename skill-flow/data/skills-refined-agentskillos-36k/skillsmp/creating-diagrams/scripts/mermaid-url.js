#!/usr/bin/env node
// Generate mermaid.live URL from stdin
// Usage: echo "sequenceDiagram..." | node mermaid-url.js
// Requires: pako in cwd's node_modules

const { createRequire } = require("module");
const require2 = createRequire(process.cwd() + "/");
const pako = require2("pako");

let input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => (input += chunk));
process.stdin.on("end", () => {
  const state = {
    code: input.trim(),
    mermaid: { theme: "default" },
    autoSync: true,
    updateDiagram: true,
  };
  const json = JSON.stringify(state);
  const compressed = pako.deflate(json, { level: 9 });
  const base64 = Buffer.from(compressed).toString("base64url");
  console.log(`https://mermaid.live/edit#pako:${base64}`);
});

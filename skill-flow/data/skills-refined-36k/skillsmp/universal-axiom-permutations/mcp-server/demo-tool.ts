#!/usr/bin/env node

/**
 * Quick demo of the analyze_permutation tool
 */

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function demo() {
  const serverPath = join(__dirname, "build", "mcp-server", "index.js");
  const transport = new StdioClientTransport({
    command: "node",
    args: [serverPath],
  });

  const client = new Client(
    { name: "demo-client", version: "0.1.0" },
    { capabilities: {} }
  );

  await client.connect(transport);

  console.log("🔍 Analyzing a problematic system permutation...\n");

  // Analyze a system with issues
  const response = await client.callTool({
    name: "analyze_permutation",
    arguments: {
      impulses: 1.0,
      elements: -0.5, // Detrimental element!
      pressure: 3.5, // High pressure!
      subjectivity: 0.85, // Very subjective
      purpose: 0.3, // Low purpose
      time: 1.0,
      n: 3,
    },
  });

  const analysis = JSON.parse(response.content[0].text);

  console.log("📊 ANALYSIS RESULTS:\n");
  console.log("Foundation Layer:", analysis.foundation_layer.status);
  console.log("  →", analysis.foundation_layer.notes);
  console.log("\nCognitive Layer:");
  console.log("  → Objectivity:", analysis.cognitive_layer.objectivity);
  console.log("  → Subjectivity:", analysis.cognitive_layer.subjectivity);
  console.log("  →", analysis.cognitive_layer.notes);
  console.log("\nOverall Intelligence:", analysis.overall.intelligence.toFixed(2));
  console.log("Coherence:", analysis.overall.coherence.toFixed(3), `(${analysis.overall.coherence_status})`);

  console.log("\n💡 RECOMMENDATIONS:");
  analysis.overall.recommendations.forEach((rec: string, i: number) => {
    console.log(`  ${i + 1}. ${rec}`);
  });

  await client.close();
  console.log("\n✨ Demo complete!\n");
}

demo().catch(console.error);

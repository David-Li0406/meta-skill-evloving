#!/usr/bin/env node

/**
 * Comprehensive test suite for Universal Axiom MCP Server
 * Tests all tools, resources, and prompts
 */

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { spawn } from "child_process";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

interface TestResult {
  name: string;
  passed: boolean;
  error?: string;
  duration: number;
}

const results: TestResult[] = [];

async function runTest(name: string, testFn: () => Promise<void>): Promise<void> {
  const start = Date.now();
  try {
    await testFn();
    results.push({ name, passed: true, duration: Date.now() - start });
    console.log(`✓ ${name}`);
  } catch (error) {
    results.push({
      name,
      passed: false,
      error: error instanceof Error ? error.message : String(error),
      duration: Date.now() - start,
    });
    console.log(`✗ ${name}`);
    console.log(`  Error: ${error instanceof Error ? error.message : String(error)}`);
  }
}

async function testMCPServer() {
  console.log("Testing Universal Axiom MCP Server...\n");

  // Start the server
  const serverPath = join(__dirname, "build", "mcp-server", "index.js");
  const serverProcess = spawn("node", [serverPath], {
    stdio: ["pipe", "pipe", "pipe"],
  });

  // Create client
  const transport = new StdioClientTransport({
    command: "node",
    args: [serverPath],
  });

  const client = new Client(
    {
      name: "test-client",
      version: "0.1.0",
    },
    {
      capabilities: {},
    }
  );

  try {
    // Connect to server
    await runTest("Server connection", async () => {
      await client.connect(transport);
    });

    // Test 1: List tools
    await runTest("List tools", async () => {
      const response = await client.listTools();
      if (!response.tools || response.tools.length !== 8) {
        throw new Error(`Expected 8 tools, got ${response.tools?.length || 0}`);
      }
      const expectedTools = [
        "compute_intelligence",
        "evolve_system",
        "apply_pressure",
        "adjust_subjectivity",
        "simulate_evolution",
        "simulate_contradiction_resolution",
        "get_coherence_metric",
        "analyze_permutation",
      ];
      const toolNames = response.tools.map((t) => t.name);
      for (const expected of expectedTools) {
        if (!toolNames.includes(expected)) {
          throw new Error(`Missing tool: ${expected}`);
        }
      }
    });

    // Test 2: Compute intelligence
    await runTest("Tool: compute_intelligence", async () => {
      const response = await client.callTool({
        name: "compute_intelligence",
        arguments: {
          impulses: 1.5,
          elements: 2.0,
          pressure: 1.2,
          subjectivity: 0.3,
          purpose: 1.0,
          time: 2.0,
          n: 5,
        },
      });

      if (!response.content || response.content.length === 0) {
        throw new Error("No content returned");
      }

      const result = JSON.parse(response.content[0].text);
      if (typeof result.intelligence !== "number") {
        throw new Error("Intelligence value not returned");
      }
      if (!result.foundation || !result.dynamic || !result.cognitive) {
        throw new Error("Missing layer information");
      }
    });

    // Test 3: Simulate evolution
    await runTest("Tool: simulate_evolution", async () => {
      const response = await client.callTool({
        name: "simulate_evolution",
        arguments: {
          impulses: 1.0,
          elements: 1.0,
          pressure: 1.0,
          subjectivity: 0.2,
          purpose: 1.0,
          time: 1.0,
          n: 1,
          steps: 5,
          delta_time: 1.0,
        },
      });

      const result = JSON.parse(response.content[0].text);
      if (result.simulation_type !== "evolution") {
        throw new Error("Wrong simulation type");
      }
      if (!result.history || result.history.length !== 6) {
        // Initial state + 5 steps
        throw new Error(`Expected 6 states, got ${result.history?.length || 0}`);
      }
    });

    // Test 4: Simulate contradiction resolution
    await runTest("Tool: simulate_contradiction_resolution", async () => {
      const response = await client.callTool({
        name: "simulate_contradiction_resolution",
        arguments: {
          subjectivity: 0.7,
          initial_pressure: 2.5,
          resolution_steps: 5,
        },
      });

      const result = JSON.parse(response.content[0].text);
      if (result.simulation_type !== "contradiction_resolution") {
        throw new Error("Wrong simulation type");
      }
      if (result.coherence_improvement === undefined) {
        throw new Error("No coherence improvement metric");
      }
    });

    // Test 5: Analyze permutation
    await runTest("Tool: analyze_permutation", async () => {
      const response = await client.callTool({
        name: "analyze_permutation",
        arguments: {
          impulses: 1.0,
          elements: -0.5, // Detrimental element
          pressure: 3.0, // High pressure
          subjectivity: 0.8, // High subjectivity
          purpose: 0.4,
          time: 1.0,
          n: 3,
        },
      });

      const result = JSON.parse(response.content[0].text);
      if (!result.foundation_layer || !result.dynamic_layer || !result.cognitive_layer) {
        throw new Error("Missing diagnostic layers");
      }
      if (!result.overall || !result.overall.recommendations) {
        throw new Error("Missing recommendations");
      }
      if (result.overall.recommendations.length === 0) {
        throw new Error("Expected recommendations for problematic permutation");
      }
    });

    // Test 6: Get coherence metric
    await runTest("Tool: get_coherence_metric", async () => {
      const state = {
        n: 3,
        foundation: {
          A_impulses: 1.0,
          B_elements: 1.0,
          C_pressure: 1.0,
          product: 1.0,
        },
        dynamic: {
          E_n: 53,
          F_n: 3,
          product: 212,
        },
        cognitive: {
          X_subjectivity: 0.2,
          X_objectivity: 0.8,
          Y_purpose: 1.0,
          Z_time: 1.0,
          product: 0.8,
        },
        intelligence: 169.6,
      };

      const response = await client.callTool({
        name: "get_coherence_metric",
        arguments: { current_state: state },
      });

      const result = JSON.parse(response.content[0].text);
      if (typeof result.coherence !== "number") {
        throw new Error("Coherence metric not returned");
      }
      if (!result.interpretation) {
        throw new Error("No interpretation provided");
      }
    });

    // Test 7: Evolve system
    await runTest("Tool: evolve_system", async () => {
      const state = {
        n: 1,
        foundation: {
          A_impulses: 1.0,
          B_elements: 1.0,
          C_pressure: 1.0,
          product: 1.0,
        },
        dynamic: {
          E_n: 5,
          F_n: 1,
          product: 10,
        },
        cognitive: {
          X_subjectivity: 0.0,
          X_objectivity: 1.0,
          Y_purpose: 1.0,
          Z_time: 1.0,
          product: 1.0,
        },
        intelligence: 10,
      };

      const response = await client.callTool({
        name: "evolve_system",
        arguments: {
          current_state: state,
          steps: 3,
          delta_time: 1.0,
        },
      });

      const result = JSON.parse(response.content[0].text);
      if (result.steps !== 3) {
        throw new Error(`Expected 3 steps, got ${result.steps}`);
      }
      if (!result.final_state) {
        throw new Error("No final state returned");
      }
    });

    // Test 8: Apply pressure
    await runTest("Tool: apply_pressure", async () => {
      const state = {
        n: 1,
        foundation: {
          A_impulses: 1.0,
          B_elements: 1.0,
          C_pressure: 1.0,
          product: 1.0,
        },
        dynamic: {
          E_n: 5,
          F_n: 1,
          product: 10,
        },
        cognitive: {
          X_subjectivity: 0.0,
          X_objectivity: 1.0,
          Y_purpose: 1.0,
          Z_time: 1.0,
          product: 1.0,
        },
        intelligence: 10,
      };

      const response = await client.callTool({
        name: "apply_pressure",
        arguments: {
          current_state: state,
          pressure_delta: 1.5,
        },
      });

      const result = JSON.parse(response.content[0].text);
      if (result.pressure_applied !== 1.5) {
        throw new Error("Pressure delta not applied correctly");
      }
      if (!result.new_state) {
        throw new Error("No new state returned");
      }
    });

    // Test 9: Adjust subjectivity
    await runTest("Tool: adjust_subjectivity", async () => {
      const state = {
        n: 1,
        foundation: {
          A_impulses: 1.0,
          B_elements: 1.0,
          C_pressure: 1.0,
          product: 1.0,
        },
        dynamic: {
          E_n: 5,
          F_n: 1,
          product: 10,
        },
        cognitive: {
          X_subjectivity: 0.5,
          X_objectivity: 0.5,
          Y_purpose: 1.0,
          Z_time: 1.0,
          product: 0.5,
        },
        intelligence: 5,
      };

      const response = await client.callTool({
        name: "adjust_subjectivity",
        arguments: {
          current_state: state,
          subjectivity_delta: -0.2, // Increase objectivity
        },
      });

      const result = JSON.parse(response.content[0].text);
      if (result.subjectivity_change !== -0.2) {
        throw new Error("Subjectivity delta not applied correctly");
      }
      if (!result.new_state) {
        throw new Error("No new state returned");
      }
    });

    // Test 10: List resources
    await runTest("List resources", async () => {
      const response = await client.listResources();
      if (!response.resources || response.resources.length === 0) {
        throw new Error("No resources returned");
      }
      const expectedResources = [
        "axiom://framework/overview",
        "axiom://framework/formula",
        "axiom://framework/layers",
        "axiom://usage/reasoning",
        "axiom://examples/debugging",
        "axiom://examples/decision-making",
      ];
      const resourceUris = response.resources.map((r) => r.uri);
      for (const expected of expectedResources) {
        if (!resourceUris.includes(expected)) {
          throw new Error(`Missing resource: ${expected}`);
        }
      }
    });

    // Test 11: Read resource
    await runTest("Read resource", async () => {
      const response = await client.readResource({
        uri: "axiom://framework/overview",
      });
      if (!response.contents || response.contents.length === 0) {
        throw new Error("No resource content returned");
      }
      const content = response.contents[0];
      if (content.mimeType !== "text/markdown") {
        throw new Error(`Expected markdown, got ${content.mimeType}`);
      }
      if (!content.text || content.text.length < 100) {
        throw new Error("Resource content too short or missing");
      }
    });

    // Test 12: List prompts
    await runTest("List prompts", async () => {
      const response = await client.listPrompts();
      if (!response.prompts || response.prompts.length !== 2) {
        throw new Error(`Expected 2 prompts, got ${response.prompts?.length || 0}`);
      }
      const promptNames = response.prompts.map((p) => p.name);
      if (!promptNames.includes("analyze_problem") || !promptNames.includes("reason_with_axiom")) {
        throw new Error("Missing expected prompts");
      }
    });

    // Test 13: Get prompt
    await runTest("Get prompt", async () => {
      const response = await client.getPrompt({
        name: "analyze_problem",
        arguments: {
          problem: "My application is slow and I don't know why",
        },
      });
      if (!response.messages || response.messages.length === 0) {
        throw new Error("No prompt messages returned");
      }
      const message = response.messages[0];
      if (message.role !== "user") {
        throw new Error(`Expected user role, got ${message.role}`);
      }
      if (typeof message.content !== "object" || !("text" in message.content)) {
        throw new Error("Message content not properly formatted");
      }
    });
  } finally {
    // Close client
    try {
      await client.close();
    } catch (e) {
      // Ignore close errors
    }

    // Kill server process
    serverProcess.kill();
  }

  // Print summary
  console.log("\n" + "=".repeat(60));
  console.log("Test Results:");
  console.log("=".repeat(60));

  const passed = results.filter((r) => r.passed).length;
  const failed = results.filter((r) => !r.passed).length;
  const totalTime = results.reduce((sum, r) => sum + r.duration, 0);

  console.log(`\nTotal: ${results.length} tests`);
  console.log(`✓ Passed: ${passed}`);
  console.log(`✗ Failed: ${failed}`);
  console.log(`⏱  Total time: ${totalTime}ms`);

  if (failed > 0) {
    console.log("\nFailed tests:");
    results
      .filter((r) => !r.passed)
      .forEach((r) => {
        console.log(`  - ${r.name}: ${r.error}`);
      });
  }

  console.log("\n" + "=".repeat(60));

  if (failed === 0) {
    console.log("\n🎉 All tests passed! MCP server is fully functional.\n");
    process.exit(0);
  } else {
    console.log(`\n❌ ${failed} test(s) failed.\n`);
    process.exit(1);
  }
}

testMCPServer().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});

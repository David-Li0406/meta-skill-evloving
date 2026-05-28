#!/usr/bin/env node

/**
 * Test slash command execution with sample inputs
 * Usage: node test-command.js <path-to-command-file> [arg1] [arg2] [...]
 */

const fs = require("fs");
const path = require("path");
const yaml = require("js-yaml");

function testCommand(filePath, args = []) {
  try {
    const content = fs.readFileSync(filePath, "utf8");
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);

    if (!frontmatterMatch) {
      console.error("❌ No frontmatter found");
      return;
    }

    const frontmatter = yaml.load(frontmatterMatch[1]);
    const body = content.replace(frontmatterMatch[0], "");

    console.log(`📝 Testing command: ${path.basename(filePath, ".md")}`);
    console.log(`📋 Description: ${frontmatter.description}`);

    if (frontmatter["argument-hint"]) {
      console.log(`💡 Argument hint: ${frontmatter["argument-hint"]}`);
    }

    // Simulate argument substitution
    let processedBody = body;

    // Replace $ARGUMENTS
    if (args.length > 0) {
      processedBody = processedBody.replace(/\$ARGUMENTS/g, args.join(" "));
    }

    // Replace positional arguments
    args.forEach((arg, index) => {
      const placeholder = `$${index + 1}`;
      processedBody = processedBody.replace(
        new RegExp(escapeRegExp(placeholder), "g"),
        arg,
      );
    });

    console.log("\n📤 Processed command output:");
    console.log("─".repeat(50));
    console.log(processedBody);
    console.log("─".repeat(50));

    // Check for unprocessed placeholders
    const remainingPlaceholders = processedBody.match(/\$\d+|\$ARGUMENTS/g);
    if (remainingPlaceholders) {
      console.warn(
        "\n⚠️  Unprocessed placeholders found:",
        remainingPlaceholders,
      );
    }

    console.log("\n✅ Command test complete");
  } catch (error) {
    console.error("❌ Error testing command:", error.message);
  }
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

const filePath = process.argv[2];
const args = process.argv.slice(3);

if (!filePath) {
  console.error(
    "Usage: node test-command.js <path-to-command-file> [arg1] [arg2] [...]",
  );
  process.exit(1);
}

testCommand(filePath, args);

#!/usr/bin/env node

/**
 * Validate slash command syntax and frontmatter
 * Usage: node validate-command.js <path-to-command-file>
 */

const fs = require("fs");
const path = require("path");
const yaml = require("js-yaml");

function validateCommand(filePath) {
  try {
    const content = fs.readFileSync(filePath, "utf8");
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);

    if (!frontmatterMatch) {
      console.error("❌ No frontmatter found");
      return false;
    }

    const frontmatter = yaml.load(frontmatterMatch[1]);

    // Check required fields
    if (!frontmatter.description) {
      console.error('❌ Missing required "description" field');
      return false;
    }

    console.log("✅ Frontmatter validation passed");

    // Check argument placeholders
    const body = content.replace(frontmatterMatch[0], "");
    const argPlaceholders = body.match(/\$(\d+|ARGUMENTS)/g);

    if (argPlaceholders) {
      console.log("📝 Found argument placeholders:", argPlaceholders);

      // Check if argument-hint is present when using arguments
      if (argPlaceholders.length > 0 && !frontmatter["argument-hint"]) {
        console.warn('⚠️  Using arguments but no "argument-hint" found');
      }
    }

    // Check file references
    const fileRefs = body.match(/@[\w\-./]+/g);
    if (fileRefs) {
      console.log("📁 Found file references:", fileRefs);
    }

    // Check allowed-tools if present
    if (frontmatter["allowed-tools"]) {
      console.log("🔧 Allowed tools:", frontmatter["allowed-tools"]);
    }

    console.log("✅ Command validation complete");
    return true;
  } catch (error) {
    console.error("❌ Error validating command:", error.message);
    return false;
  }
}

const filePath = process.argv[2];
if (!filePath) {
  console.error("Usage: node validate-command.js <path-to-command-file>");
  process.exit(1);
}

if (validateCommand(filePath)) {
  process.exit(0);
} else {
  process.exit(1);
}

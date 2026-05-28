/**
 * Fact-Check Helper Script
 *
 * Utility functions for DeepCitation operations used by the /factcheck skill.
 * Claude Code handles claim extraction and counter-argument generation directly.
 * This script handles the DeepCitation API calls.
 *
 * Usage:
 *   # Upload files
 *   bun run factcheck.ts upload ./report.pdf ./data.xlsx
 *
 *   # Verify claims (JSON input)
 *   bun run factcheck.ts verify <attachmentId> '{"claim-1": {"fullPhrase": "...", "keySpan": "..."}}'
 *
 *   # Verify from file
 *   bun run factcheck.ts verify <attachmentId> --file claims.json
 */

import { readFileSync, existsSync, writeFileSync } from "fs";
import { basename } from "path";
import {
  DeepCitation,
  getCitationStatus,
  type Citation,
} from "@deepcitation/deepcitation-js";

// ============================================
// Upload Command
// ============================================

async function uploadFiles(filePaths: string[]) {
  const apiKey = process.env.DEEPCITATION_API_KEY;
  if (!apiKey) {
    console.error("Error: DEEPCITATION_API_KEY environment variable required");
    process.exit(1);
  }

  const dc = new DeepCitation({ apiKey });

  const files = filePaths.map((path) => ({
    file: readFileSync(path),
    filename: basename(path),
  }));

  console.log(`Uploading ${files.length} file(s)...`);

  const { fileDataParts } = await deepcitation.prepareFiles(files);

  console.log("\nUploaded files:");
  const results: Array<{ filename: string; attachmentId: string }> = [];

  for (const part of fileDataParts) {
    console.log(`  ${part.filename}: ${part.attachmentId}`);
    results.push({
      filename: part.filename,
      attachmentId: part.attachmentId,
    });
  }

  // Output JSON for easy parsing
  console.log("\n--- JSON OUTPUT ---");
  console.log(JSON.stringify(results, null, 2));

  return results;
}

// ============================================
// Verify Command
// ============================================

async function verifyCitations(
  attachmentId: string,
  citations: Record<string, Citation>
) {
  const apiKey = process.env.DEEPCITATION_API_KEY;
  if (!apiKey) {
    console.error("Error: DEEPCITATION_API_KEY environment variable required");
    process.exit(1);
  }

  const dc = new DeepCitation({ apiKey });

  console.log(
    `Verifying ${Object.keys(citations).length} citation(s) against ${attachmentId.slice(0, 8)}...`
  );

  const result = await deepcitation.verify(attachmentId, citations);

  const output: Record<
    string,
    {
      status: string;
      isVerified: boolean;
      isPartialMatch: boolean;
      isMiss: boolean;
      page?: number | null;
      matchSnippet?: string | null;
    }
  > = {};

  for (const [key, verification] of Object.entries(result.verifications)) {
    const status = getCitationStatus(verification);
    output[key] = {
      status: verification.status || "unknown",
      isVerified: status.isVerified,
      isPartialMatch: status.isPartialMatch,
      isMiss: status.isMiss,
      page: verification.verifiedPageNumber,
      matchSnippet: verification.verifiedMatchSnippet?.slice(0, 100),
    };

    const icon = status.isVerified
      ? status.isPartialMatch
        ? "⚠️"
        : "✅"
      : status.isMiss
        ? "❌"
        : "⏳";

    console.log(`  ${icon} ${key}: ${verification.status || "unknown"}`);
    if (verification.verifiedPageNumber) {
      console.log(`     Page: ${verification.verifiedPageNumber}`);
    }
    if (verification.verifiedMatchSnippet) {
      console.log(
        `     Match: "${verification.verifiedMatchSnippet.slice(0, 60)}..."`
      );
    }
  }

  // Output JSON for easy parsing
  console.log("\n--- JSON OUTPUT ---");
  console.log(JSON.stringify(output, null, 2));

  return output;
}

// ============================================
// CLI Entry Point
// ============================================

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (command === "upload") {
    const filePaths = args.slice(1);
    if (filePaths.length === 0) {
      console.error("Usage: bun run factcheck.ts upload <file1> [file2] ...");
      process.exit(1);
    }
    await uploadFiles(filePaths);
  } else if (command === "verify") {
    const attachmentId = args[1];
    if (!attachmentId) {
      console.error(
        "Usage: bun run factcheck.ts verify <attachmentId> <citations-json>"
      );
      console.error(
        "   or: bun run factcheck.ts verify <attachmentId> --file <claims.json>"
      );
      process.exit(1);
    }

    let citations: Record<string, Citation>;

    if (args[2] === "--file") {
      const filePath = args[3];
      if (!filePath || !existsSync(filePath)) {
        console.error(`Error: File not found: ${filePath}`);
        process.exit(1);
      }
      citations = JSON.parse(readFileSync(filePath, "utf-8"));
    } else {
      const jsonArg = args[2];
      if (!jsonArg) {
        console.error("Error: Citations JSON required");
        process.exit(1);
      }
      citations = JSON.parse(jsonArg);
    }

    await verifyCitations(attachmentId, citations);
  } else {
    console.log("Fact-Check Helper Script");
    console.log("");
    console.log("Commands:");
    console.log("  upload <file1> [file2] ...     Upload files to DeepCitation");
    console.log("  verify <attachmentId> <json>   Verify citations against source");
    console.log("  verify <attachmentId> --file <path>  Verify from JSON file");
    console.log("");
    console.log("Environment:");
    console.log("  DEEPCITATION_API_KEY           Required for all operations");
  }
}

main().catch(console.error);

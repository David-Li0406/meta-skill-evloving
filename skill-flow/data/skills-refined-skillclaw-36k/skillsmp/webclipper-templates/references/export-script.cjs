/**
 * Web Clipper Template Export Script (v10 - Single Capture Template)
 *
 * Exports the single capture.json template for Web Clipper import.
 *
 * This script replaces the previous multi-template system with a single
 * ADHD-friendly capture template. All specialized templates have been
 * archived (see archived/README.md for rationale).
 *
 * Usage:
 *   node export-script.cjs
 *
 * Output:
 *   - Exports to ~/Downloads/
 */

const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");

// Configuration
const PLUGIN_ROOT = path.join(__dirname, "../../..");
const SOURCE_FILE = path.join(PLUGIN_ROOT, "templates/webclipper/capture.json");
const DOWNLOADS_DIR = path.join(os.homedir(), "Downloads");
const OUTPUT_DIR = DOWNLOADS_DIR;

// Validate source file exists
if (!fs.existsSync(SOURCE_FILE)) {
	console.error("ERROR: Source template not found at:", SOURCE_FILE);
	process.exit(1);
}

// Read capture template
const captureTemplate = JSON.parse(fs.readFileSync(SOURCE_FILE, "utf8"));

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
	fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Copy capture.json to vault
const outputFile = path.join(OUTPUT_DIR, "capture.json");
fs.writeFileSync(outputFile, JSON.stringify(captureTemplate, null, 4));

console.log("✓ Exported capture.json to:", outputFile);
console.log("\nNext steps:");
console.log("1. Open Obsidian Web Clipper settings");
console.log("2. Go to Templates section");
console.log("3. Click Import");
console.log("4. Select capture.json from", OUTPUT_DIR);
console.log("\nNote: All specialized templates have been archived.");
console.log(
	"See archived/README.md for the ADHD-friendly simplification rationale.",
);

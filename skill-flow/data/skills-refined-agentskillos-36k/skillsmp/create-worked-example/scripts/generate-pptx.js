/**
 * Generate PPTX from HTML Slides
 *
 * Converts PPTX-compatible HTML slides to PowerPoint format using pptxgenjs and html2pptx.
 *
 * Prerequisites:
 *   1. Install global packages: npm install -g pptxgenjs playwright react-icons react react-dom
 *   2. Extract html2pptx library: mkdir -p html2pptx && tar -xzf skills/public/pptx/html2pptx.tgz -C html2pptx
 *
 * Usage:
 *   NODE_PATH="$(npm root -g)" node generate-pptx.js <slides-dir> <output-path> [title]
 *
 * Example:
 *   NODE_PATH="$(npm root -g)" node generate-pptx.js ./slides output.pptx "Unit Rates Lesson"
 */

const path = require("path");
const fs = require("fs");

async function createPresentation(slidesDir, outputPath, metadata = {}) {
  // Dynamic imports for globally installed packages
  const pptxgen = require("pptxgenjs");

  // html2pptx should be extracted to a local directory
  const html2pptxPath = path.join(__dirname, "html2pptx");
  if (!fs.existsSync(html2pptxPath)) {
    console.error("Error: html2pptx library not found.");
    console.error("Please extract it first:");
    console.error(
      "  mkdir -p html2pptx && tar -xzf skills/public/pptx/html2pptx.tgz -C html2pptx"
    );
    process.exit(1);
  }

  const { html2pptx } = require(html2pptxPath);

  // Initialize presentation
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_16x9"; // Must match 960×540 HTML dimensions
  pptx.author = metadata.author || "AI Coaching Platform";
  pptx.title = metadata.title || "Worked Example";
  pptx.subject = metadata.subject || "Math";
  pptx.company = "AI Coaching Platform";

  // Find all HTML slide files
  const slideFiles = fs
    .readdirSync(slidesDir)
    .filter((f) => f.endsWith(".html") && !f.includes("printable"))
    .sort((a, b) => {
      // Sort by slide number if present in filename
      const numA = parseInt(a.match(/\d+/) || [0]);
      const numB = parseInt(b.match(/\d+/) || [0]);
      return numA - numB;
    });

  if (slideFiles.length === 0) {
    console.error(`Error: No HTML slide files found in ${slidesDir}`);
    process.exit(1);
  }

  console.log(`Found ${slideFiles.length} slides to convert:`);
  slideFiles.forEach((f, i) => console.log(`  ${i + 1}. ${f}`));
  console.log("");

  // Convert each slide
  for (const slideFile of slideFiles) {
    const slidePath = path.join(slidesDir, slideFile);
    console.log(`Converting: ${slideFile}...`);

    try {
      await html2pptx(slidePath, pptx);
    } catch (error) {
      console.error(`  Error converting ${slideFile}:`, error.message);
      // Continue with other slides
    }
  }

  // Save the presentation
  console.log("");
  console.log(`Saving to: ${outputPath}`);
  await pptx.writeFile(outputPath);
  console.log("Done!");

  return outputPath;
}

// CLI execution
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.log("Usage: node generate-pptx.js <slides-dir> <output-path> [title]");
    console.log("");
    console.log("Arguments:");
    console.log("  slides-dir   Directory containing HTML slide files");
    console.log("  output-path  Output PPTX file path");
    console.log("  title        Optional presentation title");
    console.log("");
    console.log("Example:");
    console.log(
      '  NODE_PATH="$(npm root -g)" node generate-pptx.js ./slides output.pptx "Unit Rates"'
    );
    process.exit(1);
  }

  const [slidesDir, outputPath, title] = args;

  createPresentation(slidesDir, outputPath, { title })
    .then(() => process.exit(0))
    .catch((error) => {
      console.error("Fatal error:", error);
      process.exit(1);
    });
}

module.exports = { createPresentation };

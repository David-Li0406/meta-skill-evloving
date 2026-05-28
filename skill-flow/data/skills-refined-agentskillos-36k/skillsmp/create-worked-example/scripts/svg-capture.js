/**
 * SVG Capture Script
 *
 * Captures SVG regions from PPTX-compatible HTML slides as high-resolution PNGs.
 * Uses Playwright for pixel-perfect browser rendering.
 *
 * The script finds SVG containers by looking for:
 * 1. data-svg-region="true" attribute
 * 2. data-region-x/y/width/height attributes for exact coordinates
 * 3. Falls back to element bounding box if no explicit coordinates
 *
 * Prerequisites:
 *   npm install playwright
 *   npx playwright install chromium
 *
 * Usage:
 *   node svg-capture.js <html-file> [output-dir]
 *   node svg-capture.js --dir <slides-dir> [output-dir]
 *
 * Example:
 *   node svg-capture.js slide-2.html ./images
 *   node svg-capture.js --dir ./slides ./images
 *
 * Output:
 *   - PNG files for each SVG region (2x scale for retina)
 *   - svg-manifest.json with region coordinates and PNG paths
 */

const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

/**
 * Capture SVG regions from an HTML file
 * @param {string} htmlPath - Path to the HTML file
 * @param {string} outputDir - Directory for PNG outputs
 * @param {Object} options - Capture options
 * @returns {Promise<Object>} - Capture results with PNG paths and regions
 */
async function captureSVGRegions(htmlPath, outputDir, options = {}) {
  const { scale = 2 } = options;
  const baseName = path.basename(htmlPath, ".html");

  // Ensure output directory exists
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Set viewport to slide dimensions (scaled)
  await page.setViewportSize({
    width: 960 * scale,
    height: 540 * scale,
  });

  // Load the HTML file
  const htmlContent = fs.readFileSync(htmlPath, "utf-8");
  await page.setContent(htmlContent);

  // Apply scale transform to body for higher resolution
  await page.evaluate((s) => {
    document.body.style.transform = `scale(${s})`;
    document.body.style.transformOrigin = "top left";
  }, scale);

  // Wait for fonts and rendering
  await page.waitForTimeout(200);

  // Find all SVG regions
  const regions = await page.evaluate(() => {
    const containers = document.querySelectorAll('[data-svg-region="true"]');
    const results = [];

    containers.forEach((container, index) => {
      // Try explicit coordinates first
      const explicitX = container.getAttribute("data-region-x");
      const explicitY = container.getAttribute("data-region-y");
      const explicitWidth = container.getAttribute("data-region-width");
      const explicitHeight = container.getAttribute("data-region-height");

      if (explicitX && explicitY && explicitWidth && explicitHeight) {
        results.push({
          index,
          x: parseInt(explicitX),
          y: parseInt(explicitY),
          width: parseInt(explicitWidth),
          height: parseInt(explicitHeight),
          source: "explicit",
        });
      } else {
        // Fall back to bounding box
        const rect = container.getBoundingClientRect();
        results.push({
          index,
          x: Math.round(rect.x),
          y: Math.round(rect.y),
          width: Math.round(rect.width),
          height: Math.round(rect.height),
          source: "bounding-box",
        });
      }
    });

    // Also find any inline <svg> elements without containers
    const standaloneSVGs = document.querySelectorAll("svg:not([data-svg-region] svg)");
    standaloneSVGs.forEach((svg, index) => {
      // Skip if already captured via container
      if (svg.closest('[data-svg-region="true"]')) return;

      const rect = svg.getBoundingClientRect();
      if (rect.width > 50 && rect.height > 50) {
        // Only capture substantial SVGs
        results.push({
          index: results.length,
          x: Math.round(rect.x),
          y: Math.round(rect.y),
          width: Math.round(rect.width),
          height: Math.round(rect.height),
          source: "standalone-svg",
        });
      }
    });

    return results;
  });

  if (regions.length === 0) {
    console.log(`  No SVG regions found in ${htmlPath}`);
    await browser.close();
    return { pngPaths: [], regions: [] };
  }

  console.log(`  Found ${regions.length} SVG region(s)`);

  const pngPaths = [];
  const capturedRegions = [];

  for (const region of regions) {
    const pngFileName = `${baseName}-svg-${region.index + 1}.png`;
    const pngPath = path.join(outputDir, pngFileName);

    console.log(`    Capturing region ${region.index + 1}: ${region.width}x${region.height} at (${region.x}, ${region.y})`);

    // Screenshot the specific region (scaled coordinates)
    await page.screenshot({
      path: pngPath,
      clip: {
        x: region.x * scale,
        y: region.y * scale,
        width: region.width * scale,
        height: region.height * scale,
      },
    });

    pngPaths.push(pngPath);
    capturedRegions.push({
      ...region,
      pngPath,
      pngFileName,
    });
  }

  await browser.close();

  return {
    htmlFile: path.basename(htmlPath),
    pngPaths,
    regions: capturedRegions,
  };
}

/**
 * Process all HTML files in a directory
 * @param {string} slidesDir - Directory containing HTML slide files
 * @param {string} outputDir - Directory for PNG outputs
 */
async function processDirectory(slidesDir, outputDir) {
  const htmlFiles = fs
    .readdirSync(slidesDir)
    .filter((f) => f.endsWith(".html") && !f.includes("printable"))
    .sort();

  console.log(`Processing ${htmlFiles.length} HTML files...\n`);

  const manifest = {
    generatedAt: new Date().toISOString(),
    slidesDir,
    outputDir,
    files: [],
  };

  for (const htmlFile of htmlFiles) {
    const htmlPath = path.join(slidesDir, htmlFile);
    console.log(`Processing: ${htmlFile}`);

    const result = await captureSVGRegions(htmlPath, outputDir);

    if (result.pngPaths.length > 0) {
      manifest.files.push(result);
    }
  }

  // Write manifest
  const manifestPath = path.join(outputDir, "svg-manifest.json");
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
  console.log(`\nManifest written to: ${manifestPath}`);

  // Summary
  const totalPNGs = manifest.files.reduce((sum, f) => sum + f.pngPaths.length, 0);
  console.log(`\n=== Summary ===`);
  console.log(`Files processed: ${htmlFiles.length}`);
  console.log(`Files with SVGs: ${manifest.files.length}`);
  console.log(`Total PNGs created: ${totalPNGs}`);

  return manifest;
}

/**
 * Generate HTML with SVGs replaced by <img> tags
 * @param {string} htmlPath - Original HTML file path
 * @param {Object} captureResult - Result from captureSVGRegions
 * @param {string} outputPath - Where to save modified HTML
 */
function generateImageHTML(htmlPath, captureResult, outputPath) {
  let html = fs.readFileSync(htmlPath, "utf-8");

  // For each captured region, we could replace SVG with img
  // This is optional - only needed if we want to update the HTML

  // For now, just add a comment noting the PNG exists
  for (const region of captureResult.regions) {
    const comment = `<!-- SVG captured to: ${region.pngFileName} -->`;
    // Insert comment at start of file
    if (!html.includes(comment)) {
      html = html.replace("<!DOCTYPE html>", `<!DOCTYPE html>\n${comment}`);
    }
  }

  fs.writeFileSync(outputPath, html);
  return outputPath;
}

// CLI execution
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length < 1) {
    console.log("SVG Capture Script - Capture SVG regions as high-res PNGs");
    console.log("");
    console.log("Usage:");
    console.log("  Single file:  node svg-capture.js <html-file> [output-dir]");
    console.log("  Directory:    node svg-capture.js --dir <slides-dir> [output-dir]");
    console.log("");
    console.log("Examples:");
    console.log("  node svg-capture.js slide-2.html ./images");
    console.log("  node svg-capture.js --dir ./slides ./images");
    console.log("");
    console.log("Output:");
    console.log("  - PNG files for each SVG region (2x resolution)");
    console.log("  - svg-manifest.json with coordinates and paths");
    console.log("");
    console.log("How it works:");
    console.log("  1. Finds elements with data-svg-region='true'");
    console.log("  2. Uses data-region-x/y/width/height for coordinates");
    console.log("  3. Falls back to bounding box if no explicit coords");
    console.log("  4. Screenshots at 2x scale for retina displays");
    process.exit(1);
  }

  const isDirectory = args[0] === "--dir";

  if (isDirectory) {
    const slidesDir = args[1] || ".";
    const outputDir = args[2] || path.join(slidesDir, "images");

    processDirectory(slidesDir, outputDir)
      .then(() => {
        console.log("\nDone!");
        process.exit(0);
      })
      .catch((error) => {
        console.error("Error:", error);
        process.exit(1);
      });
  } else {
    const htmlPath = args[0];
    const outputDir = args[1] || path.dirname(htmlPath);

    captureSVGRegions(htmlPath, outputDir)
      .then((result) => {
        if (result.pngPaths.length > 0) {
          console.log(`\nCreated ${result.pngPaths.length} PNG(s)`);
          result.pngPaths.forEach((p) => console.log(`  - ${p}`));
        } else {
          console.log("\nNo SVGs found to capture");
        }
        process.exit(0);
      })
      .catch((error) => {
        console.error("Error:", error);
        process.exit(1);
      });
  }
}

module.exports = {
  captureSVGRegions,
  processDirectory,
  generateImageHTML,
};

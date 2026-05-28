/**
 * Terminal Heritage Presentation Builder Template
 *
 * Usage: NODE_PATH="$(npm root -g)" node build-template.js
 */

const pptxgen = require("pptxgenjs");

// ===========================================
// TERMINAL HERITAGE COLOR PALETTE
// ===========================================
const COLORS = {
  surface: "C8C4B5",      // Khaki background
  navy: "1A2238",         // Dark navy (primary)
  navyLight: "2D3A52",    // Lighter navy
  cream: "F5F3E8",        // Off-white cream
  muted: "9A968A",        // Muted gray
  green: "4CAF50",        // Success green
  orange: "FFA726",       // Accent orange
  yellow: "FFD93D",       // Accent yellow
  red: "C41E3A"           // Error red
};

// ===========================================
// HELPER FUNCTIONS
// ===========================================

/**
 * Add standard header to a slide
 */
function addHeader(slide, sectionLabel, brand, slideNum) {
  // Logo dot
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.4, y: 0.25, w: 0.08, h: 0.08,
    fill: { color: COLORS.navy }
  });

  // Section label
  slide.addText(sectionLabel.toUpperCase(), {
    x: 0.55, y: 0.2, w: 2, h: 0.2,
    fontSize: 10, fontFace: "Courier New", color: COLORS.navy
  });

  // Brand badge
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 8.6, y: 0.2, w: 0.5, h: 0.22,
    fill: { color: COLORS.navy }
  });
  slide.addText(brand, {
    x: 8.6, y: 0.2, w: 0.5, h: 0.22,
    fontSize: 9, fontFace: "Courier New", color: COLORS.surface,
    align: "center", valign: "middle"
  });

  // Slide number
  const numStr = String(slideNum).padStart(4, '0');
  slide.addText(`——[${numStr}]`, {
    x: 9.15, y: 0.2, w: 0.7, h: 0.22,
    fontSize: 9, fontFace: "Courier New", color: COLORS.navy
  });
}

/**
 * Add slide title
 */
function addTitle(slide, title) {
  slide.addText(title.toUpperCase(), {
    x: 0.4, y: 0.55, w: 9, h: 0.4,
    fontSize: 24, fontFace: "Courier New", bold: true, color: COLORS.navy
  });
}

/**
 * Add footer text
 */
function addFooter(slide, text) {
  slide.addText(text, {
    x: 0.4, y: 5.1, w: 8, h: 0.2,
    fontSize: 9, fontFace: "Courier New", color: COLORS.muted
  });
}

/**
 * Add workflow chain
 */
function addWorkflowChain(slide, nodes, startX = 0.5, startY = 2.0) {
  const blockW = 1.2;
  const blockH = 1.0;
  const gap = 0.55;

  nodes.forEach((node, i) => {
    const x = startX + i * (blockW + gap);

    // Block
    const shapeOpts = {
      x: x, y: startY, w: blockW, h: blockH,
      fill: { color: node.color }
    };
    if (node.outline) {
      shapeOpts.line = { color: COLORS.navy, width: 3 };
    }
    slide.addShape(pptx.shapes.RECTANGLE, shapeOpts);

    // Label
    const textColor = node.outline ? COLORS.navy :
      (node.color === COLORS.green ? COLORS.navy : COLORS.surface);
    slide.addText(node.label, {
      x: x, y: startY, w: blockW, h: blockH,
      fontSize: 14, fontFace: "Courier New", bold: true,
      color: textColor, align: "center", valign: "middle"
    });

    // Connector
    if (i < nodes.length - 1) {
      slide.addShape(pptx.shapes.RECTANGLE, {
        x: x + blockW + 0.05, y: startY + blockH/2 - 0.03,
        w: gap - 0.1, h: 0.06,
        fill: { color: COLORS.navy }
      });
    }
  });
}

/**
 * Add waveform decoration
 */
function addWaveform(slide, x, y) {
  const bars = [0.35, 0.65, 0.45, 0.25, 0.55];
  bars.forEach((h, i) => {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: x + i * 0.15,
      y: y + (0.65 - h) / 2,
      w: 0.08, h: h,
      fill: { color: COLORS.navy }
    });
  });
}

// ===========================================
// MAIN PRESENTATION BUILDER
// ===========================================

async function createPresentation() {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_16x9";
  pptx.author = "Your Company";
  pptx.title = "Presentation Title";

  // ===================
  // SLIDE 1: Title
  // ===================
  const slide1 = pptx.addSlide();
  slide1.bkgd = COLORS.surface;

  // Logo box
  slide1.addShape(pptx.shapes.RECTANGLE, {
    x: 0.4, y: 0.3, w: 0.4, h: 0.4,
    line: { color: COLORS.navy, width: 2 },
    fill: { type: "none" }
  });
  slide1.addText("BRAND", {
    x: 0.9, y: 0.35, w: 1.5, h: 0.3,
    fontSize: 14, fontFace: "Courier New", bold: true, color: COLORS.navy
  });

  // Main title
  slide1.addText("YOUR TITLE HERE", {
    x: 0.4, y: 1.8, w: 8, h: 0.8,
    fontSize: 48, fontFace: "Courier New", bold: true, color: COLORS.navy
  });

  // Workflow visualization
  addWorkflowChain(slide1, [
    { label: "START", color: COLORS.navy },
    { label: "PROCESS", color: COLORS.navyLight },
    { label: "REVIEW", color: COLORS.cream, outline: true },
    { label: "DONE", color: COLORS.green }
  ], 0.5, 3.0);

  // Waveform decoration
  addWaveform(slide1, 8.0, 3.1);

  // Footer
  slide1.addText("COMPANY   /   PRODUCT   /   2026", {
    x: 0.4, y: 5.0, w: 6, h: 0.25,
    fontSize: 10, fontFace: "Courier New", color: COLORS.muted
  });

  // ===================
  // SLIDE 2: Content Example
  // ===================
  const slide2 = pptx.addSlide();
  slide2.bkgd = COLORS.surface;

  addHeader(slide2, "SECTION", "BRAND", 2);
  addTitle(slide2, "Content Slide Title");

  // Content blocks
  slide2.addShape(pptx.shapes.RECTANGLE, {
    x: 0.4, y: 1.2, w: 4.4, h: 2.5,
    fill: { color: COLORS.navy }
  });
  slide2.addText("CONTENT BLOCK", {
    x: 0.5, y: 1.3, w: 4.2, h: 0.4,
    fontSize: 18, fontFace: "Courier New", bold: true, color: COLORS.surface
  });

  // Gradient accent block
  slide2.addShape(pptx.shapes.RECTANGLE, {
    x: 5.0, y: 1.2, w: 4.6, h: 2.5,
    fill: { color: COLORS.green }
  });
  slide2.addShape(pptx.shapes.RECTANGLE, {
    x: 7.3, y: 1.2, w: 2.3, h: 2.5,
    fill: { color: COLORS.orange },
    transparency: 40
  });
  slide2.addText("HIGHLIGHT", {
    x: 5.1, y: 1.3, w: 4.4, h: 0.4,
    fontSize: 18, fontFace: "Courier New", bold: true, color: COLORS.navy
  });

  addFooter(slide2, "Footer text goes here");

  // ===================
  // Save Presentation
  // ===================
  await pptx.writeFile({ fileName: "presentation.pptx" });
  console.log("Presentation created: presentation.pptx");
}

// Run
createPresentation().catch(console.error);

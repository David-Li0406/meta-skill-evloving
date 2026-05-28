#!/usr/bin/env node
/**
 * SVG Overlap Checker
 * Parses SVG elements from HTML slides and checks for overlapping elements
 *
 * Usage: node check-svg-overlaps.js <slide-file.html>
 */

const fs = require('fs');
const path = require('path');

// Parse command line args
const filePath = process.argv[2];
if (!filePath) {
  console.error('Usage: node check-svg-overlaps.js <slide-file.html>');
  process.exit(1);
}

// Read the HTML file
const html = fs.readFileSync(filePath, 'utf-8');

// Extract SVG content
const svgMatch = html.match(/<svg[^>]*>([\s\S]*?)<\/svg>/gi);
if (!svgMatch) {
  console.log('No SVG elements found in file');
  process.exit(0);
}

/**
 * Calculate bounding box for different SVG elements
 */
function getBoundingBox(element) {
  // Circle: <circle cx="100" cy="50" r="5"/>
  const circleMatch = element.match(/<circle[^>]*cx="([^"]+)"[^>]*cy="([^"]+)"[^>]*r="([^"]+)"/);
  if (circleMatch) {
    const cx = parseFloat(circleMatch[1]);
    const cy = parseFloat(circleMatch[2]);
    const r = parseFloat(circleMatch[3]);
    return {
      type: 'circle',
      x: cx - r,
      y: cy - r,
      width: r * 2,
      height: r * 2,
      element: element.substring(0, 60) + '...'
    };
  }

  // Text: <text x="100" y="50" font-size="10">Label</text>
  const textMatch = element.match(/<text[^>]*x="([^"]+)"[^>]*y="([^"]+)"[^>]*(?:font-size="([^"]+)")?[^>]*>([^<]*)<\/text>/);
  if (textMatch) {
    const x = parseFloat(textMatch[1]);
    const y = parseFloat(textMatch[2]);
    const fontSize = parseFloat(textMatch[3] || '11');
    const text = textMatch[4];

    // Estimate text width: ~0.6 * fontSize per character
    const estimatedWidth = text.length * fontSize * 0.6;
    const estimatedHeight = fontSize * 1.2;

    // Check for text-anchor
    let adjustedX = x;
    if (element.includes('text-anchor="middle"')) {
      adjustedX = x - estimatedWidth / 2;
    } else if (element.includes('text-anchor="end"')) {
      adjustedX = x - estimatedWidth;
    }

    return {
      type: 'text',
      x: adjustedX,
      y: y - estimatedHeight, // text y is baseline
      width: estimatedWidth,
      height: estimatedHeight,
      element: `<text>${text}</text>`
    };
  }

  // Line with marker: check the endpoint
  const lineMatch = element.match(/<line[^>]*x1="([^"]+)"[^>]*y1="([^"]+)"[^>]*x2="([^"]+)"[^>]*y2="([^"]+)"/);
  if (lineMatch && element.includes('marker-end')) {
    const x2 = parseFloat(lineMatch[3]);
    const y2 = parseFloat(lineMatch[4]);
    // Arrow marker area (approximate)
    return {
      type: 'arrow-end',
      x: x2 - 8,
      y: y2 - 5,
      width: 16,
      height: 10,
      element: element.substring(0, 60) + '...'
    };
  }

  return null;
}

/**
 * Check if two bounding boxes overlap
 */
function boxesOverlap(box1, box2, padding = 0) {
  return !(
    box1.x + box1.width + padding < box2.x ||
    box2.x + box2.width + padding < box1.x ||
    box1.y + box1.height + padding < box2.y ||
    box2.y + box2.height + padding < box1.y
  );
}

/**
 * Check if overlap should be ignored (intentional stacking, axis labels, etc.)
 */
function shouldIgnoreOverlap(box1, box2) {
  // Ignore text-text overlaps that are intentionally stacked (same x, different y)
  if (box1.type === 'text' && box2.type === 'text') {
    const xDiff = Math.abs(box1.x - box2.x);
    if (xDiff < 5) return true; // Stacked labels
  }

  // Ignore axis label overlaps (small text near axes)
  const axisLabels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Week', 'Month', 'Time', 'Rank', 'Altitude'];
  const isAxisLabel = (box) => box.type === 'text' && axisLabels.some(l => box.element.includes(`>${l}<`));
  if (isAxisLabel(box1) && isAxisLabel(box2)) return true;

  return false;
}

/**
 * Calculate overlap area (for severity)
 */
function overlapArea(box1, box2) {
  const xOverlap = Math.max(0, Math.min(box1.x + box1.width, box2.x + box2.width) - Math.max(box1.x, box2.x));
  const yOverlap = Math.max(0, Math.min(box1.y + box1.height, box2.y + box2.height) - Math.max(box1.y, box2.y));
  return xOverlap * yOverlap;
}

// Process each SVG
let totalOverlaps = 0;
svgMatch.forEach((svg, svgIndex) => {
  console.log(`\n=== SVG #${svgIndex + 1} ===`);

  // Extract individual elements
  const elements = [];

  // Find circles
  const circles = svg.match(/<circle[^>]+\/>/g) || [];
  circles.forEach(el => {
    const box = getBoundingBox(el);
    if (box) elements.push(box);
  });

  // Find text elements
  const texts = svg.match(/<text[^>]*>[^<]*<\/text>/g) || [];
  texts.forEach(el => {
    const box = getBoundingBox(el);
    if (box) elements.push(box);
  });

  // Find lines with markers (arrows)
  const arrows = svg.match(/<line[^>]*marker-end[^>]*\/>/g) || [];
  arrows.forEach(el => {
    const box = getBoundingBox(el);
    if (box) elements.push(box);
  });

  console.log(`Found ${elements.length} elements to check`);

  // Check all pairs for overlap
  const overlaps = [];
  for (let i = 0; i < elements.length; i++) {
    for (let j = i + 1; j < elements.length; j++) {
      if (boxesOverlap(elements[i], elements[j])) {
        // Skip intentional overlaps
        if (shouldIgnoreOverlap(elements[i], elements[j])) continue;

        const area = overlapArea(elements[i], elements[j]);
        // Only report significant overlaps (> 20px²)
        if (area < 20) continue;

        overlaps.push({
          el1: elements[i],
          el2: elements[j],
          area: area
        });
      }
    }
  }

  if (overlaps.length === 0) {
    console.log('✅ No overlaps detected');
  } else {
    console.log(`⚠️  Found ${overlaps.length} potential overlaps:\n`);
    overlaps.forEach((overlap, idx) => {
      console.log(`  ${idx + 1}. ${overlap.el1.type} ↔ ${overlap.el2.type} (overlap area: ${overlap.area.toFixed(1)}px²)`);
      console.log(`     ${overlap.el1.element}`);
      console.log(`     ${overlap.el2.element}`);
      console.log('');
    });
    totalOverlaps += overlaps.length;
  }
});

// Exit with error code if overlaps found
if (totalOverlaps > 0) {
  console.log(`\n❌ Total: ${totalOverlaps} overlaps detected`);
  process.exit(1);
} else {
  console.log('\n✅ All SVGs passed overlap check');
  process.exit(0);
}

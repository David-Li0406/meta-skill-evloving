/**
 * Double Number Line Component
 *
 * Creates two parallel number lines with input boxes for proportional relationships.
 * Uses SVG foreignObject for perfect alignment of inputs with tick marks.
 *
 * Usage:
 * Call createDoubleNumberLine() within your buildLayout function
 *
 * Requirements:
 * - D3.js loaded
 * - chartState with dnl1, dnl2, dnl3, dnl4 properties
 * - sendChartState() function defined
 *
 * Based on: courses/IM-8th-Grade/modules/Unit-3/assignments/117-Equivalent-Ratios/questions/02
 */

function createDoubleNumberLine(container, config) {
  // SVG Structure
  const svgWidth = config.svgWidth || 700;
  const svgHeight = config.svgHeight || 200;
  const svg = container
    .append("svg")
    .attr("viewBox", `0 0 ${svgWidth} ${svgHeight}`)
    .attr("preserveAspectRatio", "xMidYMid meet")
    .style("width", "100%")
    .style("height", "auto")
    .style("max-width", `${svgWidth}px`);

  const lineY1 = config.lineY1 || 60;  // Top number line
  const lineY2 = config.lineY2 || 140; // Bottom number line
  const lineStartX = config.lineStartX || 50;
  const lineEndX = config.lineEndX || 650;
  const tickLength = config.tickLength || 10;

  // Top number line
  svg
    .append("line")
    .attr("x1", lineStartX)
    .attr("y1", lineY1)
    .attr("x2", lineEndX)
    .attr("y2", lineY1)
    .attr("stroke", "#1f2937")
    .attr("stroke-width", 2);

  // Label for top line
  svg
    .append("text")
    .attr("x", lineStartX - 30)
    .attr("y", lineY1 + 5)
    .attr("text-anchor", "middle")
    .attr("font-size", 14)
    .attr("font-weight", "600")
    .attr("fill", "#1f2937")
    .text(config.topLabel || "Top");

  // Bottom number line
  svg
    .append("line")
    .attr("x1", lineStartX)
    .attr("y1", lineY2)
    .attr("x2", lineEndX)
    .attr("y2", lineY2)
    .attr("stroke", "#1f2937")
    .attr("stroke-width", 2);

  // Label for bottom line
  svg
    .append("text")
    .attr("x", lineStartX - 30)
    .attr("y", lineY2 + 5)
    .attr("text-anchor", "middle")
    .attr("font-size", 14)
    .attr("font-weight", "600")
    .attr("fill", "#1f2937")
    .text(config.bottomLabel || "Bottom");

  // Calculate tick positions
  const numPositions = config.numPositions || 6;
  const spacing = (lineEndX - lineStartX) / (numPositions - 1);
  const positions = Array.from({ length: numPositions }, (_, i) => lineStartX + i * spacing);

  // Top line values (null = input box)
  const topValues = config.topValues || ["0", "3", "6", "9", null, null];
  const bottomValues = config.bottomValues || ["0", "8", "16", "24", null, null];

  // Draw ticks and labels for top line
  positions.forEach((x, i) => {
    // Draw tick
    svg
      .append("line")
      .attr("x1", x)
      .attr("y1", lineY1 - tickLength)
      .attr("x2", x)
      .attr("y2", lineY1 + tickLength)
      .attr("stroke", "#1f2937")
      .attr("stroke-width", 2);

    // Draw fixed label if not null
    if (topValues[i] !== null) {
      svg
        .append("text")
        .attr("x", x)
        .attr("y", lineY1 - 20) // Above the line
        .attr("text-anchor", "middle")
        .attr("font-size", 16)
        .attr("fill", "#1f2937")
        .text(topValues[i]);
    }
  });

  // Draw ticks and labels for bottom line
  positions.forEach((x, i) => {
    // Draw tick
    svg
      .append("line")
      .attr("x1", x)
      .attr("y1", lineY2 - tickLength)
      .attr("x2", x)
      .attr("y2", lineY2 + tickLength)
      .attr("stroke", "#1f2937")
      .attr("stroke-width", 2);

    // Draw fixed label if not null
    if (bottomValues[i] !== null) {
      svg
        .append("text")
        .attr("x", x)
        .attr("y", lineY2 + 30) // Below the line
        .attr("text-anchor", "middle")
        .attr("font-size", 16)
        .attr("fill", "#1f2937")
        .text(bottomValues[i]);
    }
  });

  // Input references
  let input1 = null;
  let input2 = null;
  let input3 = null;
  let input4 = null;

  // Create input using SVG foreignObject for perfect alignment
  function createInput(xSvg, ySvg, stateKey) {
    const foreignObj = svg
      .append("foreignObject")
      .attr("x", xSvg - 30) // Center 60px wide input (subtract half width)
      .attr("y", ySvg - 16) // Center 32px tall input (subtract half height)
      .attr("width", 60)
      .attr("height", 32);

    const input = foreignObj
      .append("xhtml:input")
      .attr("type", "text")
      .attr("maxlength", "3")
      .style("width", "100%")
      .style("height", "100%")
      .style("border", "2px solid #3b82f6")
      .style("border-radius", "6px")
      .style("text-align", "center")
      .style("font-size", "16px")
      .style("padding", "4px")
      .style("box-sizing", "border-box")
      .on("input", function () {
        chartState[stateKey] = this.value;
        sendChartState();
      });

    return input.node();
  }

  // Create inputs at blank positions
  // Adjust indices based on where nulls appear in topValues/bottomValues
  const inputConfig = config.inputPositions || {
    top: [{ index: 4, key: "dnl1" }, { index: 5, key: "dnl2" }],
    bottom: [{ index: 4, key: "dnl3" }, { index: 5, key: "dnl4" }]
  };

  // Position input boxes using EXACT same X-coordinates as tick marks
  // Top line: position above the line (lineY1 - 25 for better spacing)
  // Bottom line: position below the line (lineY2 + 30 to match fixed labels)
  inputConfig.top.forEach(({ index, key }) => {
    const input = createInput(positions[index], lineY1 - 25, key);
    if (key === "dnl1") input1 = input;
    if (key === "dnl2") input2 = input;
  });

  inputConfig.bottom.forEach(({ index, key }) => {
    const input = createInput(positions[index], lineY2 + 30, key);
    if (key === "dnl3") input3 = input;
    if (key === "dnl4") input4 = input;
  });

  // Return input references for interactivity control
  return {
    input1,
    input2,
    input3,
    input4,
    setInteractivity(enabled) {
      const disabled = !enabled;
      if (input1) input1.disabled = disabled;
      if (input2) input2.disabled = disabled;
      if (input3) input3.disabled = disabled;
      if (input4) input4.disabled = disabled;
    }
  };
}

// ============================================================
// USAGE EXAMPLE
// ============================================================
/*
function buildLayout(d3, containerSelector) {
  const container = d3.select(containerSelector);
  container.html("");

  // Create double number line
  const dnlInputs = createDoubleNumberLine(container, {
    svgWidth: 700,
    svgHeight: 200,
    lineY1: 60,
    lineY2: 140,
    lineStartX: 50,
    lineEndX: 650,
    tickLength: 10,
    topLabel: "Days",
    bottomLabel: "Pies",
    numPositions: 6,
    topValues: ["0", "3", "6", "9", null, null],
    bottomValues: ["0", "8", "16", "24", null, null],
    inputPositions: {
      top: [{ index: 4, key: "dnl1" }, { index: 5, key: "dnl2" }],
      bottom: [{ index: 4, key: "dnl3" }, { index: 5, key: "dnl4" }]
    }
  });

  // Store inputs for interactivity control
  window.dnlInputs = dnlInputs;
}

function setInteractivity(enabled) {
  if (window.dnlInputs) {
    window.dnlInputs.setInteractivity(enabled);
  }
}
*/

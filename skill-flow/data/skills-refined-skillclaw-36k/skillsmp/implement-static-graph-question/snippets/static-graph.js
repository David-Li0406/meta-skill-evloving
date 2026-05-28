/**
 * Static Graph Component
 *
 * Renders a static D3 line graph with:
 * - Coordinate grid with customizable ranges
 * - X and Y axes with labels
 * - Grid lines
 * - Line rendering with arrowhead
 * - Variable labels (optional)
 *
 * Based on: courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/02/
 */

/**
 * Render a static line graph
 *
 * @param {Object} d3 - D3 library
 * @param {Selection} svg - D3 SVG selection
 * @param {Object} options - Configuration options
 * @param {number} options.width - SVG width (default: 600)
 * @param {number} options.height - SVG height (default: 400)
 * @param {Object} options.padding - Graph padding {top, right, bottom, left} (default: {top: 40, right: 40, bottom: 60, left: 70})
 * @param {Array} options.xDomain - X-axis domain [min, max] (default: [0, 10])
 * @param {Array} options.yDomain - Y-axis domain [min, max] (default: [0, 200])
 * @param {string} options.xLabel - X-axis label (default: "x")
 * @param {string} options.yLabel - Y-axis label (default: "y")
 * @param {string} options.xVariable - X-axis variable label (optional, e.g., "d")
 * @param {string} options.yVariable - Y-axis variable label (optional, e.g., "m")
 * @param {Array} options.lineData - Data points [{x, y}, ...] for the line
 * @param {number} options.xGridStep - X grid line step (default: 1)
 * @param {number} options.yGridStep - Y grid line step (default: 20)
 * @param {number} options.xTicks - Number of X-axis ticks (default: auto)
 * @param {number} options.yTicks - Number of Y-axis ticks (default: 10)
 * @param {boolean} options.showArrow - Show arrowhead at end of line (default: true)
 * @param {string} options.lineColor - Line color (default: "#3b82f6")
 * @param {number} options.lineWidth - Line stroke width (default: 2.5)
 */
function renderStaticGraph(d3, svg, options) {
  // Default options
  const config = {
    width: 600,
    height: 400,
    padding: { top: 40, right: 40, bottom: 60, left: 70 },
    xDomain: [0, 10],
    yDomain: [0, 200],
    xLabel: "x",
    yLabel: "y",
    xVariable: null,
    yVariable: null,
    lineData: [],
    xGridStep: 1,
    yGridStep: 20,
    xTicks: null,
    yTicks: 10,
    showArrow: true,
    lineColor: "#3b82f6",
    lineWidth: 2.5,
    ...options
  };

  const { width, height, padding, xDomain, yDomain, xLabel, yLabel, lineData } = config;

  // Set up SVG
  svg
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("preserveAspectRatio", "xMidYMid meet")
    .style("width", "100%")
    .style("height", "auto")
    .style("max-width", "700px");

  // Create scales
  const xScale = d3
    .scaleLinear()
    .domain(xDomain)
    .range([padding.left, width - padding.right]);

  const yScale = d3
    .scaleLinear()
    .domain(yDomain)
    .range([height - padding.bottom, padding.top]);

  // Clear previous content
  svg.selectAll("*").remove();

  // Add background
  svg
    .append("rect")
    .attr("width", width)
    .attr("height", height)
    .attr("fill", "#ffffff");

  // Create grid lines
  const gridGroup = svg.append("g").attr("class", "grid");

  // Vertical grid lines
  for (let i = xDomain[0]; i <= xDomain[1]; i += config.xGridStep) {
    gridGroup
      .append("line")
      .attr("x1", xScale(i))
      .attr("y1", padding.top)
      .attr("x2", xScale(i))
      .attr("y2", height - padding.bottom)
      .attr("stroke", "#e5e7eb")
      .attr("stroke-width", 1);
  }

  // Horizontal grid lines
  for (let i = yDomain[0]; i <= yDomain[1]; i += config.yGridStep) {
    gridGroup
      .append("line")
      .attr("x1", padding.left)
      .attr("y1", yScale(i))
      .attr("x2", width - padding.right)
      .attr("y2", yScale(i))
      .attr("stroke", "#e5e7eb")
      .attr("stroke-width", 1);
  }

  // X-axis
  const xAxis = d3.axisBottom(xScale);
  if (config.xTicks) xAxis.ticks(config.xTicks);

  svg
    .append("g")
    .attr("class", "x-axis")
    .attr("transform", `translate(0, ${height - padding.bottom})`)
    .call(xAxis)
    .style("font-size", "12px");

  // Y-axis
  const yAxis = d3.axisLeft(yScale).ticks(config.yTicks);

  svg
    .append("g")
    .attr("class", "y-axis")
    .attr("transform", `translate(${padding.left}, 0)`)
    .call(yAxis)
    .style("font-size", "12px");

  // Y-axis label
  svg
    .append("text")
    .attr("class", "y-axis-label")
    .attr("transform", "rotate(-90)")
    .attr("x", -(height / 2))
    .attr("y", 20)
    .attr("text-anchor", "middle")
    .attr("font-size", "14px")
    .attr("font-weight", "500")
    .attr("fill", "#374151")
    .text(yLabel);

  // X-axis label
  svg
    .append("text")
    .attr("class", "x-axis-label")
    .attr("x", width / 2)
    .attr("y", height - 15)
    .attr("text-anchor", "middle")
    .attr("font-size", "14px")
    .attr("font-weight", "500")
    .attr("fill", "#374151")
    .text(xLabel);

  // Optional variable labels
  if (config.yVariable) {
    svg
      .append("text")
      .attr("class", "variable-label")
      .attr("x", 25)
      .attr("y", 25)
      .attr("font-size", "14px")
      .attr("font-style", "italic")
      .attr("fill", "#374151")
      .text(config.yVariable);
  }

  if (config.xVariable) {
    svg
      .append("text")
      .attr("class", "variable-label")
      .attr("x", width - 20)
      .attr("y", height - padding.bottom + 30)
      .attr("font-size", "14px")
      .attr("font-style", "italic")
      .attr("fill", "#374151")
      .text(config.xVariable);
  }

  // Draw the line if lineData provided
  if (lineData && lineData.length > 0) {
    const line = d3
      .line()
      .x((d) => xScale(d.x))
      .y((d) => yScale(d.y));

    svg
      .append("path")
      .datum(lineData)
      .attr("class", "line")
      .attr("d", line)
      .attr("fill", "none")
      .attr("stroke", config.lineColor)
      .attr("stroke-width", config.lineWidth);

    // Add arrowhead if requested
    if (config.showArrow && lineData.length >= 2) {
      // Add arrowhead marker definition
      svg
        .append("defs")
        .append("marker")
        .attr("id", "arrowhead")
        .attr("markerWidth", 10)
        .attr("markerHeight", 10)
        .attr("refX", 9)
        .attr("refY", 3)
        .attr("orient", "auto")
        .append("polygon")
        .attr("points", "0 0, 10 3, 0 6")
        .attr("fill", config.lineColor);

      // Get last two points for arrow direction
      const lastPoint = lineData[lineData.length - 1];
      const prevPoint = lineData[lineData.length - 2];

      const endX = xScale(lastPoint.x);
      const endY = yScale(lastPoint.y);
      const prevX = xScale(prevPoint.x);
      const prevY = yScale(prevPoint.y);

      svg
        .append("line")
        .attr("x1", prevX)
        .attr("y1", prevY)
        .attr("x2", endX)
        .attr("y2", endY)
        .attr("stroke", config.lineColor)
        .attr("stroke-width", config.lineWidth)
        .attr("marker-end", "url(#arrowhead)");
    }
  }
}

// Example usage:
/*
const svg = container.append("svg");

renderStaticGraph(d3, svg, {
  width: 600,
  height: 400,
  xDomain: [0, 10],
  yDomain: [0, 200],
  xLabel: "Days",
  yLabel: "Money Earned ($)",
  xVariable: "d",
  yVariable: "m",
  lineData: [
    { x: 0, y: 0 },
    { x: 10, y: 200 }
  ],
  xGridStep: 1,
  yGridStep: 20,
  showArrow: true
});
*/

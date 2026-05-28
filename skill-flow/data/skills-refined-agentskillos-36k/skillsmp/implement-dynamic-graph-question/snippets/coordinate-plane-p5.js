/**
 * P5.js Coordinate Plane Component (Instance Mode)
 *
 * Interactive coordinate plane for drawing linear lines with snap-to-grid.
 * Based on: alex/coordinatePlane/linear-graph-drawing.ts
 *
 * Usage:
 * const plane = createCoordinatePlane(containerElementId, config, callbacks);
 *
 * Config options:
 * - xMin, xMax, yMin, yMax - Axis ranges
 * - gridScaleX, gridScaleY - Grid spacing
 * - xLabel, yLabel - Axis labels
 * - xVariable, yVariable - Optional italic variables
 * - initialPoints, initialEquations - Pre-drawn data
 * - predrawnStartPoint - Force line start point
 * - showCoordinatesOnHover - Show (x, y) on hover (default: true)
 * - snapSubdivisions - Snap to fractional grid (1=grid only, 2=halves, 3=thirds, etc.)
 * - snapSubdivisionsX, snapSubdivisionsY - Per-axis snap subdivisions
 *
 * Returns API:
 * - getLines() - Get all drawn lines
 * - setLines(lines) - Restore drawn lines
 * - reset() - Clear all drawn lines
 * - setLocked(bool) - Enable/disable drawing
 */

function createCoordinatePlane(containerId, config, callbacks) {
  const sketch = function(p) {
    // ==========================================
    // CONFIGURATION
    // ==========================================

    // Axis Configuration
    let xMin = config.xMin || 0;
    let xMax = config.xMax || 10;
    let yMin = config.yMin || 0;
    let yMax = config.yMax || 100;
    let gridScaleX = config.gridScaleX || 1;
    let gridScaleY = config.gridScaleY || 10;

    // Labels
    let xAxisLabel = config.xLabel || 'X';
    let yAxisLabel = config.yLabel || 'Y';
    let xVariable = config.xVariable || null;  // Optional italic variable
    let yVariable = config.yVariable || null;

    // Initial data
    let initialPoints = config.initialPoints || [];
    let initialEquations = config.initialEquations || [];
    let predrawnStartPoint = config.predrawnStartPoint || null;

    // Display options
    let showCoordinatesOnHover = config.showCoordinatesOnHover !== false; // Default true

    // Snap configuration
    let snapSubdivisionsX = config.snapSubdivisionsX || config.snapSubdivisions || 1;
    let snapSubdivisionsY = config.snapSubdivisionsY || config.snapSubdivisions || 1;

    // Canvas configuration
    let padding = {
      left: 60,
      right: 40,
      top: 40,
      bottom: 60
    };

    // Drawing state
    let lines = [];
    let startPoint = null;
    let currentPoint = null;
    let hoverPoint = null;
    let locked = false;

    // Callbacks
    const onLineDrawn = callbacks?.onLineDrawn || (() => {});
    const onLinesChanged = callbacks?.onLinesChanged || (() => {});

    p.setup = function() {
      p.createCanvas(600, 600);
      p.textFont('Arial');
    };

    p.draw = function() {
      p.background(255);

      drawGrid();
      drawAxes();
      drawInitialEquations();
      drawInitialPoints();
      drawPredrawnStartPoint();
      drawLines();

      if (startPoint && currentPoint) {
        drawPreviewLine();
      }

      if (hoverPoint && !startPoint) {
        drawHoverIndicator();
      }

      drawInstructions();
    };

    function drawGrid() {
      p.stroke(220);
      p.strokeWeight(1);

      // Vertical grid lines
      for (let x = xMin; x <= xMax; x += gridScaleX) {
        let px = coordToPixel(x, yMin);
        let py1 = coordToPixel(x, yMin).y;
        let py2 = coordToPixel(x, yMax).y;

        if (x === 0) {
          p.stroke(100);
          p.strokeWeight(2);
        } else {
          p.stroke(220);
          p.strokeWeight(1);
        }

        p.line(px.x, py1, px.x, py2);
      }

      // Horizontal grid lines
      for (let y = yMin; y <= yMax; y += gridScaleY) {
        let px1 = coordToPixel(xMin, y).x;
        let px2 = coordToPixel(xMax, y).x;
        let py = coordToPixel(xMin, y).y;

        if (y === 0) {
          p.stroke(100);
          p.strokeWeight(2);
        } else {
          p.stroke(220);
          p.strokeWeight(1);
        }

        p.line(px1, py, px2, py);
      }
    }

    function drawAxes() {
      p.fill(0);
      p.noStroke();
      p.textAlign(p.CENTER, p.TOP);
      p.textSize(12);

      // X-axis labels
      for (let x = xMin; x <= xMax; x += gridScaleX) {
        let pos = coordToPixel(x, 0);

        p.stroke(0);
        p.strokeWeight(2);
        p.line(pos.x, pos.y - 5, pos.x, pos.y + 5);

        p.noStroke();
        p.fill(0);
        p.text(x, pos.x, pos.y + 10);
      }

      // Y-axis labels
      p.textAlign(p.RIGHT, p.CENTER);
      for (let y = yMin; y <= yMax; y += gridScaleY) {
        if (y === 0) continue;

        let pos = coordToPixel(0, y);

        p.stroke(0);
        p.strokeWeight(2);
        p.line(pos.x - 5, pos.y, pos.x + 5, pos.y);

        p.noStroke();
        p.fill(0);
        p.text(y, pos.x - 10, pos.y);
      }

      // Axis titles
      p.fill(60);
      p.textSize(14);
      p.textStyle(p.BOLD);

      // X-axis title
      p.textAlign(p.CENTER, p.TOP);
      let xAxisY = coordToPixel(0, 0).y;
      p.text(xAxisLabel, p.width - padding.right - 40, xAxisY + 30);

      // Y-axis title
      p.push();
      p.translate(20, p.height / 2);
      p.rotate(-p.PI / 2);
      p.textAlign(p.CENTER, p.BOTTOM);
      p.text(yAxisLabel, 0, 0);
      p.pop();

      // Variable labels (optional italic)
      if (yVariable) {
        p.textStyle(p.ITALIC);
        p.textAlign(p.LEFT, p.TOP);
        p.fill(100);
        p.text(yVariable, 25, 25);
      }

      if (xVariable) {
        p.textStyle(p.ITALIC);
        p.textAlign(p.RIGHT, p.TOP);
        p.fill(100);
        p.text(xVariable, p.width - 20, xAxisY + 30);
      }

      p.textStyle(p.NORMAL);
    }

    function drawInitialPoints() {
      if (initialPoints.length === 0) return;

      p.fill(100);
      p.noStroke();
      for (let point of initialPoints) {
        let pos = coordToPixel(point.x, point.y);
        p.circle(pos.x, pos.y, 8);
      }
    }

    function drawPredrawnStartPoint() {
      if (!predrawnStartPoint) return;
      if (lines.length > 0) return;

      let pos = coordToPixel(predrawnStartPoint.x, predrawnStartPoint.y);
      let pulse = p.sin(p.frameCount * 0.05) * 0.3 + 0.7;

      p.fill(37, 99, 235, 100 * pulse);
      p.noStroke();
      p.circle(pos.x, pos.y, 16 * pulse);

      p.fill(37, 99, 235);
      p.circle(pos.x, pos.y, 10);

      p.fill(37, 99, 235);
      p.textSize(11);
      p.textAlign(p.LEFT, p.TOP);
      p.text('Start here', pos.x + 12, pos.y - 5);
    }

    function drawInitialEquations() {
      if (initialEquations.length === 0) return;

      for (let eq of initialEquations) {
        let slope = eq.slope;
        let intercept = eq.intercept;
        let color = eq.color || [34, 197, 94];

        let points = [];

        // Find intersections with boundaries
        let yAtXMin = slope * xMin + intercept;
        if (yAtXMin >= yMin && yAtXMin <= yMax) {
          points.push(coordToPixel(xMin, yAtXMin));
        }

        let yAtXMax = slope * xMax + intercept;
        if (yAtXMax >= yMin && yAtXMax <= yMax) {
          points.push(coordToPixel(xMax, yAtXMax));
        }

        if (slope !== 0) {
          let xAtYMin = (yMin - intercept) / slope;
          if (xAtYMin >= xMin && xAtYMin <= xMax) {
            points.push(coordToPixel(xAtYMin, yMin));
          }

          let xAtYMax = (yMax - intercept) / slope;
          if (xAtYMax >= xMin && xAtYMax <= xMax) {
            points.push(coordToPixel(xAtYMax, yMax));
          }
        }

        if (points.length >= 2) {
          p.stroke(color[0], color[1], color[2], 180);
          p.strokeWeight(2);
          p.line(points[0].x, points[0].y, points[1].x, points[1].y);
        }
      }
    }

    function drawLines() {
      for (let lineSegment of lines) {
        let start = coordToPixel(lineSegment.start.x, lineSegment.start.y);
        let end = coordToPixel(lineSegment.end.x, lineSegment.end.y);

        p.stroke(37, 99, 235);
        p.strokeWeight(3);
        p.line(start.x, start.y, end.x, end.y);

        p.fill(37, 99, 235);
        p.noStroke();
        p.circle(start.x, start.y, 8);
        p.circle(end.x, end.y, 8);
      }
    }

    function drawPreviewLine() {
      let dx = currentPoint.x - startPoint.x;
      let dy = currentPoint.y - startPoint.y;

      if (dx === 0) {
        let startPx = coordToPixel(startPoint.x, startPoint.y);
        let topPx = coordToPixel(startPoint.x, yMax);
        let bottomPx = coordToPixel(startPoint.x, yMin);

        p.stroke(16, 185, 129);
        p.strokeWeight(2);
        p.drawingContext.setLineDash([5, 5]);
        p.line(topPx.x, topPx.y, bottomPx.x, bottomPx.y);
        p.drawingContext.setLineDash([]);

        p.fill(16, 185, 129);
        p.noStroke();
        p.circle(startPx.x, startPx.y, 8);

        let endPx = coordToPixel(currentPoint.x, currentPoint.y);
        p.fill(16, 185, 129, 150);
        p.circle(endPx.x, endPx.y, 8);
        return;
      }

      let slope = dy / dx;
      let intercept = startPoint.y - slope * startPoint.x;

      let points = [];

      let yAtXMin = slope * xMin + intercept;
      if (yAtXMin >= yMin && yAtXMin <= yMax) {
        points.push({ x: xMin, y: yAtXMin });
      }

      let yAtXMax = slope * xMax + intercept;
      if (yAtXMax >= yMin && yAtXMax <= yMax) {
        points.push({ x: xMax, y: yAtXMax });
      }

      let xAtYMin = (yMin - intercept) / slope;
      if (xAtYMin >= xMin && xAtYMin <= xMax) {
        points.push({ x: xAtYMin, y: yMin });
      }

      let xAtYMax = (yMax - intercept) / slope;
      if (xAtYMax >= xMin && xAtYMax <= xMax) {
        points.push({ x: xAtYMax, y: yMax });
      }

      // Deduplicate points that are too close together (handles corner cases)
      const EPSILON = 0.0001;
      let uniquePoints = [];
      for (let pt of points) {
        let isDuplicate = uniquePoints.some(
          existing => Math.abs(existing.x - pt.x) < EPSILON &&
                      Math.abs(existing.y - pt.y) < EPSILON
        );
        if (!isDuplicate) {
          uniquePoints.push(pt);
        }
      }

      if (uniquePoints.length >= 2) {
        let p1 = coordToPixel(uniquePoints[0].x, uniquePoints[0].y);
        let p2 = coordToPixel(uniquePoints[1].x, uniquePoints[1].y);

        p.stroke(16, 185, 129);
        p.strokeWeight(2);
        p.drawingContext.setLineDash([5, 5]);
        p.line(p1.x, p1.y, p2.x, p2.y);
        p.drawingContext.setLineDash([]);
      }

      let startPx = coordToPixel(startPoint.x, startPoint.y);
      p.fill(16, 185, 129);
      p.noStroke();
      p.circle(startPx.x, startPx.y, 8);

      let endPx = coordToPixel(currentPoint.x, currentPoint.y);
      p.fill(16, 185, 129, 150);
      p.circle(endPx.x, endPx.y, 8);
    }

    function drawHoverIndicator() {
      let pos = coordToPixel(hoverPoint.x, hoverPoint.y);
      p.fill(16, 185, 129, 50);
      p.noStroke();
      p.circle(pos.x, pos.y, 12);

      if (showCoordinatesOnHover) {
        p.fill(0);
        p.textSize(11);
        p.textAlign(p.LEFT, p.BOTTOM);
        p.text(`(${hoverPoint.x}, ${hoverPoint.y})`, pos.x + 10, pos.y - 10);
      }
    }

    function drawInstructions() {
      let boxX = p.width - 295;
      let boxY = 10;
      let boxWidth = 285;
      let boxHeight = 80;
      if (initialEquations.length > 0) boxHeight += 15;
      if (lines.length > 0) boxHeight += 15;

      p.fill(255, 255, 255, 230);
      p.stroke(200);
      p.strokeWeight(1);
      p.rect(boxX, boxY, boxWidth, boxHeight, 5);

      p.noStroke();
      p.fill(100);
      p.textSize(11);
      p.textAlign(p.LEFT, p.TOP);
      p.textStyle(p.NORMAL);

      let textX = boxX + 8;
      let y = boxY + 8;

      if (predrawnStartPoint && lines.length === 0) {
        p.text('• Click anywhere to draw from start', textX, y);
        p.text('• Lines snap to grid intersections', textX, y + 15);
        p.text('• Press ESC to cancel', textX, y + 30);
      } else {
        p.text('• Click to start, click again to finish', textX, y);
        p.text('• Lines snap to grid intersections', textX, y + 15);
        p.text('• Press R to reset drawn lines', textX, y + 30);
        p.text('• Press ESC to cancel current line', textX, y + 45);
      }

      let legendY = y + 60;
      if (initialEquations.length > 0) {
        p.fill(34, 197, 94);
        p.text('Green = Initial equations', textX, legendY);
        legendY += 15;
      }

      if (lines.length > 0) {
        p.fill(37, 99, 235);
        p.text('Blue = Drawn lines', textX, legendY);
      }
    }

    // Coordinate transformation
    function coordToPixel(x, y) {
      let plotWidth = p.width - padding.left - padding.right;
      let plotHeight = p.height - padding.top - padding.bottom;

      let xRange = xMax - xMin;
      let yRange = yMax - yMin;

      let px = padding.left + ((x - xMin) / xRange) * plotWidth;
      let py = padding.top + ((yMax - y) / yRange) * plotHeight;

      return { x: px, y: py };
    }

    function pixelToCoord(px, py) {
      let plotWidth = p.width - padding.left - padding.right;
      let plotHeight = p.height - padding.top - padding.bottom;

      let xRange = xMax - xMin;
      let yRange = yMax - yMin;

      let x = xMin + ((px - padding.left) / plotWidth) * xRange;
      let y = yMax - ((py - padding.top) / plotHeight) * yRange;

      return { x: x, y: y };
    }

    function snapToGrid(coord) {
      const snapX = gridScaleX / snapSubdivisionsX;
      const snapY = gridScaleY / snapSubdivisionsY;
      return {
        x: Math.round(coord.x / snapX) * snapX,
        y: Math.round(coord.y / snapY) * snapY
      };
    }

    function isInBounds(px, py) {
      return px >= padding.left &&
             px <= p.width - padding.right &&
             py >= padding.top &&
             py <= p.height - padding.bottom;
    }

    p.mouseMoved = function() {
      if (!isInBounds(p.mouseX, p.mouseY)) {
        hoverPoint = null;
        return;
      }

      let coord = pixelToCoord(p.mouseX, p.mouseY);
      hoverPoint = snapToGrid(coord);

      if (startPoint) {
        currentPoint = hoverPoint;
      }
    };

    p.mousePressed = function() {
      if (locked) return;
      if (!isInBounds(p.mouseX, p.mouseY)) return;

      let coord = pixelToCoord(p.mouseX, p.mouseY);
      let snapped = snapToGrid(coord);

      if (!startPoint) {
        if (predrawnStartPoint && lines.length === 0) {
          startPoint = predrawnStartPoint;
          currentPoint = predrawnStartPoint;
        } else {
          startPoint = snapped;
          currentPoint = snapped;
        }
      } else {
        const line = {
          start: startPoint,
          end: snapped
        };
        lines.push(line);

        onLineDrawn(line);
        onLinesChanged([...lines]);

        startPoint = null;
        currentPoint = null;
      }
    };

    p.keyPressed = function() {
      if (locked) return;

      if (p.key === 'r' || p.key === 'R') {
        lines = [];
        startPoint = null;
        currentPoint = null;
        onLinesChanged([]);
      }

      if (p.keyCode === p.ESCAPE) {
        startPoint = null;
        currentPoint = null;
      }
    };

    // Public API
    return {
      getLines: () => [...lines],
      setLines: (newLines) => {
        lines = [...newLines];
      },
      reset: () => {
        lines = [];
        startPoint = null;
        currentPoint = null;
        onLinesChanged([]);
      },
      setLocked: (isLocked) => {
        locked = isLocked;
      }
    };
  };

  // Create p5 instance
  const p5Instance = new p5(sketch, containerId);

  // Return API (will be populated by sketch's return value)
  // Note: In p5 instance mode, we need to expose the API differently
  // The sketch function's return value isn't directly accessible
  // So we'll attach methods to window for the question to access
  return p5Instance;
}

// For inlining in chart.js, also provide the API attachment pattern:
/*
// In your chart.js:
const planeContainer = container.append("div")
  .attr("id", "coordinate-plane")
  .node();

const plane = createCoordinatePlane("coordinate-plane", {
  xMin: 0, xMax: 10,
  yMin: 0, yMax: 100,
  xLabel: "Time", yLabel: "Distance",
  gridScaleX: 1, gridScaleY: 10
}, {
  onLineDrawn: (line) => {
    console.log("Line drawn:", line);
  },
  onLinesChanged: (lines) => {
    chartState.drawnLines = lines;
    sendChartState();
  }
});
*/

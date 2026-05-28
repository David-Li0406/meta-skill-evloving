/**
 * P5.js Coordinate Plane Component (Instance Mode)
 *
 * Interactive coordinate plane for drawing linear lines with snap-to-grid.
 * Can also be used as a static graph display by setting allowInput: false.
 * Based on: alex/coordinatePlane/linear-graph-drawing.ts
 *
 * Usage:
 * const plane = createCoordinatePlane(containerElementId, config, callbacks);
 *
 * Config options:
 * - width, height - Canvas size in pixels (default: 600x600)
 * - xMin, xMax, yMin, yMax - Axis ranges
 * - gridScaleX, gridScaleY - Grid spacing
 * - xLabel, yLabel - Axis labels
 * - xVariable, yVariable - Optional italic variables
 * - initialPoints - Points to display
 * - initialEquations - Equations as lines (slope/intercept)
 * - initialLines - Pre-drawn line segments with optional colors
 * - predrawnStartPoint - Force line start point (interactive mode)
 * - showCoordinatesOnHover - Show (x, y) on hover (default: true)
 * - drawFullLines - Extend lines to canvas edges (default: true)
 * - allowInput - Enable interactive drawing (default: true, set false for static display)
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

    // Canvas size
    let canvasWidth = config.width || 600;
    let canvasHeight = config.height || 600;

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
    let initialLines = config.initialLines || [];
    let predrawnStartPoint = config.predrawnStartPoint || null;

    // Display options
    let showCoordinatesOnHover = config.showCoordinatesOnHover !== false; // Default true
    let drawFullLines = config.drawFullLines !== false; // Default true (extend to canvas edges)

    // Interaction mode
    let allowInput = config.allowInput !== false; // Default true (interactive mode)

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
    let showInstructions = false; // Hidden by default

    // Callbacks
    const onLineDrawn = callbacks?.onLineDrawn || (() => {});
    const onLinesChanged = callbacks?.onLinesChanged || (() => {});

    p.setup = function() {
      p.createCanvas(canvasWidth, canvasHeight);
      p.textFont('Arial');
    };

    p.draw = function() {
      p.background(255);

      drawGrid();
      drawAxes();
      drawInitialEquations();
      drawInitialLines();
      drawInitialPoints();
      drawPredrawnStartPoint();
      drawLines();

      if (startPoint && currentPoint && allowInput) {
        drawPreviewLine();
      }

      // Show hover indicator in both modes if coordinates should be shown
      if (hoverPoint && !startPoint) {
        if (allowInput || showCoordinatesOnHover) {
          drawHoverIndicator();
        }
      }

      if (allowInput) {
        drawInstructions();
      }
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

        // Skip drawing 0 label on X-axis if we're at the origin (will be drawn once below)
        if (x === 0) continue;

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

      // Draw single "0" label at origin (bottom-left of intersection)
      if (xMin <= 0 && xMax >= 0 && yMin <= 0 && yMax >= 0) {
        let origin = coordToPixel(0, 0);
        p.noStroke();
        p.fill(0);
        p.textAlign(p.RIGHT, p.TOP);
        p.text('0', origin.x - 10, origin.y + 10);
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

      // Note: "Start here" text removed for cleaner auto-hover experience
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

    function drawInitialLines() {
      if (initialLines.length === 0) return;

      for (let lineSegment of initialLines) {
        let start = coordToPixel(lineSegment.start.x, lineSegment.start.y);
        let end = coordToPixel(lineSegment.end.x, lineSegment.end.y);
        let color = lineSegment.color || [100, 100, 100]; // Default gray

        if (drawFullLines) {
          // Draw full line extending to canvas edges
          let dx = lineSegment.end.x - lineSegment.start.x;
          let dy = lineSegment.end.y - lineSegment.start.y;

          if (dx === 0) {
            // Vertical line
            let topPx = coordToPixel(lineSegment.start.x, yMax);
            let bottomPx = coordToPixel(lineSegment.start.x, yMin);
            p.stroke(color[0], color[1], color[2], 180);
            p.strokeWeight(2);
            p.line(topPx.x, topPx.y, bottomPx.x, bottomPx.y);
          } else {
            // Calculate slope and intercept
            let slope = dy / dx;
            let intercept = lineSegment.start.y - slope * lineSegment.start.x;

            // Find intersection points with canvas edges
            let coordPoints = [];

            let yAtXMin = slope * xMin + intercept;
            if (yAtXMin >= yMin && yAtXMin <= yMax) {
              coordPoints.push({ x: xMin, y: yAtXMin });
            }

            let yAtXMax = slope * xMax + intercept;
            if (yAtXMax >= yMin && yAtXMax <= yMax) {
              coordPoints.push({ x: xMax, y: yAtXMax });
            }

            let xAtYMin = (yMin - intercept) / slope;
            if (xAtYMin >= xMin && xAtYMin <= xMax) {
              coordPoints.push({ x: xAtYMin, y: yMin });
            }

            let xAtYMax = (yMax - intercept) / slope;
            if (xAtYMax >= xMin && xAtYMax <= xMax) {
              coordPoints.push({ x: xAtYMax, y: yMax });
            }

            // Deduplicate points
            const EPSILON = 0.0001;
            let uniqueCoordPoints = [];
            for (let pt of coordPoints) {
              let isDuplicate = uniqueCoordPoints.some(
                existing => Math.abs(existing.x - pt.x) < EPSILON &&
                            Math.abs(existing.y - pt.y) < EPSILON
              );
              if (!isDuplicate) {
                uniqueCoordPoints.push(pt);
              }
            }

            if (uniqueCoordPoints.length >= 2) {
              let p1 = coordToPixel(uniqueCoordPoints[0].x, uniqueCoordPoints[0].y);
              let p2 = coordToPixel(uniqueCoordPoints[1].x, uniqueCoordPoints[1].y);
              p.stroke(color[0], color[1], color[2], 180);
              p.strokeWeight(2);
              p.line(p1.x, p1.y, p2.x, p2.y);
            }
          }
        } else {
          // Draw line segment only
          p.stroke(color[0], color[1], color[2], 180);
          p.strokeWeight(2);
          p.line(start.x, start.y, end.x, end.y);
        }

        // Draw endpoint circles
        p.fill(color[0], color[1], color[2], 180);
        p.noStroke();
        p.circle(start.x, start.y, 6);
        p.circle(end.x, end.y, 6);
      }
    }

    function drawLines() {
      for (let lineSegment of lines) {
        let start = coordToPixel(lineSegment.start.x, lineSegment.start.y);
        let end = coordToPixel(lineSegment.end.x, lineSegment.end.y);

        if (drawFullLines) {
          // Draw full line extending to canvas edges
          let dx = lineSegment.end.x - lineSegment.start.x;
          let dy = lineSegment.end.y - lineSegment.start.y;

          if (dx === 0) {
            // Vertical line
            let topPx = coordToPixel(lineSegment.start.x, yMax);
            let bottomPx = coordToPixel(lineSegment.start.x, yMin);
            p.stroke(37, 99, 235);
            p.strokeWeight(3);
            p.line(topPx.x, topPx.y, bottomPx.x, bottomPx.y);
          } else {
            // Calculate slope and intercept
            let slope = dy / dx;
            let intercept = lineSegment.start.y - slope * lineSegment.start.x;

            // Find intersection points with canvas edges (in coordinate space first)
            let coordPoints = [];

            let yAtXMin = slope * xMin + intercept;
            if (yAtXMin >= yMin && yAtXMin <= yMax) {
              coordPoints.push({ x: xMin, y: yAtXMin });
            }

            let yAtXMax = slope * xMax + intercept;
            if (yAtXMax >= yMin && yAtXMax <= yMax) {
              coordPoints.push({ x: xMax, y: yAtXMax });
            }

            let xAtYMin = (yMin - intercept) / slope;
            if (xAtYMin >= xMin && xAtYMin <= xMax) {
              coordPoints.push({ x: xAtYMin, y: yMin });
            }

            let xAtYMax = (yMax - intercept) / slope;
            if (xAtYMax >= xMin && xAtYMax <= xMax) {
              coordPoints.push({ x: xAtYMax, y: yMax });
            }

            // Deduplicate points that are too close together (handles corner cases)
            const EPSILON = 0.0001;
            let uniqueCoordPoints = [];
            for (let pt of coordPoints) {
              let isDuplicate = uniqueCoordPoints.some(
                existing => Math.abs(existing.x - pt.x) < EPSILON &&
                            Math.abs(existing.y - pt.y) < EPSILON
              );
              if (!isDuplicate) {
                uniqueCoordPoints.push(pt);
              }
            }

            if (uniqueCoordPoints.length >= 2) {
              let p1 = coordToPixel(uniqueCoordPoints[0].x, uniqueCoordPoints[0].y);
              let p2 = coordToPixel(uniqueCoordPoints[1].x, uniqueCoordPoints[1].y);
              p.stroke(37, 99, 235);
              p.strokeWeight(3);
              p.line(p1.x, p1.y, p2.x, p2.y);
            }
          }
        } else {
          // Draw line segment only
          p.stroke(37, 99, 235);
          p.strokeWeight(3);
          p.line(start.x, start.y, end.x, end.y);
        }

        // Draw endpoint circles
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

      let coordPoints = [];

      let yAtXMin = slope * xMin + intercept;
      if (yAtXMin >= yMin && yAtXMin <= yMax) {
        coordPoints.push({ x: xMin, y: yAtXMin });
      }

      let yAtXMax = slope * xMax + intercept;
      if (yAtXMax >= yMin && yAtXMax <= yMax) {
        coordPoints.push({ x: xMax, y: yAtXMax });
      }

      let xAtYMin = (yMin - intercept) / slope;
      if (xAtYMin >= xMin && xAtYMin <= xMax) {
        coordPoints.push({ x: xAtYMin, y: yMin });
      }

      let xAtYMax = (yMax - intercept) / slope;
      if (xAtYMax >= xMin && xAtYMax <= xMax) {
        coordPoints.push({ x: xAtYMax, y: yMax });
      }

      // Deduplicate points that are too close together (handles corner cases)
      const EPSILON = 0.0001;
      let uniquePoints = [];
      for (let pt of coordPoints) {
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

      // Only show green hover circle in interactive mode
      if (allowInput) {
        p.fill(16, 185, 129, 50);
        p.noStroke();
        p.circle(pos.x, pos.y, 12);
      }

      // Show coordinates if enabled (works in both modes)
      if (showCoordinatesOnHover) {
        p.fill(0);
        p.textSize(11);
        p.textAlign(p.LEFT, p.BOTTOM);
        p.text(`(${hoverPoint.x}, ${hoverPoint.y})`, pos.x + 10, pos.y - 10);
      }
    }

    function drawInstructions() {
      if (!showInstructions) {
        // Draw small toggle button when hidden
        let toggleX = p.width - 35;
        let toggleY = 10;
        let toggleSize = 25;

        p.fill(255, 255, 255, 230);
        p.stroke(200);
        p.strokeWeight(1);
        p.rect(toggleX, toggleY, toggleSize, toggleSize, 5);

        p.noStroke();
        p.fill(100);
        p.textSize(16);
        p.textAlign(p.CENTER, p.CENTER);
        p.text('?', toggleX + toggleSize/2, toggleY + toggleSize/2);
        return;
      }

      let boxX = p.width - 235;
      let boxY = 10;
      let boxWidth = 225;
      let boxHeight = 90;
      if (initialEquations.length > 0) boxHeight += 15;
      if (lines.length > 0) boxHeight += 15;

      p.fill(255, 255, 255, 230);
      p.stroke(200);
      p.strokeWeight(1);
      p.rect(boxX, boxY, boxWidth, boxHeight, 5);

      // Draw close button (X)
      let closeX = boxX + boxWidth - 20;
      let closeY = boxY + 8;
      p.stroke(150);
      p.strokeWeight(2);
      p.line(closeX, closeY, closeX + 8, closeY + 8);
      p.line(closeX + 8, closeY, closeX, closeY + 8);

      p.noStroke();
      p.fill(100);
      p.textSize(10);
      p.textAlign(p.LEFT, p.TOP);
      p.textStyle(p.NORMAL);

      let textX = boxX + 8;
      let y = boxY + 8;

      if (predrawnStartPoint && lines.length === 0) {
        p.text('Hover to preview, click to finish line', textX, y);
        p.text('Line starts from marked point', textX, y + 12);
      } else {
        p.text('Click to start, click again to finish', textX, y);
      }

      // Add delete instruction
      p.text('Click on a line to delete it', textX, y + 28);

      // Color legend
      let legendY = y + 44;
      if (initialEquations.length > 0) {
        p.fill(34, 197, 94);
        p.text('Green = Reference equations', textX, legendY);
        legendY += 15;
      }

      if (lines.length > 0) {
        p.fill(37, 99, 235);
        p.text('Blue = Your drawn line', textX, legendY);
        legendY += 15;
      }

      // Add note about preview
      p.fill(16, 185, 129);
      p.text('Light green = Preview', textX, legendY);
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
      return {
        x: Math.round(coord.x / gridScaleX) * gridScaleX,
        y: Math.round(coord.y / gridScaleY) * gridScaleY
      };
    }

    function isInBounds(px, py) {
      return px >= padding.left &&
             px <= p.width - padding.right &&
             py >= padding.top &&
             py <= p.height - padding.bottom;
    }

    p.mouseMoved = function() {
      // Check if hovering over help button (only in interactive mode)
      if (allowInput) {
        let toggleX = p.width - 35;
        let toggleY = 10;
        let toggleSize = 25;

        if (p.mouseX >= toggleX && p.mouseX <= toggleX + toggleSize &&
            p.mouseY >= toggleY && p.mouseY <= toggleY + toggleSize) {
          p.cursor(p.HAND);
        } else {
          p.cursor(p.ARROW);
        }
      }

      if (!isInBounds(p.mouseX, p.mouseY)) {
        hoverPoint = null;
        return;
      }

      let coord = pixelToCoord(p.mouseX, p.mouseY);
      hoverPoint = snapToGrid(coord);

      // In static mode, only track hover for coordinate display
      if (!allowInput) return;

      // Interactive mode: track for drawing
      // Auto-start drawing from predrawn point when hovering
      if (predrawnStartPoint && lines.length === 0 && !startPoint) {
        startPoint = predrawnStartPoint;
        currentPoint = hoverPoint;
      } else if (startPoint) {
        currentPoint = hoverPoint;
      }
    };

    p.mousePressed = function() {
      // Allow help button interaction even in static mode
      let toggleX = p.width - 35;
      let toggleY = 10;
      let toggleSize = 25;

      if (allowInput && !showInstructions &&
          p.mouseX >= toggleX && p.mouseX <= toggleX + toggleSize &&
          p.mouseY >= toggleY && p.mouseY <= toggleY + toggleSize) {
        showInstructions = true;
        return;
      }

      // Check if clicking the close button (X) when instructions are shown
      if (allowInput && showInstructions) {
        let boxX = p.width - 235;
        let boxY = 10;
        let boxWidth = 225;
        let closeX = boxX + boxWidth - 20;
        let closeY = boxY + 8;
        let closeSize = 8;

        if (p.mouseX >= closeX && p.mouseX <= closeX + closeSize &&
            p.mouseY >= closeY && p.mouseY <= closeY + closeSize) {
          showInstructions = false;
          return;
        }
      }

      if (!allowInput) return; // No drawing in static mode
      if (locked) return;
      if (!isInBounds(p.mouseX, p.mouseY)) return;

      let coord = pixelToCoord(p.mouseX, p.mouseY);
      let snapped = snapToGrid(coord);

      // Check if clicking on an existing line to delete it
      for (let i = lines.length - 1; i >= 0; i--) {
        let lineSegment = lines[i];

        // Check if clicking near the line's endpoints
        let startPx = coordToPixel(lineSegment.start.x, lineSegment.start.y);
        let endPx = coordToPixel(lineSegment.end.x, lineSegment.end.y);

        let distToStart = p.dist(p.mouseX, p.mouseY, startPx.x, startPx.y);
        let distToEnd = p.dist(p.mouseX, p.mouseY, endPx.x, endPx.y);

        // Also check distance to the line itself
        let distToLine = distanceToLineSegment(
          p.mouseX, p.mouseY,
          startPx.x, startPx.y,
          endPx.x, endPx.y
        );

        if (distToStart < 15 || distToEnd < 15 || distToLine < 10) {
          // Delete this line
          lines.splice(i, 1);
          onLinesChanged([...lines]);
          return;
        }
      }

      if (!startPoint) {
        // Normal mode: click to start (not using predrawnStartPoint)
        startPoint = snapped;
        currentPoint = snapped;
      } else {
        // Finish the line (works for both predrawn auto-start and normal start)
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

    // Helper function to calculate distance from point to line segment
    function distanceToLineSegment(px, py, x1, y1, x2, y2) {
      let dx = x2 - x1;
      let dy = y2 - y1;
      let len2 = dx*dx + dy*dy;

      if (len2 === 0) return p.dist(px, py, x1, y1);

      let t = ((px - x1) * dx + (py - y1) * dy) / len2;
      t = p.constrain(t, 0, 1);

      let projX = x1 + t * dx;
      let projY = y1 + t * dy;

      return p.dist(px, py, projX, projY);
    }

    p.keyPressed = function() {
      // H key toggles instructions (only in interactive mode)
      if (allowInput && (p.key === 'h' || p.key === 'H')) {
        showInstructions = !showInstructions;
        return;
      }

      if (!allowInput) return; // No keyboard interaction in static mode
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

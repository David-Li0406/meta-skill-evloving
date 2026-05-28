import { ExampleSketch } from "../../types";

export const DILATION_ANIMATION: ExampleSketch = {
  id: "dilation-scale-factor",
  name: "Dilation with Scale Factor",
  description: "Interactive dilation centered at a point with adjustable scale factor",
  code: `// Dilation Animation with Scale Factor Slider
// Configurable polygon points and center of dilation

// ==========================================
// CONFIGURATION - Easily modifiable
// ==========================================

// Polygon vertices (parallelogram PQRS)
let points = [
  { x: 10, y: 10, label: 'P' },
  { x: 8, y: 8, label: 'Q' },
  { x: 12, y: 6, label: 'R' },
  { x: 14, y: 8, label: 'S' }
];

// Center of dilation
let center = { x: 10, y: 8, label: 'O' };

// Scale factors available
let scaleFactors = [
  { value: 1/3, label: '1/3' },
  { value: 1/2, label: '1/2' },
  { value: 1, label: '1' },
  { value: 2, label: '2' },
  { value: 3, label: '3' },
  { value: 4, label: '4' }
];

// Current scale factor index
let scaleIndex = 3; // Start at scale factor 2

// Toggle for showing dilation rays
let showRays = true;

// Toggle for showing grid and axes
let showGrid = true;

// Axis ranges
let xMin = 0, xMax = 20;
let yMin = 0, yMax = 15;

// Colors
let originalColor = [59, 130, 246]; // Blue
let dilatedColor = [239, 68, 68];   // Red
let gridColor = 220;
let axisColor = 100;

// ==========================================
// END CONFIGURATION
// ==========================================

// Padding
let padding = { top: 40, right: 40, bottom: 60, left: 60 };

function setup() {
  createCanvas(600, 600);
  textFont('Arial');
}

function draw() {
  background(255);

  let plotWidth = width - padding.left - padding.right;
  let plotHeight = height - padding.top - padding.bottom;
  let scaleFactor = scaleFactors[scaleIndex].value;

  // Draw grid
  if (showGrid) {
    drawGrid(plotWidth, plotHeight);

    // Draw axes labels
    drawAxes(plotWidth, plotHeight);
  }

  // Calculate dilated points
  let dilatedPoints = points.map(p => ({
    x: center.x + (p.x - center.x) * scaleFactor,
    y: center.y + (p.y - center.y) * scaleFactor,
    label: p.label + "'"
  }));

  // Draw dilation rays (from center, extending outward)
  if (showRays) {
    stroke(0);
    strokeWeight(2);
    drawingContext.setLineDash([4, 4]);
    for (let i = 0; i < points.length; i++) {
      let centerPixelPos = coordToPixel(center.x, center.y, plotWidth, plotHeight);
      let pointPixel = coordToPixel(points[i].x, points[i].y, plotWidth, plotHeight);

      // Calculate direction vector
      let dx = pointPixel.x - centerPixelPos.x;
      let dy = pointPixel.y - centerPixelPos.y;

      // Ray starts at center and extends far in the direction of the point
      let scale = 1000;
      let x2 = centerPixelPos.x + dx * scale;
      let y2 = centerPixelPos.y + dy * scale;

      line(centerPixelPos.x, centerPixelPos.y, x2, y2);
    }
    drawingContext.setLineDash([]);
  }

  // Draw original polygon
  drawPolygon(points, originalColor, plotWidth, plotHeight);

  // Draw dilated polygon (always show)
  drawPolygon(dilatedPoints, dilatedColor, plotWidth, plotHeight);

  // Draw center point
  let centerPixel = coordToPixel(center.x, center.y, plotWidth, plotHeight);
  fill(0);
  noStroke();
  circle(centerPixel.x, centerPixel.y, 10);

  if (center.label) {
    textAlign(LEFT, CENTER);
    textSize(14);
    text(center.label, centerPixel.x + 12, centerPixel.y);
  }

  // Draw slider
  drawSlider();

  // Draw legend
  drawLegend();

  // Title
  fill(75, 50, 120);
  textAlign(CENTER, TOP);
  textSize(18);
  textStyle(BOLD);
  text('Dilation centered at ' + center.label + ' with scale factor ' + scaleFactors[scaleIndex].label, width/2, 10);
  textStyle(NORMAL);
}

function coordToPixel(x, y, plotWidth, plotHeight) {
  let px = padding.left + ((x - xMin) / (xMax - xMin)) * plotWidth;
  let py = padding.top + ((yMax - y) / (yMax - yMin)) * plotHeight;
  return { x: px, y: py };
}

function drawGrid(plotWidth, plotHeight) {
  stroke(gridColor);
  strokeWeight(1);

  // Vertical lines
  for (let x = xMin; x <= xMax; x++) {
    let pos = coordToPixel(x, yMin, plotWidth, plotHeight);
    let posTop = coordToPixel(x, yMax, plotWidth, plotHeight);
    if (x === 0) {
      stroke(axisColor);
      strokeWeight(2);
    } else {
      stroke(gridColor);
      strokeWeight(1);
    }
    line(pos.x, posTop.y, pos.x, pos.y);
  }

  // Horizontal lines
  for (let y = yMin; y <= yMax; y++) {
    let pos = coordToPixel(xMin, y, plotWidth, plotHeight);
    let posRight = coordToPixel(xMax, y, plotWidth, plotHeight);
    if (y === 0) {
      stroke(axisColor);
      strokeWeight(2);
    } else {
      stroke(gridColor);
      strokeWeight(1);
    }
    line(pos.x, pos.y, posRight.x, pos.y);
  }

  // Border
  stroke(200);
  strokeWeight(1);
  noFill();
  rect(padding.left, padding.top, plotWidth, plotHeight);
}

function drawAxes(plotWidth, plotHeight) {
  fill(100);
  textSize(10);
  noStroke();

  // X-axis labels
  textAlign(CENTER, TOP);
  for (let x = xMin; x <= xMax; x += 2) {
    let pos = coordToPixel(x, yMin, plotWidth, plotHeight);
    text(x, pos.x, pos.y + 5);
  }

  // Y-axis labels
  textAlign(RIGHT, CENTER);
  for (let y = yMin; y <= yMax; y += 2) {
    let pos = coordToPixel(xMin, y, plotWidth, plotHeight);
    text(y, pos.x - 5, pos.y);
  }
}

function drawPolygon(pts, col, plotWidth, plotHeight) {
  // Fill
  fill(col[0], col[1], col[2], 50);
  stroke(col[0], col[1], col[2]);
  strokeWeight(2);

  beginShape();
  for (let p of pts) {
    let pixel = coordToPixel(p.x, p.y, plotWidth, plotHeight);
    vertex(pixel.x, pixel.y);
  }
  endShape(CLOSE);

  // Draw vertices and labels
  for (let p of pts) {
    let pixel = coordToPixel(p.x, p.y, plotWidth, plotHeight);

    fill(col[0], col[1], col[2]);
    noStroke();
    circle(pixel.x, pixel.y, 8);

    if (p.label) {
      textAlign(LEFT, BOTTOM);
      textSize(12);
      textStyle(BOLD);
      text(p.label, pixel.x + 6, pixel.y - 6);
      textStyle(NORMAL);
    }
  }
}

function drawSlider() {
  let sliderY = height - 30;
  let sliderX = 100;
  let sliderWidth = 400;

  // Track
  stroke(200);
  strokeWeight(4);
  line(sliderX, sliderY, sliderX + sliderWidth, sliderY);

  // Scale factor positions
  for (let i = 0; i < scaleFactors.length; i++) {
    let x = sliderX + (i / (scaleFactors.length - 1)) * sliderWidth;

    // Tick mark
    stroke(150);
    strokeWeight(2);
    line(x, sliderY - 5, x, sliderY + 5);

    // Label
    fill(i === scaleIndex ? 0 : 150);
    noStroke();
    textAlign(CENTER, TOP);
    textSize(10);
    textStyle(i === scaleIndex ? BOLD : NORMAL);
    text(scaleFactors[i].label, x, sliderY + 8);
    textStyle(NORMAL);
  }

  // Current position handle
  let handleX = sliderX + (scaleIndex / (scaleFactors.length - 1)) * sliderWidth;
  fill(75, 50, 120);
  noStroke();
  circle(handleX, sliderY, 16);

  // Scale factor label
  fill(0);
  textAlign(RIGHT, CENTER);
  textSize(12);
  text('Scale Factor:', sliderX - 10, sliderY);
}

function drawLegend() {
  let legendX = width - 120;
  let legendY = padding.top + 10;

  textAlign(LEFT, CENTER);
  textSize(11);

  // Original
  fill(originalColor[0], originalColor[1], originalColor[2]);
  noStroke();
  rect(legendX, legendY, 12, 12);
  fill(0);
  text('Original', legendX + 18, legendY + 6);

  // Dilated
  fill(dilatedColor[0], dilatedColor[1], dilatedColor[2]);
  rect(legendX, legendY + 18, 12, 12);
  fill(0);
  text('Dilated', legendX + 18, legendY + 24);

  // Center
  fill(0);
  circle(legendX + 6, legendY + 42, 8);
  text('Center', legendX + 18, legendY + 42);

  // Toggle instructions
  textSize(9);
  fill(100);
  text('D: Rays ' + (showRays ? 'ON' : 'OFF'), legendX, legendY + 60);
  text('G: Grid ' + (showGrid ? 'ON' : 'OFF'), legendX, legendY + 74);
}

function mousePressed() {
  // Check if clicking on slider
  let sliderY = height - 30;
  let sliderX = 100;
  let sliderWidth = 400;

  if (mouseY > sliderY - 20 && mouseY < sliderY + 20) {
    if (mouseX >= sliderX && mouseX <= sliderX + sliderWidth) {
      // Find closest scale factor
      let normalized = (mouseX - sliderX) / sliderWidth;
      scaleIndex = round(normalized * (scaleFactors.length - 1));
      scaleIndex = constrain(scaleIndex, 0, scaleFactors.length - 1);
    }
  }
}

function mouseDragged() {
  mousePressed(); // Allow dragging the slider
}

function keyPressed() {
  if (keyCode === LEFT_ARROW && scaleIndex > 0) {
    scaleIndex--;
  } else if (keyCode === RIGHT_ARROW && scaleIndex < scaleFactors.length - 1) {
    scaleIndex++;
  } else if (key === 'r' || key === 'R') {
    scaleIndex = 2; // Reset to scale factor 1
  } else if (key === 'd' || key === 'D') {
    showRays = !showRays; // Toggle dilation rays
  } else if (key === 'g' || key === 'G') {
    showGrid = !showGrid; // Toggle grid
  }
}`,
};

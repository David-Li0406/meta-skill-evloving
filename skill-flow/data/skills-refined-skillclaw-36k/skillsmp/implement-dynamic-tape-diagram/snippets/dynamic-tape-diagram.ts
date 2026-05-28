// ==========================================
// CONFIGURATION - Easily modifiable
// ==========================================

// Palette items (draggable sources)
let paletteConfig = {
  variable: {
    x: 80,
    y: 100,
    w: 60,
    h: 60,
    color: [230, 57, 70],      // Red for variables
    label: 'x'
  },
  constant: {
    x: 200,
    y: 100,
    w: 100,                    // Initial width (resizable)
    h: 60,
    minWidth: 40,              // Minimum size
    maxWidth: 300,             // Maximum size
    initialValue: 1,
    maxValue: 20,
    color: [6, 167, 125],      // Green for constants
  }
};

// Tape diagram drop zone
let tapeConfig = {
  x: 50,
  y: 320,
  w: 500,
  h: 100,
  backgroundColor: [240, 240, 240],
  borderColor: [150, 150, 150],
  emptyLabel: 'Drag parts here to build your equation'
};

// Total value settings
let totalConfig = {
  initial: 0,                  // Starting total value
  min: 0,
  max: 1000,
  step: 1,
  showProportions: true        // Show calculated values when total is set
};

// Visual settings
let visualConfig = {
  showEquation: true,          // Display equation text
  showInstructions: true,      // Show helper text
  animateTransitions: true,    // Smooth width changes
  highlightDropZone: true      // Highlight when dragging
};

// ==========================================
// END CONFIGURATION
// ==========================================

// State variables
let tapeParts = [];            // Parts in the tape diagram
let nextId = 0;                // ID counter for parts
let totalValue = 0;            // Current total value
let selectedPartId = null;     // Currently selected part

// Drag state
let isDraggingVariable = false;
let isDraggingConstant = false;
let dragOffsetX = 0;
let dragOffsetY = 0;
let dragStartX = 0;
let dragStartY = 0;

// Resize state
let isResizingConstant = false;
let resizeEdge = null;         // 'left' or 'right'
let resizeStartX = 0;
let resizeStartWidth = 0;

// Constant bar state
let constantBarValue = 1;

function setup() {
  createCanvas(600, 600);
  textFont('Arial');
  totalValue = totalConfig.initial;
  constantBarValue = paletteConfig.constant.initialValue;
  paletteConfig.constant.w = calculateConstantWidth(constantBarValue);
}

function draw() {
  background(255, 255, 255);

  // Title
  fill(75, 50, 120);
  textSize(24);
  textStyle(BOLD);
  textAlign(CENTER, TOP);
  text('Build Your Tape Diagram', 300, 10);

  // Draw palette area
  drawPaletteSection();

  // Draw total value controls
  drawTotalValueSection();

  // Draw equation display
  if (visualConfig.showEquation && tapeParts.length > 0) {
    drawEquationDisplay();
  }

  // Draw tape diagram
  drawTapeDiagram();

  // Draw instructions
  if (visualConfig.showInstructions) {
    drawInstructions();
  }

  // Draw item being dragged (on top of everything)
  if (isDraggingVariable) {
    drawDraggedVariable();
  }
  if (isDraggingConstant) {
    drawDraggedConstant();
  }
}

function drawPaletteSection() {
  // Section label
  fill(0, 0, 0);
  textSize(14);
  textStyle(BOLD);
  textAlign(LEFT, TOP);
  text('Drag to add:', 50, 70);

  // Variable icon (x)
  let vConfig = paletteConfig.variable;
  let isHoveringVar = isMouseOverVariable();

  fill(vConfig.color[0], vConfig.color[1], vConfig.color[2], isDraggingVariable ? 100 : 255);
  stroke(vConfig.color[0] - 30, vConfig.color[1] - 30, vConfig.color[2] - 30);
  strokeWeight(3);
  rect(vConfig.x, vConfig.y, vConfig.w, vConfig.h, 8);

  // Highlight on hover
  if (isHoveringVar && !isDraggingVariable && !isDraggingConstant) {
    fill(255, 255, 255, 80);
    noStroke();
    rect(vConfig.x, vConfig.y, vConfig.w, vConfig.h, 8);
    cursor(HAND);
  }

  // Label
  fill(255, 255, 255);
  noStroke();
  textSize(28);
  textStyle(BOLD);
  textAlign(CENTER, CENTER);
  text(vConfig.label, vConfig.x + vConfig.w/2, vConfig.y + vConfig.h/2);

  // Constant bar
  let cConfig = paletteConfig.constant;
  let isHoveringConst = isMouseOverConstant();
  let nearLeftEdge = isNearConstantLeftEdge();
  let nearRightEdge = isNearConstantRightEdge();

  fill(cConfig.color[0], cConfig.color[1], cConfig.color[2], isDraggingConstant ? 100 : 255);
  stroke(cConfig.color[0] - 30, cConfig.color[1] - 30, cConfig.color[2] - 30);
  strokeWeight(3);
  rect(cConfig.x, cConfig.y, cConfig.w, cConfig.h, 8);

  // Resize handles
  if (!isDraggingConstant && !isDraggingVariable) {
    // Left handle
    fill(nearLeftEdge ? [75, 50, 120] : [200, 200, 200]);
    noStroke();
    rect(cConfig.x, cConfig.y, 10, cConfig.h, 8, 0, 0, 8);

    // Right handle
    fill(nearRightEdge ? [75, 50, 120] : [200, 200, 200]);
    rect(cConfig.x + cConfig.w - 10, cConfig.y, 10, cConfig.h, 0, 8, 8, 0);
  }

  // Hover effect for dragging
  if (isHoveringConst && !nearLeftEdge && !nearRightEdge && !isDraggingConstant && !isDraggingVariable) {
    fill(255, 255, 255, 80);
    noStroke();
    rect(cConfig.x, cConfig.y, cConfig.w, cConfig.h, 8);
    cursor(HAND);
  }

  // Resize cursor
  if ((nearLeftEdge || nearRightEdge) && !isDraggingConstant && !isDraggingVariable) {
    cursor('ew-resize');
  }

  // Value label
  fill(255, 255, 255);
  noStroke();
  textSize(24);
  textStyle(BOLD);
  textAlign(CENTER, CENTER);
  text(constantBarValue, cConfig.x + cConfig.w/2, cConfig.y + cConfig.h/2);

  // Reset cursor if not hovering anything
  if (!isHoveringVar && !isHoveringConst && !nearLeftEdge && !nearRightEdge && !isResizingConstant && !isDraggingVariable && !isDraggingConstant) {
    cursor(ARROW);
  }
}

function drawTotalValueSection() {
  let inputArea = {x: 50, y: 200, w: 280, h: 70};

  fill(0, 0, 0);
  textSize(14);
  textStyle(BOLD);
  textAlign(LEFT, TOP);
  text('Total Value:', inputArea.x, inputArea.y);

  // Display box
  stroke(0, 0, 0);
  strokeWeight(2);
  fill(255, 255, 255);
  rect(inputArea.x, inputArea.y + 25, 120, 35, 4);

  fill(0, 0, 0);
  noStroke();
  textSize(20);
  textAlign(CENTER, CENTER);
  text(totalValue > 0 ? totalValue : '0', inputArea.x + 60, inputArea.y + 42);

  // Plus/minus buttons
  let btnSize = 35;
  let btnY = inputArea.y + 25;

  // Minus button
  let minusX = inputArea.x + 130;
  let isHoveringMinus = mouseX > minusX && mouseX < minusX + btnSize &&
                        mouseY > btnY && mouseY < btnY + btnSize;
  fill(230, 57, 70);
  noStroke();
  rect(minusX, btnY, btnSize, btnSize, 4);
  if (isHoveringMinus) {
    fill(255, 255, 255, 60);
    rect(minusX, btnY, btnSize, btnSize, 4);
    cursor(HAND);
  }
  fill(255, 255, 255);
  textSize(24);
  textStyle(BOLD);
  textAlign(CENTER, CENTER);
  text('−', minusX + btnSize/2, btnY + btnSize/2);

  // Plus button
  let plusX = inputArea.x + 170;
  let isHoveringPlus = mouseX > plusX && mouseX < plusX + btnSize &&
                       mouseY > btnY && mouseY < btnY + btnSize;
  fill(6, 167, 125);
  noStroke();
  rect(plusX, btnY, btnSize, btnSize, 4);
  if (isHoveringPlus) {
    fill(255, 255, 255, 60);
    rect(plusX, btnY, btnSize, btnSize, 4);
    cursor(HAND);
  }
  fill(255, 255, 255);
  textSize(24);
  textStyle(BOLD);
  text('+', plusX + btnSize/2, btnY + btnSize/2);
}

function drawEquationDisplay() {
  let equation = tapeParts.map(p => {
    if (p.type === 'variable') return 'x';
    return p.value.toString();
  }).join(' + ');

  if (totalValue > 0) {
    equation += ' = ' + totalValue;
  }

  fill(15, 35, 65);
  textSize(18);
  textStyle(NORMAL);
  textAlign(CENTER, TOP);
  text('Equation: ' + equation, 400, 220);
}

function drawTapeDiagram() {
  let zone = tapeConfig;

  // Drop zone background
  if (visualConfig.highlightDropZone && (isDraggingVariable || isDraggingConstant)) {
    fill(zone.backgroundColor[0], zone.backgroundColor[1], zone.backgroundColor[2], 200);
    stroke(75, 50, 120);
    strokeWeight(3);
  } else {
    fill(zone.backgroundColor[0], zone.backgroundColor[1], zone.backgroundColor[2]);
    stroke(zone.borderColor[0], zone.borderColor[1], zone.borderColor[2]);
    strokeWeight(2);
  }
  rect(zone.x, zone.y, zone.w, zone.h, 8);

  if (tapeParts.length === 0) {
    // Empty state
    fill(150, 150, 150);
    noStroke();
    textSize(14);
    textStyle(NORMAL);
    textAlign(CENTER, CENTER);
    text(zone.emptyLabel, zone.x + zone.w/2, zone.y + zone.h/2);
  } else {
    // Draw parts
    drawTapeParts();
  }
}

function drawTapeParts() {
  // Solve for x if total is set
  // Equation: (numVariables * x) + sumOfConstants = totalValue
  // Solve: x = (totalValue - sumOfConstants) / numVariables
  let numVariables = tapeParts.filter(p => p.type === 'variable').length;
  let sumOfConstants = tapeParts.reduce((sum, p) => {
    return sum + (p.type === 'constant' ? p.value : 0);
  }, 0);

  let xValue = 0;
  if (totalValue > 0 && numVariables > 0) {
    xValue = (totalValue - sumOfConstants) / numVariables;
  }

  // Calculate total bar value for proportional widths
  let totalBarValue = 0;
  if (totalValue > 0) {
    totalBarValue = totalValue;
  } else {
    // When no total is set, use sum of parts for relative sizing
    totalBarValue = tapeParts.reduce((sum, p) => {
      return sum + (p.type === 'variable' ? 1 : p.value);
    }, 0);
  }

  if (totalBarValue === 0) return;

  // Draw each part
  let currentX = tapeConfig.x + 10;
  let availableWidth = tapeConfig.w - 20;
  let partY = tapeConfig.y + 10;
  let partHeight = tapeConfig.h - 20;

  tapeParts.forEach((part, index) => {
    // Calculate the actual value of this part
    let partActualValue;
    if (part.type === 'variable') {
      partActualValue = totalValue > 0 ? xValue : 1;  // Use solved x value or 1 for sizing
    } else {
      partActualValue = part.value;  // Constants keep their value
    }

    // Calculate width proportional to actual value
    let partWidth = (partActualValue / totalBarValue) * availableWidth;

    // Minimum width for visibility
    partWidth = max(partWidth, 50);

    let isSelected = part.id === selectedPartId;
    let isHovering = mouseX > currentX && mouseX < currentX + partWidth &&
                     mouseY > partY && mouseY < partY + partHeight &&
                     !isDraggingVariable && !isDraggingConstant;

    // Part color
    if (part.type === 'variable') {
      fill(230, 57, 70, isSelected ? 200 : 255);
      stroke(210, 37, 50);
    } else {
      fill(6, 167, 125, isSelected ? 200 : 255);
      stroke(5, 137, 105);
    }
    strokeWeight(3);
    rect(currentX, partY, partWidth, partHeight, 6);

    // Selection highlight
    if (isSelected) {
      stroke(255, 220, 80);
      strokeWeight(5);
      noFill();
      rect(currentX, partY, partWidth, partHeight, 6);
    }

    // Hover effect
    if (isHovering) {
      fill(255, 255, 255, 60);
      noStroke();
      rect(currentX, partY, partWidth, partHeight, 6);
      cursor(HAND);
    }

    // Part label
    fill(255, 255, 255);
    noStroke();
    textSize(partWidth > 80 ? 20 : 16);
    textStyle(BOLD);
    textAlign(CENTER, CENTER);
    let label = part.type === 'variable' ? 'x' : part.value.toString();
    text(label, currentX + partWidth/2, partY + partHeight/2);

    // Remove button (X)
    let removeSize = 18;
    let removeX = currentX + partWidth - removeSize - 5;
    let removeY = partY + 5;

    fill(230, 57, 70);
    noStroke();
    circle(removeX + removeSize/2, removeY + removeSize/2, removeSize);

    fill(255, 255, 255);
    textSize(14);
    textStyle(BOLD);
    textAlign(CENTER, CENTER);
    text('×', removeX + removeSize/2, removeY + removeSize/2);

    // Store bounds for interaction
    part.bounds = {x: currentX, y: partY, w: partWidth, h: partHeight};
    part.removeBtn = {x: removeX, y: removeY, w: removeSize, h: removeSize};

    currentX += partWidth + 5;
  });

  // Draw curly brace and total value above the tape
  if (totalValue > 0) {
    let tapeWidth = currentX - tapeStartX - 5;
    let braceY = tapeConfig.y - 20;
    let braceStartX = tapeStartX;
    let braceEndX = currentX - 5;
    let braceMidX = (braceStartX + braceEndX) / 2;

    // Draw curly brace
    stroke(0, 0, 0);
    strokeWeight(2);
    noFill();

    // Left curve
    beginShape();
    vertex(braceStartX, tapeConfig.y - 5);
    bezierVertex(
      braceStartX, braceY + 5,
      braceStartX + 20, braceY,
      braceMidX - 10, braceY
    );
    endShape();

    // Center point (dip down)
    beginShape();
    vertex(braceMidX - 10, braceY);
    bezierVertex(
      braceMidX - 5, braceY,
      braceMidX - 3, braceY - 5,
      braceMidX, braceY - 8
    );
    endShape();

    beginShape();
    vertex(braceMidX, braceY - 8);
    bezierVertex(
      braceMidX + 3, braceY - 5,
      braceMidX + 5, braceY,
      braceMidX + 10, braceY
    );
    endShape();

    // Right curve
    beginShape();
    vertex(braceMidX + 10, braceY);
    bezierVertex(
      braceEndX - 20, braceY,
      braceEndX, braceY + 5,
      braceEndX, tapeConfig.y - 5
    );
    endShape();

    // Total value text above brace
    fill(0, 0, 0);
    noStroke();
    textSize(20);
    textStyle(BOLD);
    textAlign(CENTER, BOTTOM);
    text(totalValue, braceMidX, braceY - 5);
  }
}

function drawDraggedVariable() {
  let vConfig = paletteConfig.variable;
  let x = mouseX - vConfig.w/2;
  let y = mouseY - vConfig.h/2;

  fill(vConfig.color[0], vConfig.color[1], vConfig.color[2], 200);
  stroke(vConfig.color[0] - 30, vConfig.color[1] - 30, vConfig.color[2] - 30);
  strokeWeight(3);
  rect(x, y, vConfig.w, vConfig.h, 8);

  fill(255, 255, 255);
  noStroke();
  textSize(28);
  textStyle(BOLD);
  textAlign(CENTER, CENTER);
  text(vConfig.label, x + vConfig.w/2, y + vConfig.h/2);
}

function drawDraggedConstant() {
  let cConfig = paletteConfig.constant;
  let x = mouseX + dragOffsetX;
  let y = mouseY + dragOffsetY;

  fill(cConfig.color[0], cConfig.color[1], cConfig.color[2], 200);
  stroke(cConfig.color[0] - 30, cConfig.color[1] - 30, cConfig.color[2] - 30);
  strokeWeight(3);
  rect(x, y, cConfig.w, cConfig.h, 8);

  fill(255, 255, 255);
  noStroke();
  textSize(24);
  textStyle(BOLD);
  textAlign(CENTER, CENTER);
  text(constantBarValue, x + cConfig.w/2, y + cConfig.h/2);
}

function drawInstructions() {
  fill(100, 100, 100);
  textSize(11);
  textStyle(NORMAL);
  textAlign(LEFT, TOP);
  let y = 450;
  text('• Drag edges of number to resize it', 50, y);
  text('• Drag parts into the tape diagram', 50, y + 20);
  text('• Set total value to see proportional sizing', 50, y + 40);
  text('• Click × to remove parts', 50, y + 60);
}

// Helper functions for mouse detection

function isMouseOverVariable() {
  let v = paletteConfig.variable;
  return mouseX > v.x && mouseX < v.x + v.w &&
         mouseY > v.y && mouseY < v.y + v.h;
}

function isMouseOverConstant() {
  let c = paletteConfig.constant;
  return mouseX > c.x + 10 && mouseX < c.x + c.w - 10 &&
         mouseY > c.y && mouseY < c.y + c.h;
}

function isNearConstantLeftEdge() {
  let c = paletteConfig.constant;
  return mouseX > c.x && mouseX < c.x + 10 &&
         mouseY > c.y && mouseY < c.y + c.h;
}

function isNearConstantRightEdge() {
  let c = paletteConfig.constant;
  return mouseX > c.x + c.w - 10 && mouseX < c.x + c.w &&
         mouseY > c.y && mouseY < c.y + c.h;
}

function isMouseOverDropZone() {
  let z = tapeConfig;
  return mouseX > z.x && mouseX < z.x + z.w &&
         mouseY > z.y && mouseY < z.y + z.h;
}

function calculateConstantWidth(value) {
  let c = paletteConfig.constant;
  let minW = c.minWidth;
  let maxW = c.maxWidth;
  let range = maxW - minW;
  let valueRange = c.maxValue - c.initialValue;
  return minW + (value - c.initialValue) * (range / valueRange);
}

function calculateConstantValueFromWidth(width) {
  let c = paletteConfig.constant;
  let minW = c.minWidth;
  let maxW = c.maxWidth;
  let range = maxW - minW;
  let valueRange = c.maxValue - c.initialValue;
  let value = c.initialValue + (width - minW) * (valueRange / range);
  return constrain(round(value), c.initialValue, c.maxValue);
}

// Mouse event handlers

function mousePressed() {
  // Check total value buttons
  let inputArea = {x: 50, y: 200};
  let btnSize = 35;
  let btnY = inputArea.y + 25;
  let minusX = inputArea.x + 130;
  let plusX = inputArea.x + 170;

  if (mouseX > minusX && mouseX < minusX + btnSize &&
      mouseY > btnY && mouseY < btnY + btnSize) {
    totalValue = max(totalConfig.min, totalValue - totalConfig.step);
    return;
  }

  if (mouseX > plusX && mouseX < plusX + btnSize &&
      mouseY > btnY && mouseY < btnY + btnSize) {
    totalValue = min(totalConfig.max, totalValue + totalConfig.step);
    return;
  }

  // Check if clicking on a tape part or remove button
  for (let part of tapeParts) {
    if (!part.bounds) continue;

    // Check remove button
    if (part.removeBtn) {
      let btn = part.removeBtn;
      if (mouseX > btn.x && mouseX < btn.x + btn.w &&
          mouseY > btn.y && mouseY < btn.y + btn.h) {
        removePart(part.id);
        return;
      }
    }

    // Check part selection
    if (mouseX > part.bounds.x && mouseX < part.bounds.x + part.bounds.w &&
        mouseY > part.bounds.y && mouseY < part.bounds.y + part.bounds.h) {
      selectedPartId = part.id === selectedPartId ? null : part.id;
      return;
    }
  }

  // Check resize handles
  if (isNearConstantLeftEdge() || isNearConstantRightEdge()) {
    isResizingConstant = true;
    resizeEdge = isNearConstantLeftEdge() ? 'left' : 'right';
    resizeStartX = mouseX;
    resizeStartWidth = paletteConfig.constant.w;
    return;
  }

  // Check dragging from palette
  if (isMouseOverVariable()) {
    isDraggingVariable = true;
    dragStartX = paletteConfig.variable.x;
    dragStartY = paletteConfig.variable.y;
    return;
  }

  if (isMouseOverConstant()) {
    isDraggingConstant = true;
    dragStartX = paletteConfig.constant.x;
    dragStartY = paletteConfig.constant.y;
    dragOffsetX = paletteConfig.constant.x - mouseX;
    dragOffsetY = paletteConfig.constant.y - mouseY;
    return;
  }

  // Click elsewhere deselects
  selectedPartId = null;
}

function mouseDragged() {
  if (isResizingConstant) {
    let delta = mouseX - resizeStartX;
    let newWidth;

    if (resizeEdge === 'right') {
      newWidth = resizeStartWidth + delta;
    } else {
      newWidth = resizeStartWidth - delta;
    }

    let c = paletteConfig.constant;
    newWidth = constrain(newWidth, c.minWidth, c.maxWidth);
    paletteConfig.constant.w = newWidth;
    constantBarValue = calculateConstantValueFromWidth(newWidth);
  }
}

function mouseReleased() {
  if (isResizingConstant) {
    isResizingConstant = false;
    resizeEdge = null;
    return;
  }

  if (isDraggingVariable) {
    if (isMouseOverDropZone()) {
      addVariableToTape();
    }
    isDraggingVariable = false;
    return;
  }

  if (isDraggingConstant) {
    if (isMouseOverDropZone()) {
      addConstantToTape();
    }
    isDraggingConstant = false;
    return;
  }
}

// Part management

function addVariableToTape() {
  tapeParts.push({
    type: 'variable',
    value: 1,
    id: nextId++
  });
}

function addConstantToTape() {
  tapeParts.push({
    type: 'constant',
    value: constantBarValue,
    id: nextId++
  });
}

function removePart(id) {
  tapeParts = tapeParts.filter(p => p.id !== id);
  if (selectedPartId === id) {
    selectedPartId = null;
  }
}

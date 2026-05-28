// ==========================================
// CONFIGURATION - Easily modifiable
// ==========================================

// Tile types configuration
let tileConfig = {
  x: {
    width: 80,
    height: 60,
    color: [102, 178, 102],      // Green for positive x
    label: 'x',
    value: 'x',
    sign: 'positive'
  },
  negX: {
    width: 80,
    height: 60,
    color: [230, 57, 70],        // Red for negative x
    label: '-x',
    value: 'x',
    sign: 'negative'
  },
  one: {
    width: 50,
    height: 50,
    color: [255, 193, 94],       // Yellow/gold for positive 1
    label: '1',
    value: '1',
    sign: 'positive'
  },
  negOne: {
    width: 50,
    height: 50,
    color: [230, 57, 70],        // Red for negative 1
    label: '-1',
    value: '1',
    sign: 'negative'
  }
};

// Palette layout (where tiles can be dragged from)
let paletteConfig = {
  x: 80,
  y: 100,
  spacing: 100,
  label: 'Drag tiles onto canvas:'
};

// Canvas area (drop zone)
let canvasConfig = {
  x: 50,
  y: 250,
  w: 500,
  h: 300,
  backgroundColor: [245, 245, 245],
  borderColor: [180, 180, 180],
  label: 'Workspace'
};

// Cancellation settings
let cancelConfig = {
  snapDistance: 40,              // How close tiles need to be to link
  cancelledColor: [150, 150, 150], // Grey color for cancelled tiles
  showCancelledLabel: true
};

// Visual settings
let visualConfig = {
  showInstructions: true,
  highlightOnHover: true,
  showEquation: true
};

// ==========================================
// END CONFIGURATION
// ==========================================

// State variables
let placedTiles = [];           // Tiles placed on canvas
let nextTileId = 0;             // ID counter for tiles
let draggedTile = null;         // Currently dragged tile
let dragOffset = {x: 0, y: 0};  // Offset for smooth dragging
let hoveredPaletteTile = null;  // Which palette tile is hovered

function setup() {
  createCanvas(600, 600);
  textFont('Arial');
}

function draw() {
  background(255, 255, 255);

  // Title
  fill(75, 50, 120);
  textSize(24);
  textStyle(BOLD);
  textAlign(CENTER, TOP);
  text('Algebra Tiles', 300, 10);

  // Draw palette section
  drawPalette();

  // Draw canvas area
  drawCanvasArea();

  // Draw placed tiles
  drawPlacedTiles();

  // Draw dragged tile on top
  if (draggedTile) {
    drawDraggedTile();
  }

  // Draw equation
  if (visualConfig.showEquation && placedTiles.length > 0) {
    drawEquation();
  }

  // Draw instructions
  if (visualConfig.showInstructions) {
    drawInstructions();
  }
}

function drawPalette() {
  // Label
  fill(0, 0, 0);
  textSize(14);
  textStyle(BOLD);
  textAlign(LEFT, TOP);
  text(paletteConfig.label, paletteConfig.x, paletteConfig.y - 30);

  // Draw each tile type in palette
  let currentX = paletteConfig.x;
  let types = ['x', 'negX', 'one', 'negOne'];

  types.forEach((type, index) => {
    let config = tileConfig[type];
    let isHovered = hoveredPaletteTile === type && !draggedTile;

    // Draw tile
    drawTile(currentX, paletteConfig.y, config, false, isHovered, 1);

    // Move to next position
    currentX += paletteConfig.spacing;
  });
}

function drawCanvasArea() {
  // Background
  fill(canvasConfig.backgroundColor[0], canvasConfig.backgroundColor[1], canvasConfig.backgroundColor[2]);
  stroke(canvasConfig.borderColor[0], canvasConfig.borderColor[1], canvasConfig.borderColor[2]);
  strokeWeight(2);
  rect(canvasConfig.x, canvasConfig.y, canvasConfig.w, canvasConfig.h, 8);

  // Label
  if (placedTiles.length === 0) {
    fill(150, 150, 150);
    noStroke();
    textSize(14);
    textStyle(NORMAL);
    textAlign(CENTER, CENTER);
    text(canvasConfig.label, canvasConfig.x + canvasConfig.w/2, canvasConfig.y + canvasConfig.h/2);
  }
}

function drawPlacedTiles() {
  // Update cancellation status for all tiles
  updateCancellations();

  // Draw each placed tile
  placedTiles.forEach(tile => {
    if (!tile.isDragging) {
      let isHovered = isMouseOverTile(tile) && !draggedTile;
      drawTile(tile.x, tile.y, tile.config, tile.isCancelled, isHovered, tile.isCancelled ? 0.7 : 1);

      // Draw link indicator if cancelled
      if (tile.isCancelled && tile.linkedTo) {
        drawLinkLine(tile, tile.linkedTo);
      }
    }
  });
}

function drawTile(x, y, config, isCancelled, isHovered, opacity) {
  let w = config.width;
  let h = config.height;

  // Determine color
  let tileColor;
  if (isCancelled) {
    tileColor = cancelConfig.cancelledColor;
  } else {
    tileColor = config.color;
  }

  // Draw tile body
  fill(tileColor[0], tileColor[1], tileColor[2], opacity * 255);
  stroke(tileColor[0] - 30, tileColor[1] - 30, tileColor[2] - 30, opacity * 255);
  strokeWeight(3);
  rect(x, y, w, h, 8);

  // Hover effect
  if (isHovered && visualConfig.highlightOnHover) {
    fill(255, 255, 255, 100);
    noStroke();
    rect(x, y, w, h, 8);
    cursor(HAND);
  }

  // Label
  fill(255, 255, 255, opacity * 255);
  noStroke();
  textSize(config.width > 60 ? 24 : 20);
  textStyle(BOLD);
  textAlign(CENTER, CENTER);
  text(config.label, x + w/2, y + h/2);

  // Cancelled indicator
  if (isCancelled && cancelConfig.showCancelledLabel) {
    fill(0, 0, 0, opacity * 200);
    textSize(10);
    textStyle(NORMAL);
    text('cancelled', x + w/2, y + h + 12);
  }
}

function drawDraggedTile() {
  let x = mouseX + dragOffset.x;
  let y = mouseY + dragOffset.y;

  fill(draggedTile.config.color[0], draggedTile.config.color[1], draggedTile.config.color[2], 200);
  stroke(draggedTile.config.color[0] - 30, draggedTile.config.color[1] - 30, draggedTile.config.color[2] - 30);
  strokeWeight(3);
  rect(x, y, draggedTile.config.width, draggedTile.config.height, 8);

  fill(255, 255, 255);
  noStroke();
  textSize(draggedTile.config.width > 60 ? 24 : 20);
  textStyle(BOLD);
  textAlign(CENTER, CENTER);
  text(draggedTile.config.label, x + draggedTile.config.width/2, y + draggedTile.config.height/2);
}

function drawLinkLine(tile1, tile2) {
  stroke(100, 100, 100, 150);
  strokeWeight(2);
  setLineDash([5, 5]);

  let x1 = tile1.x + tile1.config.width/2;
  let y1 = tile1.y + tile1.config.height/2;
  let x2 = tile2.x + tile2.config.width/2;
  let y2 = tile2.y + tile2.config.height/2;

  line(x1, y1, x2, y2);

  setLineDash([]);
}

function setLineDash(list) {
  drawingContext.setLineDash(list);
}

function drawEquation() {
  // Count tiles by type
  let counts = {
    x: 0,
    negX: 0,
    one: 0,
    negOne: 0
  };

  placedTiles.forEach(tile => {
    if (!tile.isCancelled) {
      if (tile.config.value === 'x' && tile.config.sign === 'positive') counts.x++;
      if (tile.config.value === 'x' && tile.config.sign === 'negative') counts.negX++;
      if (tile.config.value === '1' && tile.config.sign === 'positive') counts.one++;
      if (tile.config.value === '1' && tile.config.sign === 'negative') counts.negOne++;
    }
  });

  // Build equation parts
  let parts = [];
  if (counts.x > 0) parts.push(counts.x === 1 ? 'x' : counts.x + 'x');
  if (counts.negX > 0) parts.push(counts.negX === 1 ? '-x' : '-' + counts.negX + 'x');
  if (counts.one > 0) parts.push(counts.one === 1 ? '1' : counts.one);
  if (counts.negOne > 0) parts.push(counts.negOne === 1 ? '-1' : '-' + counts.negOne);

  let equation = parts.length > 0 ? parts.join(' + ').replace('+ -', '- ') : '0';

  // Draw equation box
  fill(255, 255, 255);
  stroke(75, 50, 120);
  strokeWeight(2);
  rect(50, 560, 500, 30, 4);

  fill(75, 50, 120);
  noStroke();
  textSize(16);
  textStyle(NORMAL);
  textAlign(CENTER, CENTER);
  text('Simplified: ' + equation, 300, 575);
}

function drawInstructions() {
  fill(100, 100, 100);
  textSize(11);
  textStyle(NORMAL);
  textAlign(LEFT, TOP);
  text('• Drag tiles from the top palette onto the workspace', 50, 170);
  text('• Drag tiles close together to link opposite types (x and -x, or 1 and -1)', 50, 188);
  text('• Linked tiles turn grey to show they cancel each other', 50, 206);
}

// Update which tiles are cancelled based on proximity
function updateCancellations() {
  // Reset all cancellations
  placedTiles.forEach(tile => {
    tile.isCancelled = false;
    tile.linkedTo = null;
  });

  // Check each pair of tiles
  for (let i = 0; i < placedTiles.length; i++) {
    for (let j = i + 1; j < placedTiles.length; j++) {
      let tile1 = placedTiles[i];
      let tile2 = placedTiles[j];

      // Skip if either is already cancelled
      if (tile1.isCancelled || tile2.isCancelled) continue;

      // Check if they can cancel (same value, opposite signs)
      if (tile1.config.value === tile2.config.value &&
          tile1.config.sign !== tile2.config.sign) {

        // Check if they're close enough
        let distance = dist(
          tile1.x + tile1.config.width/2,
          tile1.y + tile1.config.height/2,
          tile2.x + tile2.config.width/2,
          tile2.y + tile2.config.height/2
        );

        if (distance < cancelConfig.snapDistance) {
          tile1.isCancelled = true;
          tile2.isCancelled = true;
          tile1.linkedTo = tile2;
          tile2.linkedTo = tile1;
        }
      }
    }
  }
}

// Mouse helper functions
function isMouseOverPalette(type) {
  let types = ['x', 'negX', 'one', 'negOne'];
  let index = types.indexOf(type);
  let x = paletteConfig.x + index * paletteConfig.spacing;
  let y = paletteConfig.y;
  let config = tileConfig[type];

  return mouseX > x && mouseX < x + config.width &&
         mouseY > y && mouseY < y + config.height;
}

function isMouseOverTile(tile) {
  return mouseX > tile.x && mouseX < tile.x + tile.config.width &&
         mouseY > tile.y && mouseY < tile.y + tile.config.height;
}

function isMouseInCanvasArea() {
  return mouseX > canvasConfig.x && mouseX < canvasConfig.x + canvasConfig.w &&
         mouseY > canvasConfig.y && mouseY < canvasConfig.y + canvasConfig.h;
}

// Mouse event handlers
function mousePressed() {
  // Check if clicking on a placed tile
  for (let i = placedTiles.length - 1; i >= 0; i--) {
    let tile = placedTiles[i];
    if (isMouseOverTile(tile)) {
      // Start dragging this tile
      draggedTile = tile;
      tile.isDragging = true;
      dragOffset.x = tile.x - mouseX;
      dragOffset.y = tile.y - mouseY;
      return;
    }
  }

  // Check if clicking on palette
  let types = ['x', 'negX', 'one', 'negOne'];
  for (let type of types) {
    if (isMouseOverPalette(type)) {
      // Create new tile from palette
      let config = tileConfig[type];
      draggedTile = {
        id: nextTileId++,
        config: config,
        x: mouseX,
        y: mouseY,
        isDragging: true,
        isCancelled: false,
        linkedTo: null,
        isNew: true
      };
      dragOffset.x = -config.width / 2;
      dragOffset.y = -config.height / 2;
      return;
    }
  }
}

function mouseDragged() {
  // Update cursor
  if (draggedTile) {
    cursor(HAND);
  }
}

function mouseReleased() {
  if (draggedTile) {
    // Update position
    draggedTile.x = mouseX + dragOffset.x;
    draggedTile.y = mouseY + dragOffset.y;
    draggedTile.isDragging = false;

    // Add to placed tiles if new and in canvas area
    if (draggedTile.isNew) {
      if (isMouseInCanvasArea()) {
        delete draggedTile.isNew;
        placedTiles.push(draggedTile);
      }
    } else {
      // Existing tile - remove if dragged outside canvas
      if (!isMouseInCanvasArea()) {
        let index = placedTiles.indexOf(draggedTile);
        if (index > -1) {
          placedTiles.splice(index, 1);
        }
      }
    }

    draggedTile = null;
  }

  cursor(ARROW);
}

function mouseMoved() {
  // Update hovered palette tile
  hoveredPaletteTile = null;
  let types = ['x', 'negX', 'one', 'negOne'];
  for (let type of types) {
    if (isMouseOverPalette(type)) {
      hoveredPaletteTile = type;
      break;
    }
  }

  // Reset cursor if not hovering anything interactive
  let isHoveringAnything = hoveredPaletteTile || placedTiles.some(isMouseOverTile);
  if (!isHoveringAnything && !draggedTile) {
    cursor(ARROW);
  }
}

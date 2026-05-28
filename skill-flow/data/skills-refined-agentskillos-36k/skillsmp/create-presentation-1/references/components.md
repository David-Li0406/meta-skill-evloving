# Terminal Heritage Components

## Table of Contents
1. [Slide Header](#slide-header)
2. [Slide Title](#slide-title)
3. [Workflow Chain](#workflow-chain)
4. [Node with Attributes](#node-with-attributes)
5. [Value Grid](#value-grid)
6. [Timeline](#timeline)
7. [Waveform Decoration](#waveform-decoration)
8. [Footer](#footer)
9. [Error/Failure Visualization](#errorfailure-visualization)
10. [Event Log](#event-log)

---

## Slide Header

Standard header with section label and branding.

```javascript
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
```

---

## Slide Title

Main title with optional subtitle.

```javascript
function addTitle(slide, title, subtitle = null) {
  slide.addText(title.toUpperCase(), {
    x: 0.4, y: 0.55, w: 9, h: 0.4,
    fontSize: 24, fontFace: "Courier New", bold: true, color: COLORS.navy
  });

  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.4, y: 0.95, w: 8, h: 0.25,
      fontSize: 10, fontFace: "Courier New", color: COLORS.muted
    });
  }
}
```

---

## Workflow Chain

Connected sequence of blocks showing a process flow.

```javascript
function addWorkflowChain(slide, nodes, startY = 2.0) {
  const blockW = 1.2;
  const blockH = 1.0;
  const gap = 0.55;

  nodes.forEach((node, i) => {
    const x = 0.5 + i * (blockW + gap);

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

    // Badge (optional)
    if (node.badge) {
      slide.addShape(pptx.shapes.RECTANGLE, {
        x: x + 0.1, y: startY + blockH + 0.1,
        w: blockW - 0.2, h: 0.28,
        fill: { color: node.badgeColor || COLORS.navy }
      });
      slide.addText(node.badge, {
        x: x + 0.1, y: startY + blockH + 0.1,
        w: blockW - 0.2, h: 0.28,
        fontSize: 8, fontFace: "Courier New",
        color: node.badgeColor === COLORS.green ? COLORS.navy : COLORS.surface,
        align: "center", valign: "middle"
      });
    }
  });
}

// Usage
addWorkflowChain(slide, [
  { label: "AI", color: COLORS.navy, badge: "AGENT", badgeColor: COLORS.navy },
  { label: "DATA", color: COLORS.navyLight, badge: "MCP" },
  { label: "HUMAN", color: COLORS.cream, outline: true, badge: "SIGNAL", badgeColor: COLORS.green },
  { label: "AI", color: COLORS.navy, badge: "AGENT" },
  { label: "DONE", color: COLORS.green }
]);
```

---

## Node with Attributes

Large block with attribute badges attached.

```javascript
function addNodeWithAttributes(slide, x, y, label, sublabel, attrs) {
  // Main block
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: x, y: y, w: 2.8, h: 2.8,
    fill: { color: COLORS.navy }
  });

  // Main label
  slide.addText(label, {
    x: x, y: y + 0.8, w: 2.8, h: 0.5,
    fontSize: 20, fontFace: "Courier New", bold: true,
    color: COLORS.surface, align: "center"
  });

  // Sublabel
  if (sublabel) {
    slide.addText(sublabel, {
      x: x + 0.1, y: y + 1.4, w: 2.6, h: 0.3,
      fontSize: 9, fontFace: "Courier New",
      color: COLORS.surface, align: "center", transparency: 30
    });
  }

  // Attributes around the block
  attrs.forEach((attr) => {
    let ax, ay;
    switch(attr.position) {
      case 'top': ax = x + 0.3; ay = y - 0.7; break;
      case 'left': ax = x - 1.3; ay = y + 1.0; break;
      case 'right': ax = x + 3.0; ay = y + 1.0; break;
      case 'bottom': ax = x + 0.3; ay = y + 2.95; break;
    }

    slide.addShape(pptx.shapes.RECTANGLE, {
      x: ax, y: ay, w: 2.2, h: 0.55,
      fill: { color: attr.color }
    });
    slide.addText(attr.label, {
      x: ax, y: ay, w: 2.2, h: 0.55,
      fontSize: 11, fontFace: "Courier New", bold: true,
      color: attr.color === COLORS.yellow ? COLORS.navy : COLORS.navy,
      align: "center", valign: "middle"
    });

    // Connector line
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: ax + 1.06, y: attr.position === 'top' ? ay + 0.55 : ay - 0.15,
      w: 0.08, h: 0.15,
      fill: { color: attr.color }
    });
  });
}

// Usage
addNodeWithAttributes(slide, 1.5, 1.3, "ACTIVITY", "fetch_data()", [
  { position: "top", label: "RETRY: 3x BACKOFF", color: COLORS.green },
  { position: "left", label: "TIMEOUT: 30s", color: COLORS.orange },
  { position: "right", label: "HEARTBEAT: 5s", color: COLORS.cream },
  { position: "bottom", label: "STATE PERSISTED", color: COLORS.navyLight }
]);
```

---

## Value Grid

Grid of value proposition blocks.

```javascript
function addValueGrid(slide, items, startY = 1.0) {
  items.forEach((item, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.4 + col * 4.7;
    const y = startY + row * 1.3;
    const w = col === 1 && items.length % 2 === 1 && i === items.length - 1 ? 9.2 : 4.5;

    // Block
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: x, y: y, w: w, h: 1.15,
      fill: { color: item.color || COLORS.navy }
    });

    // Title
    slide.addText(item.title, {
      x: x + 0.1, y: y + 0.1, w: w - 0.2, h: 0.4,
      fontSize: 18, fontFace: "Courier New", bold: true,
      color: item.textColor || COLORS.surface
    });

    // Description
    if (item.desc) {
      slide.addText(item.desc, {
        x: x + 0.1, y: y + 0.55, w: w - 0.2, h: 0.5,
        fontSize: 10, fontFace: "Courier New",
        color: item.textColor || COLORS.surface, transparency: 30
      });
    }
  });
}
```

---

## Timeline

Horizontal timeline with milestone markers.

```javascript
function addTimeline(slide, phases, y = 1.5) {
  const startX = 0.4;
  const totalWidth = 9.2;
  const phaseWidth = totalWidth / phases.length;

  // Base line
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: startX + phaseWidth/2, y: y + 0.6,
    w: totalWidth - phaseWidth, h: 0.04,
    fill: { color: COLORS.muted }
  });

  phases.forEach((phase, i) => {
    const x = startX + i * phaseWidth;

    // Phase label
    slide.addText(`PHASE ${String(i+1).padStart(2,'0')}`, {
      x: x, y: y - 0.4, w: phaseWidth, h: 0.2,
      fontSize: 9, fontFace: "Courier New", color: COLORS.muted, align: "center"
    });

    // Node
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: x + (phaseWidth - 1.4)/2, y: y,
      w: 1.4, h: 1.2,
      fill: { color: phase.color },
      line: phase.outline ? { color: COLORS.navy, width: 3 } : undefined
    });

    // Node label
    slide.addText(phase.label, {
      x: x + (phaseWidth - 1.4)/2, y: y + 0.2,
      w: 1.4, h: 0.8,
      fontSize: 10, fontFace: "Courier New", bold: true,
      color: phase.outline ? COLORS.navy :
        (phase.color === COLORS.green ? COLORS.navy : COLORS.surface),
      align: "center", valign: "middle"
    });
  });
}
```

---

## Waveform Decoration

Audio/signal visualization flourish.

```javascript
function addWaveform(slide, x, y, heights = [0.35, 0.65, 0.45, 0.25, 0.55]) {
  heights.forEach((h, i) => {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: x + i * 0.15,
      y: y + (0.65 - h) / 2,
      w: 0.08, h: h,
      fill: { color: COLORS.navy }
    });
  });
}
```

---

## Footer

Standard footer with attribution.

```javascript
function addFooter(slide, text, rightText = null) {
  slide.addText(text, {
    x: 0.4, y: 5.1, w: 7, h: 0.2,
    fontSize: 9, fontFace: "Courier New", color: COLORS.muted
  });

  if (rightText) {
    slide.addText(rightText, {
      x: 7.5, y: 5.1, w: 2.2, h: 0.2,
      fontSize: 9, fontFace: "Courier New", color: COLORS.muted, align: "right"
    });
  }
}
```

---

## Error/Failure Visualization

Broken workflow showing failure state.

```javascript
function addFailureVisualization(slide, x, y) {
  // Working node
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: x, y: y, w: 1.0, h: 1.0, fill: { color: COLORS.navy }
  });
  slide.addText("1", {
    x: x, y: y, w: 1.0, h: 1.0,
    fontSize: 32, fontFace: "Courier New", bold: true,
    color: COLORS.surface, align: "center", valign: "middle"
  });

  // Connector (partial)
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: x + 1.05, y: y + 0.47, w: 0.5, h: 0.06,
    fill: { color: COLORS.navy }
  });

  // Failure X
  slide.addText("X", {
    x: x + 1.5, y: y + 0.15, w: 0.5, h: 0.7,
    fontSize: 36, fontFace: "Courier New", bold: true,
    color: COLORS.red, align: "center", valign: "middle"
  });

  // Faded connector
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: x + 1.95, y: y + 0.47, w: 0.5, h: 0.06,
    fill: { color: COLORS.navy }, transparency: 60
  });

  // Lost node
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: x + 2.5, y: y, w: 1.0, h: 1.0,
    fill: { color: COLORS.navy }, transparency: 50,
    line: { color: COLORS.navy, width: 2, dashType: "dash" }
  });
  slide.addText("?", {
    x: x + 2.5, y: y, w: 1.0, h: 1.0,
    fontSize: 32, fontFace: "Courier New", bold: true,
    color: COLORS.surface, align: "center", valign: "middle", transparency: 50
  });

  // Error badge
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: x + 1.3, y: y - 0.5, w: 1.5, h: 0.35,
    fill: { color: COLORS.red }
  });
  slide.addText("FAILURE", {
    x: x + 1.3, y: y - 0.5, w: 1.5, h: 0.35,
    fontSize: 12, fontFace: "Courier New", bold: true,
    color: "FFFFFF", align: "center", valign: "middle"
  });
}
```

---

## Event Log

Vertical log showing workflow events.

```javascript
function addEventLog(slide, x, y, events) {
  // Container
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: x, y: y, w: 2.3, h: events.length * 0.45 + 0.5,
    fill: { color: COLORS.navy }
  });

  // Header
  slide.addText("EVENT LOG", {
    x: x + 0.1, y: y + 0.1, w: 2.1, h: 0.25,
    fontSize: 9, fontFace: "Courier New", color: COLORS.surface, transparency: 40
  });

  // Events
  events.forEach((event, i) => {
    const color = event.type === 'error' ? COLORS.red :
                  event.type === 'success' ? COLORS.green : COLORS.surface;

    slide.addShape(pptx.shapes.RECTANGLE, {
      x: x + 0.1, y: y + 0.45 + i * 0.45, w: 0.08, h: 0.3,
      fill: { color: color }
    });
    slide.addText(event.name, {
      x: x + 0.25, y: y + 0.45 + i * 0.45, w: 1.95, h: 0.3,
      fontSize: 9, fontFace: "Courier New", color: COLORS.surface,
      transparency: event.type === 'success' ? 0 : 30
    });
  });
}

// Usage
addEventLog(slide, 7.3, 1.0, [
  { name: "WorkflowStarted", type: "normal" },
  { name: "ActivityScheduled", type: "normal" },
  { name: "ActivityStarted", type: "normal" },
  { name: "ActivityFailed", type: "error" },
  { name: "ActivityRetried", type: "normal" },
  { name: "ActivityCompleted", type: "success" }
]);
```

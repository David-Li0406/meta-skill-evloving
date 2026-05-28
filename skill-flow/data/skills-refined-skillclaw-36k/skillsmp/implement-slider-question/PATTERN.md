# Interactive Controls + Explanation Pattern

Students manipulate values using buttons, sliders, or counters and explain their observations or strategy.

## When to Use

- "Adjust recipe batches with +/- buttons and explain your strategy"
- "Use sliders to change the drink mix ratio"
- "Create batches and describe the pattern"
- Any "manipulate and explain" interaction

## Components Needed

```html
<script src="/podsie-curriculum/components/standard-card.standalone.js"></script>
<script src="/podsie-curriculum/components/explanation-card.standalone.js"></script>
<!-- Custom D3 for controls and visualization -->
```

## Key Implementation Decisions

1. **Control type** - Buttons (+/-), sliders, or custom controls?
2. **Single value or collection** - One count vs array of items?
3. **Visual feedback** - SVG diagram showing current state?
4. **Constraints** - Min/max values, limits on items

## State Shapes

**Single value:**
```javascript
function createDefaultState() {
  return {
    count: 0,
    explanation: "",
  };
}
```

**Collection (batches/items):**
```javascript
function createDefaultState() {
  return {
    batches: [],  // Array of objects
    explanation: "",
  };
}
```

## Core Patterns

**+/- Buttons (single value):**
```javascript
button.on("click", () => {
  if (!interactivityLocked && chartState.count < MAX) {
    chartState.count++;
    renderAll(currentD3);
    sendChartState();
  }
});
```

**Add/Remove Items (collection):**
```javascript
addButton.on("click", () => {
  if (!interactivityLocked && chartState.batches.length < MAX) {
    chartState.batches.push({ value1: 0, value2: 0 });
    renderAll(currentD3);
    sendChartState();
  }
});
```

**Slider:**
```javascript
slider
  .attr("type", "range")
  .attr("min", 0)
  .attr("max", 10)
  .on("input", function() {
    if (!interactivityLocked) {
      chartState.value = +this.value;
      renderAll(currentD3);
      sendChartState();
    }
  });
```

## Complete Examples

- **[interactive-batches.js](../examples/interactive-batches.js)** - Recipe batches with +/- buttons
  - Real question: [/courses/IM-6th-Grade/modules/Unit-2/assignments/Lesson-3-Recipes/questions/05/](/courses/IM-6th-Grade/modules/Unit-2/assignments/Lesson-3-Recipes/questions/05/attachments/chart.js)
  - Shows: Add/remove batches, +/- controls per batch, totals display

## Common Variations

**Simple counter (one value)**:
- Single +/- buttons
- Display current count
- Min/max constraints

**Batch/item collection**:
- Add button creates new item
- Each item has its own +/- controls
- Remove button per item
- Summary/totals display

**Slider-based**:
- HTML range input
- Real-time value display
- Visual diagram updates with slider

**With visualization**:
- SVG diagram reflects current state
- Update diagram in `renderAll()`

## Implementation Checklist

- [ ] Defined constants (min, max, limits)
- [ ] Created state structure (single value or array)
- [ ] Implemented controls with interactivity check
- [ ] Added `renderAll()` call after state changes
- [ ] Added constraints (min/max, item limits)
- [ ] Added visual feedback (if needed)
- [ ] Added explanation card
- [ ] Tested locking behavior

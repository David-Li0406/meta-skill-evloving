# Selection + Explanation Pattern

Students select an option (radio buttons, clickable cards) and explain their reasoning.

## When to Use

- "Select the equation that matches the relationship and explain why"
- "Choose the correct graph and justify your answer"
- "Pick the scenario that fits and describe your reasoning"
- Any "choose and explain" interaction

## Components Needed

```html
<script src="/podsie-curriculum/components/standard-card.standalone.js"></script>
<script src="/podsie-curriculum/components/explanation-card.standalone.js"></script>
```

## Key Implementation Decisions

1. **Selection UI** - Clickable cards, radio buttons, or buttons?
2. **Visual feedback** - Highlight selected option?
3. **Context display** - Show table/graph alongside options?
4. **Layout** - Two-column (context | options) or stacked?

## State Shape

```javascript
function createDefaultState() {
  return {
    selectedOption: null,  // Stores selected ID
    explanation: "",
  };
}
```

## Core Pattern (Clickable Cards)

```javascript
OPTIONS.forEach((option) => {
  const card = container
    .append("div")
    .style("background", chartState.selectedOption === option.id ? "#eff6ff" : "#ffffff")
    .style("border", `2px solid ${chartState.selectedOption === option.id ? "#3b82f6" : "#e5e7eb"}`)
    .style("border-radius", "12px")
    .style("padding", "16px")
    .style("cursor", interactivityLocked ? "default" : "pointer")
    .on("click", () => {
      if (!interactivityLocked) {
        chartState.selectedOption = option.id;
        renderAll(currentD3);
        sendChartState();
      }
    });

  card.append("div").text(option.display);
});
```

## Complete Examples

- **[selection-equation.js](../examples/selection-equation.js)** - Select equation from options
  - Real question: [/courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/04/](/courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/04/attachments/chart.js)
  - Shows: Two-column layout, table + equation options, visual selection feedback

## Common Variations

**Radio buttons (native HTML)**:
```javascript
label
  .append("input")
  .attr("type", "radio")
  .attr("name", "option")
  .property("checked", chartState.selectedOption === option.id)
  .on("change", () => { /* update state */ });
```

**Image/graph options**:
- Render SVG or image in card
- Click card to select

**Multiple selections** (checkboxes):
```javascript
state: {
  selectedOptions: [],  // Array of IDs
}
```

## Layout Options

**Two-column** (context | options):
```javascript
const { leftColumn, rightColumn } = createTwoColumnLayout(d3, content);
// Left: table/graph/diagram
// Right: selection options
```

**Stacked**:
- Context card at top
- Options below

## Implementation Checklist

- [ ] Defined OPTIONS array
- [ ] Created state with selectedOption field
- [ ] Implemented selection UI with visual feedback
- [ ] Added click handler with interactivity check
- [ ] Added explanation card
- [ ] Tested state restoration

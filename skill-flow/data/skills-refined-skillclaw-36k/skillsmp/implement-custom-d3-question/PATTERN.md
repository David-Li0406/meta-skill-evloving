# Custom D3 Visualization Pattern

For unique **D3 interactive questions** not covered by standard patterns. Build from scratch using D3 and helper utilities.

> ⚠️ **For animated visual explanations (p5.js), use the [create-p5-animation](../../create-p5-animation/SKILL.md) skill instead.**

## When to Use (D3 Custom Questions)

✅ **Use this pattern for:**
- Unique D3 interactions requiring student responses
- Custom diagrams where students manipulate elements
- Novel question types not fitting standard patterns (drag-match, table, etc.)
- Interactive visualizations that get graded

❌ **Do NOT use for:**
- Animated visual explanations → Use `create-p5-animation` skill
- Standard patterns → Use drag-and-drop, table-completion, etc.

---

## Approach

1. **Use standard components for structure** (`createStandardCard`, `createTwoColumnLayout`)
2. **Build custom D3 for unique interactions**
3. **Follow core architecture** (state, messages, locking)

## Key Implementation Decisions

1. **What's unique?** - Identify what makes this different from standard patterns
2. **State structure** - Map interactions to state fields
3. **Rendering approach** - SVG, HTML, or hybrid?
4. **Reusable pieces** - Can you use any standard components?

## State Shape

```javascript
function createDefaultState() {
  return {
    // Design based on what needs to be graded
    customValue1: 0,
    points: [],  // Arrays for collections
    selections: {},
    explanation: "",
  };
}
```

## Implementation Strategy

### 1. Break Down the Interaction

- What can students manipulate?
- What visual feedback do they need?
- What gets graded?

### 2. Reuse What You Can

```javascript
// Use standard components for structure
const { leftColumn, rightColumn } = createTwoColumnLayout(d3, content);

const card = createStandardCard(d3, leftColumn, { size: "large" });

createExplanationCard(d3, content, { /*...*/ });
```

### 3. Build Custom Elements

See [common-snippets.md](common-snippets.md) for:
- SVG setup and shapes
- Custom inputs
- Interactive elements

### 4. Follow Core Patterns

- Always check `interactivityLocked` in handlers
- Call `sendChartState()` after state changes
- Implement `applyInitialState()` and `setInteractivity()`
- Use `renderAll()` pattern

## Example Patterns

**Clickable points on diagram**:
```javascript
svg.append("circle")
  .attr("cx", point.x)
  .attr("cy", point.y)
  .style("cursor", interactivityLocked ? "default" : "pointer")
  .on("click", () => {
    if (!interactivityLocked) {
      toggleSelection(point.id);
      renderAll(currentD3);
      sendChartState();
    }
  });
```

**Custom drag behavior**:
```javascript
const drag = d3.drag()
  .on("drag", function(event) {
    if (interactivityLocked) return;
    // Update position
  })
  .on("end", () => sendChartState());

element.call(drag);
```

## Tips

- Start with a similar pattern and modify
- Use `createStandardCard` for structure
- Test frequently with chart.html
- Keep state minimal and serializable
- Document complex logic in code comments

## Complete Examples

For custom implementations, refer to:
- Real questions in `/courses/` that don't fit standard patterns
- [common-snippets.md](common-snippets.md) for building blocks

## Implementation Checklist

- [ ] Identified what makes this unique
- [ ] Reused standard components where possible
- [ ] Designed state structure around graded elements
- [ ] Implemented custom D3/HTML elements
- [ ] Added interactivity checks
- [ ] Implemented core functions (state, messages, locking)
- [ ] Tested thoroughly

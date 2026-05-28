# Table Completion Pattern

Students fill in missing values in a table based on a rate, pattern, or proportional relationship.

## When to Use

- "Complete the table showing costs for different months"
- "Fill in the missing values for this proportional relationship"
- "Complete the rate table"
- Any table with editable cells

## Components Needed

```html
<script src="/podsie-curriculum/components/table.standalone.js"></script>
<!-- OR build custom D3 table -->
<script src="/podsie-curriculum/components/standard-card.standalone.js"></script>
<script src="/podsie-curriculum/components/explanation-card.standalone.js"></script>
```

## Key Implementation Decisions

1. **Use component vs custom** - `createDataTable()` for standard tables, custom D3 for special styling
2. **Which cells are editable** - Mark with `null` (component) or conditional rendering (custom)
3. **State structure** - One field per editable cell
4. **Input validation** - Numeric only? Constraints?

## State Shape

```javascript
function createDefaultState() {
  return {
    cell1: "",  // One field per editable cell
    cell2: "",
    cell3: "",
    explanation: "",
  };
}
```

## Core Pattern (Using Component)

```javascript
const tableAPI = createDataTable(d3, tableCard, {
  headers: ["Months", 0, 1, 2, 3],
  rows: [
    {
      label: "Cost ($)",
      values: [0, null, null, null]  // null = editable
    }
  ],
  onInput: (rowIndex, colIndex, value) => {
    // Map column to state field
    if (colIndex === 0) chartState.cell1 = value;
    if (colIndex === 1) chartState.cell2 = value;
    sendChartState();
  },
  readOnly: interactivityLocked
});
```

## Core Pattern (Custom D3)

See [common-snippets.md](common-snippets.md#tables) for custom table rendering with conditional inputs.

## Complete Examples

- **[table-completion-component.js](../examples/table-completion-component.js)** - Using table component
  - Real question: [/courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/05/](/courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/05/attachments/chart.js)
  - Shows: Table component, 4 editable cells, two-column layout

## Common Variations

**Multiple rows editable**:
```javascript
rows: [
  { label: "Distance", values: [0, null, null] },
  { label: "Time", values: [0, null, null] },
]
```

**Mixed given/editable cells**:
```javascript
values: [0, null, null, 100, null]  // Some given, some editable
```

**Custom styling** - Use custom D3 table for:
- Colored cells
- Custom borders
- Special formatting

## When to Use Component vs Custom

**Use `createDataTable()` when:**
- Standard table layout
- Simple text/number inputs
- Want less code

**Use custom D3 when:**
- Need custom styling (colors, borders)
- Complex cell interactions
- Non-standard layout

## Implementation Checklist

- [ ] Defined table headers
- [ ] Defined row data with editable cells marked
- [ ] Created state with one field per editable cell
- [ ] Implemented onInput callback (component) or input handlers (custom)
- [ ] Mapped inputs to state fields correctly
- [ ] Added explanation card
- [ ] Tested state restoration in applyInitialState

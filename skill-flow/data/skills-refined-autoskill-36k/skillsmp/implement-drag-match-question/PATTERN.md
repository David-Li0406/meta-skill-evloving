# Drag-and-Drop Pattern

Students drag items (tables, graphs, equations) to match them with categories or labels.

## When to Use

- "Match each table to the equation it represents"
- "Drag graphs to the descriptions that match"
- "Match scenarios to proportional relationships"
- Any "match X with Y" interaction

## Components Needed

```html
<script src="/podsie-curriculum/components/drag-match.standalone.js"></script>
<script src="/podsie-curriculum/components/standard-card.standalone.js"></script>
<script src="/podsie-curriculum/components/explanation-card.standalone.js"></script>
```

## Key Implementation Decisions

1. **Define items** - What can be dragged? (tables, graphs, equations, text)
2. **Define categories** - Where can items be dropped? (2+ categories)
3. **Render function** - How to display each item (table, graph, simple text)
4. **State structure** - One array per category storing matched item IDs

## Data Structure

```javascript
const ITEMS = [
  { id: "item1", /* data */ },
  { id: "item2", /* data */ },
];

const CATEGORIES = [
  { id: "cat1", text: "Category 1 description" },
  { id: "cat2", text: "Category 2 description" },
];
```

## State Shape

```javascript
function createDefaultState() {
  return {
    cat1Matches: [],  // Array of matched item IDs
    cat2Matches: [],
    explanation: "",
  };
}
```

## Core Pattern

```javascript
dragMatcher = createDragMatcher(d3, content, {
  items: ITEMS.map(item => ({
    id: item.id,
    content: (container) => renderItem(container, item),  // Custom render
  })),
  categories: CATEGORIES.map(cat => ({
    id: cat.id,
    label: cat.text,
  })),
  state: {
    cat1: chartState.cat1Matches,
    cat2: chartState.cat2Matches,
  },
  onStateChange: (newState) => {
    chartState.cat1Matches = newState.cat1 || [];
    chartState.cat2Matches = newState.cat2 || [];
    sendChartState();
  },
  locked: interactivityLocked,
});
```

## Complete Examples

- **[drag-match-tables.js](../examples/drag-match-tables.js)** - Match tables to movie download plans
  - Real question: [/courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/03/](/courses/IM-8th-Grade/modules/Unit-3/assignments/Ramp-Up-01/questions/03/attachments/chart.js)
  - Shows: Table rendering, 4 items, 2 categories, explanation section

## Common Variations

**Simple text items** (not tables):
```javascript
items: ITEMS.map(item => ({
  id: item.id,
  content: item.text,  // String instead of function
}))
```

**3+ categories**:
```javascript
state: { cat1: [], cat2: [], cat3: [] }
```

**Custom rendering** (graphs, images):
```javascript
content: (container) => renderGraph(container, graphData)
```

## Implementation Checklist

- [ ] Defined ITEMS with unique IDs
- [ ] Defined CATEGORIES
- [ ] Created render function for items (if complex)
- [ ] Created state with one array per category
- [ ] Implemented createDragMatcher with onStateChange
- [ ] Added explanation card
- [ ] Implemented setInteractivity to lock matcher

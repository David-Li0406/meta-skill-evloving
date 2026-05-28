---
name: excel-pivot-wizard
description: Use this skill when you need to generate pivot tables and visualizations from raw data using natural language commands, such as analyzing sales by region or summarizing data by category.
---

# Excel Pivot Wizard

Creates pivot tables and visualizations from raw data using natural language commands.

## When to Invoke This Skill

Automatically load this Skill when the user asks to:
- "Create a pivot table"
- "Analyze [data] by [dimension]"
- "Summarize sales by region"
- "Show revenue breakdown"
- "Group data by category"
- "Cross-tab analysis"
- "Compare [X] across [Y]"

## Capabilities

### Pivot Table Generation
- **Rows**: Group data by one or more fields
- **Columns**: Cross-tabulate across another dimension
- **Values**: Aggregate functions (sum, average, count, min, max)
- **Filters**: Slice data by specific criteria
- **Calculated Fields**: Create custom formulas

### Visualization
- Column/bar charts for comparisons
- Line charts for trends over time
- Pie charts for composition
- Combo charts for multiple metrics
- Conditional formatting for heatmaps

## Common Analysis Patterns

### Pattern 1: Single Dimension Summary
**Request:** "Show total sales by region"

**Output:**
```
| Region    | Total Sales |
|-----------|-------------|
| Northeast | $1,250,000  |
| Southeast | $980,000    |
| Midwest   | $1,100,000  |
| West      | $1,450,000  |
| Total     | $4,780,000  |
```

### Pattern 2: Cross-Tabulation
**Request:** "Sales by region and product category"

**Output:**
```
| Region    | Electronics | Clothing | Home Goods | Total     |
|-----------|-------------|----------|------------|-----------|
| Northeast | $400K       | $500K    | $350K      | $1,250K   |
| Southeast | $300K       | $380K    | $300K      | $980K     |
| Midwest   | $450K       | $350K    | $300K      | $1,100K   |
| West      | $550K       | $500K    | $400K      | $1,450K   |
| Total     | $1,700K     | $1,730K  | $1,350K    | $4,780K   |
```

### Pattern 3: Time-Based Trending
**Request:** "Monthly revenue trend for 2024"

**Output:**
```
Line chart showing:
- X-axis: Jan, Feb, Mar, ..., Dec
- Y-axis: Revenue
- Line: Monthly revenue with data labels
```

### Pattern 4: Top N Analysis
**Request:** "Top 10 products by revenue"

**Output:**
```
| Rank | Product       | Revenue   | % of Total |
|------|---------------|-----------|------------|
| 1    | Product A     | $450,000  | 9.4%       |
| 2    | Product B     | ...
```
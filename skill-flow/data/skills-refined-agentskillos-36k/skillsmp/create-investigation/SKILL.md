---
name: create-investigation
description: Create a new Ethereum data investigation page in the notebooks repo. Use when the user wants to add a new investigation, analysis, or research page that queries Xatu/ClickHouse data and visualizes findings with charts.
---

# Create Investigation

Investigations are one-off analyses of something in Ethereum. 

## Golden Rules:
- They must use a fixed time range for the data so that the analysis is reproducible.
- Agents must actually check the data - do not make up conclusions. It's better to not write a conclusion than to write a conclusion that is not supported by the data.
- Ask the user for clarifying questions. Be thorough.

## Requirements to Gather

1. **Title**: Investigation title (e.g., "Head Vote Accuracy by Entity Type")
2. **Slug**: URL-safe identifier (e.g., "head-accuracy-by-entity")
3. **Description**: Brief description for SEO and sidebar hover
4. **Author**: Username from supported list (samcm, parithosh, pk910, savid, skylenet, mattevans, qu0b, barnabasbusa, ethpandaops)
5. **Tags**: Relevant tags for categorization
6. **Network**: mainnet, sepolia, hoodi, etc.
7. **Time Range**: Fixed start and end dates (investigations MUST use fixed time ranges for reproducibility)
8. **Research Question**: The specific question being investigated

## File Structure

Create the investigation at `pages/YYYY-MM/{slug}/index.md` where YYYY-MM is the current year-month.

If the year-month folder doesn't exist, create `pages/YYYY-MM/index.md`:
```markdown
---
title: YYYY Mon
sidebar_position: 1
---

Investigations from Month Year.
```

## Page Template

```markdown
---
title: {Title}
sidebar_position: {N}
description: {Brief description}
date: {YYYY-MM-DD}
author: {username}
tags:
  - tag1
  - tag2
---

<script>
    import PageMeta from '$lib/PageMeta.svelte';
    import Section from '$lib/Section.svelte';
    import SqlSource from '$lib/SqlSource.svelte';
</script>

<PageMeta
    date="{YYYY-MM-DD}"
    author="{username}"
    tags={["tag1", "tag2"]}
    description="{Brief description}"
    networks={["Ethereum Mainnet"]}
    startTime="{YYYY-MM-DD}T00:00:00Z"
    endTime="{YYYY-MM-DD}T23:59:59Z"
/>

```sql query_name
SELECT ... FROM xatu_cbt.table_name
```

<Section type="question">

## Question

{The specific research question being investigated}

</Section>

<Section type="background">

## Background

{Context and explanation of concepts. Use **bold** for key terms being defined.}

</Section>

<Section type="investigation">

## Investigation

### When {Action}

{Explanation of what this analysis shows}

<SqlSource source="$source" query="query_name" />

<LineChart
    data={query_name}
    x="x_column"
    y={["Series 1", "Series 2", "Series 3"]}
    sort=false
    title="Chart Title"
    yFmt="num2"
    chartAreaHeight=400
    yMax=100
    colorPalette={['#2563eb', '#ea580c', '#16a34a']}
    echartsOptions={{
        title: {left: 'center'},
        grid: {bottom: 50, left: 70, top: 60, right: 120},
        xAxis: {type: 'category', name: 'X Axis Label', nameLocation: 'center', nameGap: 35},
        yAxis: {min: 0, max: 100},
        legend: {show: true, right: 10, orient: 'vertical', top: 'center'},
        series: [
            {name: 'Series 1', lineStyle: {width: 3}},
            {name: 'Series 2', lineStyle: {width: 2}},
            {name: 'Series 3', lineStyle: {width: 2}}
        ],
        graphic: [{
            type: 'text',
            left: 15,
            top: 'center',
            rotation: Math.PI / 2,
            style: {
                text: 'Y Axis Label',
                fontSize: 12,
                fill: '#666'
            }
        }]
    }}
/>

</Section>

<Section type="takeaways">

## Takeaways

- Key finding 1
- Key finding 2
- Key finding 3

</Section>
```

## Critical Rules

1. **SQL queries MUST be at top level** - Not wrapped in HTML elements or Sections. Evidence's preprocessor won't process them otherwise.

2. **Fixed time range required** - PageMeta MUST have `startTime` and `endTime` props for reproducibility.

3. **Escape `<` and `>` in prose** - Use inline code backticks: `` `z < 0` `` not `z < 0`.

4. **Charts require three labels**:
   - `title` prop (centered via `title: {left: 'center'}`)
   - X-axis label via `xAxis: {name: '...', nameLocation: 'center', nameGap: 35}`
   - Y-axis label via `graphic` element (NOT `yAxis.name` which doesn't center properly)

5. **Action-based section headers** - Use "When Attesting" not "Attester Analysis".

6. **No "Analysis" suffix in titles** - "Analysis" is implied; use "RPC Snooper Overhead" not "RPC Snooper Overhead Analysis".

7. **Don't repeat header** - The title from frontmatter is already rendered by the layout.

8. **Sort time series data ascending** - SQL queries for charts MUST include `ORDER BY date_column ASC` to ensure data is sorted chronologically. Charts will display incorrectly if data is not sorted.

9. **Use high-contrast colors** - Multi-line charts MUST use `colorPalette` with high-contrast colors. Recommended palette:
   - Red: `#dc2626`
   - Blue: `#2563eb`
   - Purple: `#9333ea`
   - Green: `#16a34a`
   - Orange: `#ea580c`
   Example: `colorPalette={['#2563eb', '#ea580c', '#16a34a']}`

10. **Line styling for emphasis** - Make the primary metric line thicker (width: 3), use dashed lines for secondary metrics like averages/means:
    ```javascript
    series: [
        {name: 'Primary', lineStyle: {width: 3}},
        {name: 'Secondary', lineStyle: {width: 2, type: 'dashed'}}
    ]
    ```

11. **Reference lines with markLine** - For horizontal reference lines (e.g., "random chance"), use `markLine` NOT a separate series (which corrupts the x-axis). Position label inside the chart:
    ```javascript
    series: [{
        markLine: {
            silent: true,
            symbol: 'none',
            label: {show: true, position: 'insideEndTop', formatter: 'Label text'},
            lineStyle: {type: 'dashed', color: '#888'},
            data: [{yAxis: 0.56}]
        }
    }]
    ```

12. **Human-readable SQL column names** - Use column aliases that will appear nicely in chart legends:
    ```sql
    SELECT
        hour,
        round(avg(our_time)) as "Our Node",
        round(avg(median_time)) as "Network Median"
    ```

13. **Don't describe chart features that don't exist** - Never claim "tight IQR band", "green for negative values", or specific colors in prose unless the chart actually shows them. Verify visually before writing conclusions.

14. **Per-block comparisons for timing analysis** - When comparing timing between nodes, calculate metrics per-block first, then aggregate. Don't compare raw averages across all data which can be misleading.


## SQL Source Files

For reusable queries, create `sources/xatu_cbt/{query_name}.sql`:
```sql
SELECT
    date_column,
    column1,
    column2
FROM xatu_cbt.table_name
WHERE slot_start_date_time >= '2025-12-21'
  AND slot_start_date_time < '2026-01-21'
ORDER BY date_column ASC
```

Then reference in the page:
```sql query_name
SELECT * FROM xatu_cbt.{query_name}
```

## Available Chart Types

LineChart, BarChart, AreaChart, ScatterPlot, DataTable, BigValue, Value

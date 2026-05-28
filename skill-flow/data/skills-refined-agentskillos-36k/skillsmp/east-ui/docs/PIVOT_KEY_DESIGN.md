# Pivot Key Design for Cartesian Charts

## Overview

This document describes the addition of `pivotKey` support to cartesian charts (Line, Area, Bar, Scatter, Composed), enabling data-driven dynamic series where series names are derived from data values at runtime rather than being fixed at compile time.

## Problem Statement

Currently, cartesian charts support two data formats:

1. **Single array form** (`Chart.Line`): Series are struct field names known at compile time
   ```typescript
   Chart.Line(
       [{ month: "Jan", revenue: 100n, profit: 50n }],
       ["revenue", "profit"],  // series must be known struct fields
   )
   ```

2. **Multi-series form** (`Chart.LineMulti`): Series are record keys known at compile time
   ```typescript
   Chart.LineMulti({
       revenue: [{ month: "Jan", value: 100n }],
       profit: [{ month: "Jan", value: 50n }],
   }, { valueKey: "value" })
   ```

Neither supports **data-driven dynamic series** where:
- Series names come from data values (e.g., a "category" column)
- Number of series is unknown until runtime
- Data is in "long" or "pivoted" format (common in SQL query results)

## Solution

Add an optional `pivotKey` field to cartesian chart types. When set, the renderer:
1. Groups data rows by unique values of the `pivotKey` field
2. Each unique value becomes a series name
3. Uses `valueKey` for y-values (already exists)
4. Uses `xAxis.dataKey` for x-values (already exists)
5. Auto-assigns colors from a categorical palette
6. Applies any explicit series style overrides by name match

## Data Format (Long/Pivoted)

When `pivotKey` is set, data should be in "long" format where each row contains:
- X-axis value (e.g., `month`)
- Series identifier (e.g., `category`)
- Y-axis value (e.g., `amount`)

```typescript
// Long format - series names are data values, not schema fields
const data = [
    { month: "Jan", category: "revenue", amount: 100n },
    { month: "Jan", category: "profit", amount: 50n },
    { month: "Feb", category: "revenue", amount: 200n },
    { month: "Feb", category: "profit", amount: 80n },
    { month: "Feb", category: "expenses", amount: 30n },  // new series appears dynamically
];
```

## Type Changes

### Shared Chart Types (`src/charts/types.ts`)

No changes to shared types. `pivotKey` and `pivotColors` are chart-specific.

### Line Chart Types (`src/charts/line/types.ts`)

Add `pivotKey` field to `LineChartType`:

```typescript
export const LineChartType = StructType({
    data: ArrayType(DictType(StringType, LiteralValueType)),
    dataSeries: OptionType(MultiSeriesDataType),
    valueKey: OptionType(StringType),
    pivotKey: OptionType(StringType),  // NEW
    series: ArrayType(LineChartSeriesType),
    // ... existing fields unchanged
});
```

Add `pivotColors` to `LineChartSeriesType`:

```typescript
export const LineChartSeriesType = StructType({
    name: StringType,
    color: OptionType(StringType),
    // ... existing fields
    pivotColors: OptionType(DictType(StringType, StringType)),  // NEW
});
```

Add `pivotColors` to `LineChartSeriesConfig`:

```typescript
export interface LineChartSeriesConfig {
    /** Chakra color token (e.g., "teal.solid", "blue.500") */
    color?: SubtypeExprOrValue<StringType>;
    /** Display label (defaults to name) */
    label?: SubtypeExprOrValue<StringType>;
    // ... existing fields
    /** Optional mapping of pivot key values to colors (used with pivotKey) */
    pivotColors?: SubtypeExprOrValue<DictType<StringType, StringType>>;
}
```

Add `pivotKey` to style interface with type-safe constraint (same pattern as `xAxis.dataKey`):

```typescript
/**
 * Style for Line charts (single array form).
 *
 * @typeParam DataKey - Union of field keys from the data struct
 */
export interface LineChartStyle<DataKey extends string = string> extends LineChartStyleBase<DataKey> {
    /**
     * Field name containing series identifiers (enables pivot/long format data).
     * Type-safe: must be a field name from the data struct.
     */
    pivotKey?: DataKey;
    // ... existing fields unchanged
}
```

This provides compile-time validation that `pivotKey` is an actual field in the data:

```typescript
// Type-safe: "region" must be a field in the data struct
Chart.Line(
    [{ month: "Jan", region: "North", sales: 100n }],
    [],
    {
        xAxis: { dataKey: "month" },  // ✓ type-safe
        pivotKey: "region",           // ✓ type-safe
        valueKey: "sales",            // ✓ type-safe
    }
);

// Compile error: "invalid" is not a field name
Chart.Line(
    [{ month: "Jan", region: "North", sales: 100n }],
    [],
    {
        pivotKey: "invalid",  // ✗ TypeScript error
    }
);
```

### Area Chart Types (`src/charts/area/types.ts`)

Same pattern - add `pivotKey: OptionType(StringType)` to `AreaChartType`.

### Bar Chart Types (`src/charts/bar/types.ts`)

Same pattern - add `pivotKey: OptionType(StringType)` to `BarChartType`.

### Scatter Chart Types (`src/charts/scatter/types.ts`)

Same pattern - add `pivotKey: OptionType(StringType)` to `ScatterChartType`.

### Composed Chart Types (`src/charts/composed/types.ts`)

Same pattern - add `pivotKey: OptionType(StringType)` to `ComposedChartType`.

## Relationship with *Multi Variants

### Current State

Each chart type has two forms:
- **Single array** (`Chart.Line`): `Array<Struct>`, series from field names
- **Multi-series** (`Chart.LineMulti`): `Record<K, Array<Struct>>`, series from record keys

`*Multi` exists primarily for **sparse data** - when different series have data at different x-axis points.

### With pivotKey

`pivotKey` on the single array form can handle sparse data:

```typescript
// Sparse data in long format - works with Chart.Line + pivotKey
const data = [
    { month: "Jan", region: "North", sales: 100n },
    { month: "Jan", region: "South", sales: 80n },
    { month: "Feb", region: "North", sales: 120n },
    // South has no Feb data - sparse!
    { month: "Feb", region: "West", sales: 50n },   // new region
];

Chart.Line(data, [], {
    xAxis: { dataKey: "month" },
    pivotKey: "region",
    valueKey: "sales",
});
```

This achieves what `LineMulti` does, but with simpler data structure.

### pivotKey on *Multi Variants

`pivotKey` can also apply to `*Multi` variants for **nested grouping**:

```typescript
// Each record key is a "group", pivotKey creates series within each group
const data = {
    Q1: [
        { month: "Jan", category: "revenue", amount: 100n },
        { month: "Jan", category: "profit", amount: 50n },
        { month: "Feb", category: "revenue", amount: 120n },
    ],
    Q2: [
        { month: "Apr", category: "revenue", amount: 150n },
        { month: "Apr", category: "profit", amount: 70n },
    ],
};

Chart.LineMulti(data, {
    xAxis: { dataKey: "month" },
    valueKey: "amount",
    pivotKey: "category",  // creates sub-series within each quarter
});
```

This is an advanced use case. The renderer would:
1. For each record key (Q1, Q2), extract unique `pivotKey` values
2. Create series like "Q1-revenue", "Q1-profit", "Q2-revenue", etc.
3. Or render as grouped/faceted visualization

`pivotKey` applies to both single array and `*Multi` forms for all cartesian charts.

## API Usage

### Basic Pivot Usage

```typescript
import { Chart } from "@elaraai/east-ui";

// Data in long/pivoted format
const salesData = [
    { month: "Jan", region: "North", sales: 100n },
    { month: "Jan", region: "South", sales: 80n },
    { month: "Feb", region: "North", sales: 120n },
    { month: "Feb", region: "South", sales: 90n },
    { month: "Feb", region: "West", sales: 50n },  // new region appears
];

// Series derived from unique "region" values
Chart.Line(salesData, [], {
    xAxis: { dataKey: "month" },
    pivotKey: "region",     // group by this field's values
    valueKey: "sales",      // y-values from this field
});
```

### With pivotColors Mapping

Specify colors for pivot values via `pivotColors` in series config (value is a `Map`):

```typescript
Chart.Line(salesData, ["sales"], {
    xAxis: { dataKey: "month" },
    pivotKey: "region",
    valueKey: "sales",
    series: {
        sales: {
            color: "blue.500",  // fallback for unmapped pivot values
            pivotColors: new Map([
                ["North", "blue.700"],
                ["South", "blue.500"],
                ["West", "blue.300"],
                // Any new regions use fallback color
            ]),
        },
    },
});
```

Or dynamically computed in East:

```typescript
// pivotColors can be an East expression
const colorMap = data
    .map(row => row.region)
    .unique()
    .toDict(region => region, (region, idx) => `blue.${700 - idx * 100}`);

Chart.Line(salesData, ["sales"], {
    xAxis: { dataKey: "month" },
    pivotKey: "region",
    valueKey: "sales",
    series: {
        sales: {
            color: "blue.500",
            pivotColors: colorMap,  // East expression
        },
    },
});
```

Without `pivotColors`, all pivot series use the series `color`:

```typescript
Chart.Line(salesData, ["sales"], {
    xAxis: { dataKey: "month" },
    pivotKey: "region",
    valueKey: "sales",
    series: {
        sales: { color: "teal.solid" },  // all pivot series use this color
    },
});
```

### Combining with Other Features

`pivotKey` works alongside existing features:

```typescript
Chart.Line(salesData, [], {
    xAxis: { dataKey: "month", label: "Month" },
    yAxis: { label: "Sales ($)" },
    pivotKey: "region",
    valueKey: "sales",
    curveType: "monotone",
    showDots: true,
    grid: { horizontal: true },
    legend: { position: "top" },
    tooltip: { enabled: true },
});
```

## Renderer Behavior

When `pivotKey` is set, the renderer performs these steps:

### 1. Extract Unique Series Names

```typescript
const seriesNames = [...new Set(data.map(row => row[pivotKey]))];
// e.g., ["North", "South", "West"]
```

### 2. Group Data by Series

```typescript
const groupedData = new Map<string, DataPoint[]>();
for (const row of data) {
    const seriesName = row[pivotKey];
    if (!groupedData.has(seriesName)) {
        groupedData.set(seriesName, []);
    }
    groupedData.get(seriesName).push({
        x: row[xAxis.dataKey],
        y: row[valueKey],
    });
}
```

### 3. Assign Colors (via series pivotColors or fallback)

Colors for pivot series are determined by the optional `pivotColors` dict in the series config. This avoids complex shade generation logic in the renderer.

```typescript
// For each series that has pivotKey enabled:
// Look up color from series.pivotColors, fall back to series.color
const seriesColors = new Map<string, string>();
seriesNames.forEach((name) => {
    const pivotColor = seriesConfig?.pivotColors?.get(name);
    seriesColors.set(name, pivotColor ?? seriesConfig?.color ?? defaultColor);
});
```

**Color resolution order:**
1. `series[seriesName].pivotColors[pivotValue]` - explicit mapping for this pivot value
2. `series[seriesName].color` - series base color (fallback)
3. Default chart color (ultimate fallback)

### 4. Build Series Configuration

```typescript
const seriesConfigs = seriesNames.map((name, index) => ({
    name,
    color: seriesColors.get(name),
    // Merge any explicit overrides from series config
    ...seriesConfig?.[name],
}));
```

### 5. Render Chart

Render with the dynamically built series configuration and grouped data.

## Interaction with Existing Data Formats

| `pivotKey` | `dataSeries` | Behavior |
|------------|--------------|----------|
| Not set | Not set | Current behavior: series from struct field names |
| Not set | Set | Current behavior: multi-series with separate arrays |
| Set | Not set | **New**: pivot mode, series from `pivotKey` values |
| Set | Set | `pivotKey` takes precedence, `dataSeries` ignored |

## Edge Cases

### Empty Data

If data is empty, render empty chart (no series).

### Missing Values

If a row is missing the `pivotKey` or `valueKey` field, skip that row.

### Single Series

If all rows have the same `pivotKey` value, render single series.

### Large Number of Series

Renderer should handle many series gracefully:
- Without `pivotColors`, all pivot series share the same color (may be desired or not)
- Legend may need scrolling for many entries
- User is responsible for providing distinct colors in `pivotColors` if differentiation needed

## Implementation Plan

### 1. Type Changes

Add `pivotKey: OptionType(StringType)` to all chart types:
- `LineChartType` in `src/charts/line/types.ts`
- `AreaChartType` in `src/charts/area/types.ts`
- `BarChartType` in `src/charts/bar/types.ts`
- `ScatterChartType` in `src/charts/scatter/types.ts`
- `ComposedChartType` in `src/charts/composed/types.ts`

Add `pivotKey` to all TypeScript style interfaces (both single and multi):
- `LineChartStyle`, `LineChartMultiStyle`
- `AreaChartStyle`, `AreaChartMultiStyle`
- `BarChartStyle`, `BarChartMultiStyle`
- `ScatterChartStyle`
- `ComposedChartStyle`, `ComposedChartMultiStyle`

Update TypeDoc with `@property pivotKey` documentation.

### 2. Factory Function Updates

Update all factory functions to handle `pivotKey`:
- `createLineChart`, `createLineChartMulti` in `src/charts/line/index.ts`
- `createAreaChart`, `createAreaChartMulti` in `src/charts/area/index.ts`
- `createBarChart`, `createBarChartMulti` in `src/charts/bar/index.ts`
- `createScatterChart` in `src/charts/scatter/index.ts`
- `createComposedChart`, `createComposedChartMulti` in `src/charts/composed/index.ts`

### 3. Tests

Add tests in `test/charts/` for all chart types:

```typescript
describeEast("Line Chart Pivot", (test) => {
    test("creates chart with pivotKey", $ => {
        const data = $.let([
            { month: "Jan", category: "A", value: 100n },
            { month: "Jan", category: "B", value: 50n },
        ]);
        const chart = $.let(Chart.Line(data, [], {
            xAxis: { dataKey: "month" },
            pivotKey: "category",
            valueKey: "value",
        }));
        // Verify pivotKey is set
        $(assertEast.equal(
            chart.unwrap("LineChart").pivotKey.unwrap("some"),
            "category"
        ));
    });

    test("creates chart without pivotKey (backward compat)", $ => {
        const data = $.let([
            { month: "Jan", revenue: 100n, profit: 50n },
        ]);
        const chart = $.let(Chart.Line(data, ["revenue", "profit"], {
            xAxis: { dataKey: "month" },
        }));
        // Verify pivotKey is none
        $(assertEast.equal(
            chart.unwrap("LineChart").pivotKey.hasTag("none"),
            true
        ));
    });
});
```

Similar tests for Area, Bar, Scatter, Composed, and all `*Multi` variants.

### 4. Documentation

1. Update component TypeDoc examples
2. Add examples to `examples/charts.ts` for validation
3. Update CLAUDE.md if needed

## Files to Modify

| File | Changes |
|------|---------|
| `src/charts/line/types.ts` | Add `pivotKey` to `LineChartType`; add `pivotColors` to `LineChartSeriesType`, `LineChartSeriesConfig`; add `pivotKey` to `LineChartStyle`, `LineChartMultiStyle` |
| `src/charts/line/index.ts` | Handle `pivotKey` and `pivotColors` in `createLineChart`, `createLineChartMulti` |
| `src/charts/area/types.ts` | Add `pivotKey` to `AreaChartType`; add `pivotColors` to series types; add `pivotKey` to `AreaChartStyle`, `AreaChartMultiStyle` |
| `src/charts/area/index.ts` | Handle `pivotKey` and `pivotColors` in `createAreaChart`, `createAreaChartMulti` |
| `src/charts/bar/types.ts` | Add `pivotKey` to `BarChartType`; add `pivotColors` to series types; add `pivotKey` to `BarChartStyle`, `BarChartMultiStyle` |
| `src/charts/bar/index.ts` | Handle `pivotKey` and `pivotColors` in `createBarChart`, `createBarChartMulti` |
| `src/charts/scatter/types.ts` | Add `pivotKey` to `ScatterChartType`; add `pivotColors` to series types; add `pivotKey` to `ScatterChartStyle` |
| `src/charts/scatter/index.ts` | Handle `pivotKey` and `pivotColors` in `createScatterChart` |
| `src/charts/composed/types.ts` | Add `pivotKey` to `ComposedChartType`; add `pivotColors` to series types; add `pivotKey` to `ComposedChartStyle`, `ComposedChartMultiStyle` |
| `src/charts/composed/index.ts` | Handle `pivotKey` and `pivotColors` in `createComposedChart`, `createComposedChartMulti` |
| `test/charts/line.spec.ts` | Add pivot tests for Line and LineMulti |
| `test/charts/area.spec.ts` | Add pivot tests for Area and AreaMulti |
| `test/charts/bar.spec.ts` | Add pivot tests for Bar and BarMulti |
| `test/charts/scatter.spec.ts` | Add pivot tests for Scatter |
| `test/charts/composed.spec.ts` | Add pivot tests for Composed and ComposedMulti |
| `examples/charts.ts` | Add TypeDoc example validation |

## Compatibility

- **Backward compatible**: Existing code without `pivotKey` works unchanged
- **Additive change**: No breaking changes to existing APIs
- **Renderer responsibility**: Pivot logic is renderer-side; East UI just passes the config

## Future Considerations

### Series Order

Could add optional `seriesOrder` to control the order of pivot series:

```typescript
{
    pivotKey: "region",
    seriesOrder: ["North", "South", "West"],  // explicit order (default: order of appearance in data)
}
```

This is out of scope for initial implementation but noted for future enhancement.

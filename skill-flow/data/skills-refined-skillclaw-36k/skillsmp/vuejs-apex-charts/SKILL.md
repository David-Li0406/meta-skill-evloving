---
name: vuejs-apex-charts
description: |
  ApexCharts integration for Vue 3 using vue3-apexcharts for data visualization.
  WHEN: Creating charts in Vue 3 (line, bar, pie, donut, radar, heatmap), building dashboards, real-time chart updates, integrating API data with charts.
  WHEN NOT: Non-Vue projects, other chart libraries (Chart.js, D3), general Vue development (use vuejs-dev).
---

# Vue 3 ApexCharts

Complete guide for ApexCharts in Vue 3 using vue3-apexcharts.

## Installation

```bash
npm install apexcharts vue3-apexcharts
```

## Setup

### Global Registration (Recommended)

```javascript
// main.js
import { createApp } from 'vue'
import VueApexCharts from 'vue3-apexcharts'
import App from './App.vue'

const app = createApp(App)
app.use(VueApexCharts)
app.mount('#app')
```

### Local Registration

```vue
<script setup>
import VueApexCharts from 'vue3-apexcharts'
</script>

<template>
  <VueApexCharts type="line" :options="options" :series="series" />
</template>
```

## Component Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `type` | String | 'line' | Chart type (required) |
| `series` | Array | [] | Data series (required) |
| `options` | Object | {} | Chart configuration |
| `width` | String/Number | '100%' | Chart width |
| `height` | String/Number | 'auto' | Chart height |

## Basic Usage

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { id: 'basic-chart' },
  xaxis: { categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May'] }
})

const series = ref([{
  name: 'Sales',
  data: [30, 40, 35, 50, 49]
}])
</script>

<template>
  <apexchart 
    type="line" 
    height="350" 
    :options="options" 
    :series="series" 
  />
</template>
```

## Chart Types Quick Reference

| Type | Value | Use Case |
|------|-------|----------|
| Line | `line` | Trends over time |
| Area | `area` | Volume/cumulative data |
| Bar | `bar` | Horizontal comparisons |
| Column | `bar` + vertical | Vertical comparisons |
| Pie | `pie` | Part of whole (few items) |
| Donut | `donut` | Part of whole with center |
| Radar | `radar` | Multi-variable comparison |
| Heatmap | `heatmap` | Matrix/density data |
| Candlestick | `candlestick` | Financial OHLC data |
| RadialBar | `radialBar` | Progress/gauges |
| Treemap | `treemap` | Hierarchical data |
| Scatter | `scatter` | Correlation analysis |
| Bubble | `bubble` | 3-variable comparison |

**For detailed chart configurations, see:**
- `references/charts-cartesian.md` - Line, Area, Bar, Column, Scatter, Bubble
- `references/charts-circular.md` - Pie, Donut, RadialBar, PolarArea
- `references/charts-specialized.md` - Heatmap, Treemap, Radar, Candlestick, BoxPlot, RangeBar

## Updating Charts

In Vue 3, charts auto-update when reactive props change:

```vue
<script setup>
import { ref } from 'vue'

const series = ref([{ name: 'Sales', data: [30, 40, 35] }])
const options = ref({ chart: { id: 'my-chart' } })

// Update data - chart auto-updates
function updateData() {
  series.value = [{ name: 'Sales', data: [50, 60, 45] }]
}

// Update options - chart auto-updates
function updateOptions() {
  options.value = {
    ...options.value,
    theme: { palette: 'palette2' }
  }
}
</script>
```

## Series Data Formats

### Category Data (Most Common)

```javascript
// Data + separate categories
series: [{ name: 'Sales', data: [30, 40, 35, 50] }]
options: { xaxis: { categories: ['Jan', 'Feb', 'Mar', 'Apr'] } }
```

### XY Paired Data (Recommended)

```javascript
// Self-contained with labels
series: [{
  name: 'Sales',
  data: [
    { x: 'Jan', y: 30 },
    { x: 'Feb', y: 40 },
    { x: 'Mar', y: 35 }
  ]
}]
```

### Numeric XY Data

```javascript
// For scatter/bubble charts
series: [{
  name: 'Points',
  data: [
    { x: 10, y: 20 },
    { x: 15, y: 35 },
    { x: 20, y: 25 }
  ]
}]
options: { xaxis: { type: 'numeric' } }
```

### Datetime Data

```javascript
// Timestamps or date strings
series: [{
  name: 'Traffic',
  data: [
    { x: new Date('2024-01-01').getTime(), y: 100 },
    { x: new Date('2024-01-02').getTime(), y: 150 }
  ]
}]
options: { xaxis: { type: 'datetime' } }
```

### Pie/Donut Data

```javascript
// Single array with labels
series: [44, 55, 13, 43, 22]
options: { labels: ['Apple', 'Mango', 'Orange', 'Banana', 'Grape'] }

// Or XY format (v5.3+)
series: [{
  data: [
    { x: 'Apple', y: 44 },
    { x: 'Mango', y: 55 }
  ]
}]
```

**For data transformation patterns, see `references/data-patterns.md`**

## Common Options Structure

```javascript
const options = {
  chart: {
    id: 'unique-id',
    type: 'line',
    height: 350,
    toolbar: { show: true },
    zoom: { enabled: true }
  },
  title: { text: 'Chart Title', align: 'center' },
  subtitle: { text: 'Subtitle', align: 'center' },
  xaxis: {
    type: 'category', // 'category' | 'datetime' | 'numeric'
    categories: [],
    title: { text: 'X Axis' }
  },
  yaxis: {
    title: { text: 'Y Axis' },
    min: 0,
    max: 100
  },
  stroke: { curve: 'smooth', width: 2 },
  dataLabels: { enabled: false },
  legend: { position: 'top' },
  tooltip: { enabled: true, shared: true },
  colors: ['#008FFB', '#00E396', '#FEB019'],
  responsive: [{
    breakpoint: 768,
    options: { chart: { height: 300 } }
  }]
}
```

**For complete options reference, see `references/options-reference.md`**

## References

| File | Content |
|------|---------|
| `references/charts-cartesian.md` | Line, Area, Bar, Column, Scatter, Bubble charts |
| `references/charts-circular.md` | Pie, Donut, RadialBar, PolarArea charts |
| `references/charts-specialized.md` | Heatmap, Treemap, Radar, Candlestick, Funnel |
| `references/options-reference.md` | Complete options API reference |
| `references/methods-events.md` | Chart methods and event handlers |
| `references/data-patterns.md` | API integration, real-time updates, datetime |
| `references/styling-tailwind.md` | Tailwind CSS integration, themes, dark mode |

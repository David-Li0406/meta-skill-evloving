# Cartesian Charts

Charts with X and Y axes: Line, Area, Bar, Column, Scatter, Bubble.

## Table of Contents
- [Line Chart](#line-chart)
- [Area Chart](#area-chart)
- [Bar Chart](#bar-chart)
- [Column Chart](#column-chart)
- [Scatter Chart](#scatter-chart)
- [Bubble Chart](#bubble-chart)
- [Mixed/Combo Charts](#mixedcombo-charts)

---

## Line Chart

Best for: Trends over time, continuous data.

### Basic Line

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { id: 'line-chart' },
  xaxis: { categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May'] },
  stroke: { curve: 'smooth' }
})

const series = ref([
  { name: 'Sales', data: [30, 40, 35, 50, 49] },
  { name: 'Revenue', data: [20, 30, 25, 40, 35] }
])
</script>

<template>
  <apexchart type="line" height="350" :options="options" :series="series" />
</template>
```

### Line Curve Options

```javascript
stroke: {
  curve: 'smooth',    // Smooth spline curve
  // curve: 'straight', // Direct point-to-point
  // curve: 'stepline', // Staircase steps
  width: 2,           // Line thickness
  dashArray: [0, 5]   // Solid first series, dashed second
}
```

### Line with Markers

```javascript
markers: {
  size: 5,
  colors: ['#008FFB'],
  strokeColors: '#fff',
  strokeWidth: 2,
  hover: { size: 7 }
}
```

### Gradient Line

```javascript
fill: {
  type: 'gradient',
  gradient: {
    shade: 'dark',
    type: 'vertical',
    shadeIntensity: 0.5,
    opacityFrom: 0.7,
    opacityTo: 0.2
  }
}
```

---

## Area Chart

Best for: Volume data, cumulative values, showing magnitude.

### Basic Area

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'area' },
  xaxis: { type: 'datetime' },
  stroke: { curve: 'smooth' },
  fill: { type: 'gradient', gradient: { opacityFrom: 0.6, opacityTo: 0.1 } }
})

const series = ref([{
  name: 'Traffic',
  data: [
    { x: new Date('2024-01-01'), y: 100 },
    { x: new Date('2024-01-02'), y: 150 },
    { x: new Date('2024-01-03'), y: 120 }
  ]
}])
</script>

<template>
  <apexchart type="area" height="350" :options="options" :series="series" />
</template>
```

### Stacked Area

```javascript
chart: {
  type: 'area',
  stacked: true
},
fill: {
  type: 'gradient',
  gradient: { opacityFrom: 0.6, opacityTo: 0.8 }
}
```

### Spline Area

```javascript
stroke: {
  curve: 'smooth',
  width: 2
},
fill: {
  type: 'solid',
  opacity: 0.3
}
```

---

## Bar Chart

Best for: Horizontal comparisons, categorical data with long labels.

### Basic Horizontal Bar

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'bar' },
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: '70%'
    }
  },
  xaxis: { categories: ['Product A', 'Product B', 'Product C', 'Product D'] }
})

const series = ref([{ name: 'Sales', data: [400, 430, 448, 470] }])
</script>

<template>
  <apexchart type="bar" height="350" :options="options" :series="series" />
</template>
```

### Stacked Bar

```javascript
chart: { type: 'bar', stacked: true },
plotOptions: { bar: { horizontal: true } }
```

### 100% Stacked Bar

```javascript
chart: { 
  type: 'bar', 
  stacked: true,
  stackType: '100%'
}
```

### Bar with Data Labels

```javascript
plotOptions: {
  bar: {
    horizontal: true,
    dataLabels: { position: 'top' }
  }
},
dataLabels: {
  enabled: true,
  offsetX: -6,
  style: { fontSize: '12px', colors: ['#fff'] }
}
```

---

## Column Chart

Best for: Vertical comparisons, time-series categorical data.

### Basic Column

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'bar' },  // Note: type is 'bar', horizontal: false (default)
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: '55%',
      borderRadius: 4
    }
  },
  xaxis: { categories: ['Q1', 'Q2', 'Q3', 'Q4'] }
})

const series = ref([
  { name: '2023', data: [44, 55, 57, 56] },
  { name: '2024', data: [76, 85, 101, 98] }
])
</script>

<template>
  <apexchart type="bar" height="350" :options="options" :series="series" />
</template>
```

### Grouped Column

```javascript
plotOptions: {
  bar: {
    horizontal: false,
    columnWidth: '70%',
    borderRadius: 4,
    dataLabels: { position: 'top' }
  }
}
```

### Stacked Column

```javascript
chart: { type: 'bar', stacked: true },
plotOptions: { bar: { horizontal: false } }
```

### Column with Negative Values

```javascript
plotOptions: {
  bar: {
    colors: {
      ranges: [{
        from: -100,
        to: 0,
        color: '#F15B46'  // Red for negative
      }]
    }
  }
}
```

---

## Scatter Chart

Best for: Correlation analysis, distribution patterns.

### Basic Scatter

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'scatter', zoom: { enabled: true } },
  xaxis: { type: 'numeric', tickAmount: 10 },
  yaxis: { tickAmount: 7 }
})

const series = ref([{
  name: 'Sample A',
  data: [
    [16.4, 5.4], [21.7, 2], [25.4, 3], [19, 2],
    [10.9, 1], [13.6, 3.2], [10.9, 7.4], [10.9, 0]
  ]
}])
</script>

<template>
  <apexchart type="scatter" height="350" :options="options" :series="series" />
</template>
```

### Scatter with Custom Markers

```javascript
markers: {
  size: 10,
  shape: 'circle',  // 'circle', 'square', 'triangle'
  strokeWidth: 0
}
```

### Scatter with Datetime X-Axis

```javascript
xaxis: { type: 'datetime' },
series: [{
  name: 'Events',
  data: [
    { x: new Date('2024-01-15').getTime(), y: 45 },
    { x: new Date('2024-02-10').getTime(), y: 52 }
  ]
}]
```

---

## Bubble Chart

Best for: Three-variable comparison (x, y, size).

### Basic Bubble

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'bubble' },
  xaxis: { tickAmount: 12, type: 'numeric' },
  yaxis: { max: 70 },
  plotOptions: {
    bubble: {
      minBubbleRadius: 10,
      maxBubbleRadius: 50
    }
  }
})

// [x, y, size]
const series = ref([{
  name: 'Product A',
  data: [
    [10, 20, 30],
    [20, 35, 45],
    [30, 15, 25],
    [40, 45, 60]
  ]
}])
</script>

<template>
  <apexchart type="bubble" height="350" :options="options" :series="series" />
</template>
```

### 3D Bubble Effect

```javascript
fill: {
  opacity: 0.8,
  type: 'gradient'
},
plotOptions: {
  bubble: { zScaling: true }
}
```

---

## Mixed/Combo Charts

Combine multiple chart types in one visualization.

### Line + Column

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'line' },
  stroke: { width: [0, 2] },  // 0 for bars, 2 for line
  xaxis: { categories: ['Jan', 'Feb', 'Mar', 'Apr'] }
})

const series = ref([
  {
    name: 'Revenue',
    type: 'column',
    data: [440, 505, 414, 671]
  },
  {
    name: 'Growth %',
    type: 'line',
    data: [23, 42, 35, 27]
  }
])
</script>

<template>
  <apexchart type="line" height="350" :options="options" :series="series" />
</template>
```

### Line + Area + Column

```javascript
series: [
  { name: 'Income', type: 'column', data: [1.4, 2, 2.5, 1.5] },
  { name: 'Cashflow', type: 'column', data: [1.1, 3, 3.1, 4] },
  { name: 'Revenue', type: 'line', data: [20, 29, 37, 36] }
],
stroke: { width: [0, 0, 2] },
fill: { opacity: [0.85, 0.85, 1] }
```

### Multiple Y-Axes

```javascript
yaxis: [
  {
    title: { text: 'Revenue ($)' },
    seriesName: 'Revenue'
  },
  {
    opposite: true,
    title: { text: 'Growth (%)' },
    seriesName: 'Growth %'
  }
]
```

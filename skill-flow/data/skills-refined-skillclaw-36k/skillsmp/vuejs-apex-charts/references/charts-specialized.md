# Specialized Charts

Advanced chart types: Heatmap, Treemap, Radar, Candlestick, BoxPlot, RangeBar, Funnel.

## Table of Contents
- [Heatmap Chart](#heatmap-chart)
- [Treemap Chart](#treemap-chart)
- [Radar Chart](#radar-chart)
- [Candlestick Chart](#candlestick-chart)
- [BoxPlot Chart](#boxplot-chart)
- [RangeBar Chart](#rangebar-chart)
- [Funnel Chart](#funnel-chart)
- [Synchronized Charts](#synchronized-charts)

---

## Heatmap Chart

Best for: Matrix data, correlation visualization, activity patterns.

### Basic Heatmap

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'heatmap' },
  dataLabels: { enabled: false },
  colors: ['#008FFB'],
  plotOptions: {
    heatmap: {
      shadeIntensity: 0.5,
      colorScale: {
        ranges: [
          { from: 0, to: 20, color: '#00A100', name: 'low' },
          { from: 21, to: 40, color: '#128FD9', name: 'medium' },
          { from: 41, to: 60, color: '#FFB200', name: 'high' }
        ]
      }
    }
  }
})

const series = ref([
  { name: 'Mon', data: [{ x: 'W1', y: 22 }, { x: 'W2', y: 29 }, { x: 'W3', y: 13 }] },
  { name: 'Tue', data: [{ x: 'W1', y: 43 }, { x: 'W2', y: 35 }, { x: 'W3', y: 51 }] },
  { name: 'Wed', data: [{ x: 'W1', y: 32 }, { x: 'W2', y: 33 }, { x: 'W3', y: 12 }] }
])
</script>

<template>
  <apexchart type="heatmap" height="350" :options="options" :series="series" />
</template>
```

### Multi-Color Heatmap

```javascript
plotOptions: {
  heatmap: {
    shadeIntensity: 0.5,
    radius: 0,
    useFillColorAsStroke: true,
    colorScale: {
      ranges: [
        { from: -30, to: 5, name: 'low', color: '#00A100' },
        { from: 6, to: 20, name: 'medium', color: '#128FD9' },
        { from: 21, to: 45, name: 'high', color: '#FFB200' },
        { from: 46, to: 55, name: 'extreme', color: '#FF0000' }
      ]
    }
  }
}
```

### Rounded Heatmap

```javascript
plotOptions: {
  heatmap: {
    radius: 4,  // Rounded corners
    enableShades: true
  }
}
```

---

## Treemap Chart

Best for: Hierarchical data, proportional comparison.

### Basic Treemap

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'treemap' },
  legend: { show: false },
  plotOptions: {
    treemap: {
      distributed: true,
      enableShades: false
    }
  }
})

const series = ref([{
  data: [
    { x: 'New Delhi', y: 218 },
    { x: 'Kolkata', y: 149 },
    { x: 'Mumbai', y: 184 },
    { x: 'Ahmedabad', y: 55 },
    { x: 'Bangalore', y: 84 },
    { x: 'Pune', y: 31 },
    { x: 'Chennai', y: 70 }
  ]
}])
</script>

<template>
  <apexchart type="treemap" height="350" :options="options" :series="series" />
</template>
```

### Multi-Series Treemap (Groups)

```javascript
series: [
  {
    name: 'Desktops',
    data: [
      { x: 'ABC', y: 10 },
      { x: 'DEF', y: 60 },
      { x: 'XYZ', y: 41 }
    ]
  },
  {
    name: 'Mobile',
    data: [
      { x: 'ABCD', y: 10 },
      { x: 'DEFG', y: 20 },
      { x: 'WXYZ', y: 51 }
    ]
  }
]
```

### Treemap with Color Ranges

```javascript
plotOptions: {
  treemap: {
    enableShades: true,
    shadeIntensity: 0.5,
    reverseNegativeShade: true,
    colorScale: {
      ranges: [
        { from: -6, to: 0, color: '#CD363A' },
        { from: 0.001, to: 6, color: '#52B12C' }
      ]
    }
  }
}
```

---

## Radar Chart

Best for: Multi-variable comparison, skill assessments.

### Basic Radar

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'radar' },
  xaxis: {
    categories: ['Strength', 'Speed', 'Agility', 'Stamina', 'Defense', 'Attack']
  },
  yaxis: { show: false },
  markers: { size: 4 },
  fill: { opacity: 0.2 }
})

const series = ref([
  { name: 'Player A', data: [80, 50, 30, 40, 100, 20] },
  { name: 'Player B', data: [20, 30, 40, 80, 20, 80] }
])
</script>

<template>
  <apexchart type="radar" height="350" :options="options" :series="series" />
</template>
```

### Radar with Polygons

```javascript
plotOptions: {
  radar: {
    size: 140,
    polygons: {
      strokeColors: '#e9e9e9',
      strokeWidth: 1,
      connectorColors: '#e9e9e9',
      fill: {
        colors: ['#f8f8f8', '#fff']
      }
    }
  }
}
```

### Multiple Radar

```javascript
fill: { opacity: 0.4 },
stroke: { show: true, width: 2 },
markers: { size: 0 }
```

---

## Candlestick Chart

Best for: Financial OHLC data, stock prices.

### Basic Candlestick

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'candlestick' },
  xaxis: { type: 'datetime' },
  yaxis: { tooltip: { enabled: true } },
  plotOptions: {
    candlestick: {
      colors: {
        upward: '#00E396',
        downward: '#FF4560'
      }
    }
  }
})

// Data format: [timestamp, [open, high, low, close]]
const series = ref([{
  name: 'Stock',
  data: [
    { x: new Date('2024-01-01'), y: [51.98, 56.29, 51.59, 53.85] },
    { x: new Date('2024-01-02'), y: [53.66, 54.99, 51.35, 52.95] },
    { x: new Date('2024-01-03'), y: [52.76, 57.35, 52.15, 57.03] },
    { x: new Date('2024-01-04'), y: [57.04, 58.15, 48.88, 49.24] }
  ]
}])
</script>

<template>
  <apexchart type="candlestick" height="350" :options="options" :series="series" />
</template>
```

### Candlestick with Line (MA)

```javascript
series: [
  {
    name: 'candle',
    type: 'candlestick',
    data: candleData
  },
  {
    name: 'MA',
    type: 'line',
    data: maData
  }
]
```

---

## BoxPlot Chart

Best for: Statistical distribution, outliers visualization.

### Basic BoxPlot

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'boxPlot' },
  plotOptions: {
    boxPlot: {
      colors: {
        upper: '#5C4742',
        lower: '#A5978B'
      }
    }
  }
})

// Data format: [min, q1, median, q3, max]
const series = ref([{
  name: 'Box',
  type: 'boxPlot',
  data: [
    { x: 'Jan', y: [54, 66, 69, 75, 88] },
    { x: 'Feb', y: [43, 65, 69, 76, 81] },
    { x: 'Mar', y: [31, 39, 45, 51, 59] }
  ]
}])
</script>

<template>
  <apexchart type="boxPlot" height="350" :options="options" :series="series" />
</template>
```

### Horizontal BoxPlot

```javascript
plotOptions: {
  bar: { horizontal: true },
  boxPlot: { colors: { upper: '#008FFB', lower: '#FEB019' } }
}
```

---

## RangeBar Chart

Best for: Timelines, Gantt-like visualizations, duration comparisons.

### Basic RangeBar (Timeline)

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'rangeBar' },
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: '50%',
      rangeBarGroupRows: true
    }
  },
  xaxis: { type: 'datetime' },
  fill: { type: 'solid' }
})

const series = ref([
  {
    name: 'Bob',
    data: [{
      x: 'Design',
      y: [new Date('2024-01-01').getTime(), new Date('2024-01-08').getTime()]
    }, {
      x: 'Code',
      y: [new Date('2024-01-08').getTime(), new Date('2024-01-20').getTime()]
    }]
  },
  {
    name: 'Joe',
    data: [{
      x: 'Design',
      y: [new Date('2024-01-05').getTime(), new Date('2024-01-15').getTime()]
    }]
  }
])
</script>

<template>
  <apexchart type="rangeBar" height="350" :options="options" :series="series" />
</template>
```

### Vertical RangeBar

```javascript
plotOptions: {
  bar: { horizontal: false }
}
```

---

## Funnel Chart

Best for: Sales funnels, conversion rates, sequential stages.

### Basic Funnel

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'bar' },
  plotOptions: {
    bar: {
      borderRadius: 0,
      horizontal: true,
      barHeight: '80%',
      isFunnel: true
    }
  },
  dataLabels: {
    enabled: true,
    formatter: (val, opt) => opt.w.globals.labels[opt.dataPointIndex] + ': ' + val,
    dropShadow: { enabled: true }
  },
  xaxis: {
    categories: ['Visits', 'Leads', 'Prospects', 'Qualified', 'Closed']
  }
})

const series = ref([{ name: 'Funnel', data: [1380, 1100, 990, 880, 740] }])
</script>

<template>
  <apexchart type="bar" height="350" :options="options" :series="series" />
</template>
```

### Pyramid (Inverted Funnel)

```javascript
plotOptions: {
  bar: {
    isFunnel: true,
    isFunnel3d: true
  }
}
```

---

## Synchronized Charts

Link multiple charts together for coordinated interactions.

### Basic Sync

```vue
<script setup>
import { ref } from 'vue'

const options1 = ref({
  chart: { id: 'chart1', group: 'social', type: 'line' },
  xaxis: { type: 'datetime' }
})

const options2 = ref({
  chart: { id: 'chart2', group: 'social', type: 'area' },
  xaxis: { type: 'datetime' }
})

const series1 = ref([{ name: 'Facebook', data: generateData() }])
const series2 = ref([{ name: 'Twitter', data: generateData() }])
</script>

<template>
  <apexchart type="line" height="160" :options="options1" :series="series1" />
  <apexchart type="area" height="160" :options="options2" :series="series2" />
</template>
```

Key sync properties:
- `chart.group`: Same group name links charts
- `chart.id`: Unique identifier for each chart
- Zoom, pan, and tooltip sync automatically

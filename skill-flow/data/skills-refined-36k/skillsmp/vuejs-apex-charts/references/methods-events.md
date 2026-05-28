# Methods & Events

Chart methods for programmatic control and event handlers.

## Table of Contents
- [Accessing Chart Methods in Vue 3](#accessing-chart-methods-in-vue-3)
- [Update Methods](#update-methods)
- [Series Methods](#series-methods)
- [Navigation Methods](#navigation-methods)
- [Annotation Methods](#annotation-methods)
- [Export Methods](#export-methods)
- [Event Handlers](#event-handlers)

---

## Accessing Chart Methods in Vue 3

### Using Template Ref

```vue
<script setup>
import { ref, onMounted } from 'vue'

const chartRef = ref(null)

onMounted(() => {
  // Access chart instance
  const chartInstance = chartRef.value.chart
  
  // Call methods
  chartInstance.updateSeries([{ data: [10, 20, 30] }])
})

function updateChart() {
  chartRef.value.chart.updateOptions({
    title: { text: 'Updated Title' }
  })
}
</script>

<template>
  <apexchart 
    ref="chartRef"
    type="line" 
    :options="options" 
    :series="series" 
  />
  <button @click="updateChart">Update</button>
</template>
```

### Using ApexCharts.exec (Global)

```javascript
// Works without direct chart reference
// Requires chart.id to be set

ApexCharts.exec('my-chart-id', 'updateSeries', [{ data: [10, 20, 30] }])
ApexCharts.exec('my-chart-id', 'toggleSeries', 'Series 1')
```

---

## Update Methods

### updateOptions(options, redrawPaths, animate, updateSyncedCharts)

Update chart configuration. Merges with existing options.

```javascript
chartRef.value.chart.updateOptions({
  xaxis: { labels: { show: false } },
  yaxis: { min: 20, max: 100 },
  title: { text: 'New Title' }
})

// Parameters:
// redrawPaths: boolean (default: false) - Redraw from scratch
// animate: boolean (default: true) - Animate changes
// updateSyncedCharts: boolean (default: true) - Update grouped charts
```

### updateSeries(newSeries, animate)

Replace the entire series data.

```javascript
chartRef.value.chart.updateSeries([
  { name: 'Sales', data: [32, 44, 31, 41, 22] }
])

// Alternative data formats
chartRef.value.chart.updateSeries([{
  data: [
    { x: 'Jan', y: 44 },
    { x: 'Feb', y: 51 },
    { x: 'Mar', y: 32 }
  ]
}])
```

### appendData(newData)

Append new data points to existing series.

```javascript
// For real-time updates
chartRef.value.chart.appendData([
  { data: [32] },  // Append to series 0
  { data: [12] }   // Append to series 1
])
```

### appendSeries(newSeries, animate)

Add a new series to existing ones.

```javascript
chartRef.value.chart.appendSeries({
  name: 'New Series',
  data: [32, 44, 31, 41, 22]
})
```

---

## Series Methods

### toggleSeries(seriesName)

Toggle series visibility.

```javascript
chartRef.value.chart.toggleSeries('Sales')
// Returns: boolean (new visibility state)
```

### showSeries(seriesName)

Show a hidden series.

```javascript
chartRef.value.chart.showSeries('Sales')
```

### hideSeries(seriesName)

Hide a visible series.

```javascript
chartRef.value.chart.hideSeries('Sales')
```

### highlightSeries(seriesName)

Highlight a series (dim others).

```javascript
chartRef.value.chart.highlightSeries('Sales')
```

### resetSeries(shouldUpdateChart, shouldResetZoom)

Reset to original series state.

```javascript
chartRef.value.chart.resetSeries()

// Parameters:
// shouldUpdateChart: boolean (default: true)
// shouldResetZoom: boolean (default: true)
```

---

## Navigation Methods

### zoomX(start, end)

Programmatically zoom to a range.

```javascript
// For datetime axis
chartRef.value.chart.zoomX(
  new Date('2024-01-01').getTime(),
  new Date('2024-01-31').getTime()
)

// For numeric axis
chartRef.value.chart.zoomX(10, 50)
```

### toggleDataPointSelection(seriesIndex, dataPointIndex)

Select/deselect a data point.

```javascript
// Toggle the 4th point of the 2nd series
chartRef.value.chart.toggleDataPointSelection(1, 3)

// For pie/donut (single index)
chartRef.value.chart.toggleDataPointSelection(2)
```

---

## Annotation Methods

### addXaxisAnnotation(options, pushToMemory)

Add X-axis annotation dynamically.

```javascript
chartRef.value.chart.addXaxisAnnotation({
  id: 'my-annotation',
  x: 'Feb',  // Or timestamp for datetime
  label: {
    text: 'Event',
    style: { background: '#775DD0' }
  }
})
```

### addYaxisAnnotation(options, pushToMemory)

Add Y-axis annotation dynamically.

```javascript
chartRef.value.chart.addYaxisAnnotation({
  id: 'target-line',
  y: 50,
  borderColor: '#00E396',
  label: {
    text: 'Target',
    position: 'right'
  }
})
```

### addPointAnnotation(options, pushToMemory)

Add point annotation dynamically.

```javascript
chartRef.value.chart.addPointAnnotation({
  id: 'important-point',
  x: 'Mar',
  y: 45,
  marker: {
    size: 8,
    fillColor: '#fff',
    strokeColor: '#FF4560',
    strokeWidth: 3
  },
  label: { text: 'Peak' }
})
```

### removeAnnotation(id)

Remove a specific annotation.

```javascript
chartRef.value.chart.removeAnnotation('my-annotation')
```

### clearAnnotations()

Remove all dynamic annotations.

```javascript
chartRef.value.chart.clearAnnotations()
```

---

## Export Methods

### dataURI(options)

Get chart as base64 image.

```javascript
const { imgURI, blob } = await chartRef.value.chart.dataURI({
  scale: 2,   // Resolution multiplier
  width: 800  // Or specify width
})

// Use for PDF generation with jsPDF
const pdf = new jsPDF()
pdf.addImage(imgURI, 'PNG', 0, 0)
pdf.save('chart.pdf')
```

### destroy()

Remove chart and cleanup.

```javascript
chartRef.value.chart.destroy()
```

---

## Event Handlers

Configure in chart options:

```javascript
const options = ref({
  chart: {
    events: {
      // Chart lifecycle
      mounted: (chartContext, config) => {
        console.log('Chart mounted')
      },
      updated: (chartContext, config) => {
        console.log('Chart updated')
      },
      animationEnd: (chartContext, config) => {
        console.log('Animation complete')
      },
      beforeMount: (chartContext, config) => {},
      
      // User interactions
      click: (event, chartContext, opts) => {
        console.log('Clicked', opts.seriesIndex, opts.dataPointIndex)
      },
      mouseMove: (event, chartContext, opts) => {},
      mouseLeave: (event, chartContext, opts) => {},
      
      // Legend
      legendClick: (chartContext, seriesIndex, opts) => {
        console.log('Legend clicked', seriesIndex)
      },
      
      // Markers
      markerClick: (event, chartContext, opts) => {
        console.log('Marker clicked', opts.dataPointIndex)
      },
      
      // Data points
      dataPointSelection: (event, chartContext, opts) => {
        console.log('Selected', opts.selectedDataPoints)
      },
      dataPointMouseEnter: (event, chartContext, opts) => {},
      dataPointMouseLeave: (event, chartContext, opts) => {},
      
      // Axes
      xAxisLabelClick: (event, chartContext, opts) => {
        console.log('X label clicked', opts.labelIndex)
      },
      
      // Zoom/Pan
      beforeZoom: (chartContext, { xaxis }) => {
        return { xaxis }  // Return false to cancel
      },
      zoomed: (chartContext, { xaxis, yaxis }) => {
        console.log('Zoomed to', xaxis.min, xaxis.max)
      },
      beforeResetZoom: (chartContext, opts) => {},
      scrolled: (chartContext, { xaxis }) => {},
      
      // Selection
      selection: (chartContext, { xaxis, yaxis }) => {
        console.log('Selected range', xaxis.min, xaxis.max)
      },
      
      // Brush
      brushScrolled: (chartContext, { xaxis }) => {}
    }
  }
})
```

### Event Handler Parameters

```javascript
// opts object contains:
{
  seriesIndex: 0,           // Series index
  dataPointIndex: 2,        // Data point index
  w: {                      // Global config
    globals: {
      series: [...],
      labels: [...],
      selectedDataPoints: [...]
    },
    config: {...}
  }
}
```

### Custom Selection Handler

```javascript
events: {
  selection: (chartContext, { xaxis, yaxis }) => {
    // Get selected range
    const startX = xaxis.min
    const endX = xaxis.max
    
    // Filter data in range
    const selectedData = rawData.filter(
      point => point.x >= startX && point.x <= endX
    )
    
    console.log('Selected data:', selectedData)
  }
}
```

### Data Point Click Handler

```javascript
events: {
  dataPointSelection: (event, chartContext, opts) => {
    const { seriesIndex, dataPointIndex, selectedDataPoints } = opts
    const value = chartContext.w.globals.series[seriesIndex][dataPointIndex]
    const label = chartContext.w.globals.labels[dataPointIndex]
    
    console.log(`Clicked ${label}: ${value}`)
  }
}
```

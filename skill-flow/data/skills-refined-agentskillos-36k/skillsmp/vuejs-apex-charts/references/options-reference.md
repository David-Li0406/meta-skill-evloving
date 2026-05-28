# Options Reference

Complete ApexCharts configuration options.

## Table of Contents
- [Chart Options](#chart-options)
- [Series Options](#series-options)
- [Axes Options](#axes-options)
- [Data Labels](#data-labels)
- [Legend](#legend)
- [Tooltip](#tooltip)
- [Grid](#grid)
- [Stroke](#stroke)
- [Fill](#fill)
- [Markers](#markers)
- [Annotations](#annotations)
- [Responsive](#responsive)
- [Title & Subtitle](#title--subtitle)

---

## Chart Options

```javascript
chart: {
  // Identity
  id: 'unique-chart-id',
  type: 'line',
  group: 'sync-group',
  
  // Dimensions
  width: '100%',
  height: 350,
  
  // Appearance
  background: '#fff',
  foreColor: '#373d3f',
  fontFamily: 'Inter, sans-serif',
  
  // Behavior
  animations: {
    enabled: true,
    speed: 800,
    animateGradually: { enabled: true, delay: 150 },
    dynamicAnimation: { enabled: true, speed: 350 }
  },
  
  // Toolbar
  toolbar: {
    show: true,
    tools: {
      download: true,
      selection: true,
      zoom: true,
      zoomin: true,
      zoomout: true,
      pan: true,
      reset: true
    },
    export: {
      csv: { filename: 'chart-data' },
      svg: { filename: 'chart-image' },
      png: { filename: 'chart-image' }
    }
  },
  
  // Zoom
  zoom: {
    enabled: true,
    type: 'x',  // 'x', 'y', 'xy'
    autoScaleYaxis: true
  },
  
  // Selection
  selection: {
    enabled: true,
    type: 'x',
    fill: { color: '#24292e', opacity: 0.1 },
    stroke: { width: 1, dashArray: 3, color: '#24292e', opacity: 0.4 }
  },
  
  // Special modes
  sparkline: { enabled: false },  // Minimal chart without axes
  stacked: false,                 // Stack series
  stackType: 'normal',            // 'normal', '100%'
  
  // Shadow
  dropShadow: {
    enabled: false,
    top: 0,
    left: 0,
    blur: 3,
    opacity: 0.35
  },
  
  // Redraw behavior
  redrawOnParentResize: true,
  redrawOnWindowResize: true
}
```

---

## Series Options

```javascript
series: [
  {
    name: 'Series Name',
    data: [30, 40, 35, 50, 49],
    color: '#008FFB',           // Override series color
    type: 'line',               // For mixed charts
    group: 'group-a'            // Group for stacking
  }
]

// Axis charts data formats:
data: [30, 40, 35, 50]                           // Simple values
data: [{ x: 'Jan', y: 30 }, { x: 'Feb', y: 40 }] // XY pairs
data: [[1, 30], [2, 40], [3, 35]]                // Numeric XY arrays

// Pie/Donut format:
series: [44, 55, 13, 43, 22]
labels: ['A', 'B', 'C', 'D', 'E']
```

---

## Axes Options

### X-Axis

```javascript
xaxis: {
  type: 'category',  // 'category', 'datetime', 'numeric'
  categories: ['Jan', 'Feb', 'Mar', 'Apr'],
  
  title: {
    text: 'X Axis Title',
    style: { fontSize: '14px', fontWeight: 600 }
  },
  
  labels: {
    show: true,
    rotate: -45,
    rotateAlways: false,
    hideOverlappingLabels: true,
    showDuplicates: false,
    trim: true,
    minHeight: undefined,
    maxHeight: 120,
    style: { fontSize: '12px', colors: [] },
    formatter: (value) => value,
    datetimeFormatter: {
      year: 'yyyy',
      month: "MMM 'yy",
      day: 'dd MMM',
      hour: 'HH:mm'
    }
  },
  
  axisBorder: { show: true, color: '#78909C' },
  axisTicks: { show: true, color: '#78909C' },
  
  tickAmount: 'dataPoints',  // Number or 'dataPoints'
  tickPlacement: 'between',  // 'on', 'between'
  
  min: undefined,
  max: undefined,
  
  crosshairs: {
    show: true,
    position: 'back',
    stroke: { color: '#b6b6b6', width: 1, dashArray: 0 }
  },
  
  tooltip: { enabled: true }
}
```

### Y-Axis

```javascript
yaxis: {
  show: true,
  opposite: false,  // Right side
  
  title: {
    text: 'Y Axis Title',
    rotate: -90,
    style: { fontSize: '14px' }
  },
  
  labels: {
    show: true,
    align: 'right',
    minWidth: 0,
    maxWidth: 160,
    style: { fontSize: '12px' },
    formatter: (val) => val.toFixed(0)
  },
  
  min: 0,
  max: 100,
  tickAmount: 6,
  forceNiceScale: true,
  floating: false,
  
  decimalsInFloat: 2,
  logarithmic: false,
  
  axisBorder: { show: true },
  axisTicks: { show: true },
  
  crosshairs: { show: true },
  tooltip: { enabled: true }
}

// Multiple Y-Axes
yaxis: [
  {
    seriesName: 'Revenue',
    title: { text: 'Revenue ($)' },
    min: 0,
    max: 1000
  },
  {
    opposite: true,
    seriesName: 'Profit',
    title: { text: 'Profit (%)' },
    min: 0,
    max: 100
  }
]
```

---

## Data Labels

```javascript
dataLabels: {
  enabled: true,
  enabledOnSeries: [0, 1],  // Only specific series
  
  formatter: (val, opts) => {
    return val + '%'
  },
  
  textAnchor: 'middle',
  distributed: false,
  offsetX: 0,
  offsetY: 0,
  
  style: {
    fontSize: '12px',
    fontFamily: 'Inter, sans-serif',
    fontWeight: 'bold',
    colors: undefined  // Uses series colors
  },
  
  background: {
    enabled: true,
    foreColor: '#fff',
    padding: 4,
    borderRadius: 2,
    borderWidth: 1,
    borderColor: '#fff',
    opacity: 0.9
  },
  
  dropShadow: {
    enabled: false,
    top: 1,
    left: 1,
    blur: 1,
    color: '#000',
    opacity: 0.45
  }
}
```

---

## Legend

```javascript
legend: {
  show: true,
  showForSingleSeries: false,
  showForNullSeries: true,
  showForZeroSeries: true,
  
  position: 'bottom',  // 'top', 'bottom', 'left', 'right'
  horizontalAlign: 'center',  // 'left', 'center', 'right'
  floating: false,
  
  fontSize: '14px',
  fontFamily: 'Inter, sans-serif',
  fontWeight: 400,
  
  offsetX: 0,
  offsetY: 0,
  
  labels: {
    colors: undefined,
    useSeriesColors: false
  },
  
  markers: {
    width: 12,
    height: 12,
    strokeWidth: 0,
    strokeColor: '#fff',
    radius: 12,
    customHTML: undefined,
    onClick: undefined,
    offsetX: 0,
    offsetY: 0
  },
  
  itemMargin: {
    horizontal: 5,
    vertical: 0
  },
  
  onItemClick: { toggleDataSeries: true },
  onItemHover: { highlightDataSeries: true }
}
```

---

## Tooltip

```javascript
tooltip: {
  enabled: true,
  shared: true,
  followCursor: false,
  intersect: false,
  inverseOrder: false,
  
  custom: undefined,  // Custom HTML function
  
  fillSeriesColor: false,
  theme: 'light',  // 'light', 'dark'
  
  style: {
    fontSize: '12px',
    fontFamily: 'Inter, sans-serif'
  },
  
  onDatasetHover: { highlightDataSeries: false },
  
  x: {
    show: true,
    format: 'dd MMM',
    formatter: undefined
  },
  
  y: {
    formatter: (val) => val + ' units',
    title: {
      formatter: (seriesName) => seriesName + ':'
    }
  },
  
  z: {
    formatter: undefined,
    title: 'Size: '
  },
  
  marker: { show: true },
  
  fixed: {
    enabled: false,
    position: 'topRight',
    offsetX: 0,
    offsetY: 0
  }
}

// Custom Tooltip
tooltip: {
  custom: function({ series, seriesIndex, dataPointIndex, w }) {
    return '<div class="tooltip">' +
      '<span>' + w.globals.labels[dataPointIndex] + '</span>' +
      '<strong>' + series[seriesIndex][dataPointIndex] + '</strong>' +
      '</div>'
  }
}
```

---

## Grid

```javascript
grid: {
  show: true,
  borderColor: '#e0e0e0',
  strokeDashArray: 0,
  position: 'back',
  
  xaxis: { lines: { show: false } },
  yaxis: { lines: { show: true } },
  
  row: {
    colors: undefined,  // ['#f3f3f3', 'transparent']
    opacity: 0.5
  },
  
  column: {
    colors: undefined,
    opacity: 0.5
  },
  
  padding: {
    top: 0,
    right: 0,
    bottom: 0,
    left: 0
  }
}
```

---

## Stroke

```javascript
stroke: {
  show: true,
  curve: 'smooth',  // 'smooth', 'straight', 'stepline'
  lineCap: 'butt',  // 'butt', 'square', 'round'
  colors: undefined,
  width: 2,
  dashArray: 0  // Or [0, 5, 10] for dashed
}
```

---

## Fill

```javascript
fill: {
  type: 'solid',  // 'solid', 'gradient', 'pattern', 'image'
  colors: undefined,
  opacity: 1,
  
  gradient: {
    shade: 'dark',
    type: 'vertical',  // 'horizontal', 'vertical', 'diagonal1', 'diagonal2'
    shadeIntensity: 0.5,
    gradientToColors: undefined,
    inverseColors: true,
    opacityFrom: 1,
    opacityTo: 1,
    stops: [0, 50, 100]
  },
  
  pattern: {
    style: 'verticalLines',  // 'circles', 'squares', 'slantedLines', etc.
    width: 6,
    height: 6,
    strokeWidth: 2
  },
  
  image: {
    src: ['image1.png', 'image2.png'],
    width: undefined,
    height: undefined
  }
}
```

---

## Markers

```javascript
markers: {
  size: 0,  // 0 to hide
  colors: undefined,
  strokeColors: '#fff',
  strokeWidth: 2,
  strokeOpacity: 0.9,
  strokeDashArray: 0,
  fillOpacity: 1,
  discrete: [],
  shape: 'circle',  // 'circle', 'square', 'rect'
  radius: 2,
  offsetX: 0,
  offsetY: 0,
  
  onClick: undefined,
  onDblClick: undefined,
  
  showNullDataPoints: true,
  
  hover: {
    size: undefined,
    sizeOffset: 3
  }
}
```

---

## Annotations

```javascript
annotations: {
  position: 'front',
  
  yaxis: [{
    y: 50,
    y2: null,  // For range
    strokeDashArray: 0,
    borderColor: '#c2c2c2',
    fillColor: '#c2c2c2',
    opacity: 0.3,
    offsetX: 0,
    offsetY: 0,
    label: {
      borderColor: '#c2c2c2',
      borderWidth: 1,
      text: 'Target',
      textAnchor: 'end',
      position: 'right',
      offsetX: 0,
      offsetY: 0,
      style: { background: '#fff', color: '#777', fontSize: '11px' }
    }
  }],
  
  xaxis: [{
    x: 'Feb',  // Or timestamp
    x2: null,
    strokeDashArray: 0,
    borderColor: '#c2c2c2',
    fillColor: '#c2c2c2',
    opacity: 0.3,
    label: { text: 'Event' }
  }],
  
  points: [{
    x: 'Mar',
    y: 45,
    marker: {
      size: 8,
      fillColor: '#fff',
      strokeColor: '#FF4560',
      strokeWidth: 3,
      shape: 'circle',
      radius: 2
    },
    label: { text: 'Point Label' }
  }]
}
```

---

## Responsive

```javascript
responsive: [
  {
    breakpoint: 768,  // Below this width
    options: {
      chart: { height: 300 },
      legend: { position: 'bottom' },
      plotOptions: {
        bar: { horizontal: true }
      }
    }
  },
  {
    breakpoint: 480,
    options: {
      chart: { height: 250 },
      legend: { show: false }
    }
  }
]
```

---

## Title & Subtitle

```javascript
title: {
  text: 'Chart Title',
  align: 'center',  // 'left', 'center', 'right'
  margin: 10,
  offsetX: 0,
  offsetY: 0,
  floating: false,
  style: {
    fontSize: '16px',
    fontWeight: 'bold',
    fontFamily: 'Inter, sans-serif',
    color: '#263238'
  }
},

subtitle: {
  text: 'Subtitle text',
  align: 'center',
  margin: 10,
  offsetX: 0,
  offsetY: 30,
  floating: false,
  style: {
    fontSize: '12px',
    fontWeight: 'normal',
    fontFamily: 'Inter, sans-serif',
    color: '#9699a2'
  }
}
```

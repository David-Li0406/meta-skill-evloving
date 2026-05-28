# Circular Charts

Non-axis charts: Pie, Donut, RadialBar, PolarArea.

## Table of Contents
- [Pie Chart](#pie-chart)
- [Donut Chart](#donut-chart)
- [RadialBar / Gauge](#radialbar--gauge)
- [PolarArea Chart](#polararea-chart)

---

## Pie Chart

Best for: Part-of-whole relationships with few categories (3-7 recommended).

### Basic Pie

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'pie' },
  labels: ['Desktop', 'Mobile', 'Tablet'],
  legend: { position: 'bottom' }
})

const series = ref([44, 55, 13])
</script>

<template>
  <apexchart type="pie" width="380" :options="options" :series="series" />
</template>
```

### Pie with XY Data (v5.3+)

```javascript
// Alternative format - self-contained
series: [{
  data: [
    { x: 'Desktop', y: 44 },
    { x: 'Mobile', y: 55 },
    { x: 'Tablet', y: 13 }
  ]
}]
// No separate labels needed
```

### Pie with Data Labels

```javascript
dataLabels: {
  enabled: true,
  formatter: function (val, opts) {
    return opts.w.config.labels[opts.seriesIndex] + ': ' + val.toFixed(1) + '%'
  }
},
plotOptions: {
  pie: {
    dataLabels: {
      offset: -5
    }
  }
}
```

### Pie with Custom Colors

```javascript
colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560', '#775DD0']
```

### Monochrome Pie

```javascript
theme: {
  monochrome: {
    enabled: true,
    color: '#008FFB',
    shadeTo: 'light',
    shadeIntensity: 0.6
  }
}
```

### Pie with Patterns

```javascript
fill: {
  type: 'pattern',
  pattern: {
    style: ['verticalLines', 'horizontalLines', 'slantedLines']
  }
}
```

---

## Donut Chart

Best for: Part-of-whole with center metric display.

### Basic Donut

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'donut' },
  labels: ['Direct', 'Organic', 'Referral', 'Social'],
  plotOptions: {
    pie: {
      donut: {
        size: '65%'
      }
    }
  }
})

const series = ref([44, 55, 41, 17])
</script>

<template>
  <apexchart type="donut" width="380" :options="options" :series="series" />
</template>
```

### Donut with Center Label

```javascript
plotOptions: {
  pie: {
    donut: {
      size: '70%',
      labels: {
        show: true,
        name: {
          show: true,
          fontSize: '16px',
          fontWeight: 600
        },
        value: {
          show: true,
          fontSize: '24px',
          fontWeight: 700,
          formatter: (val) => val
        },
        total: {
          show: true,
          label: 'Total',
          fontSize: '12px',
          formatter: (w) => {
            return w.globals.seriesTotals.reduce((a, b) => a + b, 0)
          }
        }
      }
    }
  }
}
```

### Semi-Donut (Half Circle)

```javascript
plotOptions: {
  pie: {
    startAngle: -90,
    endAngle: 90,
    donut: {
      size: '75%'
    }
  }
},
grid: {
  padding: { bottom: -80 }
}
```

### Gradient Donut

```javascript
fill: {
  type: 'gradient'
},
colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560']
```

---

## RadialBar / Gauge

Best for: Progress indicators, single metrics, KPIs.

### Basic RadialBar

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'radialBar' },
  plotOptions: {
    radialBar: {
      hollow: { size: '70%' }
    }
  },
  labels: ['Progress']
})

const series = ref([70])  // Percentage value
</script>

<template>
  <apexchart type="radialBar" height="350" :options="options" :series="series" />
</template>
```

### Multiple RadialBars

```javascript
options: {
  chart: { type: 'radialBar' },
  plotOptions: {
    radialBar: {
      dataLabels: {
        name: { fontSize: '14px' },
        value: { fontSize: '20px' },
        total: {
          show: true,
          label: 'Total',
          formatter: () => '249'
        }
      }
    }
  },
  labels: ['Apples', 'Oranges', 'Bananas', 'Berries']
},
series: [44, 55, 67, 83]
```

### Gradient RadialBar

```javascript
fill: {
  type: 'gradient',
  gradient: {
    shade: 'dark',
    type: 'horizontal',
    shadeIntensity: 0.5,
    gradientToColors: ['#ABE5A1'],
    inverseColors: true,
    opacityFrom: 1,
    opacityTo: 1,
    stops: [0, 100]
  }
}
```

### Stroked Gauge

```javascript
plotOptions: {
  radialBar: {
    startAngle: -135,
    endAngle: 135,
    hollow: {
      margin: 0,
      size: '70%',
      background: '#fff'
    },
    track: {
      background: '#e7e7e7',
      strokeWidth: '67%',
      margin: 0
    },
    dataLabels: {
      show: true,
      name: {
        offsetY: -10,
        show: true,
        color: '#888',
        fontSize: '14px'
      },
      value: {
        formatter: (val) => parseInt(val) + '%',
        color: '#111',
        fontSize: '30px',
        show: true
      }
    }
  }
}
```

### Semi-Circle Gauge

```javascript
plotOptions: {
  radialBar: {
    startAngle: -90,
    endAngle: 90,
    track: {
      background: '#e7e7e7',
      strokeWidth: '97%',
      margin: 5
    },
    dataLabels: {
      name: { show: false },
      value: {
        offsetY: -2,
        fontSize: '22px'
      }
    }
  }
},
grid: {
  padding: { top: -10 }
},
fill: {
  type: 'gradient',
  gradient: {
    shade: 'light',
    shadeIntensity: 0.4,
    inverseColors: false,
    opacityFrom: 1,
    opacityTo: 1,
    stops: [0, 50, 53, 91]
  }
}
```

---

## PolarArea Chart

Best for: Comparing categories with varying magnitudes in circular form.

### Basic PolarArea

```vue
<script setup>
import { ref } from 'vue'

const options = ref({
  chart: { type: 'polarArea' },
  labels: ['Rose A', 'Rose B', 'Rose C', 'Rose D', 'Rose E'],
  fill: { opacity: 0.8 },
  stroke: { width: 1, colors: undefined },
  yaxis: { show: false },
  legend: { position: 'bottom' },
  plotOptions: {
    polarArea: {
      rings: { strokeWidth: 0 },
      spokes: { strokeWidth: 0 }
    }
  }
})

const series = ref([14, 23, 21, 17, 15])
</script>

<template>
  <apexchart type="polarArea" width="380" :options="options" :series="series" />
</template>
```

### PolarArea with Monochrome

```javascript
theme: {
  monochrome: {
    enabled: true,
    shadeTo: 'light',
    shadeIntensity: 0.6
  }
}
```

### PolarArea Customization

```javascript
plotOptions: {
  polarArea: {
    rings: {
      strokeWidth: 1,
      strokeColor: '#e8e8e8'
    },
    spokes: {
      strokeWidth: 1,
      connectorColors: '#e8e8e8'
    }
  }
},
fill: {
  opacity: 0.8
},
responsive: [{
  breakpoint: 480,
  options: {
    chart: { width: 200 },
    legend: { position: 'bottom' }
  }
}]
```

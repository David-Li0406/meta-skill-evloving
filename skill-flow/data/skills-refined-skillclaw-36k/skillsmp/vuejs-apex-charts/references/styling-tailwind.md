# Styling & Tailwind CSS

Tailwind CSS integration, themes, colors, and dark mode.

## Table of Contents
- [Tailwind Integration](#tailwind-integration)
- [Chart Container Styling](#chart-container-styling)
- [Color Customization](#color-customization)
- [Dark Mode](#dark-mode)
- [Themes](#themes)
- [Custom Tooltip](#custom-tooltip)
- [Responsive Design](#responsive-design)
- [Dashboard Layouts](#dashboard-layouts)

---

## Tailwind Integration

### Basic Chart with Tailwind Container

```vue
<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
    <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
      Sales Overview
    </h3>
    <apexchart 
      type="line" 
      height="350" 
      :options="options" 
      :series="series" 
    />
  </div>
</template>
```

### Chart Card Component

```vue
<script setup>
defineProps({
  title: String,
  subtitle: String,
  type: { type: String, default: 'line' },
  options: Object,
  series: Array,
  height: { type: [String, Number], default: 350 }
})
</script>

<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
    <!-- Header -->
    <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        {{ title }}
      </h3>
      <p v-if="subtitle" class="text-sm text-gray-500 dark:text-gray-400">
        {{ subtitle }}
      </p>
    </div>
    
    <!-- Chart -->
    <div class="p-4">
      <apexchart 
        :type="type" 
        :height="height" 
        :options="options" 
        :series="series" 
      />
    </div>
  </div>
</template>
```

---

## Chart Container Styling

### Responsive Container

```vue
<template>
  <div class="w-full max-w-4xl mx-auto">
    <div class="aspect-[16/9] sm:aspect-[2/1] lg:aspect-[3/1]">
      <apexchart 
        type="area" 
        height="100%" 
        :options="options" 
        :series="series" 
      />
    </div>
  </div>
</template>
```

### Loading State

```vue
<template>
  <div class="relative bg-white dark:bg-gray-800 rounded-lg p-4 min-h-[350px]">
    <!-- Loading overlay -->
    <div 
      v-if="loading" 
      class="absolute inset-0 bg-white/80 dark:bg-gray-800/80 
             flex items-center justify-center z-10 rounded-lg"
    >
      <div class="flex flex-col items-center gap-2">
        <div class="w-8 h-8 border-4 border-blue-500 border-t-transparent 
                    rounded-full animate-spin"></div>
        <span class="text-sm text-gray-500">Loading chart...</span>
      </div>
    </div>
    
    <apexchart :options="options" :series="series" />
  </div>
</template>
```

---

## Color Customization

### Tailwind Color Palette

```javascript
// Use Tailwind colors in chart
const tailwindColors = {
  blue: '#3B82F6',
  green: '#10B981',
  yellow: '#F59E0B',
  red: '#EF4444',
  purple: '#8B5CF6',
  pink: '#EC4899',
  indigo: '#6366F1',
  teal: '#14B8A6',
  orange: '#F97316',
  cyan: '#06B6D4'
}

const options = ref({
  colors: [
    tailwindColors.blue,
    tailwindColors.green,
    tailwindColors.yellow,
    tailwindColors.red
  ]
})
```

### Dynamic Colors from CSS Variables

```javascript
// In tailwind.config.js - define CSS variables
// Or use computed style

const options = ref({
  colors: [
    getComputedStyle(document.documentElement)
      .getPropertyValue('--color-primary').trim(),
    getComputedStyle(document.documentElement)
      .getPropertyValue('--color-secondary').trim()
  ]
})
```

### Gradient with Tailwind Colors

```javascript
fill: {
  type: 'gradient',
  gradient: {
    shadeIntensity: 1,
    opacityFrom: 0.7,
    opacityTo: 0.2,
    stops: [0, 90, 100],
    colorStops: [
      { offset: 0, color: '#3B82F6', opacity: 0.7 },   // blue-500
      { offset: 100, color: '#3B82F6', opacity: 0.1 }
    ]
  }
}
```

---

## Dark Mode

### Dark Mode Options

```vue
<script setup>
import { ref, computed, watch } from 'vue'

// Detect dark mode (Tailwind's dark class or media query)
const isDark = ref(document.documentElement.classList.contains('dark'))

// Watch for changes
const observer = new MutationObserver(() => {
  isDark.value = document.documentElement.classList.contains('dark')
})
observer.observe(document.documentElement, { attributes: true })

const options = computed(() => ({
  chart: {
    type: 'line',
    background: 'transparent',
    foreColor: isDark.value ? '#9CA3AF' : '#374151'  // gray-400 / gray-700
  },
  grid: {
    borderColor: isDark.value ? '#374151' : '#E5E7EB'  // gray-700 / gray-200
  },
  xaxis: {
    labels: {
      style: { colors: isDark.value ? '#9CA3AF' : '#6B7280' }
    },
    axisBorder: { color: isDark.value ? '#4B5563' : '#D1D5DB' },
    axisTicks: { color: isDark.value ? '#4B5563' : '#D1D5DB' }
  },
  yaxis: {
    labels: {
      style: { colors: isDark.value ? '#9CA3AF' : '#6B7280' }
    }
  },
  tooltip: {
    theme: isDark.value ? 'dark' : 'light'
  },
  legend: {
    labels: { colors: isDark.value ? '#D1D5DB' : '#374151' }
  }
}))
</script>

<template>
  <div class="bg-white dark:bg-gray-900 rounded-lg p-4">
    <apexchart type="line" :options="options" :series="series" />
  </div>
</template>
```

### Dark Mode Composable

```javascript
// composables/useChartTheme.js
import { ref, computed, onMounted, onUnmounted } from 'vue'

export function useChartTheme() {
  const isDark = ref(false)
  let observer = null
  
  onMounted(() => {
    isDark.value = document.documentElement.classList.contains('dark')
    
    observer = new MutationObserver(() => {
      isDark.value = document.documentElement.classList.contains('dark')
    })
    observer.observe(document.documentElement, { 
      attributes: true, 
      attributeFilter: ['class'] 
    })
  })
  
  onUnmounted(() => {
    if (observer) observer.disconnect()
  })
  
  const chartTheme = computed(() => ({
    chart: {
      background: 'transparent',
      foreColor: isDark.value ? '#9CA3AF' : '#374151'
    },
    grid: {
      borderColor: isDark.value ? '#374151' : '#E5E7EB'
    },
    tooltip: { theme: isDark.value ? 'dark' : 'light' }
  }))
  
  return { isDark, chartTheme }
}
```

---

## Themes

### Built-in Themes

```javascript
theme: {
  mode: 'light',  // 'light', 'dark'
  palette: 'palette1',  // palette1-10
  monochrome: {
    enabled: false,
    color: '#255aee',
    shadeTo: 'light',
    shadeIntensity: 0.65
  }
}
```

### Custom Theme

```javascript
const customTheme = {
  chart: {
    fontFamily: 'Inter, sans-serif',
    foreColor: '#64748B'  // slate-500
  },
  colors: ['#0EA5E9', '#22C55E', '#F59E0B', '#EF4444', '#8B5CF6'],
  stroke: { colors: ['transparent'] },
  dataLabels: {
    style: { colors: ['#fff'] }
  },
  grid: {
    borderColor: '#E2E8F0'  // slate-200
  },
  xaxis: {
    axisBorder: { color: '#CBD5E1' },
    axisTicks: { color: '#CBD5E1' },
    labels: { style: { colors: '#64748B' } }
  },
  yaxis: {
    labels: { style: { colors: '#64748B' } }
  },
  legend: {
    labels: { colors: '#475569' }
  },
  tooltip: {
    theme: 'light',
    style: { fontSize: '12px' }
  }
}
```

---

## Custom Tooltip

### Tailwind-styled Tooltip

```javascript
tooltip: {
  custom: function({ series, seriesIndex, dataPointIndex, w }) {
    const value = series[seriesIndex][dataPointIndex]
    const label = w.globals.labels[dataPointIndex]
    const seriesName = w.globals.seriesNames[seriesIndex]
    
    return `
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg 
                  border border-gray-200 dark:border-gray-700 p-3">
        <div class="text-xs text-gray-500 dark:text-gray-400 mb-1">
          ${label}
        </div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full" 
                style="background-color: ${w.globals.colors[seriesIndex]}">
          </span>
          <span class="text-sm font-medium text-gray-900 dark:text-white">
            ${seriesName}: ${value.toLocaleString()}
          </span>
        </div>
      </div>
    `
  }
}
```

### Multi-series Tooltip

```javascript
tooltip: {
  shared: true,
  custom: function({ series, dataPointIndex, w }) {
    const label = w.globals.labels[dataPointIndex]
    
    let content = `
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl 
                  border border-gray-200 dark:border-gray-700 p-4 min-w-[180px]">
        <div class="text-sm font-semibold text-gray-900 dark:text-white mb-2 
                    pb-2 border-b border-gray-200 dark:border-gray-700">
          ${label}
        </div>
    `
    
    series.forEach((s, i) => {
      if (s[dataPointIndex] !== undefined) {
        content += `
          <div class="flex items-center justify-between py-1">
            <div class="flex items-center gap-2">
              <span class="w-2 h-2 rounded-full" 
                    style="background-color: ${w.globals.colors[i]}"></span>
              <span class="text-sm text-gray-600 dark:text-gray-300">
                ${w.globals.seriesNames[i]}
              </span>
            </div>
            <span class="text-sm font-medium text-gray-900 dark:text-white">
              ${s[dataPointIndex].toLocaleString()}
            </span>
          </div>
        `
      }
    })
    
    content += '</div>'
    return content
  }
}
```

---

## Responsive Design

### Responsive Chart Options

```javascript
responsive: [
  {
    breakpoint: 1024,  // lg
    options: {
      chart: { height: 300 },
      legend: { position: 'bottom' }
    }
  },
  {
    breakpoint: 768,   // md
    options: {
      chart: { height: 280 },
      plotOptions: { bar: { horizontal: true } },
      xaxis: { labels: { rotate: -45 } }
    }
  },
  {
    breakpoint: 480,   // sm
    options: {
      chart: { height: 250 },
      legend: { show: false },
      dataLabels: { enabled: false }
    }
  }
]
```

---

## Dashboard Layouts

### Grid Dashboard

```vue
<template>
  <div class="p-4 bg-gray-100 dark:bg-gray-900 min-h-screen">
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      <!-- Main Chart -->
      <div class="md:col-span-2 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
        <h3 class="text-lg font-semibold mb-4">Revenue Trend</h3>
        <apexchart type="area" height="300" :options="areaOptions" :series="areaSeries" />
      </div>
      
      <!-- Side Chart -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
        <h3 class="text-lg font-semibold mb-4">Distribution</h3>
        <apexchart type="donut" height="300" :options="donutOptions" :series="donutSeries" />
      </div>
      
      <!-- Stat Cards -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4">
        <div class="flex justify-between items-start mb-2">
          <span class="text-sm text-gray-500">Total Sales</span>
          <span class="text-green-500 text-sm">+12%</span>
        </div>
        <div class="text-2xl font-bold mb-2">$24,500</div>
        <apexchart type="line" height="60" :options="sparkOptions" :series="sparkSeries" />
      </div>
    </div>
  </div>
</template>
```

### Sparkline for KPI Cards

```javascript
const sparkOptions = ref({
  chart: {
    type: 'line',
    sparkline: { enabled: true }
  },
  stroke: { curve: 'smooth', width: 2 },
  colors: ['#10B981'],
  tooltip: { enabled: false }
})

const sparkSeries = ref([{ data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54] }])
```

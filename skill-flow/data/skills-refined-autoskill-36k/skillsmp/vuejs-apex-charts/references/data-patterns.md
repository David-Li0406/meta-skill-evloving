# Data Patterns

API integration, real-time updates, and datetime handling.

## Table of Contents
- [API Integration](#api-integration)
- [Real-time Updates](#real-time-updates)
- [Datetime Handling](#datetime-handling)
- [Data Transformation](#data-transformation)
- [No Data States](#no-data-states)

---

## API Integration

### Fetch Data on Mount

```vue
<script setup>
import { ref, onMounted } from 'vue'

const options = ref({
  chart: { type: 'bar' },
  noData: { text: 'Loading...' }
})
const series = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await fetch('/api/sales-data')
    const data = await response.json()
    
    // Transform API data to series format
    series.value = [{
      name: 'Sales',
      data: data.map(item => ({
        x: item.month,
        y: item.value
      }))
    }]
  } catch (error) {
    console.error('Failed to fetch data:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <apexchart 
    type="bar" 
    height="350" 
    :options="options" 
    :series="series" 
  />
</template>
```

### Fetch with Axios

```vue
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const chartRef = ref(null)
const options = ref({
  chart: { id: 'api-chart', type: 'line' },
  xaxis: { type: 'datetime' },
  noData: { text: 'Loading...' }
})
const series = ref([])

async function fetchData() {
  const { data } = await axios.get('/api/timeseries')
  
  series.value = [{
    name: 'Values',
    data: data.map(item => [
      new Date(item.date).getTime(),
      item.value
    ])
  }]
}

onMounted(() => fetchData())
</script>
```

### Periodic Refresh

```vue
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const series = ref([{ name: 'Data', data: [] }])
let intervalId = null

async function fetchLatestData() {
  const response = await fetch('/api/latest')
  const data = await response.json()
  series.value = [{ name: 'Data', data }]
}

onMounted(() => {
  fetchLatestData()
  intervalId = setInterval(fetchLatestData, 30000) // Every 30 seconds
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})
</script>
```

---

## Real-time Updates

### Streaming Data (Append)

```vue
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const chartRef = ref(null)
const MAX_POINTS = 50

const options = ref({
  chart: {
    id: 'realtime',
    type: 'line',
    animations: {
      enabled: true,
      easing: 'linear',
      dynamicAnimation: { speed: 1000 }
    }
  },
  xaxis: { type: 'datetime', range: 60000 },  // Show last 60 seconds
  stroke: { curve: 'smooth', width: 2 }
})

const series = ref([{
  name: 'Value',
  data: []
}])

function addDataPoint() {
  const now = Date.now()
  const newValue = Math.floor(Math.random() * 100)
  
  // Add new point
  series.value[0].data.push({ x: now, y: newValue })
  
  // Remove old points to prevent memory issues
  if (series.value[0].data.length > MAX_POINTS) {
    series.value[0].data.shift()
  }
}

let intervalId = null

onMounted(() => {
  // Initialize with some data
  const now = Date.now()
  for (let i = 10; i > 0; i--) {
    series.value[0].data.push({
      x: now - i * 1000,
      y: Math.floor(Math.random() * 100)
    })
  }
  
  // Start streaming
  intervalId = setInterval(addDataPoint, 1000)
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})
</script>

<template>
  <apexchart
    ref="chartRef"
    type="line"
    height="350"
    :options="options"
    :series="series"
  />
</template>
```

### WebSocket Integration

```vue
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const series = ref([{ name: 'Price', data: [] }])
let socket = null

onMounted(() => {
  socket = new WebSocket('wss://api.example.com/realtime')
  
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    
    series.value[0].data.push({
      x: data.timestamp,
      y: data.price
    })
    
    // Keep last 100 points
    if (series.value[0].data.length > 100) {
      series.value[0].data = series.value[0].data.slice(-100)
    }
  }
  
  socket.onerror = (error) => {
    console.error('WebSocket error:', error)
  }
})

onUnmounted(() => {
  if (socket) socket.close()
})
</script>
```

### Optimized Updates with appendData

```javascript
// More efficient for real-time - doesn't replace entire series
function addPoint(value) {
  chartRef.value.chart.appendData([{
    data: [{ x: Date.now(), y: value }]
  }])
}
```

---

## Datetime Handling

### Datetime X-Axis Setup

```javascript
const options = ref({
  xaxis: {
    type: 'datetime',
    labels: {
      datetimeUTC: false,  // Use local timezone
      datetimeFormatter: {
        year: 'yyyy',
        month: "MMM 'yy",
        day: 'dd MMM',
        hour: 'HH:mm'
      }
    }
  },
  tooltip: {
    x: { format: 'dd MMM yyyy HH:mm' }
  }
})
```

### Date Formats

```javascript
// Timestamps (recommended)
series: [{
  data: [
    { x: 1704067200000, y: 30 },  // Jan 1, 2024
    { x: 1704153600000, y: 40 }   // Jan 2, 2024
  ]
}]

// Date objects
series: [{
  data: [
    { x: new Date('2024-01-01').getTime(), y: 30 },
    { x: new Date('2024-01-02').getTime(), y: 40 }
  ]
}]

// ISO strings (parsed automatically)
series: [{
  data: [
    { x: '2024-01-01', y: 30 },
    { x: '2024-01-02', y: 40 }
  ]
}]
```

### Timezone Handling

```javascript
// Convert to local time for display
function toLocalTime(utcTimestamp) {
  return new Date(utcTimestamp).getTime()
}

// Format in specific timezone
xaxis: {
  labels: {
    formatter: (value, timestamp) => {
      return new Date(timestamp).toLocaleString('en-US', {
        timeZone: 'America/New_York',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
```

### Date Range Filtering

```vue
<script setup>
import { ref, computed } from 'vue'

const rawData = ref([/* all data */])
const startDate = ref(null)
const endDate = ref(null)

const filteredSeries = computed(() => {
  let data = rawData.value
  
  if (startDate.value) {
    data = data.filter(d => d.x >= startDate.value.getTime())
  }
  if (endDate.value) {
    data = data.filter(d => d.x <= endDate.value.getTime())
  }
  
  return [{ name: 'Values', data }]
})
</script>
```

---

## Data Transformation

### API Response to Chart Data

```javascript
// API returns: [{ date: '2024-01-01', revenue: 100, profit: 50 }, ...]

function transformToSeries(apiData) {
  return [
    {
      name: 'Revenue',
      data: apiData.map(item => ({
        x: new Date(item.date).getTime(),
        y: item.revenue
      }))
    },
    {
      name: 'Profit',
      data: apiData.map(item => ({
        x: new Date(item.date).getTime(),
        y: item.profit
      }))
    }
  ]
}
```

### Aggregating Data

```javascript
// Daily data to monthly
function aggregateMonthly(dailyData) {
  const monthlyMap = new Map()
  
  dailyData.forEach(item => {
    const date = new Date(item.x)
    const monthKey = `${date.getFullYear()}-${date.getMonth()}`
    
    if (!monthlyMap.has(monthKey)) {
      monthlyMap.set(monthKey, { sum: 0, count: 0, firstDate: date })
    }
    
    const entry = monthlyMap.get(monthKey)
    entry.sum += item.y
    entry.count++
  })
  
  return Array.from(monthlyMap.values()).map(entry => ({
    x: entry.firstDate.getTime(),
    y: entry.sum / entry.count  // Average
  }))
}
```

### Percentage Calculation

```javascript
// Convert values to percentages
function toPercentages(series) {
  const total = series.reduce((sum, item) => sum + item.y, 0)
  return series.map(item => ({
    ...item,
    y: ((item.y / total) * 100).toFixed(1)
  }))
}
```

### Cumulative Sum

```javascript
// Running total
function toCumulative(data) {
  let cumulative = 0
  return data.map(item => ({
    x: item.x,
    y: cumulative += item.y
  }))
}
```

---

## No Data States

### Loading State

```javascript
const options = ref({
  noData: {
    text: 'Loading...',
    align: 'center',
    verticalAlign: 'middle',
    offsetX: 0,
    offsetY: 0,
    style: {
      color: '#888',
      fontSize: '14px',
      fontFamily: 'Inter, sans-serif'
    }
  }
})

// Start with empty series
const series = ref([])

// Update when data arrives
async function loadData() {
  const data = await fetchData()
  series.value = [{ name: 'Data', data }]
}
```

### Error State

```vue
<script setup>
import { ref, onMounted } from 'vue'

const series = ref([])
const error = ref(null)

const options = computed(() => ({
  noData: {
    text: error.value ? 'Failed to load data' : 'Loading...'
  }
}))

onMounted(async () => {
  try {
    const data = await fetchData()
    series.value = [{ name: 'Data', data }]
  } catch (e) {
    error.value = e.message
  }
})
</script>

<template>
  <div v-if="error" class="error-message">
    {{ error }}
    <button @click="retry">Retry</button>
  </div>
  <apexchart v-else type="line" :options="options" :series="series" />
</template>
```

### Empty Data Message

```javascript
noData: {
  text: 'No data available for the selected period',
  align: 'center',
  verticalAlign: 'middle',
  style: {
    color: '#999',
    fontSize: '16px'
  }
}
```

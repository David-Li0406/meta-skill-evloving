<template>
  <div class="token-trend-chart">
    <div class="chart-header">
      <h3>{{ title }}</h3>
      <div class="chart-legend">
        <span class="legend-item">
          <span class="legend-color" style="background: var(--chart-primary, #00D9FF);"></span>
          Tokens per bucket
        </span>
        <span class="legend-item">
          <span class="legend-color" style="background: var(--theme-primary, #BBA0FF);"></span>
          Cumulative
        </span>
      </div>
    </div>

    <div v-if="hasData" class="chart-container">
      <svg ref="svgRef" :viewBox="`0 0 ${width} ${height}`" preserveAspectRatio="xMidYMid meet">
        <!-- Grid lines -->
        <g class="grid">
          <line
            v-for="i in 5"
            :key="`h-grid-${i}`"
            :x1="padding.left"
            :y1="padding.top + ((chartHeight / 4) * (i - 1))"
            :x2="width - padding.right"
            :y2="padding.top + ((chartHeight / 4) * (i - 1))"
            class="grid-line"
          />
        </g>

        <!-- Y-axis labels -->
        <g class="y-axis">
          <text
            v-for="(label, i) in yLabels"
            :key="`y-label-${i}`"
            :x="padding.left - 10"
            :y="padding.top + ((chartHeight / 4) * i)"
            class="axis-label"
            text-anchor="end"
            dominant-baseline="middle"
          >
            {{ label }}
          </text>
        </g>

        <!-- X-axis labels -->
        <g class="x-axis">
          <text
            v-for="(label, i) in xLabels"
            :key="`x-label-${i}`"
            :x="padding.left + ((chartWidth / (xLabels.length - 1)) * i)"
            :y="height - padding.bottom + 20"
            class="axis-label"
            text-anchor="middle"
          >
            {{ label }}
          </text>
        </g>

        <!-- Token bars -->
        <g class="bars">
          <rect
            v-for="(point, i) in chartData"
            :key="`bar-${i}`"
            :x="point.barX"
            :y="point.barY"
            :width="point.barWidth"
            :height="point.barHeight"
            class="bar"
            @mouseenter="onHover(point, i)"
            @mouseleave="onLeave"
          />
        </g>

        <!-- Cumulative line -->
        <g class="lines">
          <path
            :d="cumulativePath"
            class="line-cumulative"
            fill="none"
          />
          <circle
            v-for="(point, i) in chartData"
            :key="`dot-${i}`"
            :cx="point.x"
            :cy="point.cumulativeY"
            r="4"
            class="dot"
            @mouseenter="onHover(point, i)"
            @mouseleave="onLeave"
          />
        </g>
      </svg>

      <!-- Tooltip -->
      <div
        v-if="tooltip"
        class="tooltip"
        :style="{
          left: tooltip.x + 'px',
          top: tooltip.y + 'px'
        }"
      >
        <div class="tooltip-time">{{ tooltip.time }}</div>
        <div class="tooltip-row">
          <span class="tooltip-label">Tokens:</span>
          <span class="tooltip-value">{{ tooltip.tokens }}</span>
        </div>
        <div class="tooltip-row">
          <span class="tooltip-label">Cumulative:</span>
          <span class="tooltip-value">{{ tooltip.cumulative }}</span>
        </div>
        <div v-if="tooltip.cost" class="tooltip-row">
          <span class="tooltip-label">Cost:</span>
          <span class="tooltip-value">${{ tooltip.cost.toFixed(4) }}</span>
        </div>
      </div>
    </div>

    <div v-else class="no-data">
      <p>No token data available</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { TokenTrendPoint } from '../services/metricsCalculator';

const props = withDefaults(
  defineProps<{
    data: TokenTrendPoint[];
    title?: string;
    width?: number;
    height?: number;
  }>(),
  {
    title: 'Token Usage Over Time',
    width: 800,
    height: 300
  }
);

const padding = { top: 20, right: 30, bottom: 40, left: 60 };
const svgRef = ref<SVGElement | null>(null);
const tooltip = ref<{
  x: number;
  y: number;
  time: string;
  tokens: number;
  cumulative: number;
  cost: number;
} | null>(null);

const hasData = computed(() => props.data.length > 0);
const chartWidth = computed(() => props.width - padding.left - padding.right);
const chartHeight = computed(() => props.height - padding.top - padding.bottom);

// Calculate scales
const maxTokens = computed(() => Math.max(...props.data.map(d => d.tokens), 1));
const maxCumulative = computed(() => Math.max(...props.data.map(d => d.cumulative), 1));

// Y-axis labels (based on max cumulative)
const yLabels = computed(() => {
  const max = maxCumulative.value;
  return [
    formatNumber(max),
    formatNumber(max * 0.75),
    formatNumber(max * 0.5),
    formatNumber(max * 0.25),
    '0'
  ];
});

// X-axis labels (timestamps)
const xLabels = computed(() => {
  if (props.data.length === 0) return [];
  
  const labels: string[] = [];
  const step = Math.max(1, Math.floor(props.data.length / 6));
  
  for (let i = 0; i < props.data.length; i += step) {
    labels.push(formatTime(props.data[i].timestamp));
  }
  
  // Always include last point
  if (labels.length < props.data.length) {
    labels.push(formatTime(props.data[props.data.length - 1].timestamp));
  }
  
  return labels;
});

// Chart data with calculated positions
const chartData = computed(() => {
  const barWidth = chartWidth.value / props.data.length * 0.8;
  
  return props.data.map((point, i) => {
    const x = padding.left + (i / (props.data.length - 1 || 1)) * chartWidth.value;
    const barHeight = (point.tokens / maxTokens.value) * chartHeight.value;
    const barY = padding.top + chartHeight.value - barHeight;
    const cumulativeY = padding.top + chartHeight.value - (point.cumulative / maxCumulative.value) * chartHeight.value;
    
    return {
      x,
      barX: x - barWidth / 2,
      barWidth,
      barY,
      barHeight,
      cumulativeY,
      ...point
    };
  });
});

// Cumulative line path
const cumulativePath = computed(() => {
  if (chartData.value.length === 0) return '';
  
  const points = chartData.value.map(d => `${d.x},${d.cumulativeY}`).join(' L ');
  return `M ${points}`;
});

function formatNumber(num: number): string {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
  return num.toFixed(0);
}

function formatTime(timestamp: number): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

function formatFullTime(timestamp: number): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

function onHover(point: any, index: number) {
  if (!svgRef.value) return;
  
  const rect = svgRef.value.getBoundingClientRect();
  tooltip.value = {
    x: point.x + rect.left - 80,
    y: point.barY + rect.top - 100,
    time: formatFullTime(point.timestamp),
    tokens: point.tokens,
    cumulative: point.cumulative,
    cost: point.cost
  };
}

function onLeave() {
  tooltip.value = null;
}
</script>

<style scoped>
.token-trend-chart {
  background: var(--theme-bg-secondary, #141414);
  border-radius: 0.5rem;
  padding: 1.5rem;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.chart-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--theme-text-primary, #F5F5F5);
}

.chart-legend {
  display: flex;
  gap: 1.5rem;
  font-size: 0.75rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--theme-text-secondary, #B3B3B3);
}

.legend-color {
  width: 1rem;
  height: 0.5rem;
  border-radius: 0.125rem;
}

.chart-container {
  position: relative;
  width: 100%;
}

svg {
  width: 100%;
  height: auto;
}

.grid-line {
  stroke: var(--theme-border-primary, #2A2A2A);
  stroke-width: 1;
  stroke-dasharray: 4 4;
}

.axis-label {
  fill: var(--theme-text-tertiary, #808080);
  font-size: 11px;
  font-family: 'JetBrains Mono', monospace;
}

.bar {
  fill: var(--chart-primary, #00D9FF);
  opacity: 0.7;
  transition: opacity 0.2s;
}

.bar:hover {
  opacity: 1;
  filter: drop-shadow(0 0 4px var(--chart-primary, #00D9FF));
}

.line-cumulative {
  stroke: var(--theme-primary, #BBA0FF);
  stroke-width: 2;
  stroke-linejoin: round;
  stroke-linecap: round;
}

.dot {
  fill: var(--theme-primary, #BBA0FF);
  transition: r 0.2s;
}

.dot:hover {
  r: 6;
  filter: drop-shadow(0 0 4px var(--theme-primary, #BBA0FF));
}

.tooltip {
  position: fixed;
  background: var(--theme-bg-tertiary, #1E1E1E);
  border: 1px solid var(--theme-primary, #BBA0FF);
  border-radius: 0.375rem;
  padding: 0.75rem;
  pointer-events: none;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  min-width: 160px;
}

.tooltip-time {
  font-size: 0.75rem;
  color: var(--theme-text-secondary, #B3B3B3);
  margin-bottom: 0.5rem;
  font-family: 'JetBrains Mono', monospace;
}

.tooltip-row {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  font-size: 0.8rem;
  margin-bottom: 0.25rem;
}

.tooltip-label {
  color: var(--theme-text-tertiary, #808080);
}

.tooltip-value {
  color: var(--theme-text-primary, #F5F5F5);
  font-weight: 600;
  font-family: 'JetBrains Mono', monospace;
}

.no-data {
  padding: 4rem 2rem;
  text-align: center;
  color: var(--theme-text-tertiary, #808080);
  font-size: 0.875rem;
}
</style>

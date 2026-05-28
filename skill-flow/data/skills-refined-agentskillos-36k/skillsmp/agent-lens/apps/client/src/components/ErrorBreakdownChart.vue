<template>
  <div class="error-breakdown-chart">
    <div class="chart-header">
      <h3>{{ title }}</h3>
      <div v-if="hasData" class="total-count">
        <span class="error-icon">⚠️</span>
        <span class="count">{{ totalErrors }} errors</span>
      </div>
    </div>

    <div v-if="hasData" class="chart-container">
      <!-- Horizontal bar chart -->
      <div class="bars">
        <div
          v-for="(item, i) in sortedData"
          :key="`error-${i}`"
          class="bar-row"
          @mouseenter="onHover(item, i)"
          @mouseleave="onLeave"
        >
          <div class="bar-label">
            <span class="error-type">{{ item.type }}</span>
            <span class="error-count">{{ item.count }}</span>
          </div>
          <div class="bar-wrapper">
            <div
              class="bar-fill"
              :style="{
                width: item.percentage + '%',
                background: getErrorColor(i)
              }"
            >
              <span class="bar-percentage">{{ item.percentage.toFixed(1) }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Tooltip -->
      <div
        v-if="tooltip"
        class="tooltip"
        :style="{
          left: tooltip.x + 'px',
          top: tooltip.y + 'px'
        }"
      >
        <div class="tooltip-title">{{ tooltip.type }}</div>
        <div class="tooltip-row">
          <span class="tooltip-label">Count:</span>
          <span class="tooltip-value">{{ tooltip.count }}</span>
        </div>
        <div class="tooltip-row">
          <span class="tooltip-label">Percentage:</span>
          <span class="tooltip-value">{{ tooltip.percentage.toFixed(2) }}%</span>
        </div>
        <div class="tooltip-row">
          <span class="tooltip-label">Rate:</span>
          <span class="tooltip-value">{{ (tooltip.count / totalErrors).toFixed(3) }}</span>
        </div>
      </div>
    </div>

    <div v-else class="no-data">
      <p>✅ No errors detected</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface ErrorData {
  type: string;
  count: number;
  percentage: number;
}

const props = withDefaults(
  defineProps<{
    data: ErrorData[];
    title?: string;
  }>(),
  {
    title: 'Error Breakdown by Type'
  }
);

const tooltip = ref<{
  x: number;
  y: number;
  type: string;
  count: number;
  percentage: number;
} | null>(null);

const hasData = computed(() => props.data.length > 0);
const totalErrors = computed(() => props.data.reduce((sum, item) => sum + item.count, 0));

// Sort by count descending
const sortedData = computed(() => {
  return [...props.data].sort((a, b) => b.count - a.count);
});

// Color gradient for error types
const errorColors = [
  '#F87171', // Red
  '#FF6B9D', // Pink
  '#FBBF24', // Yellow
  '#FB923C', // Orange
  '#DC2626', // Dark red
  '#EF4444', // Lighter red
  '#F59E0B', // Amber
  '#FCA5A5'  // Light red
];

function getErrorColor(index: number): string {
  return errorColors[index % errorColors.length];
}

function onHover(item: ErrorData, index: number) {
  const event = window.event as MouseEvent;
  tooltip.value = {
    x: event.clientX + 10,
    y: event.clientY - 80,
    type: item.type,
    count: item.count,
    percentage: item.percentage
  };
}

function onLeave() {
  tooltip.value = null;
}
</script>

<style scoped>
.error-breakdown-chart {
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

.total-count {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--theme-accent-error, #F87171);
  font-weight: 600;
}

.error-icon {
  font-size: 1.25rem;
}

.chart-container {
  position: relative;
}

.bars {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.bar-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.bar-row:hover {
  transform: translateX(4px);
}

.bar-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
}

.error-type {
  color: var(--theme-text-primary, #F5F5F5);
  font-weight: 500;
  font-family: 'JetBrains Mono', monospace;
}

.error-count {
  color: var(--theme-text-tertiary, #808080);
  font-size: 0.75rem;
}

.bar-wrapper {
  position: relative;
  height: 2rem;
  background: var(--theme-bg-tertiary, #1E1E1E);
  border-radius: 0.375rem;
  overflow: hidden;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
}

.bar-fill {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 0.75rem;
  transition: width 0.5s ease, filter 0.2s;
  border-radius: 0.375rem;
}

.bar-row:hover .bar-fill {
  filter: brightness(1.2) drop-shadow(0 0 8px currentColor);
}

.bar-percentage {
  font-size: 0.75rem;
  font-weight: 700;
  color: #FFFFFF;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
  font-family: 'JetBrains Mono', monospace;
}

.tooltip {
  position: fixed;
  background: var(--theme-bg-tertiary, #1E1E1E);
  border: 1px solid var(--theme-accent-error, #F87171);
  border-radius: 0.375rem;
  padding: 0.75rem;
  pointer-events: none;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  min-width: 180px;
}

.tooltip-title {
  font-size: 0.875rem;
  color: var(--theme-text-primary, #F5F5F5);
  font-weight: 600;
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
  color: var(--theme-accent-success, #4ADE80);
  font-size: 0.875rem;
  font-weight: 600;
}
</style>

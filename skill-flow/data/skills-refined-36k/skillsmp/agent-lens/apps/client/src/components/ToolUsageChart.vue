<template>
  <div class="tool-usage-chart">
    <div v-if="data.length === 0" class="empty-chart">
      <p>No tool usage data available</p>
    </div>

    <div v-else class="chart-content">
      <div
        v-for="(item, index) in topTools"
        :key="item.tool"
        class="tool-bar"
        :style="{ animationDelay: (index * 50) + 'ms' }"
      >
        <div class="tool-info">
          <span class="tool-name">{{ item.tool }}</span>
          <span class="tool-count">{{ item.count }}×</span>
        </div>
        <div class="bar-container">
          <div
            class="bar-fill"
            :style="{
              width: item.percentage + '%',
              background: getToolColor(index)
            }"
          >
            <span class="bar-label">{{ item.percentage.toFixed(1) }}%</span>
          </div>
        </div>
        <div v-if="item.averageLatency > 0" class="tool-latency">
          {{ formatLatency(item.averageLatency) }}
        </div>
      </div>

      <div v-if="data.length > maxDisplay" class="more-tools">
        +{{ data.length - maxDisplay }} more tools
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { ToolUsageData } from '../services/metricsCalculator';

const props = defineProps<{
  data: ToolUsageData[];
  maxDisplay?: number;
}>();

const maxDisplay = props.maxDisplay || 10;

const topTools = computed(() => {
  return props.data.slice(0, maxDisplay);
});

const toolColors = [
  'var(--chart-primary, #00D9FF)',     // Cyan
  'var(--chart-secondary, #BBA0FF)',   // Purple
  'var(--chart-tertiary, #FF6B9D)',    // Pink
  'var(--chart-quaternary, #FFD93D)',  // Yellow
  'var(--theme-accent-success, #4ADE80)', // Green
  'var(--theme-accent-info, #00D9FF)',   // Info blue
];

function getToolColor(index: number): string {
  return toolColors[index % toolColors.length];
}

function formatLatency(ms: number): string {
  if (ms < 1000) return `${Math.round(ms)}ms`;
  return `${(ms / 1000).toFixed(1)}s`;
}
</script>

<style scoped>
.tool-usage-chart {
  min-height: 200px;
}

.empty-chart {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: var(--theme-text-tertiary, #808080);
  font-size: 0.875rem;
}

.chart-content {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
}

.tool-bar {
  animation: slideInBar 0.4s ease-out backwards;
}

@keyframes slideInBar {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.tool-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.375rem;
  font-size: 0.875rem;
}

.tool-name {
  color: var(--theme-text-primary, #F5F5F5);
  font-weight: 500;
  font-family: 'JetBrains Mono', monospace;
}

.tool-count {
  color: var(--theme-text-tertiary, #808080);
  font-size: 0.8125rem;
}

.bar-container {
  position: relative;
  height: 2.25rem;
  background: var(--theme-bg-tertiary, #1E1E1E);
  border-radius: 0.5rem;
  overflow: hidden;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
}

.bar-fill {
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 0.75rem;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.bar-fill::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.bar-label {
  color: #0A0A0A;
  font-weight: 700;
  font-size: 0.8125rem;
  position: relative;
  z-index: 1;
}

.tool-latency {
  margin-top: 0.25rem;
  font-size: 0.75rem;
  color: var(--theme-text-quaternary, #666666);
  text-align: right;
  font-family: 'JetBrains Mono', monospace;
}

.more-tools {
  margin-top: 0.5rem;
  padding: 0.75rem;
  background: var(--theme-bg-tertiary, #1E1E1E);
  border-radius: 0.375rem;
  text-align: center;
  font-size: 0.8125rem;
  color: var(--theme-text-tertiary, #808080);
  border: 1px dashed var(--theme-border-primary, #2A2A2A);
}
</style>

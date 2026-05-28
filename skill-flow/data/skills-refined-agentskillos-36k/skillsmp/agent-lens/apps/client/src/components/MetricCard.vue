<template>
  <div class="metric-card" :class="{ alert, highlight }">
    <div class="card-header">
      <span class="icon">{{ icon }}</span>
      <span class="title">{{ title }}</span>
    </div>

    <div class="card-value" :class="valueClass">
      {{ value }}
    </div>

    <div class="card-subtitle">
      {{ subtitle }}
    </div>

    <div v-if="trend" class="card-trend" :class="trendClass">
      <svg width="12" height="12" viewBox="0 0 12 12" class="trend-arrow">
        <path
          :d="trendArrowPath"
          fill="none"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
      <span class="trend-text">{{ trend }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  title: string;
  value: string;
  icon: string;
  subtitle: string;
  trend?: string;
  alert?: boolean;
  highlight?: boolean;
  valueClass?: string;
}>();

const trendClass = computed(() => {
  if (!props.trend) return '';
  if (props.trend.startsWith('+')) return 'trend-up';
  if (props.trend.startsWith('-')) return 'trend-down';
  return 'trend-neutral';
});

const trendArrowPath = computed(() => {
  if (trendClass.value === 'trend-up') {
    return 'M6 9 L6 3 M3 6 L6 3 L9 6'; // Up arrow
  }
  if (trendClass.value === 'trend-down') {
    return 'M6 3 L6 9 M3 6 L6 9 L9 6'; // Down arrow
  }
  return 'M3 6 L9 6'; // Horizontal line
});
</script>

<style scoped>
.metric-card {
  background: var(--theme-bg-secondary, #141414);
  border: 1px solid var(--theme-border-primary, #2A2A2A);
  border-radius: 0.5rem;
  padding: 1.25rem;
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: transparent;
  transition: background 0.2s;
}

.metric-card:hover {
  border-color: var(--theme-primary, #BBA0FF);
  box-shadow: 0 0 15px rgba(187, 160, 255, 0.2);
}

.metric-card:hover::before {
  background: linear-gradient(90deg, var(--theme-primary, #BBA0FF), var(--chart-tertiary, #FF6B9D));
}

.metric-card.alert {
  border-color: var(--theme-accent-error, #F87171);
  background: var(--theme-error-bg, rgba(248, 113, 113, 0.1));
}

.metric-card.alert::before {
  background: var(--theme-accent-error, #F87171);
}

.metric-card.highlight {
  border-color: var(--theme-accent-success, #4ADE80);
}

.metric-card.highlight::before {
  background: var(--theme-accent-success, #4ADE80);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  margin-bottom: 0.875rem;
}

.icon {
  font-size: 1.5rem;
  line-height: 1;
}

.title {
  font-size: 0.875rem;
  color: var(--theme-text-secondary, #B3B3B3);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.card-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--theme-text-primary, #F5F5F5);
  margin-bottom: 0.375rem;
  line-height: 1.2;
  font-variant-numeric: tabular-nums;
}

.card-value.large {
  font-size: 2.5rem;
}

.card-value.small {
  font-size: 1.5rem;
}

.card-value.monospace {
  font-family: 'JetBrains Mono', monospace;
}

.card-subtitle {
  font-size: 0.8125rem;
  color: var(--theme-text-tertiary, #808080);
  line-height: 1.4;
}

.card-trend {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  margin-top: 0.625rem;
  padding-top: 0.625rem;
  border-top: 1px solid var(--theme-border-primary, #2A2A2A);
  font-size: 0.8125rem;
  font-weight: 600;
}

.trend-arrow {
  flex-shrink: 0;
}

.trend-text {
  font-variant-numeric: tabular-nums;
}

.trend-up {
  color: var(--theme-accent-success, #4ADE80);
}

.trend-down {
  color: var(--theme-accent-error, #F87171);
}

.trend-neutral {
  color: var(--theme-text-tertiary, #808080);
}
</style>

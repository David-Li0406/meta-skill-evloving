<template>
  <div class="enhanced-context-bar">
    <div class="context-header">
      <h3>📝 Context Window Usage (CC 2.1.6)</h3>
      <div v-if="hasData" class="context-stats">
        <span class="stat">{{ contextUsed }}% used</span>
        <span class="divider">•</span>
        <span class="stat">{{ contextRemaining }}% available</span>
      </div>
    </div>

    <div v-if="hasData" class="context-visualization">
      <!-- Main progress bar with segments -->
      <div class="progress-container">
        <div class="progress-bar" :class="contextLevel">
          <div
            class="progress-fill"
            :style="{ width: contextUsed + '%' }"
          >
            <span v-if="contextUsed > 10" class="progress-label">
              {{ contextUsed }}%
            </span>
          </div>
          
          <!-- Threshold markers -->
          <div class="threshold-marker" style="left: 60%;" title="Warning threshold (60%)">
            <div class="marker-line warning"></div>
          </div>
          <div class="threshold-marker" style="left: 80%;" title="Critical threshold (80%)">
            <div class="marker-line critical"></div>
          </div>
        </div>
      </div>

      <!-- Detailed breakdown -->
      <div class="context-details">
        <div class="detail-grid">
          <div class="detail-item">
            <span class="detail-icon">📊</span>
            <div class="detail-content">
              <span class="detail-label">Current Usage</span>
              <span class="detail-value">{{ contextUsed }}%</span>
            </div>
          </div>

          <div class="detail-item">
            <span class="detail-icon">🔄</span>
            <div class="detail-content">
              <span class="detail-label">Remaining</span>
              <span class="detail-value">{{ contextRemaining }}%</span>
            </div>
          </div>

          <div class="detail-item">
            <span class="detail-icon">⚡</span>
            <div class="detail-content">
              <span class="detail-label">Status</span>
              <span class="detail-value" :class="`status-${contextLevel}`">
                {{ contextStatus }}
              </span>
            </div>
          </div>

          <div v-if="estimatedCapacity" class="detail-item">
            <span class="detail-icon">🎯</span>
            <div class="detail-content">
              <span class="detail-label">Capacity</span>
              <span class="detail-value">~{{ estimatedCapacity }} tokens</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Warning messages -->
      <div v-if="contextWarning" class="context-warning" :class="`warning-${contextLevel}`">
        <span class="warning-icon">{{ warningIcon }}</span>
        <span class="warning-text">{{ contextWarning }}</span>
      </div>

      <!-- Context evolution over time -->
      <div v-if="contextHistory.length > 1" class="context-history">
        <h4>Context Usage History</h4>
        <div class="history-chart">
          <svg viewBox="0 0 400 60" preserveAspectRatio="none">
            <!-- Grid lines -->
            <line x1="0" y1="0" x2="400" y2="0" class="grid-line" />
            <line x1="0" y1="30" x2="400" y2="30" class="grid-line" />
            <line x1="0" y1="60" x2="400" y2="60" class="grid-line" />
            
            <!-- Threshold lines -->
            <line x1="0" y1="24" x2="400" y2="24" class="threshold-line warning" />
            <line x1="0" y1="12" x2="400" y2="12" class="threshold-line critical" />
            
            <!-- Usage line -->
            <polyline
              :points="historyPoints"
              class="history-line"
              :class="contextLevel"
              fill="none"
            />
            
            <!-- Data points -->
            <circle
              v-for="(point, i) in contextHistory"
              :key="`point-${i}`"
              :cx="(i / (contextHistory.length - 1)) * 400"
              :cy="60 - (point.percentage / 100) * 60"
              r="2"
              class="history-point"
            />
          </svg>
        </div>
        <div class="history-labels">
          <span>Start</span>
          <span>Now</span>
        </div>
      </div>

      <!-- Recommendations -->
      <div v-if="recommendations.length > 0" class="recommendations">
        <h4>💡 Recommendations</h4>
        <ul>
          <li v-for="(rec, i) in recommendations" :key="`rec-${i}`">
            {{ rec }}
          </li>
        </ul>
      </div>
    </div>

    <div v-else class="no-data">
      <p>No context usage data available</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { HookEvent } from '../types';

const props = defineProps<{
  events: HookEvent[];
}>();

// Context metrics
const hasData = computed(() => {
  return props.events.some(e => e.context_used_percentage !== undefined);
});

const contextUsed = computed(() => {
  const latest = [...props.events]
    .reverse()
    .find(e => e.context_used_percentage !== undefined);
  return Math.round(latest?.context_used_percentage || 0);
});

const contextRemaining = computed(() => {
  const latest = [...props.events]
    .reverse()
    .find(e => e.context_remaining_percentage !== undefined);
  return Math.round(latest?.context_remaining_percentage || 100);
});

const contextLevel = computed(() => {
  if (contextUsed.value >= 80) return 'critical';
  if (contextUsed.value >= 60) return 'warning';
  return 'normal';
});

const contextStatus = computed(() => {
  if (contextUsed.value >= 80) return 'Critical';
  if (contextUsed.value >= 60) return 'High';
  if (contextUsed.value >= 40) return 'Moderate';
  return 'Healthy';
});

const warningIcon = computed(() => {
  if (contextLevel.value === 'critical') return '🚨';
  if (contextLevel.value === 'warning') return '⚠️';
  return 'ℹ️';
});

const contextWarning = computed(() => {
  if (contextUsed.value >= 90) {
    return 'Context window near capacity! Consider checkpointing or summarizing.';
  }
  if (contextUsed.value >= 80) {
    return 'Context degradation likely. Performance may be impacted.';
  }
  if (contextUsed.value >= 60) {
    return 'Approaching context limit. Monitor usage carefully.';
  }
  return null;
});

// Estimated capacity (assuming 200k tokens for CC 2.1.6)
const estimatedCapacity = computed(() => {
  if (contextUsed.value === 0) return null;
  // Rough estimate: 200k tokens total capacity
  return Math.round(200000 * (contextUsed.value / 100));
});

// Context history for visualization
const contextHistory = computed(() => {
  const history: Array<{ percentage: number; timestamp: number }> = [];
  
  props.events.forEach(e => {
    if (e.context_used_percentage !== undefined && e.timestamp) {
      history.push({
        percentage: e.context_used_percentage,
        timestamp: e.timestamp
      });
    }
  });

  // Sample to max 20 points for clean visualization
  if (history.length <= 20) return history;
  
  const step = Math.floor(history.length / 20);
  return history.filter((_, i) => i % step === 0);
});

const historyPoints = computed(() => {
  if (contextHistory.value.length === 0) return '';
  
  return contextHistory.value
    .map((point, i) => {
      const x = (i / (contextHistory.value.length - 1)) * 400;
      const y = 60 - (point.percentage / 100) * 60;
      return `${x},${y}`;
    })
    .join(' ');
});

// Smart recommendations
const recommendations = computed(() => {
  const recs: string[] = [];
  
  if (contextUsed.value >= 70) {
    recs.push('Consider using checkpointing to save current state');
    recs.push('Summarize or compress older context if possible');
  }
  
  if (contextUsed.value >= 60) {
    recs.push('Monitor context usage closely for remaining session');
  }
  
  if (contextHistory.value.length > 0) {
    const recentGrowth = contextHistory.value.slice(-5);
    if (recentGrowth.length >= 2) {
      const growth = recentGrowth[recentGrowth.length - 1].percentage - recentGrowth[0].percentage;
      if (growth > 10) {
        recs.push('Context usage growing rapidly - consider breaking into subtasks');
      }
    }
  }
  
  return recs;
});
</script>

<style scoped>
.enhanced-context-bar {
  background: var(--theme-bg-secondary, #141414);
  border-radius: 0.5rem;
  padding: 1.5rem;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
}

.context-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.context-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--theme-text-primary, #F5F5F5);
}

.context-stats {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: var(--theme-text-secondary, #B3B3B3);
  font-weight: 600;
}

.divider {
  color: var(--theme-text-tertiary, #808080);
}

.context-visualization {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.progress-container {
  position: relative;
}

.progress-bar {
  position: relative;
  height: 2rem;
  background: var(--theme-bg-tertiary, #1E1E1E);
  border-radius: 1rem;
  overflow: visible;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
}

.progress-fill {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 1rem;
  transition: width 0.5s ease, background 0.3s ease;
  background: linear-gradient(90deg, var(--theme-accent-success, #4ADE80), var(--chart-primary, #00D9FF));
}

.progress-bar.warning .progress-fill {
  background: linear-gradient(90deg, var(--theme-accent-warning, #FBBF24), var(--chart-quaternary, #FFD93D));
}

.progress-bar.critical .progress-fill {
  background: linear-gradient(90deg, var(--theme-accent-error, #F87171), var(--chart-tertiary, #FF6B9D));
  animation: pulse-critical 2s ease-in-out infinite;
}

@keyframes pulse-critical {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

.progress-label {
  font-size: 0.875rem;
  font-weight: 700;
  color: #FFFFFF;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
  font-family: 'JetBrains Mono', monospace;
}

.threshold-marker {
  position: absolute;
  top: -4px;
  bottom: -4px;
  width: 2px;
  transform: translateX(-1px);
  pointer-events: none;
}

.marker-line {
  width: 100%;
  height: 100%;
  border-left: 2px dashed;
  opacity: 0.5;
}

.marker-line.warning {
  border-color: var(--theme-accent-warning, #FBBF24);
}

.marker-line.critical {
  border-color: var(--theme-accent-error, #F87171);
}

.context-details {
  background: var(--theme-bg-tertiary, #1E1E1E);
  border-radius: 0.5rem;
  padding: 1rem;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.detail-icon {
  font-size: 1.5rem;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-label {
  font-size: 0.7rem;
  color: var(--theme-text-tertiary, #808080);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--theme-text-primary, #F5F5F5);
  font-family: 'JetBrains Mono', monospace;
}

.status-normal {
  color: var(--theme-accent-success, #4ADE80);
}

.status-warning {
  color: var(--theme-accent-warning, #FBBF24);
}

.status-critical {
  color: var(--theme-accent-error, #F87171);
}

.context-warning {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid;
  font-size: 0.875rem;
  font-weight: 500;
}

.warning-normal {
  background: rgba(74, 222, 128, 0.1);
  border-color: var(--theme-accent-success, #4ADE80);
  color: var(--theme-accent-success, #4ADE80);
}

.warning-warning {
  background: rgba(251, 191, 36, 0.1);
  border-color: var(--theme-accent-warning, #FBBF24);
  color: var(--theme-accent-warning, #FBBF24);
}

.warning-critical {
  background: rgba(248, 113, 113, 0.1);
  border-color: var(--theme-accent-error, #F87171);
  color: var(--theme-accent-error, #F87171);
  animation: pulse-warning 2s ease-in-out infinite;
}

@keyframes pulse-warning {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.warning-icon {
  font-size: 1.25rem;
}

.context-history {
  background: var(--theme-bg-tertiary, #1E1E1E);
  border-radius: 0.5rem;
  padding: 1rem;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
}

.context-history h4 {
  margin: 0 0 1rem 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--theme-text-primary, #F5F5F5);
}

.history-chart {
  width: 100%;
  height: 60px;
  margin-bottom: 0.5rem;
}

.grid-line {
  stroke: var(--theme-border-primary, #2A2A2A);
  stroke-width: 1;
}

.threshold-line {
  stroke-width: 1;
  stroke-dasharray: 4 2;
  opacity: 0.5;
}

.threshold-line.warning {
  stroke: var(--theme-accent-warning, #FBBF24);
}

.threshold-line.critical {
  stroke: var(--theme-accent-error, #F87171);
}

.history-line {
  stroke-width: 2;
  stroke-linejoin: round;
  stroke-linecap: round;
  stroke: var(--theme-primary, #BBA0FF);
}

.history-line.warning {
  stroke: var(--theme-accent-warning, #FBBF24);
}

.history-line.critical {
  stroke: var(--theme-accent-error, #F87171);
}

.history-point {
  fill: var(--theme-primary, #BBA0FF);
}

.history-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: var(--theme-text-tertiary, #808080);
  font-family: 'JetBrains Mono', monospace;
}

.recommendations {
  background: var(--theme-bg-tertiary, #1E1E1E);
  border-radius: 0.5rem;
  padding: 1rem;
  border: 1px solid var(--theme-primary, #BBA0FF);
}

.recommendations h4 {
  margin: 0 0 0.75rem 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--theme-text-primary, #F5F5F5);
}

.recommendations ul {
  margin: 0;
  padding-left: 1.5rem;
  list-style: none;
}

.recommendations li {
  font-size: 0.8rem;
  color: var(--theme-text-secondary, #B3B3B3);
  margin-bottom: 0.5rem;
  position: relative;
}

.recommendations li::before {
  content: '→';
  position: absolute;
  left: -1.25rem;
  color: var(--theme-primary, #BBA0FF);
  font-weight: bold;
}

.no-data {
  padding: 4rem 2rem;
  text-align: center;
  color: var(--theme-text-tertiary, #808080);
  font-size: 0.875rem;
}
</style>

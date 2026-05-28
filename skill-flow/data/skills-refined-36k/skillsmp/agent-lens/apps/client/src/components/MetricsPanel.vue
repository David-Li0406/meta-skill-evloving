<template>
  <div class="metrics-panel">
    <!-- Summary Cards -->
    <div class="metrics-grid">
      <div class="metric-card">
        <div class="card-header">
          <span class="icon">📊</span>
          <span class="title">Events</span>
        </div>
        <div class="card-value">{{ eventCount }}</div>
        <div class="card-subtitle">Total captured</div>
      </div>

      <div class="metric-card">
        <div class="card-header">
          <span class="icon">🔧</span>
          <span class="title">Tool Calls</span>
        </div>
        <div class="card-value">{{ toolCallCount }}</div>
        <div class="card-subtitle">{{ uniqueToolCount }} unique tools</div>
      </div>

      <div class="metric-card">
        <div class="card-header">
          <span class="icon">⏱️</span>
          <span class="title">Duration</span>
        </div>
        <div class="card-value">{{ formattedDuration }}</div>
        <div class="card-subtitle">Session length</div>
      </div>

      <div class="metric-card">
        <div class="card-header">
          <span class="icon">🤖</span>
          <span class="title">Agents</span>
        </div>
        <div class="card-value">{{ agentCount }}</div>
        <div class="card-subtitle">{{ agentsList }}</div>
      </div>

      <div v-if="hasSkills" class="metric-card">
        <div class="card-header">
          <span class="icon">🛠️</span>
          <span class="title">Skills</span>
        </div>
        <div class="card-value">{{ skillCount }}</div>
        <div class="card-subtitle">Invoked</div>
      </div>

      <div v-if="hasContextData" class="metric-card" :class="{ alert: contextUsed >= 60 }">
        <div class="card-header">
          <span class="icon">📝</span>
          <span class="title">Context</span>
        </div>
        <div class="card-value">{{ contextUsed }}%</div>
        <div class="card-subtitle">{{ contextRemaining }}% remaining</div>
      </div>

      <div v-if="sessionMetrics.totalTokens > 0" class="metric-card">
        <div class="card-header">
          <span class="icon">🔤</span>
          <span class="title">Tokens</span>
        </div>
        <div class="card-value">{{ formatTokens(sessionMetrics.totalTokens) }}</div>
        <div class="card-subtitle">{{ sessionMetrics.inputTokens }}in / {{ sessionMetrics.outputTokens }}out</div>
      </div>

      <div v-if="sessionMetrics.estimatedCost > 0" class="metric-card">
        <div class="card-header">
          <span class="icon">💰</span>
          <span class="title">Cost</span>
        </div>
        <div class="card-value">${{ sessionMetrics.estimatedCost.toFixed(4) }}</div>
        <div class="card-subtitle">${{ sessionMetrics.costPerThousandTokens.toFixed(3) }}/1K</div>
      </div>

      <div v-if="sessionMetrics.errors > 0" class="metric-card alert">
        <div class="card-header">
          <span class="icon">⚠️</span>
          <span class="title">Errors</span>
        </div>
        <div class="card-value">{{ sessionMetrics.errors }}</div>
        <div class="card-subtitle">{{ sessionMetrics.errorRate.toFixed(1) }}% error rate</div>
      </div>
    </div>

    <!-- Enhanced Context Bar (CC 2.1.6) -->
    <EnhancedContextBar
      v-if="hasContextData"
      :events="events"
    />

    <!-- Charts Section -->
    <div class="charts-section">
      <!-- Token Trend Chart -->
      <TokenTrendChart
        v-if="tokenTrend.length > 0"
        :data="tokenTrend"
      />

      <!-- Tool Usage Chart -->
      <ToolUsageChart
        v-if="toolUsageData.length > 0"
        :data="toolUsageData"
      />

      <!-- Error Breakdown Chart -->
      <ErrorBreakdownChart
        v-if="errorBreakdown.length > 0"
        :data="errorBreakdown"
      />
    </div>

    <!-- Skill Usage Panel -->
    <SkillUsagePanel
      v-if="hasSkills"
      :events="events"
    />

    <!-- Event Details Section -->
    <div v-if="selectedEvent" class="event-details-section">
      <h3>Selected Event</h3>
      <div class="event-details-card">
        <div class="detail-row">
          <span class="detail-label">Type:</span>
          <span class="detail-value">{{ selectedEvent.hook_event_type }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Event ID:</span>
          <span class="detail-value code">{{ selectedEvent.event_id?.substring(0, 13) }}...</span>
        </div>
        <div v-if="selectedEvent.parent_event_id" class="detail-row">
          <span class="detail-label">Parent ID:</span>
          <span class="detail-value code">{{ selectedEvent.parent_event_id?.substring(0, 13) }}...</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Span Kind:</span>
          <span class="detail-value">{{ selectedEvent.span_kind || 'N/A' }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Depth:</span>
          <span class="detail-value">{{ selectedEvent.depth ?? 'N/A' }}</span>
        </div>
        <div v-if="selectedEvent.children && selectedEvent.children.length > 0" class="detail-row">
          <span class="detail-label">Children:</span>
          <span class="detail-value">{{ selectedEvent.children.length }}</span>
        </div>
        <div v-if="selectedEvent.skill_name" class="detail-row">
          <span class="detail-label">Skill:</span>
          <span class="detail-value">{{ selectedEvent.skill_name }}</span>
        </div>
        <div v-if="selectedEvent.timestamp_aedt" class="detail-row">
          <span class="detail-label">Time:</span>
          <span class="detail-value">{{ selectedEvent.timestamp_aedt }}</span>
        </div>

        <!-- Payload (collapsible) -->
        <div class="payload-section">
          <button class="btn-link" @click="showPayload = !showPayload">
            {{ showPayload ? 'Hide' : 'Show' }} Payload
          </button>
          <pre v-if="showPayload" class="payload-content">{{ formatPayload(selectedEvent.payload) }}</pre>
        </div>
      </div>
    </div>

    <!-- Placeholder for no selection -->
    <div v-else class="no-selection">
      <p>Click an event in the timeline to view details</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { HookEvent } from '../types';
import { MetricsCalculator } from '../services/metricsCalculator';
import TokenTrendChart from './TokenTrendChart.vue';
import ErrorBreakdownChart from './ErrorBreakdownChart.vue';
import ToolUsageChart from './ToolUsageChart.vue';
import SkillUsagePanel from './SkillUsagePanel.vue';
import EnhancedContextBar from './EnhancedContextBar.vue';

const props = defineProps<{
  events: HookEvent[];
  selectedEvent?: HookEvent | null;
}>();

const showPayload = ref(false);

// Expose MetricsCalculator for template use
const { formatTokens } = MetricsCalculator;

// Calculate comprehensive metrics using MetricsCalculator
const sessionMetrics = computed(() => MetricsCalculator.calculateSessionMetrics(props.events));
const tokenTrend = computed(() => MetricsCalculator.getTokenTrend(props.events, 10000));
const toolUsageData = computed(() => MetricsCalculator.getToolUsageBreakdown(props.events));
const errorBreakdown = computed(() => MetricsCalculator.getErrorBreakdown(props.events));

// Event counts
const eventCount = computed(() => props.events.length);

const toolCallCount = computed(() => {
  return props.events.filter(e => e.hook_event_type === 'PreToolUse').length;
});

const uniqueToolCount = computed(() => {
  const tools = new Set(
    props.events
      .filter(e => e.hook_event_type === 'PreToolUse')
      .map(e => e.payload?.tool_name)
      .filter(Boolean)
  );
  return tools.size;
});

// Agent counts
const agentCount = computed(() => {
  const agents = new Set(props.events.map(e => e.source_app));
  return agents.size;
});

const agentsList = computed(() => {
  const agents = Array.from(new Set(props.events.map(e => e.source_app)));
  if (agents.length <= 3) return agents.join(', ');
  return agents.slice(0, 2).join(', ') + ` +${agents.length - 2}`;
});

// Skill tracking
const hasSkills = computed(() => {
  return props.events.some(e => e.skill_name);
});

const skillCount = computed(() => {
  return props.events.filter(e => e.skill_name).length;
});

// Duration
const formattedDuration = computed(() => {
  if (props.events.length === 0) return '0s';

  const timestamps = props.events
    .map(e => e.timestamp)
    .filter((t): t is number => t !== undefined)
    .sort((a, b) => a - b);

  if (timestamps.length < 2) return '0s';

  const first = timestamps[0];
  const last = timestamps[timestamps.length - 1];
  if (first === undefined || last === undefined) return '0s';

  const duration = last - first;
  return formatDuration(duration);
});

// Context tracking
const hasContextData = computed(() => {
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

const contextWarning = computed(() => {
  if (contextUsed.value >= 80) {
    return '🚨 Context degradation likely';
  }
  if (contextUsed.value >= 60) {
    return '⚠️ Approaching limit';
  }
  return null;
});

function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(0)}s`;
  const minutes = Math.floor(ms / 60000);
  const seconds = Math.floor((ms % 60000) / 1000);
  return `${minutes}m ${seconds}s`;
}

function formatPayload(payload: any): string {
  if (!payload) return '{}';
  return JSON.stringify(payload, null, 2);
}
</script>

<style scoped>
.metrics-panel {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}

.metric-card {
  background: var(--theme-bg-secondary, #141414);
  border: 1px solid var(--theme-border-primary, #2A2A2A);
  border-radius: 0.5rem;
  padding: 1rem;
  transition: all 0.2s;
}

.metric-card:hover {
  border-color: var(--theme-primary, #BBA0FF);
  box-shadow: 0 0 10px rgba(187, 160, 255, 0.2);
}

.metric-card.alert {
  border-color: var(--theme-accent-error, #F87171);
  background: var(--theme-error-bg, rgba(248, 113, 113, 0.1));
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.icon {
  font-size: 1.25rem;
}

.title {
  font-size: 0.875rem;
  color: var(--theme-text-secondary, #B3B3B3);
  font-weight: 500;
}

.card-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--theme-text-primary, #F5F5F5);
  margin-bottom: 0.25rem;
}

.card-subtitle {
  font-size: 0.75rem;
  color: var(--theme-text-tertiary, #808080);
}

.context-section {
  background: var(--theme-bg-secondary, #141414);
  border-radius: 0.5rem;
  padding: 1.5rem;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
}

.context-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--theme-text-primary, #F5F5F5);
}

.progress-bar {
  position: relative;
  height: 1.5rem;
  background: var(--theme-bg-tertiary, #1E1E1E);
  border-radius: 0.75rem;
  overflow: hidden;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
  margin-bottom: 0.75rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--theme-accent-success, #4ADE80), var(--chart-primary, #00D9FF));
  transition: width 0.3s ease, background 0.3s ease;
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
  50% { opacity: 0.7; }
}

.context-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
}

.remaining-text {
  color: var(--theme-text-tertiary, #808080);
}

.warning-message {
  color: var(--theme-accent-warning, #FBBF24);
  font-weight: 600;
}

.progress-bar.critical + .context-footer .warning-message {
  color: var(--theme-accent-error, #F87171);
}

.event-details-section {
  background: var(--theme-bg-secondary, #141414);
  border-radius: 0.5rem;
  padding: 1.5rem;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
}

.event-details-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--theme-text-primary, #F5F5F5);
}

.event-details-card {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-row {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 1rem;
  font-size: 0.875rem;
}

.detail-label {
  color: var(--theme-text-secondary, #B3B3B3);
  font-weight: 500;
}

.detail-value {
  color: var(--theme-text-primary, #F5F5F5);
}

.detail-value.code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
}

.payload-section {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--theme-border-primary, #2A2A2A);
}

.btn-link {
  padding: 0;
  border: none;
  background: transparent;
  color: var(--theme-primary, #BBA0FF);
  text-decoration: underline;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-link:hover {
  color: var(--theme-primary-hover, #D4C5FF);
}

.payload-content {
  margin-top: 0.5rem;
  padding: 1rem;
  background: var(--theme-bg-primary, #0A0A0A);
  border-radius: 0.375rem;
  max-height: 300px;
  overflow-y: auto;
  font-size: 0.75rem;
  color: var(--theme-text-secondary, #B3B3B3);
  white-space: pre-wrap;
  word-break: break-word;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
}

.no-selection {
  padding: 4rem 2rem;
  text-align: center;
  color: var(--theme-text-tertiary, #808080);
  font-size: 0.875rem;
}

.charts-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
</style>

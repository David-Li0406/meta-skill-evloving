<template>
  <div class="session-timeline">
    <!-- Session Info -->
    <div v-if="sessionInfo" class="session-info">
      <div class="session-header">
        <span class="session-label">Session</span>
        <span class="session-id">{{ sessionInfo.shortId }}</span>
      </div>
      <div class="session-stats">
        <span class="stat">{{ sessionInfo.eventCount }} events</span>
        <span v-if="sessionInfo.duration" class="stat">{{ formatDuration(sessionInfo.duration) }}</span>
        <span v-if="sessionInfo.agentName" class="stat">{{ sessionInfo.agentName }}</span>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="rootEvents.length === 0" class="empty-state">
      <div class="empty-icon">👁️</div>
      <h3>No Events Yet</h3>
      <p>Events will appear here as you use Claude Code</p>
    </div>

    <!-- Hierarchical Events -->
    <div v-else class="events-container">
      <HierarchicalEvent
        v-for="event in rootEvents"
        :key="event.event_id"
        :event="event"
        :all-events-map="eventsMap"
        :collapsed-events="collapsedEvents"
        :selected-event-id="selectedEventId"
        :depth="0"
        @event-click="handleEventClick"
        @toggle-collapse="handleToggleCollapse"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { HookEvent } from '../types';
import HierarchicalEvent from './HierarchicalEvent.vue';

const props = defineProps<{
  events: HookEvent[];
  collapsedEvents: Set<string>;
  selectedEventId?: string | null;
}>();

const emit = defineEmits<{
  'event-click': [event: HookEvent];
  'toggle-collapse': [eventId: string];
}>();

// Build map for fast lookups
const eventsMap = computed(() => {
  const map = new Map<string, HookEvent>();
  props.events.forEach(event => {
    if (event.event_id) {
      map.set(event.event_id, event);
    }
  });
  return map;
});

// Root events (no parent or parent not in current set)
const rootEvents = computed(() => {
  return props.events.filter(event => {
    if (!event.event_id) return false; // Skip old events without hierarchy
    if (!event.parent_event_id) return true; // Truly root

    // Check if parent exists in current event set
    return !eventsMap.value.has(event.parent_event_id);
  });
});

// Session info (from first/last events)
const sessionInfo = computed(() => {
  if (props.events.length === 0) return null;

  const sortedEvents = [...props.events].sort((a, b) =>
    (a.timestamp || 0) - (b.timestamp || 0)
  );

  const firstEvent = sortedEvents[0];
  const lastEvent = sortedEvents[sortedEvents.length - 1];

  if (!firstEvent || !lastEvent) return null;

  const duration = lastEvent.timestamp && firstEvent.timestamp
    ? lastEvent.timestamp - firstEvent.timestamp
    : null;

  return {
    shortId: firstEvent.session_id.substring(0, 8),
    eventCount: props.events.length,
    duration,
    agentName: firstEvent.source_app
  };
});

function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(0)}s`;
  const minutes = Math.floor(ms / 60000);
  const seconds = Math.floor((ms % 60000) / 1000);
  return `${minutes}m ${seconds}s`;
}

function handleEventClick(event: HookEvent) {
  emit('event-click', event);
}

function handleToggleCollapse(eventId: string) {
  emit('toggle-collapse', eventId);
}
</script>

<style scoped>
.session-timeline {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.session-info {
  padding: 1rem;
  background: var(--theme-bg-tertiary, #1E1E1E);
  border-radius: 0.5rem;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
}

.session-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.session-label {
  font-size: 0.75rem;
  color: var(--theme-text-tertiary, #808080);
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.05em;
}

.session-id {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  color: var(--theme-primary, #BBA0FF);
  font-weight: 600;
}

.session-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
}

.stat {
  color: var(--theme-text-secondary, #B3B3B3);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  color: var(--theme-text-secondary, #B3B3B3);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.3;
}

.empty-state h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--theme-text-primary, #F5F5F5);
}

.empty-state p {
  margin: 0;
  font-size: 0.875rem;
  color: var(--theme-text-tertiary, #808080);
}

.events-container {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
</style>

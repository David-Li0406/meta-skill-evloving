<template>
  <div
    class="hierarchical-event"
    :class="[
      `depth-${depth}`,
      { collapsed, 'has-children': hasChildren, active: isActive }
    ]"
  >
    <!-- Event Header -->
    <div
      class="event-header"
      @click="handleClick"
      :style="{ paddingLeft: (depth * 1.5 + 0.5) + 'rem' }"
    >
      <!-- Expand/Collapse Icon -->
      <button
        v-if="hasChildren"
        class="collapse-btn"
        @click.stop="toggleCollapse"
      >
        <svg
          :class="['chevron', { collapsed }]"
          width="12"
          height="12"
          viewBox="0 0 12 12"
        >
          <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" stroke-width="1.5" fill="none"/>
        </svg>
      </button>
      <div v-else class="collapse-spacer"></div>

      <!-- Event Icon -->
      <span class="event-icon">{{ eventIcon }}</span>

      <!-- Event Name -->
      <span class="event-name">{{ eventDisplayName }}</span>

      <!-- Duration Badge -->
      <span v-if="duration !== null" class="duration-badge">
        {{ formatDuration(duration) }}
      </span>

      <!-- Status Badge -->
      <span v-if="statusText" class="status-badge" :class="statusClass">
        {{ statusText }}
      </span>
    </div>

    <!-- Child Events (if expanded) -->
    <div v-if="!collapsed && hasChildren" class="children">
      <HierarchicalEvent
        v-for="childId in event.children"
        :key="childId"
        :event="allEventsMap.get(childId)!"
        :all-events-map="allEventsMap"
        :collapsed-events="collapsedEvents"
        :selected-event-id="selectedEventId"
        :depth="depth + 1"
        @event-click="(e) => emit('event-click', e)"
        @toggle-collapse="(id) => emit('toggle-collapse', id)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { HookEvent } from '../types';

const props = defineProps<{
  event: HookEvent;
  allEventsMap: Map<string, HookEvent>;
  collapsedEvents: Set<string>;
  selectedEventId?: string | null;
  depth: number;
}>();

const emit = defineEmits<{
  'event-click': [event: HookEvent];
  'toggle-collapse': [eventId: string];
}>();

const hasChildren = computed(() => {
  return (props.event.children?.length || 0) > 0;
});

const collapsed = computed(() => {
  return props.collapsedEvents.has(props.event.event_id);
});

const isActive = computed(() => {
  return props.selectedEventId === props.event.event_id;
});

const eventIcon = computed(() => {
  const icons: Record<string, string> = {
    SessionStart: '🚀',
    SessionEnd: '🏁',
    UserPromptSubmit: '💬',
    PreToolUse: '🔧',
    PostToolUse: '✅',
    Stop: '⏹️',
    SubagentStop: '🤖',
    PreCompact: '🗜️',
    Notification: '🔔'
  };
  return icons[props.event.hook_event_type] || '📄';
});

const eventDisplayName = computed(() => {
  const type = props.event.hook_event_type;
  const payload = props.event.payload;

  if (type === 'PreToolUse') {
    const toolName = payload?.tool_name || 'Unknown';
    return `Pre: ${toolName}`;
  }

  if (type === 'PostToolUse') {
    const toolName = payload?.tool_name || 'Unknown';
    return `Post: ${toolName}`;
  }

  if (type === 'UserPromptSubmit') {
    const prompt = payload?.prompt || '';
    const preview = prompt.length > 60 ? prompt.substring(0, 60) + '...' : prompt;
    return `User: "${preview}"`;
  }

  if (type === 'SubagentStop') {
    const subagentType = props.event.skill_name || 'Subagent';
    return `${subagentType} completed`;
  }

  // Remove camelCase for readability
  return type.replace(/([A-Z])/g, ' $1').trim();
});

// Calculate duration if we have paired events (PreToolUse → PostToolUse)
const duration = computed((): number | null => {
  if (props.event.hook_event_type === 'PreToolUse') {
    const toolUseId = props.event.payload?.tool_use_id;
    if (!toolUseId) return null;

    // Find matching PostToolUse in children
    const postEvent = props.event.children
      ?.map(childId => props.allEventsMap.get(childId))
      .find(child =>
        child &&
        child.hook_event_type === 'PostToolUse' &&
        child.payload?.tool_use_id === toolUseId
      );

    if (postEvent?.timestamp && props.event.timestamp) {
      return postEvent.timestamp - props.event.timestamp;
    }
  }

  // For UserPromptSubmit, calculate time to Stop
  if (props.event.hook_event_type === 'UserPromptSubmit') {
    const stopEvent = props.event.children
      ?.map(childId => props.allEventsMap.get(childId))
      .find(child => child && child.hook_event_type === 'Stop');

    if (stopEvent?.timestamp && props.event.timestamp) {
      return stopEvent.timestamp - props.event.timestamp;
    }
  }

  return null;
});

function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  const minutes = Math.floor(ms / 60000);
  const seconds = Math.floor((ms % 60000) / 1000);
  return `${minutes}m ${seconds}s`;
}

const statusClass = computed(() => {
  if (props.event.hook_event_type === 'Stop') return 'success';
  if (props.event.humanInTheLoop?.type) return 'pending';
  if (props.event.payload?.error) return 'error';
  return 'default';
});

const statusText = computed(() => {
  if (props.event.humanInTheLoop?.type) {
    return 'HITL';
  }
  if (props.event.hook_event_type === 'Stop') {
    return 'Done';
  }
  if (props.event.payload?.error) {
    return 'Error';
  }
  return '';
});

function handleClick() {
  emit('event-click', props.event);
}

function toggleCollapse() {
  emit('toggle-collapse', props.event.event_id);
}
</script>

<style scoped>
.hierarchical-event {
  position: relative;
}

.event-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background 0.15s;
  font-size: 0.875rem;
  min-height: 2.5rem;
}

.event-header:hover {
  background: var(--theme-bg-tertiary, #1E1E1E);
}

.hierarchical-event.active .event-header {
  background: rgba(187, 160, 255, 0.1);
  border-left: 3px solid var(--theme-primary, #BBA0FF);
}

.collapse-btn {
  padding: 0;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1rem;
  height: 1rem;
  color: var(--theme-text-secondary, #B3B3B3);
  flex-shrink: 0;
}

.collapse-spacer {
  width: 1rem;
  flex-shrink: 0;
}

.collapse-btn:hover {
  color: var(--theme-text-primary, #F5F5F5);
}

.chevron {
  transition: transform 0.2s;
}

.chevron.collapsed {
  transform: rotate(-90deg);
}

.event-icon {
  font-size: 1rem;
  flex-shrink: 0;
  line-height: 1;
}

.event-name {
  flex: 1;
  color: var(--theme-text-primary, #F5F5F5);
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.duration-badge {
  padding: 0.125rem 0.5rem;
  font-size: 0.75rem;
  color: var(--theme-text-tertiary, #808080);
  background: var(--theme-bg-tertiary, #1E1E1E);
  border-radius: 0.25rem;
  font-family: 'JetBrains Mono', monospace;
  flex-shrink: 0;
}

.status-badge {
  padding: 0.125rem 0.5rem;
  font-size: 0.75rem;
  border-radius: 0.25rem;
  font-weight: 600;
  flex-shrink: 0;
}

.status-badge.success {
  color: var(--theme-accent-success, #4ADE80);
  background: rgba(74, 222, 128, 0.1);
}

.status-badge.pending {
  color: var(--theme-accent-warning, #FBBF24);
  background: rgba(251, 191, 36, 0.1);
  animation: pulse 2s ease-in-out infinite;
}

.status-badge.error {
  color: var(--theme-accent-error, #F87171);
  background: rgba(248, 113, 113, 0.1);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.children {
  /* Visual indicator of nesting */
  border-left: 2px solid var(--theme-border-secondary, #2A2A2A);
  margin-left: 1.5rem;
  margin-top: 0.25rem;
  margin-bottom: 0.25rem;
}

/* Depth-based opacity for visual hierarchy */
.depth-0 { }
.depth-1 { opacity: 0.98; }
.depth-2 { opacity: 0.95; }
.depth-3 { opacity: 0.92; }
.depth-4 { opacity: 0.89; }
.depth-5 { opacity: 0.86; }
</style>

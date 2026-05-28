<template>
  <div class="agent-lens-app h-screen flex flex-col bg-[var(--theme-bg-primary)] theme-agent-lens-oled">
    <!-- Top Header -->
    <header class="app-header">
      <div class="header-content">
        <div class="brand">
          <span class="brand-icon">👁️</span>
          <h1 class="brand-title">Agent Lens</h1>
          <span class="connection-status" :class="{ connected: isConnected }">
            {{ isConnected ? '●' : '○' }}
          </span>
        </div>

        <div class="header-actions">
          <button @click="showFilters = !showFilters" class="header-btn">
            🔍 Filters
          </button>
          <button @click="handleClearClick" class="header-btn">
            🗑️ Clear
          </button>
          <button @click="showThemeManager = true" class="header-btn">
            🎨 Themes
          </button>
        </div>
      </div>
    </header>

    <!-- Filters Panel (collapsible) -->
    <FilterPanel
      v-if="showFilters"
      :filters="filters"
      @update:filters="filters = $event"
    />

    <!-- Main Content: Dual-Pane Layout -->
    <div class="main-content">
      <DualPaneLayout
        :tabs="rightPaneTabs"
        :default-tab="'metrics'"
        :pending-h-i-t-l-count="pendingHITLCount"
        @collapse-all="collapseAll"
        @expand-all="expandAll"
        @tab-change="handleTabChange"
      >
        <!-- Process Timeline (Left Pane) -->
        <template #process-timeline>
          <SessionTimeline
            :events="filteredEvents"
            :collapsed-events="collapsedEvents"
            :selected-event-id="selectedEvent?.event_id"
            @event-click="handleEventClick"
            @toggle-collapse="toggleEventCollapse"
          />
        </template>

        <!-- Metrics Tab (Right Pane) -->
        <template #tab-metrics>
          <MetricsPanel
            :events="filteredEvents"
            :selected-event="selectedEvent"
          />
        </template>

        <!-- Legacy Tab (Right Pane) - Shows old swim lane view -->
        <template #tab-legacy>
          <div class="legacy-view">
            <LivePulseChart
              :events="filteredEvents"
              :filters="filters"
              :is-connected="isConnected"
              :total-events="filteredEvents.length"
              @update-unique-apps="uniqueAppNames = $event"
              @update-all-apps="allAppNames = $event"
              @update-time-range="currentTimeRange = $event"
              @clear-events="handleClearClick"
              @toggle-filters="showFilters = !showFilters"
              @open-theme-manager="showThemeManager = true"
            />

            <div v-if="selectedAgentLanes.length > 0" class="swim-lanes-container">
              <AgentSwimLaneContainer
                :selected-agents="selectedAgentLanes"
                :events="filteredEvents"
                :time-range="currentTimeRange"
                @update:selected-agents="selectedAgentLanes = $event"
              />
            </div>
          </div>
        </template>

        <!-- HITL Tab (Right Pane) -->
        <template #tab-hitl>
          <HITLPanel
            :pending-requests="pendingHITLRequests"
            @approve="handleHITLApprove"
            @edit="handleHITLEdit"
            @reject="handleHITLReject"
          />
        </template>
      </DualPaneLayout>
    </div>

    <!-- Theme Manager Modal -->
    <ThemeManager
      :is-open="showThemeManager"
      @close="showThemeManager = false"
    />

    <!-- Toast Notifications -->
    <ToastNotification
      v-for="(toast, index) in toasts"
      :key="toast.id"
      :index="index"
      :agent-name="toast.agentName"
      :agent-color="toast.agentColor"
      @dismiss="dismissToast(toast.id)"
    />

    <!-- Error Message -->
    <div
      v-if="error"
      class="error-banner"
    >
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import type { HookEvent, TimeRange } from './types';
import { useWebSocket } from './composables/useWebSocket';
import { useThemes } from './composables/useThemes';
import { useEventColors } from './composables/useEventColors';
import { useHITLNotifications } from './composables/useHITLNotifications';

// New Agent Lens components
import DualPaneLayout from './components/DualPaneLayout.vue';
import SessionTimeline from './components/SessionTimeline.vue';
import MetricsPanel from './components/MetricsPanel.vue';
import HITLPanel from './components/HITLPanel.vue';

// Existing components
import FilterPanel from './components/FilterPanel.vue';
import ThemeManager from './components/ThemeManager.vue';
import ToastNotification from './components/ToastNotification.vue';
import LivePulseChart from './components/LivePulseChart.vue';
import AgentSwimLaneContainer from './components/AgentSwimLaneContainer.vue';

// WebSocket connection
const { events, isConnected, error, clearEvents } = useWebSocket('ws://localhost:4000/stream');

// Theme management
useThemes();

// Event colors
const { getHexColorForApp } = useEventColors();

// Filters
const filters = ref({
  sourceApp: '',
  sessionId: '',
  eventType: ''
});

// Filtered events
const filteredEvents = computed(() => {
  return events.value.filter(event => {
    if (filters.value.sourceApp && event.source_app !== filters.value.sourceApp) {
      return false;
    }
    if (filters.value.sessionId && !event.session_id.includes(filters.value.sessionId)) {
      return false;
    }
    if (filters.value.eventType && event.hook_event_type !== filters.value.eventType) {
      return false;
    }
    return true;
  });
});

// UI state
const showFilters = ref(false);
const showThemeManager = ref(false);
const collapsedEvents = ref(new Set<string>());
const selectedEvent = ref<HookEvent | null>(null);

// Legacy view state
const uniqueAppNames = ref<string[]>([]);
const allAppNames = ref<string[]>([]);
const selectedAgentLanes = ref<string[]>([]);
const currentTimeRange = ref<TimeRange>('1m');

// Right pane tabs
const rightPaneTabs = computed(() => [
  { id: 'metrics', label: 'Metrics' },
  { id: 'legacy', label: 'Legacy View' },
  { id: 'hitl', label: 'HITL', badge: pendingHITLCount.value }
]);

// HITL tracking
interface HITLRequestData {
  hookEvent: HookEvent;
  receivedAt: number;
}

const pendingHITLRequests = computed((): HITLRequestData[] => {
  return filteredEvents.value
    .filter(e =>
      e.humanInTheLoop &&
      (!e.humanInTheLoopStatus || e.humanInTheLoopStatus.status === 'pending')
    )
    .map(event => ({
      hookEvent: event,
      receivedAt: event.timestamp || Date.now()
    }));
});

const pendingHITLCount = computed(() => pendingHITLRequests.value.length);

// HITL notifications
const { hasPermission, requestPermission, notifyHITLRequest } = useHITLNotifications();

// Watch for new HITL requests and notify
const seenHITLEvents = new Set<string>();
watch(() => filteredEvents.value, (newEvents) => {
  newEvents.forEach(event => {
    if (event.humanInTheLoop &&
        event.event_id &&
        !seenHITLEvents.has(event.event_id) &&
        (!event.humanInTheLoopStatus || event.humanInTheLoopStatus.status === 'pending')) {
      seenHITLEvents.add(event.event_id);

      // Request permission if not already granted
      if (!hasPermission.value) {
        requestPermission();
      }

      // Show notification
      notifyHITLRequest(event, () => {
        // On click, switch to HITL tab
        handleTabChange('hitl');
      });
    }
  });
}, { deep: true });

// Toast notifications
interface Toast {
  id: number;
  agentName: string;
  agentColor: string;
}
const toasts = ref<Toast[]>([]);
let toastIdCounter = 0;
const seenAgents = new Set<string>();

watch(uniqueAppNames, (newAppNames) => {
  newAppNames.forEach(appName => {
    if (!seenAgents.has(appName)) {
      seenAgents.add(appName);
      const toast: Toast = {
        id: toastIdCounter++,
        agentName: appName,
        agentColor: getHexColorForApp(appName)
      };
      toasts.value.push(toast);
    }
  });
}, { deep: true });

// Event handlers
function handleEventClick(event: HookEvent) {
  selectedEvent.value = event;
}

function toggleEventCollapse(eventId: string) {
  if (collapsedEvents.value.has(eventId)) {
    collapsedEvents.value.delete(eventId);
  } else {
    collapsedEvents.value.add(eventId);
  }
  // Trigger reactivity
  collapsedEvents.value = new Set(collapsedEvents.value);
}

function collapseAll() {
  filteredEvents.value.forEach(event => {
    if (event.event_id) {
      collapsedEvents.value.add(event.event_id);
    }
  });
  collapsedEvents.value = new Set(collapsedEvents.value);
}

function expandAll() {
  collapsedEvents.value.clear();
  collapsedEvents.value = new Set();
}

function handleTabChange(tabId: string) {
  console.log('Tab changed to:', tabId);
}

function handleClearClick() {
  clearEvents();
  selectedAgentLanes.value = [];
  selectedEvent.value = null;
  collapsedEvents.value.clear();
}

function dismissToast(id: number) {
  const index = toasts.value.findIndex(t => t.id === id);
  if (index !== -1) {
    toasts.value.splice(index, 1);
  }
}

// HITL Handlers
function handleHITLApprove(request: HITLRequestData, response?: string) {
  console.log('HITL Approved:', {
    eventId: request.hookEvent.event_id,
    response
  });

  // TODO: Send approval to agent via WebSocket
  // For now, just mark as responded in UI
  if (request.hookEvent.humanInTheLoopStatus) {
    request.hookEvent.humanInTheLoopStatus.status = 'responded';
    request.hookEvent.humanInTheLoopStatus.respondedAt = Date.now();
  } else {
    request.hookEvent.humanInTheLoopStatus = {
      status: 'responded',
      respondedAt: Date.now()
    };
  }

  // Show success toast
  showSuccessToast('Request approved');
}

function handleHITLEdit(request: HITLRequestData, response: string) {
  console.log('HITL Edited:', {
    eventId: request.hookEvent.event_id,
    response
  });

  // TODO: Send edited response to agent via WebSocket
  if (request.hookEvent.humanInTheLoopStatus) {
    request.hookEvent.humanInTheLoopStatus.status = 'responded';
    request.hookEvent.humanInTheLoopStatus.respondedAt = Date.now();
  } else {
    request.hookEvent.humanInTheLoopStatus = {
      status: 'responded',
      respondedAt: Date.now()
    };
  }

  showSuccessToast('Response submitted with edits');
}

function handleHITLReject(request: HITLRequestData) {
  console.log('HITL Rejected:', {
    eventId: request.hookEvent.event_id
  });

  // TODO: Send rejection to agent via WebSocket
  if (request.hookEvent.humanInTheLoopStatus) {
    request.hookEvent.humanInTheLoopStatus.status = 'responded';
    request.hookEvent.humanInTheLoopStatus.respondedAt = Date.now();
  } else {
    request.hookEvent.humanInTheLoopStatus = {
      status: 'responded',
      respondedAt: Date.now()
    };
  }

  showSuccessToast('Request rejected');
}

function showSuccessToast(message: string) {
  // Simple console log for now - could be enhanced with toast component
  console.log('✅', message);
}
</script>

<style scoped>
.agent-lens-app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.app-header {
  background: var(--theme-bg-secondary, #141414);
  border-bottom: 1px solid var(--theme-border-primary, #2A2A2A);
  flex-shrink: 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.brand-icon {
  font-size: 1.75rem;
  line-height: 1;
}

.brand-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--theme-text-primary, #F5F5F5);
  background: linear-gradient(135deg, var(--theme-primary, #BBA0FF), var(--chart-tertiary, #FF6B9D));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.connection-status {
  font-size: 1.25rem;
  color: var(--theme-text-tertiary, #808080);
  line-height: 1;
}

.connection-status.connected {
  color: var(--theme-accent-success, #4ADE80);
  animation: pulse-connection 2s ease-in-out infinite;
}

@keyframes pulse-connection {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.header-btn {
  padding: 0.5rem 1rem;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
  background: transparent;
  color: var(--theme-text-primary, #F5F5F5);
  cursor: pointer;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.header-btn:hover {
  background: var(--theme-bg-tertiary, #1E1E1E);
  border-color: var(--theme-primary, #BBA0FF);
}

.main-content {
  flex: 1;
  overflow: hidden;
}

.legacy-view {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
}

.swim-lanes-container {
  flex: 1;
  overflow-y: auto;
}

.hitl-placeholder,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
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

.error-banner {
  position: fixed;
  bottom: 1rem;
  left: 1rem;
  right: 1rem;
  max-width: 600px;
  margin: 0 auto;
  padding: 1rem 1.5rem;
  background: var(--theme-error-bg, rgba(248, 113, 113, 0.1));
  border: 1px solid var(--theme-accent-error, #F87171);
  color: var(--theme-accent-error, #F87171);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  z-index: 1000;
}
</style>

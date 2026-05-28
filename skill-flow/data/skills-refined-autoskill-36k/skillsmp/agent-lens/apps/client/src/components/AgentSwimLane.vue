<template>
  <div class="agent-swim-lane">
    <div class="lane-header">
      <div class="header-left">
        <div class="agent-label-container">
          <span class="agent-label-app" :style="{
            backgroundColor: getHexColorForApp(appName),
            borderColor: getHexColorForApp(appName)
          }">
            <span class="font-mono text-xs">{{ appName }}</span>
          </span>
          <span class="agent-label-session" :style="{
            backgroundColor: getHexColorForSession(sessionId),
            borderColor: getHexColorForSession(sessionId)
          }">
            <span class="font-mono text-xs">{{ sessionId }}</span>
          </span>
        </div>
        <div v-if="modelName" class="model-badge" :title="`Model: ${modelName}`">
          <Brain :size="14" :stroke-width="2.5" />
          <span class="text-xs font-bold">{{ formatModelName(modelName) }}</span>
        </div>
        <div class="event-count-badge"
          :title="`Total events in the last ${timeRange === '1m' ? '1 minute' : timeRange === '3m' ? '3 minutes' : '5 minutes'}`">
          <Zap :size="14" :stroke-width="2.5" class="flex-shrink-0" />
          <span class="text-xs font-bold">
            {{ totalEventCount }} Events
          </span>
        </div>
        <div class="tool-call-badge"
          :title="`Tool calls in the last ${timeRange === '1m' ? '1 minute' : timeRange === '3m' ? '3 minutes' : '5 minutes'}`">
          <Wrench :size="14" :stroke-width="2.5" class="flex-shrink-0" />
          <span class="text-xs font-bold">
            {{ toolCallCount }} Tool Calls
          </span>
        </div>
        <div
          class="avg-time-badge flex items-center gap-1.5 px-2 py-2 bg-[var(--theme-bg-tertiary)] rounded-lg border border-[var(--theme-border-primary)] shadow-sm min-h-[28px]"
          :title="`Average time between events in the last ${timeRange === '1m' ? '1 minute' : timeRange === '3m' ? '3 minutes' : '5 minutes'}`">
          <Clock :size="16" :stroke-width="2.5" class="flex-shrink-0" />
          <span class="text-sm font-bold text-[var(--theme-text-primary)]">
            Avg Gap: {{ formatGap(agentEventTimingMetrics.avgGap) }}
          </span>
        </div>
        <button @click="emit('close')" class="close-btn" title="Remove this swim lane">
          <X :size="16" :stroke-width="2.5" />
        </button>
      </div>
    </div>
    <div ref="chartContainer" class="chart-wrapper" :style="{ height: chartHeight + 'px' }">
      <canvas ref="canvas" class="w-full cursor-crosshair" :style="{ height: chartHeight + 'px' }"
        @mousemove="handleMouseMove" @mouseleave="handleMouseLeave" role="img" :aria-label="chartAriaLabel"></canvas>
      <div v-if="tooltip.visible"
        class="absolute bg-gradient-to-r from-[var(--theme-primary)] to-[var(--theme-primary-dark)] text-white px-2 py-1.5 rounded-lg text-xs pointer-events-none z-10 shadow-lg border border-[var(--theme-primary-light)] font-bold drop-shadow-md"
        :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }">
        {{ tooltip.text }}
      </div>
      <div v-if="!hasData" class="absolute inset-0 flex items-center justify-center">
        <p class="flex items-center gap-2 text-[var(--theme-text-tertiary)] text-sm font-semibold">
          <Loader2 :size="16" :stroke-width="2.5" class="animate-spin" />
          Waiting for events...
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue';
import type { HookEvent, TimeRange } from '../types';
import { useSwimLaneEvents } from '../composables/useSwimLaneEvents';
import { createSwimLaneRenderer, type SwimLaneDimensions, type SwimLaneConfig } from '../utils/swimLaneRenderer';
import { useEventColors } from '../composables/useEventColors';
import { Brain, Wrench, Clock, X, Zap, Loader2 } from 'lucide-vue-next';

const props = withDefaults(defineProps<{
  agentName: string; // Format: "app:session" (e.g., "claude-code:a1b2c3d4")
  events: HookEvent[];
  timeRange: TimeRange;
  colorMode?: 'app' | 'event-type'; // Color bubbles by app or event type
}>(), {
  colorMode: 'event-type' // Default to event-type for better distinction
});

const emit = defineEmits<{
  close: [];
}>();

const canvas = ref<HTMLCanvasElement>();
const chartContainer = ref<HTMLDivElement>();
const tick = ref(0); // Force reactivity updates

const chartHeight = computed(() => {
  const events = getFilteredEvents.value;
  const baseHeight = 120;
  const minHeight = 80;

  if (events.length === 0) {
    return minHeight;
  }

  // Calculate height based on event count
  // Use logarithmic scaling to prevent excessive growth with many events
  const densityFactor = Math.log10(events.length + 1) * 30;
  const calculatedHeight = baseHeight + densityFactor;

  // No upper bound - let it grow as needed
  return Math.max(minHeight, Math.round(calculatedHeight));
});

// Format gap time in ms to readable string (e.g., "125ms" or "1.2s")
const formatGap = (gapMs: number): string => {
  if (gapMs === 0) return '—';
  if (gapMs < 1000) {
    return `${Math.round(gapMs)}ms`;
  }
  return `${(gapMs / 1000).toFixed(1)}s`;
};

// Extract app name and session ID from agent ID for display
const appName = computed(() => props.agentName.split(':')[0]);
const sessionId = computed(() => props.agentName.split(':')[1]);

// Get model name from most recent event for this agent
const modelName = computed(() => {
  const [targetApp, targetSession] = props.agentName.split(':');
  const agentEvents = props.events
    .filter(e => e.source_app === targetApp && e.session_id.slice(0, 8) === targetSession)
    .filter(e => e.model_name); // Only events with model_name

  if (agentEvents.length === 0) return null;

  // Get most recent event's model name
  const mostRecent = agentEvents[agentEvents.length - 1];
  return mostRecent.model_name;
});

// Format model name for display (e.g., "claude-haiku-4-5-20251001" -> "haiku-4-5")
const formatModelName = (name: string | null | undefined): string => {
  if (!name) return '';

  const parts = name.split('-');
  if (parts.length >= 4) {
    return `${parts[1]}-${parts[2]}-${parts[3]}`;
  }
  return name;
};

// NEW: Use swim lane events (raw events, no aggregation)
const {
  getFilteredEvents,
  addEvent,
  setTimeRange,
  cleanup: cleanupEventData,
  totalEventCount: eventsCount,
  toolCallCount: toolsCount,
  eventTimingMetrics: agentEventTimingMetrics,
  currentConfig
} = useSwimLaneEvents(props.agentName);


let renderer: ReturnType<typeof createSwimLaneRenderer> | null = null;
let resizeObserver: ResizeObserver | null = null;
let animationFrame: number | null = null;
let dirtyInterval: number | null = null;
const processedEventIds = new Set<string>();
const isDirty = ref(true); // Track if render is needed

const { getHexColorForApp, getHexColorForSession, getEventTypeColor } = useEventColors();

const hasData = computed(() => eventsCount.value > 0);
const totalEventCount = computed(() => eventsCount.value);
const toolCallCount = computed(() => toolsCount.value);

const chartAriaLabel = computed(() => {
  const [app, session] = props.agentName.split(':');
  return `Activity chart for ${app} (session: ${session}) showing ${totalEventCount.value} events`;
});

const tooltip = ref({
  visible: false,
  x: 0,
  y: 0,
  text: ''
});

const getThemeColor = (property: string): string => {
  const style = getComputedStyle(document.documentElement);
  const color = style.getPropertyValue(`--theme-${property}`).trim();
  return color || '#3B82F6';
};

const getActiveConfig = (): SwimLaneConfig => {
  return {
    bubbleHeight: 28,        // Height of each event bubble
    bubbleMinWidth: 100,     // Minimum bubble width
    bubbleMaxWidth: 300,     // Maximum bubble width
    bubbleSpacing: 8,        // Minimum spacing between bubbles
    iconSize: 16,            // Size of event type icon
    animationDuration: 400,  // Duration of entrance animation (ms)
    colors: {
      primary: getThemeColor('primary'),
      glow: getThemeColor('primary-light'),
      axis: getThemeColor('border-primary'),
      text: getThemeColor('text-tertiary')
    }
  };
};


const getDimensions = (): SwimLaneDimensions => {
  const width = chartContainer.value?.offsetWidth || 800;
  return {
    width,
    height: chartHeight.value,
    padding: {
      top: 10,
      right: 10,
      bottom: 10,  // Reduced - less needed for swim lanes
      left: 10
    }
  };
};

const render = () => {
  if (!renderer || !canvas.value) return;

  // Force reactivity by reading tick
  tick.value;

  // Get raw events
  const events = getFilteredEvents.value;

  // Calculate fresh time bounds (not cached)
  const now = Date.now();
  const duration = currentConfig.value.duration;
  const bounds = { start: now - duration, end: now };

  // Set time range for X-axis positioning
  renderer.setTimeRange(bounds.start, bounds.end);

  // Set events with color mapping based on colorMode
  renderer.setEvents(events, (event: HookEvent) => {
    if (props.colorMode === 'event-type') {
      // Color by event type for better visual distinction
      return getEventTypeColor(event.hook_event_type);
    } else {
      // Color by app (original behavior)
      return getHexColorForApp(event.source_app);
    }
  });

  // Force canvas update by resizing and recalculating layout
  renderer.resize(getDimensions());


  // Render the swim lane
  renderer.clear();
  renderer.drawBackground();
  renderer.drawAxes();
  renderer.drawTimeLabels(props.timeRange);
  renderer.drawBubbles();

  // Mark as clean after rendering
  isDirty.value = false;
};

const handleResize = () => {
  if (!renderer || !canvas.value) return;

  const dimensions = getDimensions();
  renderer.resize(dimensions);
  isDirty.value = true; // Mark dirty to trigger re-render
};

const processNewEvents = () => {
  const currentEvents = props.events;
  const newEventsToProcess: HookEvent[] = [];

  // Find events that haven't been processed yet
  currentEvents.forEach(event => {
    const eventKey = `${event.id}-${event.timestamp}`;
    if (!processedEventIds.has(eventKey)) {
      processedEventIds.add(eventKey);
      newEventsToProcess.push(event);
    }
  });

  // Parse agent ID to get app and session
  const [targetApp, targetSession] = props.agentName.split(':');

  // Process new events (filter by agent ID: app:session)
  newEventsToProcess.forEach(event => {
    if (
      event.hook_event_type !== 'refresh' &&
      event.hook_event_type !== 'initial' &&
      event.source_app === targetApp &&
      event.session_id.slice(0, 8) === targetSession
    ) {
      addEvent(event);
    }
  });

  // Clean up old event IDs to prevent memory leak
  const currentEventIds = new Set(currentEvents.map(e => `${e.id}-${e.timestamp}`));
  processedEventIds.forEach(id => {
    if (!currentEventIds.has(id)) {
      processedEventIds.delete(id);
    }
  });

  isDirty.value = true; // Mark dirty to trigger re-render
};

// Watch for new events - immediate: true ensures we process existing events on mount
watch(() => props.events, processNewEvents, { deep: true, immediate: true });

// Watch for time range changes - update internal timeRange and trigger re-render
watch(() => props.timeRange, (newRange) => {
  setTimeRange(newRange);
  isDirty.value = true; // Mark dirty to trigger re-render
}, { immediate: true });

// Watch for new events to trigger auto-scroll
watch(() => props.events.length, (newLength, oldLength) => {
  if (newLength > oldLength) {
    isDirty.value = true;
  }
});

// Watch for height changes to reinitialize renderer
watch(chartHeight, () => {
  if (canvas.value && chartContainer.value) {
    // Reinitialize renderer with new dimensions
    const dimensions = getDimensions();
    const config = getActiveConfig();

    renderer = createSwimLaneRenderer(canvas.value, dimensions, config);
    isDirty.value = true;
  }
}, { immediate: true });


const handleMouseMove = (event: MouseEvent) => {
  if (!canvas.value || !chartContainer.value || !renderer) return;

  const rect = canvas.value.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;

  // Check if mouse is over a bubble
  const bubble = renderer.getBubbleAtPosition(x, y);

  if (bubble) {
    // Build tooltip text
    const eventType = bubble.event.hook_event_type;
    const toolName = bubble.event.payload?.tool_name || '';
    const session = bubble.event.session_id.slice(0, 8);

    let tooltipText = `${eventType}`;
    if (toolName) {
      tooltipText += ` • ${toolName}`;
    }
    tooltipText += ` (${session})`;

    tooltip.value = {
      visible: true,
      x: event.clientX - rect.left,
      y: event.clientY - rect.top - 30,
      text: tooltipText
    };
  } else {
    tooltip.value.visible = false;
  }
};

const handleMouseLeave = () => {
  tooltip.value.visible = false;
};

// Watch for theme changes
const themeObserver = new MutationObserver(() => {
  if (renderer) {
    isDirty.value = true; // Mark dirty to trigger re-render
  }
});

onMounted(() => {
  if (!canvas.value || !chartContainer.value) {
    console.error('❌ Canvas or container not found!', { canvas: canvas.value, container: chartContainer.value });
    return;
  }

  const dimensions = getDimensions();
  const config = getActiveConfig();

  try {
    renderer = createSwimLaneRenderer(canvas.value, dimensions, config);
  } catch (error) {
    console.error('❌ Error creating renderer:', error);
  }

  // Set up resize observer
  resizeObserver = new ResizeObserver(handleResize);
  resizeObserver.observe(chartContainer.value);

  // Observe theme changes
  themeObserver.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  });

  // Initial render
  render();

  // Force re-render every 200ms by updating tick (forces time bounds recalc)
  dirtyInterval = window.setInterval(() => {
    tick.value++;
    isDirty.value = true;
  }, 1000);

  // Start optimized render loop with FPS limiting and dirty flag
  let lastRenderTime = 0;
  const targetFPS = 30;
  const frameInterval = 1000 / targetFPS;

  const renderLoop = (currentTime: number) => {
    const deltaTime = currentTime - lastRenderTime;

    // Always render if dirty, or periodically for auto-scroll
    const shouldRender = isDirty.value || deltaTime >= frameInterval * 200; // Auto-scroll every 10 frames

    if (shouldRender && deltaTime >= frameInterval) {
      render();
      lastRenderTime = currentTime - (deltaTime % frameInterval);
    }

    requestAnimationFrame(renderLoop);
  };

  requestAnimationFrame(renderLoop);

});


onUnmounted(() => {
  cleanupEventData();

  if (resizeObserver && chartContainer.value) {
    resizeObserver.disconnect();
  }

  if (animationFrame) {
    cancelAnimationFrame(animationFrame);
  }

  if (dirtyInterval) {
    clearInterval(dirtyInterval);
  }

  themeObserver.disconnect();
});
</script>

<style scoped>
.agent-swim-lane {
  width: 100%;
  background: transparent;
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
  /* Add spacing to prevent label overlap with next swimlane */
}

.lane-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  font-weight: 600;
  padding: 0 7px;
  gap: 8px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 6px;
}

.agent-label-container {
  display: flex;
  align-items: center;
  gap: 0;
  white-space: nowrap;
}

.agent-label-app,
.agent-label-session {
  padding: 8px 8px;
  border-radius: 0;
  border: 1px solid currentColor;
  color: white;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: inline-flex;
  align-items: center;
  min-height: 28px;
}

.agent-label-app {
  border-radius: 3px 0 0 3px;
}

.agent-label-session {
  border-radius: 0 3px 3px 0;
  border-left: none;
}

.model-badge,
.event-count-badge,
.tool-call-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 8px;
  background: var(--theme-bg-tertiary);
  border: 1px solid var(--theme-border-primary);
  border-radius: 8px;
  color: var(--theme-text-primary);
  font-size: 11px;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  min-height: 28px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.model-badge {
  cursor: default;
}

.event-count-badge:hover,
.tool-call-badge:hover,
.model-badge:hover {
  background: var(--theme-bg-quaternary);
  border-color: var(--theme-primary);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.avg-time-badge {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: var(--theme-text-tertiary);
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 3px;
  transition: all 0.2s;
  flex-shrink: 0;
}

.close-btn:hover {
  background: var(--theme-bg-quaternary);
  color: var(--theme-text-primary);
  transform: scale(1.1);
}

.chart-wrapper {
  position: relative;
  width: 100%;
  border: 1px solid var(--theme-border-primary);
  border-radius: 6px;
  overflow: hidden;
  background: var(--theme-bg-tertiary);
}

.chart-wrapper::-webkit-scrollbar {
  width: 6px;
}

.chart-wrapper::-webkit-scrollbar-track {
  background: transparent;
}

.chart-wrapper::-webkit-scrollbar-thumb {
  background: var(--theme-primary);
  border-radius: 3px;
}

.chart-wrapper::-webkit-scrollbar-thumb:hover {
  background: var(--theme-primary-dark);
}
</style>

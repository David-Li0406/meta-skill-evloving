import { ref, computed } from 'vue';
import type { HookEvent, TimeRange } from '../types';

/**
 * useSwimLaneEvents - Event Storage for Swim Lane Visualization
 *
 * Key difference from useChartData:
 * - NO aggregation into time buckets
 * - Returns individual events, not aggregated counts
 * - Events positioned by exact timestamp (not bucket)
 *
 * This composable provides filtered, sorted raw events for the SwimLaneRenderer.
 */

interface TimeRangeConfig {
  duration: number; // milliseconds
}

export function useSwimLaneEvents(agentIdFilter?: string) {
  const timeRange = ref<TimeRange>('1m');
  const allEvents = ref<HookEvent[]>([]);

  // Time range configurations (duration only, no buckets)
  const timeRangeConfig: Record<TimeRange, TimeRangeConfig> = {
    '1m': { duration: 60 * 1000 },        // 1 minute
    '3m': { duration: 3 * 60 * 1000 },    // 3 minutes
    '5m': { duration: 5 * 60 * 1000 },    // 5 minutes
    '10m': { duration: 10 * 60 * 1000 }   // 10 minutes
  };

  const currentConfig = computed(() => timeRangeConfig[timeRange.value]);

  // Parse agent ID filter (format: "app:session")
  const parseAgentId = (agentId: string): { app: string; session: string } | null => {
    const parts = agentId.split(':');
    if (parts.length === 2) {
      return { app: parts[0], session: parts[1] };
    }
    return null;
  };

  const agentIdParsed = agentIdFilter ? parseAgentId(agentIdFilter) : null;

  /**
   * Add a new event to the store
   * Events are filtered by agent ID (if specified) before storage
   */
  const addEvent = (event: HookEvent) => {
    if (!event.timestamp) return;

    // Skip if event doesn't match agent ID filter
    if (agentIdParsed) {
      if (event.source_app !== agentIdParsed.app) {
        return;
      }
      if (event.session_id.slice(0, 8) !== agentIdParsed.session) {
        return;
      }
    }

    // Add to event store
    allEvents.value.push(event);

    // Clean old events immediately after adding
    cleanOldEvents();
  };

  /**
   * Remove events older than the maximum time range (10 minutes)
   * This prevents unbounded memory growth
   */
  const cleanOldEvents = () => {
    const now = Date.now();
    const maxDuration = 10 * 60 * 1000; // Keep events for max 10 minutes
    const cutoffTime = now - maxDuration;

    allEvents.value = allEvents.value.filter(
      event => event.timestamp && event.timestamp >= cutoffTime
    );
  };

  /**
   * Get filtered events for current time range
   * Returns raw events (NOT aggregated) sorted chronologically
   */
  const getFilteredEvents = computed(() => {
    const now = Date.now();
    const cutoffTime = now - currentConfig.value.duration;

    const filtered = allEvents.value
      .filter(event => event.timestamp && event.timestamp >= cutoffTime)
      .sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0));

    return filtered;
  });

  /**
   * Get time range boundaries (for SwimLaneRenderer positioning)
   */
  const getTimeRangeBounds = computed(() => {
    const now = Date.now();
    const start = now - currentConfig.value.duration;
    return { start, end: now };
  });

  /**
   * Set time range (1m, 3m, 5m, 10m)
   */
  const setTimeRange = (range: TimeRange) => {
    timeRange.value = range;
    // No re-aggregation needed - just changes the filter cutoff
  };

  /**
   * Clear all stored events
   */
  const clearData = () => {
    allEvents.value = [];
  };

  // Auto-clean old events every second
  const cleanupInterval = setInterval(() => {
    cleanOldEvents();
  }, 1000);

  /**
   * Cleanup on unmount
   */
  const cleanup = () => {
    clearInterval(cleanupInterval);
  };

  // === Computed Metrics (same as useChartData for compatibility) ===

  /**
   * Total event count in current time window
   */
  const totalEventCount = computed(() => getFilteredEvents.value.length);

  /**
   * Tool call count (PreToolUse events) in current time window
   */
  const toolCallCount = computed(() => {
    return getFilteredEvents.value.filter(e => e.hook_event_type === 'PreToolUse').length;
  });

  /**
   * Event timing metrics (min, max, average gap between events in ms)
   */
  const eventTimingMetrics = computed(() => {
    const events = getFilteredEvents.value;

    if (events.length < 2) {
      return { minGap: 0, maxGap: 0, avgGap: 0 };
    }

    // Calculate gaps between consecutive events
    const gaps: number[] = [];
    for (let i = 1; i < events.length; i++) {
      const gap = (events[i].timestamp || 0) - (events[i - 1].timestamp || 0);
      if (gap > 0) {
        gaps.push(gap);
      }
    }

    if (gaps.length === 0) {
      return { minGap: 0, maxGap: 0, avgGap: 0 };
    }

    const minGap = Math.min(...gaps);
    const maxGap = Math.max(...gaps);
    const avgGap = gaps.reduce((a, b) => a + b, 0) / gaps.length;

    return { minGap, maxGap, avgGap };
  });

  /**
   * Get unique agent IDs in current time window
   */
  const uniqueAgentIdsInWindow = computed(() => {
    const uniqueAgents = new Set<string>();

    getFilteredEvents.value.forEach(event => {
      const agentId = `${event.source_app}:${event.session_id.slice(0, 8)}`;
      uniqueAgents.add(agentId);
    });

    return Array.from(uniqueAgents);
  });

  /**
   * Get ALL unique agent IDs ever seen
   */
  const allUniqueAgentIds = computed(() => {
    const uniqueAgents = new Set<string>();

    allEvents.value.forEach(event => {
      const agentId = `${event.source_app}:${event.session_id.slice(0, 8)}`;
      uniqueAgents.add(agentId);
    });

    return Array.from(uniqueAgents);
  });

  return {
    // Core data access
    getFilteredEvents,
    getTimeRangeBounds,

    // Event management
    addEvent,
    clearData,
    cleanup,

    // Configuration
    timeRange,
    setTimeRange,
    currentConfig,

    // Metrics (for compatibility with existing components)
    totalEventCount,
    toolCallCount,
    eventTimingMetrics,
    uniqueAgentIdsInWindow,
    allUniqueAgentIds
  };
}

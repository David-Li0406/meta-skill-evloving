#!/usr/bin/env bun
/**
 * File-based Event Streaming (In-Memory Only) - Agent Lens Edition
 * Watches JSONL files from capture-all-events.ts hook
 * NO DATABASE - streams directly to WebSocket clients
 * Fresh start each time - no persistence
 *
 * NEW in Agent Lens:
 * - Builds parent-child hierarchy from event_id/parent_event_id fields
 * - Calculates depth for visualization
 * - Enriches events with children array
 *
 * ENVIRONMENT VARIABLES:
 * - PAI_DIR: Path to your PAI directory (defaults to ~/.claude/)
 *   Example: export PAI_DIR="/Users/yourname/.claude"
 *
 * Reads events from: ~/.claude/history/raw-outputs/YYYY-MM/YYYY-MM-DD_all-events.jsonl
 */

import { watch, existsSync } from 'fs';
import { readFileSync } from 'fs';
import { join } from 'path';
import type { HookEvent } from './types';
import { MAX_EVENTS_IN_MEMORY, HISTORY_DIR } from './config';

// In-memory event store (last N events only)
const MAX_EVENTS = MAX_EVENTS_IN_MEMORY;

// Valid event types (whitelist) - must match hook configuration
const VALID_EVENT_TYPES = [
  'SessionStart',
  'SessionEnd',
  'PreToolUse',
  'PostToolUse',
  'UserPromptSubmit',
  'Stop',
  'SubagentStop',
  'Notification',
  'PreCompact'
] as const;
const events: HookEvent[] = [];

// Basic ingestion health tracking
let ingestionStartedAt: number | null = null;
let lastEventTimestamp: number | null = null;

// Track the last read position for each file
const filePositions = new Map<string, number>();

// Track which files we're currently watching
const watchedFiles = new Set<string>();

// Callback for when new events arrive (for WebSocket broadcasting)
let onEventsReceived: ((events: HookEvent[]) => void) | null = null;

/**
 * Validate event structure to ensure all required fields are present
 */
function isValidHookEvent(event: any): event is HookEvent {
  // Check required fields
  if (typeof event.source_app !== 'string' || !event.source_app.trim()) {
    console.warn('⚠️  Invalid event: missing or invalid source_app');
    return false;
  }

  if (typeof event.session_id !== 'string' || !event.session_id.trim()) {
    console.warn('⚠️  Invalid event: missing or invalid session_id');
    return false;
  }

  // Validate session ID format
  if (event.session_id.length < 3 || event.session_id.length > 100) {
    console.warn(`⚠️  Invalid event: session_id length out of bounds (${event.session_id.length})`);
    return false;
  }

  if (typeof event.hook_event_type !== 'string' || !event.hook_event_type.trim()) {
    console.warn('⚠️  Invalid event: missing or invalid hook_event_type');
    return false;
  }

  // Validate event type is in whitelist
  if (!VALID_EVENT_TYPES.includes(event.hook_event_type as any)) {
    console.warn(`⚠️  Invalid event: unknown hook_event_type "${event.hook_event_type}"`);
    return false;
  }

  if (typeof event.payload !== 'object' || event.payload === null) {
    console.warn('⚠️  Invalid event: missing or invalid payload');
    return false;
  }

  if (typeof event.timestamp !== 'number' || event.timestamp <= 0) {
    console.warn('⚠️  Invalid event: missing or invalid timestamp');
    return false;
  }

  // Timestamp sanity checks
  const now = Date.now();
  const oneHourInFuture = now + (60 * 60 * 1000);
  const oneYearInPast = now - (365 * 24 * 60 * 60 * 1000);

  if (event.timestamp > oneHourInFuture) {
    console.warn(`⚠️  Invalid event: timestamp is more than 1 hour in the future`);
    return false;
  }

  if (event.timestamp < oneYearInPast) {
    console.warn(`⚠️  Invalid event: timestamp is more than 1 year in the past`);
    return false;
  }

  if (typeof event.timestamp_aedt !== 'string' || !event.timestamp_aedt.trim()) {
    console.warn('⚠️  Invalid event: missing or invalid timestamp_aedt');
    return false;
  }

  return true;
}

/**
 * Get the path to today's all-events file
 */
function getTodayEventsFile(): string {
  // Use configured history directory for event data
  const historyDir = HISTORY_DIR;
  const now = new Date();
  // Convert to Australia/Sydney timezone using Intl
  const formatter = new Intl.DateTimeFormat('en-AU', {
    timeZone: 'Australia/Sydney',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
  const parts = formatter.formatToParts(now);
  const year = parts.find(p => p.type === 'year')!.value;
  const month = parts.find(p => p.type === 'month')!.value;
  const day = parts.find(p => p.type === 'day')!.value;

  const monthDir = join(historyDir, 'raw-outputs', `${year}-${month}`);
  return join(monthDir, `${year}-${month}-${day}_all-events.jsonl`);
}

/**
 * Read new events from a JSONL file starting from a given position
 */
function readNewEvents(filePath: string): HookEvent[] {
  if (!existsSync(filePath)) {
    console.log(`⚠️  File does not exist: ${filePath}`);
    return [];
  }

  const lastPosition = filePositions.get(filePath) || 0;

  try {
    const content = readFileSync(filePath, 'utf-8');
    const newContent = content.slice(lastPosition);

    console.log(`📖 Reading from position ${lastPosition} to ${content.length} (${newContent.length} bytes)`);

    // Update position to end of file
    filePositions.set(filePath, content.length);

    if (!newContent.trim()) {
      console.log(`   No new content to read`);
      return [];
    }

    // Parse JSONL - one JSON object per line
    const lines = newContent.trim().split('\n');
    const newEvents: HookEvent[] = [];

    console.log(`   Parsing ${lines.length} line(s)`);

    for (const line of lines) {
      if (!line.trim()) continue;

      try {
        const event = JSON.parse(line);

        // Validate event structure before adding
        if (!isValidHookEvent(event)) {
          console.error(`⚠️  Skipping invalid event: ${line.slice(0, 100)}...`);
          continue;
        }

        // Add auto-incrementing ID for UI
        event.id = events.length + newEvents.length + 1;
        newEvents.push(event);
      } catch (error) {
        console.error(`Failed to parse line: ${line.slice(0, 100)}...`, error);
      }
    }

    console.log(`   Parsed ${newEvents.length} event(s)`);
    return newEvents;
  } catch (error) {
    console.error(`Error reading file ${filePath}:`, error);
    return [];
  }
}

/**
 * Build parent-child hierarchy for events
 * Mutates events to add 'children' and 'depth' fields
 */
function buildHierarchy(eventsToProcess: HookEvent[]): void {
  // Create event map for fast lookups
  const eventMap = new Map<string, HookEvent>();

  // First pass: index all events and initialize children arrays
  eventsToProcess.forEach(event => {
    event.children = [];
    eventMap.set(event.event_id, event);
  });

  // Second pass: link parents to children
  eventsToProcess.forEach(event => {
    if (event.parent_event_id) {
      const parent = eventMap.get(event.parent_event_id);
      if (parent) {
        parent.children = parent.children || [];
        parent.children.push(event.event_id);
      } else {
        // Parent not found (might be outside our window)
        console.warn(`⚠️  Parent event ${event.parent_event_id} not found for event ${event.event_id}`);
      }
    }
  });

  // Third pass: calculate depth
  function calculateDepth(eventId: string, visited = new Set<string>()): number {
    if (visited.has(eventId)) {
      console.warn(`⚠️  Circular reference detected for event ${eventId}`);
      return 0; // Prevent infinite loops
    }
    visited.add(eventId);

    const event = eventMap.get(eventId);
    if (!event || !event.parent_event_id) {
      return 0; // Root event or parent not found
    }

    const parent = eventMap.get(event.parent_event_id);
    if (!parent) {
      return 0; // Parent outside our window
    }

    return 1 + calculateDepth(event.parent_event_id, visited);
  }

  eventsToProcess.forEach(event => {
    event.depth = calculateDepth(event.event_id);
  });
}

/**
 * Add events to in-memory store (keeping last MAX_EVENTS only)
 */
function storeEvents(newEvents: HookEvent[]): void {
  if (newEvents.length === 0) return;

  // Add to in-memory array
  events.push(...newEvents);

  // Track when we most recently saw an event
  lastEventTimestamp = Date.now();

  // Keep only last MAX_EVENTS
  if (events.length > MAX_EVENTS) {
    events.splice(0, events.length - MAX_EVENTS);
  }

  // Build hierarchy for ALL events in memory (including old ones)
  // This ensures parent-child links work even across batches
  buildHierarchy(events);

  console.log(`✅ Received ${newEvents.length} event(s) (${events.length} in memory, hierarchy built)`);

  // Notify subscribers (WebSocket clients)
  // Send enriched events with hierarchy metadata
  if (onEventsReceived) {
    onEventsReceived(newEvents);
  }
}

/**
 * Load all existing events from today's file into memory for initial WebSocket sends
 */
function loadExistingEvents(filePath: string): void {
  if (!existsSync(filePath)) {
    console.log(`⚠️  Today's file does not exist yet: ${filePath}`);
    return;
  }

  try {
    const content = readFileSync(filePath, 'utf-8');
    if (!content.trim()) {
      console.log(`📂 Today's file is empty`);
      return;
    }

    const lines = content.trim().split('\n');
    const loadedEvents: HookEvent[] = [];

    for (const line of lines) {
      if (!line.trim()) continue;
      try {
        const event = JSON.parse(line);
        if (isValidHookEvent(event)) {
          // Add auto-incrementing ID for UI
          event.id = events.length + loadedEvents.length + 1;
          loadedEvents.push(event);
        }
      } catch (err) {
        console.warn(`⚠️  Failed to parse event line: ${err}`);
      }
    }

    // Store in memory (keep most recent MAX_EVENTS_IN_MEMORY)
    const maxEvents = MAX_EVENTS_IN_MEMORY;
    events.push(...loadedEvents.slice(-maxEvents));
    console.log(`📂 Loaded ${loadedEvents.length} existing events into memory (kept last ${events.length})`);

    // Set file position to END so we only read NEW events from now on
    filePositions.set(filePath, content.length);
  } catch (error) {
    console.error(`❌ Failed to load existing events from ${filePath}:`, error);
  }
}

/**
 * Watch a file for changes and stream new events
 */
function watchFile(filePath: string): void {
  if (watchedFiles.has(filePath)) {
    return; // Already watching
  }

  console.log(`👀 Watching: ${filePath}`);

  // Check if file exists - if not, poll until it does
  if (!existsSync(filePath)) {
    console.log(`⏳ File doesn't exist yet, will poll every 5s until created...`);
    const pollInterval = setInterval(() => {
      if (existsSync(filePath)) {
        console.log(`✅ File created! Starting watch...`);
        clearInterval(pollInterval);
        watchFile(filePath); // Recursive call now that file exists
      }
    }, 5000); // Check every 5 seconds
    return;
  }

  watchedFiles.add(filePath);

  // Set file position to END of file - only read NEW events from now on
  // Do NOT load historical events from before server start
  const content = readFileSync(filePath, 'utf-8');
  filePositions.set(filePath, content.length);
  console.log(`📍 Positioned at end of file - only new events will be captured`);

  // Watch for changes
  const watcher = watch(filePath, (eventType: string) => {
    console.log(`📝 File change detected: ${eventType} on ${filePath}`);
    if (eventType === 'change') {
      const newEvents = readNewEvents(filePath);
      if (newEvents.length > 0) {
        console.log(`🔥 Read ${newEvents.length} new event(s) from file`);
      }
      storeEvents(newEvents);
    }
  });

  watcher.on('error', (error: Error) => {
    console.error(`Error watching ${filePath}:`, error);
    watchedFiles.delete(filePath);
  });
}

/**
 * Start watching for events
 * @param callback Optional callback to be notified when new events arrive
 */
export function startFileIngestion(callback?: (events: HookEvent[]) => void): void {
  console.log('🚀 Starting file-based event streaming (in-memory only)');
  const historyDir = HISTORY_DIR;
  console.log(`📂 Reading from: ${historyDir}/raw-outputs/`);

  // Mark ingestion as started
  ingestionStartedAt = Date.now();

  // Set the callback for event notifications
  if (callback) {
    onEventsReceived = callback;
  }

  // Determine today's file path
  const todayFile = getTodayEventsFile();
  console.log(`📅 Today's file: ${todayFile}`);

  // Load existing events from today's file into memory (for initial WebSocket sends)
  console.log('📂 Loading existing events from today\'s file...');
  loadExistingEvents(todayFile);

  // Watch today's file for NEW events
  watchFile(todayFile);

  // Check for new day's file every hour
  setInterval(() => {
    const newTodayFile = getTodayEventsFile();
    if (newTodayFile !== todayFile) {
      console.log('📅 New day detected, watching new file');
      watchFile(newTodayFile);
    }
  }, 60 * 60 * 1000); // Check every hour

  console.log('✅ File streaming started');
}

/**
 * Get all events currently in memory
 */
export function getRecentEvents(limit: number = 100): HookEvent[] {
  return events.slice(-limit).reverse();
}

/**
 * Get filter options from in-memory events
 */
export function getFilterOptions() {
  const sourceApps = new Set<string>();
  const sessionIds = new Set<string>();
  const hookEventTypes = new Set<string>();

  for (const event of events) {
    if (event.source_app) sourceApps.add(event.source_app);
    if (event.session_id) sessionIds.add(event.session_id);
    if (event.hook_event_type) hookEventTypes.add(event.hook_event_type);
  }

  return {
    source_apps: Array.from(sourceApps).sort(),
    session_ids: Array.from(sessionIds).slice(0, 100),
    hook_event_types: Array.from(hookEventTypes).sort()
  };
}

/**
 * Basic ingestion health for diagnostics
 */
export function getIngestionHealth() {
  return {
    ingestionStartedAt,
    eventsInMemory: events.length,
    lastEventTimestamp
  };
}

// For testing - can be run directly
if (import.meta.main) {
  startFileIngestion();

  console.log('Press Ctrl+C to stop');

  // Keep process alive
  process.on('SIGINT', () => {
    console.log('\n👋 Shutting down...');
    process.exit(0);
  });
}

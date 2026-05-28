#!/usr/bin/env node

const ORCHESTRATOR_SESSION_ID = 'coder-orchestrator';
const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';
const ORCHESTRATOR_KEY = 'coders:orchestrator:meta';

let redisClient = null;

/**
 * Get or create Redis client (with dynamic import)
 */
async function getRedisClient() {
  if (!redisClient) {
    try {
      // Use dynamic import to avoid top-level import errors
      const { createClient } = await import('redis');
      redisClient = createClient({ url: REDIS_URL });
      redisClient.on('error', (err) => console.error('[Redis] Error:', err));
      redisClient.on('end', () => {
        console.warn('[Redis] Connection closed, will reconnect on next use.');
        redisClient = null;
      });
      await redisClient.connect();
    } catch (err) {
      throw new Error(`Failed to load redis: ${err.message}`);
    }
  }
  if (redisClient && !redisClient.isOpen) {
    try {
      await redisClient.connect();
    } catch (err) {
      console.warn('[Redis] Reconnect failed, recreating client.');
      redisClient = null;
      return getRedisClient();
    }
  }
  return redisClient;
}

/**
 * Load orchestrator state from Redis
 */
export async function loadOrchestratorState() {
  try {
    const client = await getRedisClient();
    const data = await client.get(ORCHESTRATOR_KEY);

    if (!data) {
      return {
        sessionId: ORCHESTRATOR_SESSION_ID,
        createdAt: new Date().toISOString(),
        lastStarted: null,
        spawnedSessions: [],
        isActive: false
      };
    }

    return JSON.parse(data);
  } catch (e) {
    console.error('Failed to load orchestrator state from Redis:', e.message);
    return {
      sessionId: ORCHESTRATOR_SESSION_ID,
      createdAt: new Date().toISOString(),
      lastStarted: null,
      spawnedSessions: [],
      isActive: false
    };
  }
}

/**
 * Save orchestrator state to Redis
 */
export async function saveOrchestratorState(state) {
  try {
    const client = await getRedisClient();
    await client.set(ORCHESTRATOR_KEY, JSON.stringify(state));
  } catch (e) {
    console.error('Failed to save orchestrator state to Redis:', e.message);
  }
}

/**
 * Mark orchestrator as started
 */
export async function markOrchestratorStarted() {
  const state = await loadOrchestratorState();
  state.lastStarted = new Date().toISOString();
  state.isActive = true;
  await saveOrchestratorState(state);
  return state;
}

/**
 * Mark orchestrator as stopped
 */
export async function markOrchestratorStopped() {
  const state = await loadOrchestratorState();
  state.isActive = false;
  await saveOrchestratorState(state);
  return state;
}

/**
 * Add a spawned session to the orchestrator's tracking
 */
export async function trackSpawnedSession(sessionId) {
  const state = await loadOrchestratorState();

  if (!state.spawnedSessions.includes(sessionId)) {
    state.spawnedSessions.push(sessionId);
    await saveOrchestratorState(state);
  }

  return state;
}

/**
 * Remove a session from the orchestrator's tracking
 */
export async function untrackSession(sessionId) {
  const state = await loadOrchestratorState();
  state.spawnedSessions = state.spawnedSessions.filter(id => id !== sessionId);
  await saveOrchestratorState(state);
  return state;
}

/**
 * Get orchestrator session ID
 */
export function getOrchestratorSessionId() {
  return ORCHESTRATOR_SESSION_ID;
}

/**
 * Check if a session ID is the orchestrator
 */
export function isOrchestratorSession(sessionId) {
  return sessionId === ORCHESTRATOR_SESSION_ID;
}

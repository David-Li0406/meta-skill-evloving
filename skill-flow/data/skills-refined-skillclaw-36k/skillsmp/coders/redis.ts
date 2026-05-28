/**
 * Redis Manager for Coders Skill
 * 
 * Provides heartbeat publishing, dead-letter handling, and pane ID injection
 * for tmux-based AI agent sessions.
 */

import { createClient, RedisClientType } from 'redis';
import { execSync, spawn, ChildProcess } from 'child_process';
import * as os from 'os';

const SNAPSHOT_DIR = os.homedir() + '/.coders/snapshots';
export const HEARTBEAT_CHANNEL = 'coders:heartbeats';
export const PROMISES_CHANNEL = 'coders:promises';
export const DEAD_LETTER_KEY = 'coders:dead-letter';
const PANE_ID_KEY_PREFIX = 'coders:pane:';
export const SESSION_META_KEY_PREFIX = 'coders:session-meta:';
export const PROMISE_KEY_PREFIX = 'coders:promise:';

// Types
export interface RedisConfig {
  url?: string;
  host?: string;
  port?: number;
  password?: string;
}

export interface PaneInfo {
  paneId: string;
  sessionId: string;
  windowId: string;
  tool: string;
  task: string;
  pid: number;
  createdAt: number;
  parentSessionId?: string;
}

export interface HeartbeatData {
  paneId: string;
  sessionId: string;
  timestamp: number;
  status: 'alive' | 'processing' | 'idle';
  lastActivity: string;
  parentSessionId?: string;
}

export interface SnapshotData {
  version: number;
  timestamp: number;
  sessionId: string;
  panes: PaneInfo[];
  layout: any;
}

export interface SessionMetadata {
  displayName: string;
  tool: string;
  task: string;
  createdAt: number;
}

export interface CoderPromise {
  sessionId: string;
  timestamp: number;
  summary: string;
  status: 'completed' | 'blocked' | 'needs-review';
  filesChanged?: string[];
  blockers?: string[];
}

/**
 * Get pane ID from environment or generate one
 */
export function getPaneId(): string {
  return process.env.CODERS_PANE_ID || `pane-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Inject pane ID into system context for the agent
 */
export function injectPaneIdContext(systemPrompt: string, paneId: string): string {
  const contextBlock = `
<!-- SYSTEM CONTEXT -->
<!-- PANE_ID: ${paneId} -->
<!-- HEARTBEAT_CHANNEL: ${HEARTBEAT_CHANNEL} -->

Your session has a unique pane ID for heartbeat monitoring.
Publish heartbeats to Redis channel "${HEARTBEAT_CHANNEL}" with your pane ID.
If you become unresponsive for >2 minutes, you will be auto-respawned.

To publish a heartbeat:
\`\`\`javascript
await redis.publish('${HEARTBEAT_CHANNEL}', JSON.stringify({
  paneId: '${paneId}',
  status: 'alive',
  timestamp: Date.now()
}));
\`\`\`
`;
  
  // Insert after any existing system context markers
  if (systemPrompt.includes('<!-- SYSTEM CONTEXT -->')) {
    return systemPrompt.replace(
      '<!-- SYSTEM CONTEXT -->',
      contextBlock
    );
  }
  
  return contextBlock + '\n\n' + systemPrompt;
}

export class RedisManager {
  private client!: RedisClientType;
  private config: RedisConfig;
  private paneId: string;
  private heartbeatInterval: NodeJS.Timeout | null = null;
  private deadLetterListener: ChildProcess | null = null;
  private subscribers: Map<string, RedisClientType> = new Map();
  private subscriptionHandlers: Map<string, (message: any) => void> = new Map();
  private reconnectAttempts = 0;
  private reconnectTimer: NodeJS.Timeout | null = null;
  private connectPromise: Promise<void> | null = null;
  private isShuttingDown = false;
  private subscriberReconnectTimers: Map<string, NodeJS.Timeout> = new Map();
  private subscriberReconnectAttempts: Map<string, number> = new Map();

  constructor(config: RedisConfig = {}) {
    this.config = {
      url: config.url || process.env.REDIS_URL || 'redis://localhost:6379',
      host: config.host || 'localhost',
      port: config.port || 6379,
      password: config.password || process.env.REDIS_PASSWORD || undefined
    };
    this.paneId = getPaneId();
  }

  /**
   * Connect to Redis
   */
  async connect(): Promise<void> {
    if (this.client?.isOpen) return;

    if (this.connectPromise) return this.connectPromise;

    this.isShuttingDown = false;

    this.connectPromise = (async () => {
      if (!this.client) {
        this.client = this.createRedisClient();
      }

      try {
        await this.client.connect();
      } catch (err) {
        console.warn('[Redis] Connect failed, recreating client:', (err as Error).message);
        this.client = this.createRedisClient();
        await this.client.connect();
      }

      this.reconnectAttempts = 0;
      if (this.reconnectTimer) {
        clearTimeout(this.reconnectTimer);
        this.reconnectTimer = null;
      }

      console.log('[Redis] Connected to', this.config.url);
    })().finally(() => {
      this.connectPromise = null;
    });

    return this.connectPromise;
  }

  private createRedisClient(): RedisClientType {
    const client = createClient({
      url: this.config.url
    });

    client.on('error', (err) => {
      console.error('[Redis] Error:', err.message);
    });

    client.on('end', () => {
      if (this.isShuttingDown) return;
      this.scheduleReconnect('end');
    });

    client.on('ready', () => {
      this.reconnectAttempts = 0;
    });

    return client;
  }

  private getReconnectDelay(attempt: number): number {
    const base = 500;
    const max = 30000;
    const jitter = Math.floor(Math.random() * 250);
    return Math.min(base * Math.pow(2, attempt), max) + jitter;
  }

  private scheduleReconnect(reason: string): void {
    if (this.isShuttingDown || this.reconnectTimer) return;
    const delay = this.getReconnectDelay(this.reconnectAttempts++);
    console.warn(`[Redis] Disconnected (${reason}). Reconnecting in ${delay}ms`);

    this.reconnectTimer = setTimeout(async () => {
      this.reconnectTimer = null;
      if (this.isShuttingDown) return;

      try {
        await this.connect();
        await this.restoreSubscriptions();
      } catch (err) {
        console.error('[Redis] Reconnect failed:', (err as Error).message);
        this.scheduleReconnect('retry');
      }
    }, delay);
  }

  private async ensureConnected(): Promise<boolean> {
    if (this.client?.isOpen) return true;
    try {
      await this.connect();
      return this.client?.isOpen || false;
    } catch (err) {
      this.scheduleReconnect('ensureConnected');
      return false;
    }
  }

  private async ensureSubscriber(channel: string): Promise<void> {
    if (!(await this.ensureConnected())) return;

    const existing = this.subscribers.get(channel);
    if (existing?.isOpen) return;

    if (existing) {
      try {
        await existing.quit();
      } catch {}
      this.subscribers.delete(channel);
    }

    const callback = this.subscriptionHandlers.get(channel);
    if (!callback || !this.client) return;

    const subscriber = this.client.duplicate();
    subscriber.on('error', (err) => {
      console.error('[Redis Sub] Error:', err.message);
    });
    subscriber.on('end', () => {
      if (this.isShuttingDown) return;
      this.scheduleSubscriberReconnect(channel);
    });

    await subscriber.connect();
    await subscriber.subscribe(`coders:msg:${channel}`, (message) => {
      try {
        const data = JSON.parse(message);
        callback(data);
      } catch (e) {
        console.error('[Redis] Failed to parse message:', e);
      }
    });

    this.subscribers.set(channel, subscriber);
  }

  private scheduleSubscriberReconnect(channel: string): void {
    if (this.isShuttingDown || this.subscriberReconnectTimers.has(channel)) return;

    const attempt = this.subscriberReconnectAttempts.get(channel) || 0;
    const delay = this.getReconnectDelay(attempt);
    this.subscriberReconnectAttempts.set(channel, attempt + 1);

    const timer = setTimeout(async () => {
      this.subscriberReconnectTimers.delete(channel);
      if (this.isShuttingDown) return;

      try {
        await this.ensureSubscriber(channel);
        this.subscriberReconnectAttempts.delete(channel);
      } catch (err) {
        console.error(`[Redis Sub] Reconnect failed for ${channel}:`, (err as Error).message);
        this.scheduleSubscriberReconnect(channel);
      }
    }, delay);

    this.subscriberReconnectTimers.set(channel, timer);
  }

  private async restoreSubscriptions(): Promise<void> {
    const channels = Array.from(this.subscriptionHandlers.keys());
    for (const channel of channels) {
      try {
        await this.ensureSubscriber(channel);
      } catch (err) {
        console.error(`[Redis Sub] Failed to restore ${channel}:`, (err as Error).message);
      }
    }
  }

  /**
   * Disconnect from Redis
   */
  async disconnect(): Promise<void> {
    this.stopHeartbeat();
    this.isShuttingDown = true;
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    for (const timer of this.subscriberReconnectTimers.values()) {
      clearTimeout(timer);
    }
    this.subscriberReconnectTimers.clear();
    this.subscriberReconnectAttempts.clear();
    // Clean up all subscribers
    for (const [channel, sub] of this.subscribers.entries()) {
      try {
        if (sub.isOpen) await sub.quit();
      } catch {}
    }
    this.subscribers.clear();
    if (this.client?.isOpen) {
      await this.client.quit();
    }
  }

  /**
   * Get the Redis client (public accessor)
   */
  getClient(): RedisClientType | undefined {
    return this.client;
  }

  /**
   * Get the pane ID for this session
   */
  getPaneId(): string {
    return this.paneId;
  }

  /**
   * Set a custom pane ID
   */
  setPaneId(id: string): void {
    this.paneId = id;
    process.env.CODERS_PANE_ID = id;
  }

  /**
   * Publish heartbeat for this pane
   */
  async publishHeartbeat(status: HeartbeatData['status'] = 'alive', lastActivity: string = 'working'): Promise<void> {
    if (!(await this.ensureConnected())) return;

    const data: HeartbeatData = {
      paneId: this.paneId,
      sessionId: this.getSessionId(),
      timestamp: Date.now(),
      status,
      lastActivity,
      parentSessionId: this.getParentSessionId()
    };

    await this.client.publish(HEARTBEAT_CHANNEL, JSON.stringify(data));

    // Also set expiration-based key for dead-letter queue
    await this.client.set(`${PANE_ID_KEY_PREFIX}${this.paneId}`, JSON.stringify(data), {
      EX: 150 // 2.5 min TTL (longer than dead-letter timeout)
    });
  }

  /**
   * Start periodic heartbeat publishing
   */
  startHeartbeat(intervalMs: number = 30000): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
    }

    this.heartbeatInterval = setInterval(() => {
      this.publishHeartbeat('alive').catch(console.error);
    }, intervalMs);
    
    console.log(`[Redis] Heartbeat started (interval: ${intervalMs}ms, pane: ${this.paneId})`);
  }

  /**
   * Stop heartbeat publishing
   */
  stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  /**
   * Get the tmux session ID
   */
  private getSessionId(): string {
    return process.env.CODERS_SESSION_ID || 'coder-unknown';
  }

  /**
   * Get the parent session ID (if spawned from another coder session)
   */
  private getParentSessionId(): string | undefined {
    return process.env.CODERS_PARENT_SESSION_ID || undefined;
  }

  /**
   * Publish to inter-agent communication channel
   */
  async publishMessage(channel: string, message: any): Promise<void> {
    if (!(await this.ensureConnected())) return;
    
    const topic = `coders:msg:${channel}`;
    await this.client.publish(topic, JSON.stringify({
      fromPane: this.paneId,
      timestamp: Date.now(),
      message
    }));
  }

  /**
   * Subscribe to inter-agent communication channel
   */
  async subscribeToChannel(channel: string, callback: (message: any) => void): Promise<void> {
    this.subscriptionHandlers.set(channel, callback);
    await this.ensureSubscriber(channel);
  }

  /**
   * Unsubscribe from inter-agent communication channel
   */
  async unsubscribe(channel: string): Promise<void> {
    const topic = `coders:msg:${channel}`;
    const subscriber = this.subscribers.get(channel);
    if (subscriber) {
      await subscriber.unsubscribe(topic);
      if (subscriber.isOpen) await subscriber.quit();
      this.subscribers.delete(channel);
    }
    this.subscriptionHandlers.delete(channel);
    const timer = this.subscriberReconnectTimers.get(channel);
    if (timer) clearTimeout(timer);
    this.subscriberReconnectTimers.delete(channel);
    this.subscriberReconnectAttempts.delete(channel);
  }

  /**
   * Get all active panes from Redis
   */
  async getActivePanes(): Promise<PaneInfo[]> {
    if (!(await this.ensureConnected())) return [];
    
    const keys = await this.client.keys(`${PANE_ID_KEY_PREFIX}*`);
    const panes: PaneInfo[] = [];
    
    for (const key of keys) {
      const data = await this.client.get(key);
      if (data) {
        try {
          panes.push(JSON.parse(data));
        } catch (e) {}
      }
    }
    
    return panes;
  }

  /**
   * Mark pane as dead (called by dead-letter listener)
   */
  async markPaneDead(paneId: string): Promise<void> {
    if (!(await this.ensureConnected())) return;

    await this.client.rPush(DEAD_LETTER_KEY, paneId);
    console.log(`[Redis] Marked pane ${paneId} as dead`);
  }

  /**
   * Store session metadata (including displayName)
   */
  async setSessionMetadata(sessionId: string, metadata: SessionMetadata): Promise<void> {
    if (!(await this.ensureConnected())) return;

    const key = `${SESSION_META_KEY_PREFIX}${sessionId}`;
    await this.client.set(key, JSON.stringify(metadata), {
      EX: 86400 * 7 // 7 day TTL
    });
  }

  /**
   * Get session metadata
   */
  async getSessionMetadata(sessionId: string): Promise<SessionMetadata | null> {
    if (!(await this.ensureConnected())) return null;

    const key = `${SESSION_META_KEY_PREFIX}${sessionId}`;
    const data = await this.client.get(key);

    if (!data) return null;

    try {
      return JSON.parse(data) as SessionMetadata;
    } catch {
      return null;
    }
  }

  /**
   * Get all session metadata
   */
  async getAllSessionMetadata(): Promise<Map<string, SessionMetadata>> {
    const result = new Map<string, SessionMetadata>();
    if (!(await this.ensureConnected())) return result;

    const keys = await this.client.keys(`${SESSION_META_KEY_PREFIX}*`);

    for (const key of keys) {
      const data = await this.client.get(key);
      if (data) {
        try {
          const sessionId = key.replace(SESSION_META_KEY_PREFIX, '');
          result.set(sessionId, JSON.parse(data));
        } catch {}
      }
    }

    return result;
  }

  /**
   * Publish a promise (completion message) for this session
   */
  async publishPromise(promise: Omit<CoderPromise, 'sessionId' | 'timestamp'>): Promise<void> {
    if (!(await this.ensureConnected())) return;

    const sessionId = this.getSessionId();
    const fullPromise: CoderPromise = {
      ...promise,
      sessionId,
      timestamp: Date.now()
    };

    // Store the promise
    const key = `${PROMISE_KEY_PREFIX}${sessionId}`;
    await this.client.set(key, JSON.stringify(fullPromise), {
      EX: 86400 // 24 hour TTL
    });

    // Publish to promises channel for real-time updates
    await this.client.publish(PROMISES_CHANNEL, JSON.stringify(fullPromise));

    console.log(`[Redis] Promise published for ${sessionId}: ${promise.summary}`);
  }

  /**
   * Get a promise for a specific session
   */
  async getPromise(sessionId: string): Promise<CoderPromise | null> {
    if (!(await this.ensureConnected())) return null;

    const key = `${PROMISE_KEY_PREFIX}${sessionId}`;
    const data = await this.client.get(key);

    if (!data) return null;

    try {
      return JSON.parse(data) as CoderPromise;
    } catch {
      return null;
    }
  }

  /**
   * Get all promises
   */
  async getAllPromises(): Promise<Map<string, CoderPromise>> {
    const result = new Map<string, CoderPromise>();
    if (!(await this.ensureConnected())) return result;

    const keys = await this.client.keys(`${PROMISE_KEY_PREFIX}*`);

    for (const key of keys) {
      const data = await this.client.get(key);
      if (data) {
        try {
          const sessionId = key.replace(PROMISE_KEY_PREFIX, '');
          result.set(sessionId, JSON.parse(data));
        } catch {}
      }
    }

    return result;
  }

  /**
   * Delete a promise (used when resuming a session)
   */
  async deletePromise(sessionId: string): Promise<void> {
    if (!(await this.ensureConnected())) return;

    const key = `${PROMISE_KEY_PREFIX}${sessionId}`;
    await this.client.del(key);

    console.log(`[Redis] Promise deleted for ${sessionId}`);
  }
}

/**
 * Dead-letter listener - watches for dead panes and respawns them
 */
export class DeadLetterListener {
  private redisManager: RedisManager;
  private listenerProcess: ChildProcess | null = null;
  private isRunning: boolean = false;

  constructor(redisConfig?: RedisConfig) {
    this.redisManager = new RedisManager(redisConfig);
  }

  /**
   * Start listening for dead letters
   */
  async start(timeoutMs: number = 120000): Promise<void> {
    if (this.isRunning) return;
    
    await this.redisManager.connect();
    this.isRunning = true;

    const checkInterval = setInterval(async () => {
      try {
        await this.redisManager.connect();
        const client = this.redisManager.getClient();
        const deadPane = await client?.blPop(DEAD_LETTER_KEY, 0);
        
        if (deadPane?.element) {
          await this.handleDeadPane(deadPane.element);
        }
      } catch (e) {
        console.error('[DeadLetter] Error:', e);
      }
    }, 1000);

    // Store interval handle for cleanup
    (this as any)._interval = checkInterval;
    
    console.log('[DeadLetter] Listener started (timeout:', timeoutMs / 1000, 's)');
  }

  /**
   * Handle a dead pane - respawn it
   */
  private async handleDeadPane(paneId: string): Promise<void> {
    console.log(`[DeadLetter] Respawning dead pane: ${paneId}`);
    
    try {
      // Extract session info from pane ID
      const sessionId = this.extractSessionId(paneId);
      
      if (sessionId) {
        // Kill and respawn the tmux pane
        this.respawnPane(paneId, sessionId);
      }
    } catch (e) {
      console.error('[DeadLetter] Failed to respawn pane:', e);
    }
  }

  /**
   * Extract session ID from pane ID
   */
  private extractSessionId(paneId: string): string | null {
    // pane IDs are typically in format: pane-{timestamp}-{random}
    // Session info is stored in Redis
    return null; // Override to extract from your specific naming convention
  }

  /**
   * Respawn a tmux pane
   */
  private respawnPane(paneId: string, sessionId: string): void {
    try {
      // Kill the dead pane
      execSync(`respawn-pane -k -t ${paneId} 2>/dev/null || tmux kill-pane -t ${paneId} 2>/dev/null`, {
        encoding: 'utf8'
      });
      
      console.log(`[DeadLetter] Respawned pane: ${paneId}`);
    } catch (e) {
      console.error('[DeadLetter] Respawn failed:', e);
    }
  }

  /**
   * Stop the listener
   */
  stop(): void {
    this.isRunning = false;
    if ((this as any)._interval) {
      clearInterval((this as any)._interval);
    }
    this.redisManager.disconnect();
  }
}

/**
 * Factory function for creating a Redis manager with heartbeat
 */
export async function createHeartbeatSession(
  config?: RedisConfig
): Promise<RedisManager> {
  const manager = new RedisManager(config);
  await manager.connect();
  manager.startHeartbeat();
  return manager;
}

export default {
  RedisManager,
  DeadLetterListener,
  createHeartbeatSession,
  getPaneId,
  injectPaneIdContext,
  SNAPSHOT_DIR,
  HEARTBEAT_CHANNEL,
  PROMISES_CHANNEL,
  DEAD_LETTER_KEY,
  SESSION_META_KEY_PREFIX,
  PROMISE_KEY_PREFIX
};

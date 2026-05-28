/**
 * Agent Observability Configuration
 *
 * Centralized configuration for the observability system.
 * Uses environment variables with sensible defaults.
 */

import { homedir } from 'os';
import { join } from 'path';

/**
 * Default agent name for the primary agent
 * Can be overridden with PAI_AGENT_NAME environment variable
 */
export const DEFAULT_AGENT_NAME = process.env.PAI_AGENT_NAME || 'claude';

/**
 * Path to PAI directory
 * Can be overridden with PAI_DIR environment variable
 */
export const PAI_DIR = process.env.PAI_DIR || join(homedir(), '.claude');

/**
 * Path to history directory where event files are stored
 */
export const HISTORY_DIR = join(homedir(), '.claude', 'history');

/**
 * Maximum number of events to keep in memory
 */
export const MAX_EVENTS_IN_MEMORY = 1000;

/**
 * Maximum number of session mappings to keep
 */
export const MAX_SESSION_MAPPINGS = 1000;

/**
 * WebSocket server port
 * Can be overridden with OBS_SERVER_PORT environment variable
 */
export const SERVER_PORT = Number(process.env.OBS_SERVER_PORT || '4000');

/**
 * Get the configured agent name
 */
export function getDefaultAgentName(): string {
  return DEFAULT_AGENT_NAME;
}

/**
 * Log configuration on startup
 */
export function logConfiguration(): void {
  console.log('📋 Agent Observability Configuration:');
  console.log(`   • Default Agent Name: ${DEFAULT_AGENT_NAME}`);
  console.log(`   • PAI Directory: ${PAI_DIR}`);
  console.log(`   • History Directory: ${HISTORY_DIR}`);
  console.log(`   • Max Events in Memory: ${MAX_EVENTS_IN_MEMORY}`);
  console.log(`   • Server Port: ${SERVER_PORT}`);

  if (process.env.PAI_AGENT_NAME) {
    console.log(`   ✅ Custom agent name set via PAI_AGENT_NAME`);
  } else {
    console.log(`   ℹ️  Using default agent name (set PAI_AGENT_NAME to customize)`);
  }
}

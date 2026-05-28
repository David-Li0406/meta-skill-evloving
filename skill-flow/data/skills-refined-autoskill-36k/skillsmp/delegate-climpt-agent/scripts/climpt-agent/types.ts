/**
 * @fileoverview Type definitions for Climpt Agent script
 * @module climpt-plugins/skills/delegate-climpt-agent/scripts/types
 */

// =============================================================================
// Log Types
// =============================================================================

/**
 * Log levels for JSONL format
 */
export type LogLevel =
  | "info"
  | "error"
  | "debug"
  | "assistant"
  | "system"
  | "result";

/**
 * Log entry for JSONL format
 */
export interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  metadata?: Record<string, unknown>;
}

/**
 * Logger summary result
 */
export interface LogSummary {
  status: "success" | "error" | "pending";
  cost: number;
  messageCount: number;
}

// =============================================================================
// CLI Types
// =============================================================================

/**
 * Parsed CLI arguments
 */
export interface CliArgs {
  /** Action-focused query for command search (what to do, emphasizes c2) */
  action?: string;

  /** Target-focused query for command search (what to act on, emphasizes c3) */
  target?: string;

  /** Detailed intent for option resolution (optional, defaults to action+target) */
  intent?: string;

  /** Agent name (default: "climpt") */
  agent: string;

  /** Additional CLI options to pass to climpt */
  options: string[];
}

// =============================================================================
// Command Types
// =============================================================================

/**
 * Command parameters for execution
 */
export interface ClimptCommand {
  /** Agent name (e.g., "climpt") */
  agent: string;

  /** Domain identifier (C3L level 1) */
  c1: string;

  /** Action identifier (C3L level 2) */
  c2: string;

  /** Target identifier (C3L level 3) */
  c3: string;

  /** CLI options to pass to the command */
  options?: string[];
}

// =============================================================================
// Options Prompt Types (for LLM-based option resolution)
// =============================================================================

/**
 * Context for building options prompt
 */
export interface PromptContext {
  /** Current working directory */
  workingDir: string;

  /** Related files for file option */
  files?: string[];
}

/**
 * User variable definition from registry
 */
export interface UserVariable {
  [key: string]: string;
}

/**
 * Extended command with uv field for options prompt building
 */
export interface CommandWithUV {
  c1: string;
  c2: string;
  c3: string;
  description: string;
  usage?: string;
  options?: {
    edition?: string[];
    adaptation?: string[];
    file?: boolean;
    stdin?: boolean;
    destination?: boolean;
  };
  /** User variables (uv-*) array */
  uv?: UserVariable[];
}

/**
 * Resolved options from LLM response
 */
export type ResolvedOptions = Record<string, string>;

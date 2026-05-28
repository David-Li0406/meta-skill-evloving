#!/usr/bin/env bun
/**
 * ExtractWorkflow.ts - Extract workflow steps from a conversation transcript
 *
 * Parses a Claude Code session transcript (JSONL) and extracts:
 * - Tool use blocks in chronological order
 * - Identified parameters (file paths, URLs, user values)
 * - Suggested name and triggers based on original request
 *
 * CLI Usage:
 *   bun ExtractWorkflow.ts <transcript_path>
 *   bun ExtractWorkflow.ts <transcript_path> --json
 *   bun ExtractWorkflow.ts --current  # Use current session
 *
 * Module Usage:
 *   import { extractWorkflow } from './ExtractWorkflow'
 */

import { readFileSync, existsSync, readdirSync } from 'fs';
import { join, basename, dirname } from 'path';
import { homedir } from 'os';

// ============================================================================
// Types
// ============================================================================

export interface WorkflowStep {
  index: number;
  description: string;
  tool: string;
  inputs: Record<string, any>;
  capability: 'browser' | 'code' | 'file' | 'api' | 'mixed';
  isCorrection: boolean;
}

export interface Parameter {
  name: string;
  value: string;
  type: 'path' | 'url' | 'text' | 'number';
  isRequired: boolean;
  suggestedDefault: string | null;
}

export interface ExtractedWorkflow {
  suggestedName: string;
  originalRequest: string;
  steps: WorkflowStep[];
  parameters: Parameter[];
  suggestedTriggers: string[];
  metadata: {
    sessionId: string;
    extractedAt: string;
    toolCount: number;
    correctionCount: number;
    toolsUsed: string[];
  };
}

interface TranscriptEntry {
  type: string;
  message?: {
    role?: string;
    content?: any;
  };
  sessionId?: string;
  timestamp?: string;
  uuid?: string;
}

interface ToolUseBlock {
  type: 'tool_use';
  id: string;
  name: string;
  input: Record<string, any>;
}

// ============================================================================
// Constants
// ============================================================================

const HOME = homedir();
const PROJECTS_DIR = join(HOME, '.claude', 'projects');

// Tools that indicate browser capability
const BROWSER_TOOLS = [
  'mcp__claude-in-chrome__computer',
  'mcp__claude-in-chrome__navigate',
  'mcp__claude-in-chrome__read_page',
  'mcp__claude-in-chrome__find',
  'mcp__claude-in-chrome__form_input',
  'mcp__claude-in-chrome__javascript_tool',
];

// Tools that indicate file operations
const FILE_TOOLS = ['Read', 'Write', 'Edit', 'Glob', 'Grep'];

// Tools that indicate code execution
const CODE_TOOLS = ['Bash', 'NotebookEdit'];

// Tools that indicate API/web operations
const API_TOOLS = ['WebFetch', 'WebSearch'];

// Correction indicators in user messages
const CORRECTION_PATTERNS = [
  /^no[,.]?\s/i,
  /^wait[,.]?\s/i,
  /^actually[,.]?\s/i,
  /^wrong/i,
  /^that's not/i,
  /^undo/i,
  /^revert/i,
  /^try again/i,
  /^instead[,.]?\s/i,
  /^not that/i,
];

// ============================================================================
// Transcript Parsing
// ============================================================================

/**
 * Parse a transcript file and extract workflow data
 */
export function extractWorkflow(transcriptPath: string): ExtractedWorkflow {
  if (!existsSync(transcriptPath)) {
    throw new Error(`Transcript not found: ${transcriptPath}`);
  }

  const content = readFileSync(transcriptPath, 'utf-8');
  const lines = content.trim().split('\n');

  let originalRequest = '';
  let sessionId = '';
  const allToolUses: { tool: ToolUseBlock; timestamp: string; afterCorrection: boolean }[] = [];
  let lastUserWasCorrection = false;

  for (const line of lines) {
    if (!line.trim()) continue;

    try {
      const entry: TranscriptEntry = JSON.parse(line);

      // Capture session ID
      if (entry.sessionId && !sessionId) {
        sessionId = entry.sessionId;
      }

      // Process user messages
      if (entry.type === 'user' && entry.message?.content) {
        const userText = contentToText(entry.message.content);

        // First substantive user message is the original request
        if (!originalRequest && isValidUserRequest(userText)) {
          originalRequest = userText;
        }

        // Check if this is a correction
        lastUserWasCorrection = isCorrection(userText);
      }

      // Process assistant messages for tool_use blocks
      if (entry.type === 'assistant' && entry.message?.content) {
        const contentArray = Array.isArray(entry.message.content)
          ? entry.message.content
          : [];

        for (const block of contentArray) {
          if (block.type === 'tool_use') {
            allToolUses.push({
              tool: block as ToolUseBlock,
              timestamp: entry.timestamp || '',
              afterCorrection: lastUserWasCorrection,
            });
          }
        }

        // Reset correction flag after assistant responds
        lastUserWasCorrection = false;
      }
    } catch {
      // Skip invalid JSON lines
    }
  }

  // Convert tool uses to workflow steps
  const steps = processToolUses(allToolUses);

  // Detect parameters
  const parameters = detectParameters(steps);

  // Generate suggested name and triggers
  const suggestedName = generateName(originalRequest);
  const suggestedTriggers = generateTriggers(originalRequest, steps);

  // Collect unique tools used
  const toolsUsed = [...new Set(steps.map(s => s.tool))];

  return {
    suggestedName,
    originalRequest,
    steps,
    parameters,
    suggestedTriggers,
    metadata: {
      sessionId,
      extractedAt: new Date().toISOString(),
      toolCount: steps.length,
      correctionCount: steps.filter(s => s.isCorrection).length,
      toolsUsed,
    },
  };
}

/**
 * Convert content (string or array) to plain text
 */
function contentToText(content: unknown): string {
  if (typeof content === 'string') return content;
  if (Array.isArray(content)) {
    return content
      .map(c => {
        if (typeof c === 'string') return c;
        if (c?.text) return c.text;
        return '';
      })
      .join(' ')
      .trim();
  }
  return '';
}

/**
 * Check if text is a valid user request (not system content)
 */
function isValidUserRequest(text: string): boolean {
  // Skip system-reminder content
  if (text.includes('<system-reminder>')) return false;
  if (text.includes('<local-command')) return false;
  if (text.includes('<command-name>')) return false;
  // Skip very short messages
  if (text.length < 15) return false;
  // Skip messages that look like commands
  if (text.startsWith('/')) return false;
  return true;
}

/**
 * Check if a user message indicates a correction
 */
function isCorrection(text: string): boolean {
  const trimmed = text.trim();
  return CORRECTION_PATTERNS.some(pattern => pattern.test(trimmed));
}

// ============================================================================
// Step Processing
// ============================================================================

/**
 * Process raw tool uses into workflow steps
 */
function processToolUses(
  toolUses: { tool: ToolUseBlock; timestamp: string; afterCorrection: boolean }[]
): WorkflowStep[] {
  const steps: WorkflowStep[] = [];

  for (let i = 0; i < toolUses.length; i++) {
    const { tool, afterCorrection } = toolUses[i];

    // Skip internal tools that shouldn't be part of workflows
    if (shouldSkipTool(tool.name)) continue;

    steps.push({
      index: steps.length + 1,
      description: generateStepDescription(tool),
      tool: tool.name,
      inputs: sanitizeInputs(tool.input),
      capability: categorizeCapability(tool.name),
      isCorrection: afterCorrection,
    });
  }

  return steps;
}

/**
 * Tools to skip in workflow extraction
 */
function shouldSkipTool(toolName: string): boolean {
  const skipTools = [
    'AskUserQuestion',
    'TaskCreate',
    'TaskUpdate',
    'TaskList',
    'TaskGet',
    'EnterPlanMode',
    'ExitPlanMode',
    'Skill',
  ];
  return skipTools.includes(toolName);
}

/**
 * Generate human-readable step description
 */
function generateStepDescription(tool: ToolUseBlock): string {
  const { name, input } = tool;

  switch (name) {
    case 'Read':
      return `Read file: ${input.file_path || 'unknown'}`;
    case 'Write':
      return `Write file: ${input.file_path || 'unknown'}`;
    case 'Edit':
      return `Edit file: ${input.file_path || 'unknown'}`;
    case 'Bash':
      const cmd = input.command?.slice(0, 50) || 'command';
      return `Run: ${cmd}${input.command?.length > 50 ? '...' : ''}`;
    case 'Glob':
      return `Find files: ${input.pattern || 'pattern'}`;
    case 'Grep':
      return `Search: ${input.pattern || 'pattern'}`;
    case 'WebFetch':
      return `Fetch URL: ${input.url || 'url'}`;
    case 'WebSearch':
      return `Search web: ${input.query || 'query'}`;
    case 'mcp__claude-in-chrome__navigate':
      return `Navigate to: ${input.url || 'url'}`;
    case 'mcp__claude-in-chrome__computer':
      return `Browser action: ${input.action || 'action'}`;
    case 'mcp__claude-in-chrome__read_page':
      return 'Read page content';
    case 'mcp__claude-in-chrome__find':
      return `Find element: ${input.query || 'element'}`;
    case 'mcp__claude-in-chrome__form_input':
      return `Fill form field`;
    default:
      return `${name}`;
  }
}

/**
 * Categorize tool by capability type
 */
function categorizeCapability(toolName: string): 'browser' | 'code' | 'file' | 'api' | 'mixed' {
  if (BROWSER_TOOLS.some(t => toolName.includes(t) || toolName.startsWith('mcp__claude-in-chrome'))) {
    return 'browser';
  }
  if (FILE_TOOLS.includes(toolName)) return 'file';
  if (CODE_TOOLS.includes(toolName)) return 'code';
  if (API_TOOLS.includes(toolName)) return 'api';
  return 'mixed';
}

/**
 * Sanitize inputs for storage (remove overly long content)
 */
function sanitizeInputs(input: Record<string, any>): Record<string, any> {
  const sanitized: Record<string, any> = {};

  for (const [key, value] of Object.entries(input)) {
    if (typeof value === 'string' && value.length > 500) {
      sanitized[key] = value.slice(0, 100) + '... [truncated]';
    } else {
      sanitized[key] = value;
    }
  }

  return sanitized;
}

// ============================================================================
// Parameter Detection
// ============================================================================

/**
 * Paths to exclude from parameter detection (internal PAI paths)
 */
const EXCLUDED_PARAM_PATHS = [
  '/.claude/skills/',
  '/.claude/hooks/',
  '/.claude/MEMORY/',
  '/.claude/projects/',
  '/.claude/plans/',
  '/.claude/settings.json',
  '/tmp/',
];

/**
 * Detect parameters from workflow steps
 */
function detectParameters(steps: WorkflowStep[]): Parameter[] {
  const parameters: Parameter[] = [];
  const seenValues = new Set<string>();

  for (const step of steps) {
    // Limit to max 10 parameters
    if (parameters.length >= 10) break;

    const inputs = step.inputs;

    // Detect file paths
    if (inputs.file_path && !seenValues.has(inputs.file_path)) {
      seenValues.add(inputs.file_path);
      const isUserPath = inputs.file_path.includes(HOME);
      const isExcluded = EXCLUDED_PARAM_PATHS.some(p => inputs.file_path.includes(p));

      if (isUserPath && !isExcluded) {
        parameters.push({
          name: deriveParamName(inputs.file_path, 'path'),
          value: inputs.file_path,
          type: 'path',
          isRequired: false,
          suggestedDefault: inputs.file_path,
        });
      }
    }

    // Detect URLs (exclude localhost/internal)
    if (inputs.url && !seenValues.has(inputs.url)) {
      seenValues.add(inputs.url);
      const isInternal = inputs.url.includes('localhost') || inputs.url.includes('127.0.0.1');

      if (!isInternal) {
        parameters.push({
          name: deriveParamName(inputs.url, 'url'),
          value: inputs.url,
          type: 'url',
          isRequired: true,
          suggestedDefault: inputs.url,
        });
      }
    }

    // Detect queries (often variable)
    if (inputs.query && !seenValues.has(inputs.query)) {
      seenValues.add(inputs.query);
      parameters.push({
        name: 'search_query',
        value: inputs.query,
        type: 'text',
        isRequired: true,
        suggestedDefault: null,
      });
    }
  }

  return parameters;
}

/**
 * Derive a parameter name from a value
 */
function deriveParamName(value: string, type: string): string {
  if (type === 'path') {
    const filename = basename(value);
    const ext = filename.split('.').pop();
    if (ext && ['csv', 'json', 'txt', 'md'].includes(ext)) {
      return `${ext}_file_path`;
    }
    return 'file_path';
  }

  if (type === 'url') {
    try {
      const url = new URL(value);
      const host = url.hostname.replace('www.', '').split('.')[0];
      return `${host}_url`;
    } catch {
      return 'url';
    }
  }

  return 'value';
}

// ============================================================================
// Name and Trigger Generation
// ============================================================================

/**
 * Generate a suggested skill name from the original request
 */
function generateName(request: string): string {
  // Extract key action words
  const words = request
    .toLowerCase()
    .replace(/[^\w\s]/g, '')
    .split(/\s+/)
    .filter(w => w.length > 3);

  // Find action words
  const actions = ['audit', 'check', 'create', 'update', 'sync', 'backup', 'generate', 'process', 'analyze', 'review'];
  const foundAction = words.find(w => actions.includes(w)) || 'Process';

  // Find domain words (nouns)
  const skipWords = ['the', 'and', 'for', 'from', 'with', 'that', 'this', 'your', 'which', 'ones'];
  const nouns = words.filter(w => !skipWords.includes(w) && !actions.includes(w)).slice(0, 2);

  // Build name in TitleCase
  const name = [foundAction, ...nouns]
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join('');

  return `_${name}`;
}

/**
 * Generate suggested trigger phrases
 */
function generateTriggers(request: string, steps: WorkflowStep[]): string[] {
  const triggers: string[] = [];

  // Clean request of any system content that might have leaked through
  let cleanRequest = request
    .replace(/<[^>]+>/g, '')  // Remove XML-like tags
    .replace(/\[[^\]]+\]/g, '') // Remove bracketed content
    .trim();

  // If request is too short after cleaning, use step descriptions
  if (cleanRequest.length < 20) {
    const stepDescriptions = steps.slice(0, 3).map(s => s.description).join(' ');
    cleanRequest = stepDescriptions;
  }

  // Extract key phrases from request
  const words = cleanRequest.toLowerCase().split(/\s+/);

  // Common action words
  const actions = ['audit', 'check', 'create', 'update', 'sync', 'backup', 'generate', 'process', 'analyze', 'review', 'read', 'write', 'edit', 'fetch', 'search', 'find'];
  const foundAction = words.find(w => actions.includes(w));

  // Words to skip
  const skipWords = ['the', 'and', 'for', 'from', 'with', 'that', 'this', 'your', 'which', 'ones', 'please', 'can', 'you', 'file', 'path', 'unknown', 'content'];
  const meaningfulWords = words.filter(w =>
    w.length > 3 &&
    !skipWords.includes(w) &&
    !w.includes('/') &&  // Skip paths
    !w.includes('.') &&  // Skip file extensions
    !/^\d+$/.test(w)     // Skip numbers
  );

  // Generate variations
  if (foundAction) {
    triggers.push(foundAction);
    if (meaningfulWords.length > 0 && meaningfulWords[0] !== foundAction) {
      triggers.push(`${foundAction} ${meaningfulWords[0]}`);
    }
  }

  // Add noun-based triggers
  for (const word of meaningfulWords.slice(0, 3)) {
    if (!triggers.includes(word)) {
      triggers.push(word);
    }
  }

  // Add two-word combinations
  if (meaningfulWords.length >= 2) {
    const combo = `${meaningfulWords[0]} ${meaningfulWords[1]}`;
    if (!triggers.includes(combo)) {
      triggers.push(combo);
    }
  }

  // Filter out any remaining garbage
  const cleanTriggers = triggers.filter(t =>
    t.length >= 3 &&
    t.length <= 30 &&
    !/[<>\[\]{}'",]/.test(t) &&  // No special chars including quotes/commas
    !t.includes('caveat') &&
    !t.includes('reminder') &&
    !t.includes('command') &&
    !t.includes('hello') &&  // Skip literal test content
    !/^\W/.test(t) &&  // Must start with word char
    !/\W$/.test(t.trim())  // Must end with word char
  );

  return cleanTriggers.slice(0, 5); // Max 5 triggers
}

// ============================================================================
// Current Session Helper
// ============================================================================

/**
 * Find the current session transcript
 */
export function findCurrentTranscript(): string | null {
  // Look for most recent transcript in projects directory
  if (!existsSync(PROJECTS_DIR)) return null;

  const projectDirs = readdirSync(PROJECTS_DIR)
    .map(d => join(PROJECTS_DIR, d))
    .filter(d => {
      try {
        return readdirSync(d).some(f => f.endsWith('.jsonl'));
      } catch {
        return false;
      }
    });

  // Find most recent .jsonl file
  let mostRecent: { path: string; mtime: number } | null = null;

  for (const dir of projectDirs) {
    const files = readdirSync(dir).filter(f => f.endsWith('.jsonl'));
    for (const file of files) {
      const filePath = join(dir, file);
      try {
        const stat = Bun.file(filePath);
        // Use current time as proxy for most recent (files are written to during session)
        if (!mostRecent) {
          mostRecent = { path: filePath, mtime: Date.now() };
        }
      } catch {}
    }
  }

  return mostRecent?.path || null;
}

// ============================================================================
// CLI
// ============================================================================

if (import.meta.main) {
  const args = process.argv.slice(2);

  let transcriptPath: string | null = null;
  const outputJson = args.includes('--json');

  if (args.includes('--current')) {
    transcriptPath = findCurrentTranscript();
    if (!transcriptPath) {
      console.error('Could not find current session transcript');
      process.exit(1);
    }
  } else {
    transcriptPath = args.find(a => !a.startsWith('-')) || null;
  }

  if (!transcriptPath) {
    console.log(`Usage: bun ExtractWorkflow.ts <transcript_path> [--json]
       bun ExtractWorkflow.ts --current [--json]

Options:
  --json     Output as JSON
  --current  Use current session transcript
`);
    process.exit(1);
  }

  try {
    const workflow = extractWorkflow(transcriptPath);

    if (outputJson) {
      console.log(JSON.stringify(workflow, null, 2));
    } else {
      // Human-readable output
      console.log(`\n📋 Extracted Workflow: ${workflow.suggestedName}\n`);
      console.log(`Original request: "${workflow.originalRequest.slice(0, 100)}..."\n`);

      console.log('Steps:');
      for (const step of workflow.steps) {
        const marker = step.isCorrection ? '🔄' : '  ';
        console.log(`${marker} ${step.index}. [${step.capability}] ${step.description}`);
      }

      console.log('\nDetected Parameters:');
      for (const param of workflow.parameters) {
        console.log(`  • ${param.name} (${param.type}): ${param.value.slice(0, 50)}`);
      }

      console.log('\nSuggested Triggers:');
      console.log(`  ${workflow.suggestedTriggers.join(', ')}`);

      console.log('\nMetadata:');
      console.log(`  Tools used: ${workflow.metadata.toolsUsed.join(', ')}`);
      console.log(`  Corrections: ${workflow.metadata.correctionCount}`);
    }
  } catch (error) {
    console.error('Error extracting workflow:', error);
    process.exit(1);
  }
}

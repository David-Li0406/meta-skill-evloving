#!/usr/bin/env node

/**
 * condense-transcript.js
 *
 * Condenses Claude Code session transcripts for easier analysis.
 * Removes verbose metadata, condenses tool calls, and produces
 * human-readable markdown or machine-parseable JSON output.
 *
 * Usage: node condense-transcript.js <input> [options]
 * Run with --help for full documentation
 */

const fs = require('fs');
const path = require('path');

// ============================================================================
// Configuration & Constants
// ============================================================================

const DEFAULT_OPTIONS = {
  format: 'markdown',
  output: null,
  outputDir: null,
  verbosity: 'standard', // minimal, standard, detailed
  onlyTools: false,
  onlySubagents: false,
  noSystem: false,
  includeUsage: false,
  linkSubagents: false,
  merge: false,
  preserveOriginal: true,
  help: false
};

const TOOL_NAMES = [
  'Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob',
  'Task', 'TodoWrite', 'BashOutput'
];

const SYSTEM_REMINDER_MARKERS = [
  '<system-reminder>',
  '# claudeMd',
  'Codebase and user instructions'
];

// ============================================================================
// CLI Argument Parsing
// ============================================================================

/**
 * Parse command-line arguments into structured options
 */
function parseArguments(args) {
  const options = { ...DEFAULT_OPTIONS };
  const positional = [];

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === '--help' || arg === '-h') {
      options.help = true;
    } else if (arg.startsWith('--format=')) {
      options.format = arg.split('=')[1];
    } else if (arg.startsWith('--output=')) {
      options.output = arg.split('=')[1];
    } else if (arg.startsWith('--output-dir=')) {
      options.outputDir = arg.split('=')[1];
    } else if (arg.startsWith('--verbosity=')) {
      options.verbosity = arg.split('=')[1];
    } else if (arg === '--only-tools') {
      options.onlyTools = true;
    } else if (arg === '--only-subagents') {
      options.onlySubagents = true;
    } else if (arg === '--no-system') {
      options.noSystem = true;
    } else if (arg === '--include-usage') {
      options.includeUsage = true;
    } else if (arg === '--link-subagents') {
      options.linkSubagents = true;
    } else if (arg === '--merge') {
      options.merge = true;
    } else if (arg === '--preserve-original') {
      options.preserveOriginal = true;
    } else if (!arg.startsWith('--')) {
      positional.push(arg);
    } else {
      console.error(`Unknown option: ${arg}`);
      process.exit(1);
    }
  }

  if (positional.length > 0) {
    options.input = positional[0];
  }

  return options;
}

/**
 * Display help message
 */
function showHelp() {
  console.log(`
Claude Code Transcript Condenser

Condenses Claude Code session transcripts for easier analysis.

USAGE:
  node condense-transcript.js <input> [options]

ARGUMENTS:
  input                 Path to transcript file or directory

OPTIONS:
  --format=<type>       Output format: "markdown" (default) or "json"
  --output=<file>       Output file (default: stdout)
  --output-dir=<dir>    Output directory for batch processing
  --verbosity=<level>   Level: "minimal", "standard" (default), "detailed"
  --only-tools          Show only tool usage
  --only-subagents      Show only subagent interactions
  --no-system           Strip all system messages
  --include-usage       Include token usage statistics
  --link-subagents      Find and link related subagent transcripts
  --merge               Merge main + subagent transcripts into one timeline
  --preserve-original   Keep original files (default: true)
  --help, -h            Show this help message

EXAMPLES:
  # Condense single transcript to markdown
  node condense-transcript.js transcript.json --output=condensed.md

  # Condense to JSON summary
  node condense-transcript.js transcript.json --format=json --output=summary.json

  # Batch process directory
  node condense-transcript.js logs/20251011/ --output-dir=condensed/

  # Minimal output (only user requests and outcomes)
  node condense-transcript.js transcript.json --verbosity=minimal

  # Show only tool usage
  node condense-transcript.js transcript.json --only-tools
`);
}

// ============================================================================
// File System Utilities
// ============================================================================

/**
 * Load and parse JSON transcript file
 */
function loadTranscript(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(content);

    if (!Array.isArray(data)) {
      throw new Error('Transcript must be a JSON array');
    }

    return data;
  } catch (error) {
    throw new Error(`Failed to load transcript ${filePath}: ${error.message}`);
  }
}

/**
 * Get all JSON files from a directory
 */
function getTranscriptFiles(dirPath) {
  try {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    return entries
      .filter(entry => entry.isFile() && entry.name.endsWith('.json'))
      .map(entry => path.join(dirPath, entry.name));
  } catch (error) {
    throw new Error(`Failed to read directory ${dirPath}: ${error.message}`);
  }
}

/**
 * Write output to file or stdout
 */
function writeOutput(content, outputPath) {
  if (outputPath) {
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(outputPath, content, 'utf8');
    console.error(`Output written to: ${outputPath}`);
  } else {
    console.log(content);
  }
}

// ============================================================================
// Data Extraction & Filtering
// ============================================================================

/**
 * Extract session metadata from transcript
 */
function extractSessionMetadata(events) {
  const firstEvent = events[0] || {};
  const lastEvent = events[events.length - 1] || {};

  const startTime = new Date(firstEvent.timestamp || Date.now());
  const endTime = new Date(lastEvent.timestamp || Date.now());
  const duration = formatDuration(endTime - startTime);

  const fullId = firstEvent.sessionId || 'unknown';
  const shortId = fullId.split('-')[0] || fullId;

  return {
    id: shortId,
    fullId: fullId,
    date: startTime.toISOString().split('T')[0],
    branch: firstEvent.gitBranch || 'unknown',
    cwd: firstEvent.cwd || 'unknown',
    version: firstEvent.version || 'unknown',
    startTime: startTime.toISOString(),
    endTime: endTime.toISOString(),
    duration
  };
}

/**
 * Format duration in human-readable format
 */
function formatDuration(ms) {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);

  if (hours > 0) {
    return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
  } else if (minutes > 0) {
    return `${minutes}m ${seconds % 60}s`;
  } else {
    return `${seconds}s`;
  }
}

/**
 * Format timestamp as HH:MM:SS relative to start
 */
function formatTimestamp(timestamp, startTime) {
  const date = new Date(timestamp);
  const start = new Date(startTime);
  const diff = date - start;

  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);

  const h = String(hours).padStart(2, '0');
  const m = String(minutes % 60).padStart(2, '0');
  const s = String(seconds % 60).padStart(2, '0');

  return `${h}:${m}:${s}`;
}

/**
 * Check if event is a system hook notification
 */
function isHookNotification(event) {
  return event.type === 'system' &&
         event.message?.subtype === 'informational';
}

/**
 * Check if event is a meta message (should be filtered)
 */
function isMetaMessage(event) {
  return event.isMeta === true;
}

/**
 * Check if event is a command clear message (should be filtered)
 */
function isCommandClear(event) {
  const content = extractTextContent(event.message);
  return content.includes('<command-name>/clear</command-name>');
}

/**
 * Check if event is empty stdout (should be filtered)
 */
function isEmptyStdout(event) {
  const content = extractTextContent(event.message);
  return content === '<local-command-stdout></local-command-stdout>';
}

/**
 * Check if event is a system reminder
 */
function isSystemReminder(event) {
  if (event.type !== 'user') return false;
  const content = extractTextContent(event.message);
  return SYSTEM_REMINDER_MARKERS.some(marker => content.includes(marker));
}

/**
 * Strip system reminders from user message
 */
function stripSystemReminders(content) {
  // Remove <system-reminder>...</system-reminder> blocks
  let cleaned = content.replace(/<system-reminder>[\s\S]*?<\/system-reminder>/g, '');
  return cleaned.trim();
}

/**
 * Extract tool calls from assistant message
 * Handles both array-based content (API format) and string-based content
 */
function extractToolCalls(event) {
  if (!event.message || !event.message.content) {
    return [];
  }

  const content = event.message.content;
  const tools = [];

  // Handle array-based content (API format)
  if (Array.isArray(content)) {
    for (const item of content) {
      if (item.type === 'tool_use') {
        tools.push({
          name: item.name,
          params: item.input || {}
        });
      }
    }
    return tools;
  }

  // Handle string-based content (legacy format)
  if (typeof content !== 'string') {
    return [];
  }

  // Look for <function_calls> blocks
  const functionCallsMatch = content.match(/<function_calls>([\s\S]*?)<\/antml:function_calls>/g);

  if (functionCallsMatch) {
    functionCallsMatch.forEach(block => {
      const invokeMatches = block.matchAll(/<invoke name="([^"]+)">([\s\S]*?)<\/antml:invoke>/g);

      for (const match of invokeMatches) {
        const toolName = match[1];
        const paramsBlock = match[2];

        // Extract parameters
        const params = {};
        const paramMatches = paramsBlock.matchAll(/<parameter name="([^"]+)">([^<]*)<\/antml:parameter>/g);

        for (const paramMatch of paramMatches) {
          params[paramMatch[1]] = paramMatch[2];
        }

        tools.push({ name: toolName, params });
      }
    });
  }

  return tools;
}

/**
 * Detect if message is a subagent invocation
 */
function detectSubagentCall(event) {
  const content = extractTextContent(event.message);

  if (!content) {
    return null;
  }

  // Look for @subagent-name pattern
  const subagentMatch = content.match(/@([\w-]+)/);
  if (subagentMatch) {
    return {
      subagent: subagentMatch[1],
      content: content
    };
  }

  return null;
}

/**
 * Truncate text to max length
 */
function truncate(text, maxLength = 200) {
  // Handle non-string inputs
  if (typeof text !== 'string') {
    text = String(text);
  }
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

/**
 * Filter events based on options
 */
function filterEvents(events, options) {
  return events.filter(event => {
    // Remove meta messages (always filter)
    if (isMetaMessage(event)) return false;

    // Remove hook notifications (always filter)
    if (isHookNotification(event)) return false;

    // Remove command clear messages (always filter)
    if (isCommandClear(event)) return false;

    // Remove empty stdout (always filter)
    if (isEmptyStdout(event)) return false;

    // Remove system messages if requested
    if (options.noSystem && event.type === 'system') return false;

    // Filter by type if only-tools or only-subagents is set
    if (options.onlyTools) {
      if (event.type !== 'assistant') return false;
      const tools = extractToolCalls(event);
      if (tools.length === 0) return false;
    }

    if (options.onlySubagents) {
      if (event.type !== 'user') return false;
      if (!detectSubagentCall(event)) return false;
    }

    return true;
  });
}

// ============================================================================
// Timeline Building
// ============================================================================

/**
 * Extract text content from message (handles both array and string formats)
 */
function extractTextContent(message) {
  if (!message || !message.content) {
    return '';
  }

  const content = message.content;

  // Handle array-based content (API format)
  if (Array.isArray(content)) {
    const textParts = content
      .filter(item => item.type === 'text')
      .map(item => item.text);
    return textParts.join('\n');
  }

  // Handle string-based content
  if (typeof content === 'string') {
    return content;
  }

  return '';
}

/**
 * Build condensed timeline from filtered events
 */
function buildTimeline(events, options, metadata) {
  const timeline = [];

  for (const event of events) {
    const timestamp = formatTimestamp(event.timestamp, metadata.startTime);
    const content = extractTextContent(event.message);

    // Process based on event type
    if (event.type === 'user') {
      const subagentCall = detectSubagentCall(event);

      if (subagentCall) {
        timeline.push({
          time: timestamp,
          type: 'subagent',
          subagent: subagentCall.subagent,
          content: options.verbosity === 'detailed' ? content : truncate(content, 300),
          raw: event
        });
      } else {
        const cleaned = stripSystemReminders(content);
        if (cleaned) {
          timeline.push({
            time: timestamp,
            type: 'user',
            content: options.verbosity === 'minimal' ? truncate(cleaned, 150) : cleaned,
            raw: event
          });
        }
      }
    } else if (event.type === 'assistant') {
      const tools = extractToolCalls(event);

      // Extract text content (non-tool parts) - already extracted above
      let textContent = '';
      if (typeof content === 'string') {
        textContent = content
          .replace(/<function_calls>[\s\S]*?<\/antml:function_calls>/g, '')
          .trim();
      }

      if (options.verbosity === 'minimal' && tools.length > 0) {
        // In minimal mode, only show tool summary
        timeline.push({
          time: timestamp,
          type: 'assistant',
          tools: tools,
          content: null,
          raw: event
        });
      } else if (options.verbosity === 'detailed') {
        // In detailed mode, show everything
        timeline.push({
          time: timestamp,
          type: 'assistant',
          content: textContent || null,
          tools: tools,
          raw: event
        });
      } else {
        // Standard mode: show condensed text + tool summary
        timeline.push({
          time: timestamp,
          type: 'assistant',
          content: textContent ? truncate(textContent, 300) : null,
          tools: tools,
          raw: event
        });
      }
    } else if (event.type === 'system' && !options.noSystem) {
      timeline.push({
        time: timestamp,
        type: 'system',
        content: truncate(content, 200),
        raw: event
      });
    }
  }

  return timeline;
}

/**
 * Generate summary statistics from timeline
 */
function generateSummary(timeline, events, options) {
  const summary = {
    toolsUsed: {},
    subagentsUsed: {},
    filesModified: 0,
    errors: 0,
    warnings: 0,
    totalEvents: events.length,
    filteredEvents: timeline.length
  };

  // Count tool usage
  for (const entry of timeline) {
    if (entry.tools) {
      for (const tool of entry.tools) {
        summary.toolsUsed[tool.name] = (summary.toolsUsed[tool.name] || 0) + 1;
      }
    }

    if (entry.type === 'subagent') {
      summary.subagentsUsed[entry.subagent] = (summary.subagentsUsed[entry.subagent] || 0) + 1;
    }
  }

  // Count file modifications
  for (const entry of timeline) {
    if (entry.tools) {
      for (const tool of entry.tools) {
        if (tool.name === 'Write' || tool.name === 'Edit') {
          summary.filesModified++;
        }
      }
    }
  }

  // Count errors (look for error messages)
  for (const event of events) {
    const content = extractTextContent(event.message).toLowerCase();
    if (content.includes('error')) {
      summary.errors++;
    }
    if (content.includes('warning')) {
      summary.warnings++;
    }
  }

  return summary;
}

// ============================================================================
// Output Formatting - Markdown
// ============================================================================

/**
 * Format timeline as markdown
 */
function formatMarkdown(timeline, metadata, summary, options) {
  let md = '';

  // Header
  md += `# Session Analysis: ${metadata.id}\n\n`;
  md += `**Date:** ${metadata.date}\n`;
  md += `**Branch:** ${metadata.branch}\n`;
  md += `**Duration:** ${metadata.duration}\n`;
  md += `**Working Directory:** ${metadata.cwd}\n`;
  md += `**Version:** ${metadata.version}\n\n`;

  // Timeline
  md += `## Timeline\n\n`;

  for (const entry of timeline) {
    if (entry.type === 'user') {
      md += `**[${entry.time}] USER:** ${entry.content}\n\n`;
    } else if (entry.type === 'assistant') {
      md += `**[${entry.time}] ASSISTANT:**`;

      if (entry.content) {
        md += ` ${entry.content}\n`;
      } else {
        md += `\n`;
      }

      if (entry.tools && entry.tools.length > 0) {
        for (const tool of entry.tools) {
          const paramsStr = formatToolParams(tool.params, options.verbosity);
          md += `- Tool: **${tool.name}**(${paramsStr})\n`;
        }
      }

      md += `\n`;
    } else if (entry.type === 'subagent') {
      md += `**[${entry.time}] SUBAGENT:** @${entry.subagent}\n`;
      if (options.verbosity !== 'minimal') {
        md += `${entry.content}\n`;
      }
      md += `\n`;
    } else if (entry.type === 'system') {
      md += `**[${entry.time}] SYSTEM:** ${entry.content}\n\n`;
    }
  }

  // Summary
  md += `## Summary\n\n`;
  md += `**Total Events:** ${summary.totalEvents} (filtered to ${summary.filteredEvents})\n\n`;

  if (Object.keys(summary.toolsUsed).length > 0) {
    md += `**Tools Used:**\n`;
    for (const [tool, count] of Object.entries(summary.toolsUsed).sort((a, b) => b[1] - a[1])) {
      md += `- ${tool}: ${count}\n`;
    }
    md += `\n`;
  }

  if (Object.keys(summary.subagentsUsed).length > 0) {
    md += `**Subagents:**\n`;
    for (const [subagent, count] of Object.entries(summary.subagentsUsed)) {
      md += `- @${subagent}: ${count}\n`;
    }
    md += `\n`;
  }

  md += `**Files Modified:** ${summary.filesModified}\n`;
  md += `**Errors:** ${summary.errors}\n`;
  md += `**Warnings:** ${summary.warnings}\n`;
  md += `**Duration:** ${metadata.duration}\n`;

  return md;
}

/**
 * Format tool parameters for display
 */
function formatToolParams(params, verbosity) {
  if (verbosity === 'minimal') {
    return Object.keys(params).join(', ');
  }

  const parts = [];
  for (const [key, value] of Object.entries(params)) {
    if (verbosity === 'detailed') {
      parts.push(`${key}="${value}"`);
    } else {
      parts.push(`${key}="${truncate(value, 50)}"`);
    }
  }

  return parts.join(', ');
}

// ============================================================================
// Output Formatting - JSON
// ============================================================================

/**
 * Format timeline as JSON
 */
function formatJSON(timeline, metadata, summary, options) {
  const output = {
    session: {
      id: metadata.id,
      fullId: metadata.fullId,
      date: metadata.date,
      branch: metadata.branch,
      cwd: metadata.cwd,
      version: metadata.version,
      startTime: metadata.startTime,
      endTime: metadata.endTime,
      duration: metadata.duration
    },
    timeline: timeline.map(entry => {
      const result = {
        time: entry.time,
        type: entry.type
      };

      if (entry.content) {
        result.content = entry.content;
      }

      if (entry.tools) {
        result.tools = entry.tools;
      }

      if (entry.subagent) {
        result.subagent = entry.subagent;
      }

      return result;
    }),
    summary: summary
  };

  return JSON.stringify(output, null, 2);
}

// ============================================================================
// Main Processing Logic
// ============================================================================

/**
 * Process a single transcript file
 */
function processTranscript(inputPath, options) {
  try {
    // Load transcript
    const events = loadTranscript(inputPath);

    // Extract metadata
    const metadata = extractSessionMetadata(events);

    // Filter events
    const filtered = filterEvents(events, options);

    // Build timeline
    const timeline = buildTimeline(filtered, options, metadata);

    // Generate summary
    const summary = generateSummary(timeline, events, options);

    // Format output
    let output;
    if (options.format === 'json') {
      output = formatJSON(timeline, metadata, summary, options);
    } else {
      output = formatMarkdown(timeline, metadata, summary, options);
    }

    // Determine output path
    let outputPath = options.output;

    if (options.outputDir && !options.output) {
      const basename = path.basename(inputPath, '.json');
      const ext = options.format === 'json' ? '.json' : '.md';
      outputPath = path.join(options.outputDir, basename + '-condensed' + ext);
    }

    // Write output
    writeOutput(output, outputPath);

    return true;
  } catch (error) {
    console.error(`Error processing ${inputPath}: ${error.message}`);
    return false;
  }
}

/**
 * Process multiple transcript files (batch mode)
 */
function processBatch(inputPath, options) {
  const files = getTranscriptFiles(inputPath);

  if (files.length === 0) {
    console.error(`No transcript files found in ${inputPath}`);
    return false;
  }

  console.error(`Processing ${files.length} transcript(s)...`);

  let successCount = 0;
  for (const file of files) {
    console.error(`Processing ${path.basename(file)}...`);
    if (processTranscript(file, options)) {
      successCount++;
    }
  }

  console.error(`\nCompleted: ${successCount}/${files.length} successful`);
  return successCount === files.length;
}

// ============================================================================
// Entry Point
// ============================================================================

function main() {
  const args = process.argv.slice(2);
  const options = parseArguments(args);

  // Show help if requested
  if (options.help) {
    showHelp();
    process.exit(0);
  }

  // Validate input
  if (!options.input) {
    console.error('Error: No input file or directory specified');
    console.error('Run with --help for usage information');
    process.exit(1);
  }

  // Check if input exists
  if (!fs.existsSync(options.input)) {
    console.error(`Error: Input path does not exist: ${options.input}`);
    process.exit(1);
  }

  // Validate format
  if (options.format !== 'markdown' && options.format !== 'json') {
    console.error(`Error: Invalid format "${options.format}". Must be "markdown" or "json"`);
    process.exit(1);
  }

  // Validate verbosity
  if (!['minimal', 'standard', 'detailed'].includes(options.verbosity)) {
    console.error(`Error: Invalid verbosity "${options.verbosity}". Must be "minimal", "standard", or "detailed"`);
    process.exit(1);
  }

  // Determine if input is file or directory
  const stats = fs.statSync(options.input);
  let success;

  if (stats.isDirectory()) {
    // Batch processing
    if (!options.outputDir && !options.output) {
      console.error('Error: Batch processing requires --output-dir option');
      process.exit(1);
    }
    success = processBatch(options.input, options);
  } else if (stats.isFile()) {
    // Single file processing
    success = processTranscript(options.input, options);
  } else {
    console.error(`Error: Input must be a file or directory: ${options.input}`);
    process.exit(1);
  }

  process.exit(success ? 0 : 1);
}

// Run main function
if (require.main === module) {
  main();
}

module.exports = {
  parseArguments,
  loadTranscript,
  extractSessionMetadata,
  filterEvents,
  buildTimeline,
  generateSummary,
  formatMarkdown,
  formatJSON
};

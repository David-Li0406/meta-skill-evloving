/**
 * Metrics Calculator - Agent Lens
 *
 * Calculates comprehensive metrics from event streams:
 * - Token usage estimation
 * - Cost calculation with model pricing
 * - Tool usage breakdown
 * - Error rate tracking
 * - Session duration and timing metrics
 */

import type { HookEvent } from '../types';

// Model pricing (per 1M tokens) - Updated 2026-01-14
const MODEL_PRICING: Record<string, { input: number; output: number }> = {
  'claude-sonnet-4-5-20250929[1m]': { input: 3.00, output: 15.00 },
  'claude-opus-4-5-20251101': { input: 15.00, output: 75.00 },
  'claude-haiku-4-5': { input: 0.80, output: 4.00 },
  // Fallback for unknown models
  'unknown': { input: 3.00, output: 15.00 }
};

export interface SessionMetrics {
  // Token metrics
  totalTokens: number;
  inputTokens: number;
  outputTokens: number;
  estimatedCost: number;
  costPerThousandTokens: number;

  // Tool metrics
  toolCalls: number;
  uniqueTools: Set<string>;
  toolBreakdown: Array<{ tool: string; count: number; percentage: number }>;

  // Timing metrics
  duration: number; // milliseconds
  firstTokenLatency?: number; // milliseconds
  averageToolLatency: number;

  // Error metrics
  errors: number;
  errorTypes: Record<string, number>;
  errorRate: number; // percentage

  // Agent metrics
  agentCount: number;
  uniqueAgents: Set<string>;

  // Skill metrics
  skillInvocations: number;
  uniqueSkills: Set<string>;

  // Model usage
  modelName?: string;
  modelCalls: number;
}

export interface TokenTrendPoint {
  timestamp: number;
  tokens: number;
  cumulative: number;
  cost: number;
}

export interface ToolUsageData {
  tool: string;
  count: number;
  percentage: number;
  averageLatency: number;
}

export class MetricsCalculator {
  /**
   * Calculate comprehensive metrics for a session's events
   */
  static calculateSessionMetrics(events: HookEvent[]): SessionMetrics {
    const metrics: SessionMetrics = {
      totalTokens: 0,
      inputTokens: 0,
      outputTokens: 0,
      estimatedCost: 0,
      costPerThousandTokens: 0,
      toolCalls: 0,
      uniqueTools: new Set(),
      toolBreakdown: [],
      duration: 0,
      averageToolLatency: 0,
      errors: 0,
      errorTypes: {},
      errorRate: 0,
      agentCount: 0,
      uniqueAgents: new Set(),
      skillInvocations: 0,
      uniqueSkills: new Set(),
      modelCalls: 0
    };

    if (events.length === 0) return metrics;

    // Calculate session duration
    const timestamps = events
      .map(e => e.timestamp)
      .filter((t): t is number => t !== undefined)
      .sort((a, b) => a - b);

    if (timestamps.length >= 2) {
      metrics.duration = timestamps[timestamps.length - 1] - timestamps[0];
    }

    // Track tool latencies for averaging
    const toolLatencies: number[] = [];
    const toolCounts = new Map<string, number>();

    // Process each event
    for (const event of events) {
      // Token tracking from event metadata
      if (event.estimated_tokens) {
        metrics.totalTokens += event.estimated_tokens;
      }

      // Tool calls
      if (event.hook_event_type === 'PreToolUse') {
        metrics.toolCalls++;
        const toolName = event.payload?.tool_name;
        if (toolName) {
          metrics.uniqueTools.add(toolName);
          toolCounts.set(toolName, (toolCounts.get(toolName) || 0) + 1);
        }

        // Calculate tool latency (PreToolUse → PostToolUse duration)
        if (event.children && event.children.length > 0) {
          const postToolUseChild = events.find(e =>
            e.event_id === event.children![0] &&
            e.hook_event_type === 'PostToolUse'
          );

          if (postToolUseChild?.timestamp && event.timestamp) {
            const latency = postToolUseChild.timestamp - event.timestamp;
            toolLatencies.push(latency);
          }
        }
      }

      // Errors
      if (event.payload?.error || event.payload?.status === 'error') {
        metrics.errors++;
        const errorType = this.classifyError(event.payload);
        metrics.errorTypes[errorType] = (metrics.errorTypes[errorType] || 0) + 1;
      }

      // Agents
      if (event.source_app) {
        metrics.uniqueAgents.add(event.source_app);
      }

      // Skills
      if (event.skill_name) {
        metrics.skillInvocations++;
        metrics.uniqueSkills.add(event.skill_name);
      }

      // Model usage
      if (event.model_name) {
        metrics.modelName = event.model_name; // Use most recent
        metrics.modelCalls++;
      }
    }

    metrics.agentCount = metrics.uniqueAgents.size;

    // Calculate average tool latency
    if (toolLatencies.length > 0) {
      metrics.averageToolLatency = toolLatencies.reduce((a, b) => a + b, 0) / toolLatencies.length;
    }

    // Estimate cost based on model pricing
    const model = metrics.modelName || 'unknown';
    const pricing = MODEL_PRICING[model] || MODEL_PRICING.unknown;

    // Assume 70% input, 30% output (rough heuristic - improve with actual tracking)
    metrics.inputTokens = Math.floor(metrics.totalTokens * 0.7);
    metrics.outputTokens = Math.floor(metrics.totalTokens * 0.3);

    metrics.estimatedCost =
      (metrics.inputTokens / 1_000_000) * pricing.input +
      (metrics.outputTokens / 1_000_000) * pricing.output;

    // Cost per thousand tokens
    if (metrics.totalTokens > 0) {
      metrics.costPerThousandTokens = (metrics.estimatedCost / metrics.totalTokens) * 1000;
    }

    // Error rate
    if (events.length > 0) {
      metrics.errorRate = (metrics.errors / events.length) * 100;
    }

    // Tool breakdown with percentages
    metrics.toolBreakdown = Array.from(toolCounts.entries())
      .map(([tool, count]) => ({
        tool,
        count,
        percentage: (count / metrics.toolCalls) * 100,
        averageLatency: this.getAverageToolLatency(events, tool)
      }))
      .sort((a, b) => b.count - a.count);

    // First token latency (UserPromptSubmit → first PreToolUse)
    const firstPrompt = events.find(e => e.hook_event_type === 'UserPromptSubmit');
    const firstTool = events.find(e => e.hook_event_type === 'PreToolUse');
    if (firstPrompt?.timestamp && firstTool?.timestamp) {
      metrics.firstTokenLatency = firstTool.timestamp - firstPrompt.timestamp;
    }

    return metrics;
  }

  /**
   * Get token usage trend over time for charting
   */
  static getTokenTrend(
    events: HookEvent[],
    bucketSizeMs: number = 10000 // 10 second buckets
  ): TokenTrendPoint[] {
    if (events.length === 0) return [];

    const sortedEvents = [...events]
      .filter(e => e.timestamp && e.estimated_tokens)
      .sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0));

    if (sortedEvents.length === 0) return [];

    const startTime = sortedEvents[0].timestamp!;
    const endTime = sortedEvents[sortedEvents.length - 1].timestamp!;
    const bucketCount = Math.ceil((endTime - startTime) / bucketSizeMs) || 1;

    const trend: TokenTrendPoint[] = [];
    let cumulative = 0;

    for (let i = 0; i < bucketCount; i++) {
      const bucketStart = startTime + (i * bucketSizeMs);
      const bucketEnd = bucketStart + bucketSizeMs;

      const bucketEvents = sortedEvents.filter(e =>
        e.timestamp! >= bucketStart && e.timestamp! < bucketEnd
      );

      const bucketTokens = bucketEvents.reduce((sum, e) => sum + (e.estimated_tokens || 0), 0);
      cumulative += bucketTokens;

      // Estimate cost for this bucket
      const bucketCost = bucketEvents.reduce((sum, e) => sum + (e.estimated_cost || 0), 0);

      trend.push({
        timestamp: bucketStart,
        tokens: bucketTokens,
        cumulative,
        cost: bucketCost
      });
    }

    return trend;
  }

  /**
   * Get tool usage breakdown
   */
  static getToolUsageBreakdown(events: HookEvent[]): ToolUsageData[] {
    const toolData = new Map<string, { count: number; latencies: number[] }>();

    events
      .filter(e => e.hook_event_type === 'PreToolUse')
      .forEach(e => {
        const toolName = e.payload?.tool_name || 'Unknown';

        if (!toolData.has(toolName)) {
          toolData.set(toolName, { count: 0, latencies: [] });
        }

        const data = toolData.get(toolName)!;
        data.count++;

        // Calculate latency if PostToolUse exists
        if (e.children && e.children.length > 0) {
          const postToolUse = events.find(evt =>
            evt.event_id === e.children![0] &&
            evt.hook_event_type === 'PostToolUse'
          );

          if (postToolUse?.timestamp && e.timestamp) {
            const latency = postToolUse.timestamp - e.timestamp;
            data.latencies.push(latency);
          }
        }
      });

    const totalToolCalls = events.filter(e => e.hook_event_type === 'PreToolUse').length;

    return Array.from(toolData.entries())
      .map(([tool, data]) => ({
        tool,
        count: data.count,
        percentage: totalToolCalls > 0 ? (data.count / totalToolCalls) * 100 : 0,
        averageLatency: data.latencies.length > 0
          ? data.latencies.reduce((a, b) => a + b, 0) / data.latencies.length
          : 0
      }))
      .sort((a, b) => b.count - a.count);
  }

  /**
   * Get error breakdown by type
   */
  static getErrorBreakdown(events: HookEvent[]): Array<{ type: string; count: number; percentage: number }> {
    const errors = events.filter(e => e.payload?.error || e.payload?.status === 'error');

    if (errors.length === 0) return [];

    const errorTypes = new Map<string, number>();

    errors.forEach(event => {
      const type = this.classifyError(event.payload);
      errorTypes.set(type, (errorTypes.get(type) || 0) + 1);
    });

    return Array.from(errorTypes.entries())
      .map(([type, count]) => ({
        type,
        count,
        percentage: (count / errors.length) * 100
      }))
      .sort((a, b) => b.count - a.count);
  }

  /**
   * Get average latency for a specific tool
   */
  private static getAverageToolLatency(events: HookEvent[], toolName: string): number {
    const latencies: number[] = [];

    events
      .filter(e =>
        e.hook_event_type === 'PreToolUse' &&
        e.payload?.tool_name === toolName
      )
      .forEach(e => {
        if (e.children && e.children.length > 0) {
          const postToolUse = events.find(evt =>
            evt.event_id === e.children![0] &&
            evt.hook_event_type === 'PostToolUse'
          );

          if (postToolUse?.timestamp && e.timestamp) {
            latencies.push(postToolUse.timestamp - e.timestamp);
          }
        }
      });

    if (latencies.length === 0) return 0;
    return latencies.reduce((a, b) => a + b, 0) / latencies.length;
  }

  /**
   * Classify error type from payload
   */
  private static classifyError(payload: any): string {
    const error = payload?.error || payload?.message || '';

    if (typeof error !== 'string') return 'Unknown Error';

    // File system errors
    if (error.includes('ENOENT') || error.includes('not found')) return 'File Not Found';
    if (error.includes('EACCES') || error.includes('permission')) return 'Permission Denied';
    if (error.includes('EISDIR')) return 'Is Directory';
    if (error.includes('ENOTDIR')) return 'Not a Directory';

    // Network errors
    if (error.includes('ECONNREFUSED') || error.includes('connection refused')) return 'Connection Refused';
    if (error.includes('ETIMEDOUT') || error.includes('timeout')) return 'Timeout';
    if (error.includes('ENOTFOUND') || error.includes('DNS')) return 'DNS Error';
    if (error.includes('network')) return 'Network Error';

    // Code errors
    if (error.includes('SyntaxError') || error.includes('syntax')) return 'Syntax Error';
    if (error.includes('TypeError')) return 'Type Error';
    if (error.includes('ReferenceError')) return 'Reference Error';

    // Git errors
    if (error.includes('git') && error.includes('conflict')) return 'Git Conflict';
    if (error.includes('git') && error.includes('merge')) return 'Git Merge Error';

    // HTTP errors
    if (error.includes('404')) return 'HTTP 404';
    if (error.includes('500')) return 'HTTP 500';
    if (error.includes('403')) return 'HTTP 403';

    return 'Other Error';
  }

  /**
   * Estimate tokens from event payload (heuristic until real tokenizer)
   *
   * This is a rough estimation based on payload size.
   * Future: Integrate tiktoken or similar for accurate counting.
   */
  static estimateEventTokens(event: HookEvent): number {
    let estimate = 0;

    // UserPromptSubmit: Count prompt tokens
    if (event.hook_event_type === 'UserPromptSubmit' && event.payload?.prompt) {
      estimate += this.roughTokenCount(event.payload.prompt);
    }

    // Tool usage: Count input/output
    if (event.hook_event_type === 'PreToolUse' && event.payload?.tool_input) {
      estimate += this.roughTokenCount(JSON.stringify(event.payload.tool_input));
    }

    if (event.hook_event_type === 'PostToolUse' && event.payload?.tool_response) {
      estimate += this.roughTokenCount(JSON.stringify(event.payload.tool_response));
    }

    // Stop: Often includes final output
    if (event.hook_event_type === 'Stop' && event.payload?.output) {
      estimate += this.roughTokenCount(event.payload.output);
    }

    return estimate;
  }

  /**
   * Rough token count (4 chars ≈ 1 token)
   * This is a heuristic approximation until we integrate a real tokenizer
   */
  private static roughTokenCount(text: string): number {
    if (!text) return 0;
    return Math.ceil(text.length / 4);
  }

  /**
   * Estimate cost for a single event
   */
  static estimateEventCost(event: HookEvent): number {
    const tokens = this.estimateEventTokens(event);
    if (tokens === 0) return 0;

    const model = event.model_name || 'unknown';
    const pricing = MODEL_PRICING[model] || MODEL_PRICING.unknown;

    // Assume 70% input, 30% output
    const inputTokens = Math.floor(tokens * 0.7);
    const outputTokens = Math.floor(tokens * 0.3);

    return (
      (inputTokens / 1_000_000) * pricing.input +
      (outputTokens / 1_000_000) * pricing.output
    );
  }

  /**
   * Format token count for display
   */
  static formatTokens(tokens: number): string {
    if (tokens >= 1_000_000) return `${(tokens / 1_000_000).toFixed(2)}M`;
    if (tokens >= 1_000) return `${(tokens / 1_000).toFixed(1)}K`;
    return tokens.toString();
  }

  /**
   * Format cost for display
   */
  static formatCost(cost: number): string {
    if (cost === 0) return '$0.00';
    if (cost < 0.0001) return '< $0.0001';
    if (cost < 0.01) return `$${cost.toFixed(4)}`;
    if (cost < 1) return `$${cost.toFixed(3)}`;
    return `$${cost.toFixed(2)}`;
  }

  /**
   * Format duration for display
   */
  static formatDuration(ms: number): string {
    if (ms < 1000) return `${ms}ms`;
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    return `${minutes}m ${seconds}s`;
  }
}

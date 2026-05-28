/**
 * processItems - Process items in bulk
 *
 * This tool processes multiple items. In code execution pattern,
 * loop through items in execution env, not through model.
 */

import { callMCPTool } from '../mcp-client';

export interface ProcessItemsInput {
  /** IDs of items to process */
  itemIds: string[];
  /** Operation to perform */
  operation: 'validate' | 'transform' | 'archive';
  /** Optional configuration */
  options?: Record<string, unknown>;
}

export interface ProcessResult {
  itemId: string;
  success: boolean;
  error?: string;
}

export interface ProcessItemsOutput {
  /** Total items processed */
  processed: number;
  /** Successful operations */
  successful: number;
  /** Failed operations */
  failed: number;
  /** Individual results */
  results: ProcessResult[];
}

/**
 * Process multiple items in bulk
 *
 * @example
 * // In execution script:
 * const result = await processItems({
 *   itemIds: ['a', 'b', 'c'],
 *   operation: 'validate'
 * });
 * console.log(`Processed: ${result.processed}, Failed: ${result.failed}`);
 * if (result.failed > 0) {
 *   console.log('Failures:', result.results.filter(r => !r.success));
 * }
 */
export async function processItems(
  input: ProcessItemsInput
): Promise<ProcessItemsOutput> {
  return callMCPTool<ProcessItemsOutput>('example_server__process_items', input);
}

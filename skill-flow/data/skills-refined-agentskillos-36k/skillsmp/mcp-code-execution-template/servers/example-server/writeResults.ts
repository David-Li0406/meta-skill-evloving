/**
 * writeResults - Write processed results to destination
 *
 * This tool writes data to external systems. Data flows from
 * one MCP tool to another without going through model context.
 */

import { callMCPTool } from '../mcp-client';

export interface WriteResultsInput {
  /** Destination identifier */
  destinationId: string;
  /** Data to write (can be large) */
  data: unknown;
  /** Write mode */
  mode: 'append' | 'overwrite' | 'merge';
}

export interface WriteResultsOutput {
  /** Whether write succeeded */
  success: boolean;
  /** Number of records written */
  recordsWritten: number;
  /** Destination URL/path */
  destination: string;
  /** Any warnings */
  warnings?: string[];
}

/**
 * Write results to destination
 *
 * Key pattern: Data flows between MCP tools without entering model context.
 *
 * @example
 * // Data flows: fetchData → processItems → writeResults
 * // All in execution env, model never sees the data
 *
 * const source = await fetchData({ id: 'input' });
 * const processed = await processItems({
 *   itemIds: source.items.map(i => i.id),
 *   operation: 'transform'
 * });
 * const written = await writeResults({
 *   destinationId: 'output',
 *   data: processed.results,
 *   mode: 'overwrite'
 * });
 * console.log(`Wrote ${written.recordsWritten} records`);
 */
export async function writeResults(
  input: WriteResultsInput
): Promise<WriteResultsOutput> {
  return callMCPTool<WriteResultsOutput>('example_server__write_results', input);
}

/**
 * fetchData - Retrieves data from external source
 *
 * This tool fetches potentially large datasets. Use code execution
 * pattern to process data outside model context.
 *
 * Token efficiency: Process in execution env, return only summary
 */

import { callMCPTool } from '../mcp-client';

export interface FetchDataInput {
  /** Unique identifier for the data source */
  id: string;
  /** Optional: specific fields to retrieve */
  fields?: string[];
  /** Optional: maximum items to fetch */
  limit?: number;
}

export interface DataItem {
  id: string;
  name: string;
  value: number;
  metadata: Record<string, unknown>;
  createdAt: string;
  status: 'active' | 'inactive' | 'pending';
}

export interface FetchDataOutput {
  /** Total count of items available */
  totalCount: number;
  /** Items retrieved (may be large!) */
  items: DataItem[];
  /** Pagination cursor for next batch */
  nextCursor?: string;
}

/**
 * Fetch data from the example server
 *
 * WARNING: This may return large datasets. Always process in
 * execution environment and return only summaries to model.
 *
 * @example
 * // In execution script (not model context):
 * const data = await fetchData({ id: 'dataset-123' });
 * const activeItems = data.items.filter(i => i.status === 'active');
 * console.log(`Found ${activeItems.length} active items`);
 * console.log(JSON.stringify(activeItems.slice(0, 5))); // Only 5 to model
 */
export async function fetchData(input: FetchDataInput): Promise<FetchDataOutput> {
  return callMCPTool<FetchDataOutput>('example_server__fetch_data', {
    id: input.id,
    fields: input.fields,
    limit: input.limit
  });
}

/**
 * Example Task: Demonstrate MCP Code Execution Pattern
 *
 * This file shows how to write code that processes data outside
 * the model context for 98%+ token efficiency.
 *
 * Run with:
 *   MCP_MOCK_MODE=true npx tsx workspace/example-task.ts
 *   # or
 *   python scripts/execute.py workspace/example-task.ts
 */

import { fetchData, FetchDataOutput } from '../servers/example-server/fetchData';
import { processItems, ProcessItemsOutput } from '../servers/example-server/processItems';
import { writeResults, WriteResultsOutput } from '../servers/example-server/writeResults';

async function main() {
  console.log('Starting MCP Code Execution Example...\n');

  // Step 1: Fetch data from source
  // In real usage, this would fetch from Google Drive, Salesforce, etc.
  console.log('Step 1: Fetching data...');
  const sourceData: FetchDataOutput = await fetchData({
    id: 'example-source-123',
    fields: ['name', 'status', 'value'],
    limit: 1000
  });
  console.log(`Fetched ${sourceData.totalCount} items\n`);

  // Step 2: Process the data
  // All processing happens in execution environment, NOT in model context
  console.log('Step 2: Processing items...');
  const processed: ProcessItemsOutput = await processItems({
    itemIds: sourceData.items.map(item => item.id),
    operation: 'transform',
    filters: {
      minValue: 100,
      status: 'active'
    }
  });
  console.log(`Processed ${processed.successCount}/${processed.totalProcessed} items\n`);

  // Step 3: Write results to destination
  console.log('Step 3: Writing results...');
  const written: WriteResultsOutput = await writeResults({
    destinationId: 'output-destination-456',
    data: processed.results,
    mode: 'overwrite'
  });
  console.log(`Wrote ${written.recordsWritten} records to ${written.destination}\n`);

  // Step 4: Return ONLY the summary
  // This is what goes back to model context (~100 tokens)
  console.log('='.repeat(50));
  console.log('EXECUTION SUMMARY');
  console.log('='.repeat(50));
  console.log(`Source: ${sourceData.totalCount} items fetched`);
  console.log(`Processed: ${processed.successCount} items transformed`);
  console.log(`Written: ${written.recordsWritten} records saved`);
  console.log(`Status: ${written.success ? 'SUCCESS' : 'FAILED'}`);

  if (written.warnings && written.warnings.length > 0) {
    console.log(`Warnings: ${written.warnings.join(', ')}`);
  }
}

// Execute
main().catch(error => {
  console.error('Task failed:', error.message);
  process.exit(1);
});

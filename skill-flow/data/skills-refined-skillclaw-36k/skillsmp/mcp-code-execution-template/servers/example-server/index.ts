/**
 * Example Server - MCP Tool Wrappers
 *
 * This file exports all tools from the example-server.
 * Import this to access all tools from this server.
 *
 * Usage:
 *   import * as example from './servers/example-server';
 *   const result = await example.fetchData({ id: '123' });
 */

export { fetchData, type FetchDataInput, type FetchDataOutput } from './fetchData';
export { processItems, type ProcessItemsInput, type ProcessItemsOutput } from './processItems';
export { writeResults, type WriteResultsInput, type WriteResultsOutput } from './writeResults';

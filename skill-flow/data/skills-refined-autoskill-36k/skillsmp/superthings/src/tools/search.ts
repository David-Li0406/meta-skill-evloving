import { executeAppleScriptFile } from '../lib/applescript.js';
import { SearchTodosSchema } from '../types/mcp.js';
import { AbstractToolHandler, ToolDefinition } from '../lib/abstract-tool-handler.js';
import { z } from 'zod';

type SearchParams = z.infer<typeof SearchTodosSchema>;

interface SearchResult {
  id: string;
  name: string;
  area: string;
  tags: string;
  list: string;
}

/**
 * Handler for searching Things 3 todos across lists
 */
class SearchToolHandler extends AbstractToolHandler<SearchParams> {
  protected definitions: ToolDefinition<SearchParams>[] = [
    {
      name: 'things_search',
      description: 'Search for to-dos across all lists by keyword, tag, or URL presence. Perfect for finding specific tasks or filtering URL-only items during triage.',
      schema: SearchTodosSchema
    }
  ];

  async execute(toolName: string, params: SearchParams): Promise<string> {
    if (toolName !== 'things_search') {
      throw new Error(`Unknown tool: ${toolName}`);
    }

    const {
      query = '*',
      list = '',
      tag = '',
      has_url = false,
      max_results = 100
    } = params;

    // Build script arguments
    const scriptArgs = [
      query,
      list,
      tag,
      has_url ? 'true' : '',
      String(max_results)
    ];

    const output = await executeAppleScriptFile('search-todos', scriptArgs);

    // Return empty array for empty output
    if (!output.trim()) {
      return JSON.stringify({ todos: [], count: 0 }, null, 2);
    }

    // Parse the output (format: id|name|area|tags|list)
    const todos: SearchResult[] = output
      .trim()
      .split('\n')
      .filter(line => line.trim())
      .map(line => {
        const [id, name, area, tags, listName] = line.split('|');
        return {
          id: id || '',
          name: name || '',
          area: area || '',
          tags: tags || '',
          list: listName || ''
        };
      })
      .filter(todo => todo.id && todo.name);

    return JSON.stringify({
      todos,
      count: todos.length,
      query: query !== '*' ? query : undefined,
      filters: {
        list: list || undefined,
        tag: tag || undefined,
        has_url: has_url || undefined
      }
    }, null, 2);
  }
}

export const searchToolHandler = new SearchToolHandler();

export const searchTools = searchToolHandler.tools;
export const handleSearch = searchToolHandler.handle.bind(searchToolHandler);

#!/usr/bin/env tsx
import { Client } from '@notionhq/client';
import { parseArgs } from 'util';

const notion = new Client({ auth: process.env.NOTION_API_KEY });

const { values } = parseArgs({
  options: {
    query: { type: 'string', short: 'q' },
    filter: { type: 'string', short: 'f' },
    limit: { type: 'string', short: 'l', default: '10' },
    json: { type: 'boolean', default: false },
  },
});

if (!values.query) {
  console.error(`Usage: search-pages.ts --query <text> [--filter <page|database>] [--limit <n>]

Search Notion pages by keyword.

Options:
  --query, -q   Search text (required)
  --filter, -f  Filter by object type: "page" or "database"
  --limit, -l   Max results (default: 10)
  --json        Output full response as JSON

Examples:
  search-pages.ts -q "meeting notes"
  search-pages.ts -q "Q4 planning" --filter page --limit 20
`);
  process.exit(1);
}

async function main() {
  try {
    const searchParams: any = {
      query: values.query,
      page_size: Math.min(parseInt(values.limit || '10'), 100),
    };

    if (values.filter === 'page' || values.filter === 'database') {
      searchParams.filter = { property: 'object', value: values.filter };
    }

    const response = await notion.search(searchParams);

    if (values.json) {
      console.log(JSON.stringify(response.results, null, 2));
      return;
    }

    console.log(`Found ${response.results.length} results:\n`);

    for (const result of response.results as any[]) {
      const isPage = result.object === 'page';
      const title = isPage ? getPageTitle(result) : getDatabaseTitle(result);
      const type = isPage ? 'page' : 'database';
      const parent = getParentInfo(result);

      console.log(`[${type}] ${title}`);
      console.log(`  ID: ${result.id}`);
      if (parent) console.log(`  Parent: ${parent}`);
      console.log(`  URL: ${result.url}`);
      console.log();
    }
  } catch (error: any) {
    console.error('Error:', JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

function getPageTitle(page: any): string {
  for (const val of Object.values(page.properties || {}) as any[]) {
    if (val.type === 'title' && val.title?.[0]) {
      return val.title[0].plain_text;
    }
  }
  return '(Untitled)';
}

function getDatabaseTitle(db: any): string {
  return db.title?.[0]?.plain_text || '(Untitled Database)';
}

function getParentInfo(item: any): string | null {
  if (item.parent?.type === 'workspace') return 'Workspace';
  if (item.parent?.type === 'page_id') return `Page: ${item.parent.page_id}`;
  if (item.parent?.type === 'database_id') return `Database: ${item.parent.database_id}`;
  return null;
}

main();

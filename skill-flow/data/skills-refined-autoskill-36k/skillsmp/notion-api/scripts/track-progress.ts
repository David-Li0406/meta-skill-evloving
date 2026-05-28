#!/usr/bin/env tsx
import { Client } from '@notionhq/client';
import { parseArgs } from 'util';

const notion = new Client({ auth: process.env.NOTION_API_KEY });

function extractId(input: string): string {
  if (input.includes('notion.so')) {
    const url = new URL(input);
    const pParam = url.searchParams.get('p');
    if (pParam) return pParam.replace(/-/g, '');
    const match = url.pathname.match(/([a-f0-9]{32})$/i)
      || url.pathname.match(/([a-f0-9-]{36})$/i)
      || url.pathname.match(/-([a-f0-9]{32})(?:\?|$)/i);
    if (match) return match[1].replace(/-/g, '');
  }
  return input.replace(/-/g, '');
}

const { values } = parseArgs({
  options: {
    database: { type: 'string', short: 'd' },
    status: { type: 'string', short: 's' },
    'group-by': { type: 'string', short: 'g', default: 'Status' },
    json: { type: 'boolean', default: false },
  },
});

if (!values.database) {
  console.error(`Usage: track-progress.ts --database <DB_ID|URL> [--status <status>] [--group-by <property>]

Summarize progress of items in a database.

Options:
  --database, -d   Database ID or URL (required)
  --status, -s     Filter by specific status
  --group-by, -g   Property to group by (default: Status)
  --json           Output as JSON

Examples:
  track-progress.ts -d abc123
  track-progress.ts -d abc123 --status "In Progress"
  track-progress.ts -d abc123 --group-by "Priority"
`);
  process.exit(1);
}

const databaseId = extractId(values.database);

async function getAllPages(): Promise<any[]> {
  const pages: any[] = [];
  let cursor: string | undefined;

  const queryParams: any = {
    database_id: databaseId,
    page_size: 100,
  };

  if (values.status) {
    queryParams.filter = {
      property: 'Status',
      status: { equals: values.status },
    };
  }

  do {
    const response = await notion.databases.query({
      ...queryParams,
      start_cursor: cursor,
    });
    pages.push(...response.results);
    cursor = response.has_more ? response.next_cursor! : undefined;
  } while (cursor);

  return pages;
}

function getPropertyValue(page: any, propName: string): string {
  const prop = page.properties[propName];
  if (!prop) return '(none)';

  switch (prop.type) {
    case 'status':
      return prop.status?.name || '(none)';
    case 'select':
      return prop.select?.name || '(none)';
    case 'multi_select':
      return prop.multi_select?.map((s: any) => s.name).join(', ') || '(none)';
    case 'people':
      return prop.people?.[0]?.name || '(unassigned)';
    default:
      return '(none)';
  }
}

async function main() {
  try {
    const pages = await getAllPages();
    const groupBy = values['group-by'] || 'Status';

    // Group pages
    const groups: Record<string, any[]> = {};
    for (const page of pages) {
      const groupValue = getPropertyValue(page, groupBy);
      if (!groups[groupValue]) groups[groupValue] = [];
      groups[groupValue].push(page);
    }

    // Calculate stats
    const total = pages.length;
    const stats = Object.entries(groups).map(([name, items]) => ({
      name,
      count: items.length,
      percent: Math.round((items.length / total) * 100),
    })).sort((a, b) => b.count - a.count);

    if (values.json) {
      console.log(JSON.stringify({ total, groupBy, stats }, null, 2));
      return;
    }

    // Display summary
    console.log(`\n📊 Progress Summary (${total} items)\n`);
    console.log(`Grouped by: ${groupBy}\n`);

    const maxNameLen = Math.max(...stats.map(s => s.name.length), 10);
    const barWidth = 30;

    for (const { name, count, percent } of stats) {
      const filled = Math.round((percent / 100) * barWidth);
      const bar = '█'.repeat(filled) + '░'.repeat(barWidth - filled);
      console.log(`${name.padEnd(maxNameLen)}  ${bar}  ${count} (${percent}%)`);
    }

    // Show completion if Status-based
    if (groupBy === 'Status') {
      const doneCount = groups['Done']?.length || 0;
      const completionRate = Math.round((doneCount / total) * 100);
      console.log(`\n✓ Completion: ${doneCount}/${total} (${completionRate}%)`);
    }

    console.log();
  } catch (error: any) {
    console.error('Error:', JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

main();

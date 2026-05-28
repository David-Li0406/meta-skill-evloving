#!/usr/bin/env tsx
import { Client } from '@notionhq/client';
import { NotionToMarkdown } from 'notion-to-md';
import { parseArgs } from 'util';
import { writeFile, mkdir } from 'fs/promises';
import { join } from 'path';

const notion = new Client({ auth: process.env.NOTION_API_KEY });
const n2m = new NotionToMarkdown({ notionClient: notion });

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
    format: { type: 'string', short: 'f', default: 'csv' },
    output: { type: 'string', short: 'o' },
    'include-content': { type: 'boolean', default: false },
  },
});

if (!values.database) {
  console.error(`Usage: export-db.ts --database <DB_ID|URL> --format <csv|md|json> [--output <file>]

Export a database as CSV, Markdown, or JSON.

Options:
  --database, -d      Database ID or URL (required)
  --format, -f        Output format: csv, md, json (default: csv)
  --output, -o        Output file/folder (default: stdout for csv/json, ./export for md)
  --include-content   Include page content (md format only)

Examples:
  export-db.ts -d abc123 -f csv -o tasks.csv
  export-db.ts -d abc123 -f md -o ./docs --include-content
  export-db.ts -d abc123 -f json > backup.json
`);
  process.exit(1);
}

const databaseId = extractId(values.database);

async function getAllPages(): Promise<any[]> {
  const pages: any[] = [];
  let cursor: string | undefined;

  do {
    const response = await notion.databases.query({
      database_id: databaseId,
      start_cursor: cursor,
      page_size: 100,
    });
    pages.push(...response.results);
    cursor = response.has_more ? response.next_cursor! : undefined;
  } while (cursor);

  return pages;
}

async function exportCsv(pages: any[]): Promise<string> {
  if (pages.length === 0) return '';

  // Get all property names from first page
  const propNames = Object.keys(pages[0].properties);
  const headers = ['id', 'url', ...propNames];

  const rows = [headers.join(',')];

  for (const page of pages) {
    const row = [
      page.id,
      page.url,
      ...propNames.map(name => {
        const val = formatPropertyForCsv(page.properties[name]);
        return `"${val.replace(/"/g, '""')}"`;
      }),
    ];
    rows.push(row.join(','));
  }

  return rows.join('\n');
}

async function exportMarkdown(pages: any[], folder: string, includeContent: boolean): Promise<void> {
  await mkdir(folder, { recursive: true });

  for (const page of pages) {
    const title = getTitle(page.properties);
    const safeTitle = title.replace(/[<>:"/\\|?*]/g, '_').slice(0, 100);

    let content = `# ${title}\n\n`;
    content += `<!-- id: ${page.id} -->\n\n`;

    // Properties
    content += '## Properties\n\n';
    for (const [name, prop] of Object.entries(page.properties) as [string, any][]) {
      if (prop.type === 'title') continue;
      const val = formatProperty(prop);
      if (val) content += `- **${name}**: ${val}\n`;
    }

    // Content
    if (includeContent) {
      content += '\n## Content\n\n';
      const mdBlocks = await n2m.pageToMarkdown(page.id);
      const mdString = n2m.toMarkdownString(mdBlocks);
      content += mdString.parent || '(No content)';
    }

    const filePath = join(folder, `${safeTitle}.md`);
    await writeFile(filePath, content);
    console.error(`✓ ${filePath}`);
  }
}

function exportJson(pages: any[]): string {
  return JSON.stringify(pages.map(p => ({
    id: p.id,
    url: p.url,
    created_time: p.created_time,
    last_edited_time: p.last_edited_time,
    properties: p.properties,
  })), null, 2);
}

function getTitle(props: any): string {
  for (const val of Object.values(props) as any[]) {
    if (val.type === 'title' && val.title?.[0]) {
      return val.title[0].plain_text;
    }
  }
  return 'Untitled';
}

function formatPropertyForCsv(prop: any): string {
  return formatProperty(prop) || '';
}

function formatProperty(prop: any): string | null {
  switch (prop.type) {
    case 'title':
      return prop.title?.map((t: any) => t.plain_text).join('') || null;
    case 'rich_text':
      return prop.rich_text?.map((t: any) => t.plain_text).join('') || null;
    case 'number':
      return prop.number?.toString() ?? null;
    case 'select':
      return prop.select?.name || null;
    case 'multi_select':
      return prop.multi_select?.map((s: any) => s.name).join(', ') || null;
    case 'status':
      return prop.status?.name || null;
    case 'date':
      if (!prop.date) return null;
      return prop.date.end ? `${prop.date.start} to ${prop.date.end}` : prop.date.start;
    case 'people':
      return prop.people?.map((p: any) => p.name).join(', ') || null;
    case 'checkbox':
      return prop.checkbox ? 'Yes' : 'No';
    case 'url':
      return prop.url || null;
    case 'email':
      return prop.email || null;
    case 'phone_number':
      return prop.phone_number || null;
    case 'relation':
      return prop.relation?.map((r: any) => r.id).join(', ') || null;
    case 'unique_id':
      return prop.unique_id?.prefix
        ? `${prop.unique_id.prefix}-${prop.unique_id.number}`
        : prop.unique_id?.number?.toString() || null;
    default:
      return null;
  }
}

async function main() {
  try {
    const pages = await getAllPages();
    console.error(`Found ${pages.length} pages`);

    switch (values.format) {
      case 'csv': {
        const csv = await exportCsv(pages);
        if (values.output) {
          await writeFile(values.output, csv);
          console.error(`Saved to ${values.output}`);
        } else {
          console.log(csv);
        }
        break;
      }
      case 'md': {
        const folder = values.output || './export';
        await exportMarkdown(pages, folder, values['include-content'] || false);
        console.error(`Exported ${pages.length} files to ${folder}`);
        break;
      }
      case 'json': {
        const json = exportJson(pages);
        if (values.output) {
          await writeFile(values.output, json);
          console.error(`Saved to ${values.output}`);
        } else {
          console.log(json);
        }
        break;
      }
      default:
        console.error(`Unknown format: ${values.format}`);
        process.exit(1);
    }
  } catch (error: any) {
    console.error('Error:', JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

main();

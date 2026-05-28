#!/usr/bin/env tsx
import { Client } from '@notionhq/client';
import { NotionToMarkdown } from 'notion-to-md';
import { parseArgs } from 'util';
import { mkdir, writeFile } from 'fs/promises';
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
    page: { type: 'string', short: 'p' },
    database: { type: 'string', short: 'd' },
    local: { type: 'string', short: 'l' },
    depth: { type: 'string', default: '2' },
  },
});

if ((!values.page && !values.database) || !values.local) {
  console.error(`Usage: sync-changes.ts --page <PAGE_ID|URL> --local <folder>
       sync-changes.ts --database <DB_ID|URL> --local <folder>

Sync Notion pages to local Markdown files, including subpages.

Options:
  --page, -p      Page ID or URL to sync
  --database, -d  Database ID or URL to sync all pages from
  --local, -l     Local folder to save files (required)
  --depth         Max depth for subpages (default: 2)

Examples:
  sync-changes.ts --page abc123 --local ./docs
  sync-changes.ts --database abc123 --local ./wiki --depth 3
`);
  process.exit(1);
}

const maxDepth = parseInt(values.depth || '2');

async function syncPage(pageId: string, folder: string, depth: number = 0): Promise<void> {
  if (depth > maxDepth) return;

  const page = await notion.pages.retrieve({ page_id: pageId }) as any;
  const title = getTitle(page.properties);
  const safeTitle = title.replace(/[<>:"/\\|?*]/g, '_').slice(0, 100);

  // Get page content
  const mdBlocks = await n2m.pageToMarkdown(pageId);
  const mdString = n2m.toMarkdownString(mdBlocks);

  let content = `# ${title}\n\n`;
  content += `<!-- notion-id: ${pageId} -->\n`;
  content += `<!-- synced: ${new Date().toISOString()} -->\n\n`;

  if (mdString.parent.trim()) {
    content += mdString.parent;
  }

  // Save file
  const filePath = join(folder, `${safeTitle}.md`);
  await writeFile(filePath, content);
  console.log(`✓ ${filePath}`);

  // Find and sync child pages
  const blocks = await notion.blocks.children.list({ block_id: pageId });
  const childPages = blocks.results.filter((b: any) => b.type === 'child_page');

  if (childPages.length > 0 && depth < maxDepth) {
    const subFolder = join(folder, safeTitle);
    await mkdir(subFolder, { recursive: true });

    for (const child of childPages as any[]) {
      await syncPage(child.id, subFolder, depth + 1);
    }
  }
}

async function syncDatabase(databaseId: string, folder: string): Promise<void> {
  let cursor: string | undefined;

  do {
    const response = await notion.databases.query({
      database_id: databaseId,
      start_cursor: cursor,
      page_size: 100,
    });

    for (const page of response.results) {
      await syncPage(page.id, folder, 0);
    }

    cursor = response.has_more ? response.next_cursor! : undefined;
  } while (cursor);
}

function getTitle(props: any): string {
  for (const val of Object.values(props || {}) as any[]) {
    if (val.type === 'title' && val.title?.[0]) {
      return val.title[0].plain_text;
    }
  }
  return 'Untitled';
}

async function main() {
  try {
    await mkdir(values.local!, { recursive: true });

    if (values.page) {
      const pageId = extractId(values.page);
      await syncPage(pageId, values.local!);
    } else if (values.database) {
      const databaseId = extractId(values.database);
      await syncDatabase(databaseId, values.local!);
    }

    console.log('\nSync complete!');
  } catch (error: any) {
    console.error('Error:', JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

main();

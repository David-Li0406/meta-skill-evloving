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
    page: { type: 'string', short: 'p' },
    'target-db': { type: 'string', short: 't' },
    'target-page': { type: 'string' },
    json: { type: 'boolean', default: false },
  },
});

if (!values.page || (!values['target-db'] && !values['target-page'])) {
  console.error(`Usage: clone-page.ts --page <PAGE_ID|URL> --target-db <DB_ID|URL>
       clone-page.ts --page <PAGE_ID|URL> --target-page <PAGE_ID|URL>

Deep clone a page (properties + content blocks) to another location.
Does NOT clone subpages.

Options:
  --page, -p       Source page ID or URL (required)
  --target-db, -t  Target database ID or URL
  --target-page    Target page ID or URL (clone as child page)
  --json           Output full response as JSON

Examples:
  clone-page.ts --page abc123 --target-db def456
  clone-page.ts --page 'https://notion.so/...' --target-page xyz789
`);
  process.exit(1);
}

const sourceId = extractId(values.page);
const targetDbId = values['target-db'] ? extractId(values['target-db']) : null;
const targetPageId = values['target-page'] ? extractId(values['target-page']) : null;

async function cloneBlocks(sourceBlockId: string, targetBlockId: string): Promise<void> {
  const blocks = await notion.blocks.children.list({ block_id: sourceBlockId });

  for (const block of blocks.results as any[]) {
    // Skip child_page and child_database - we don't clone subpages
    if (block.type === 'child_page' || block.type === 'child_database') {
      continue;
    }

    // Create a copy of the block without system properties
    const blockData: any = {
      object: 'block',
      type: block.type,
      [block.type]: block[block.type],
    };

    // Remove read-only properties
    if (blockData[block.type]) {
      delete blockData[block.type].id;
      delete blockData[block.type].created_time;
      delete blockData[block.type].last_edited_time;
    }

    try {
      const newBlock = await notion.blocks.children.append({
        block_id: targetBlockId,
        children: [blockData],
      });

      // Recursively clone children if block has them
      if (block.has_children && block.type !== 'child_page' && block.type !== 'child_database') {
        const newBlockId = (newBlock.results[0] as any).id;
        await cloneBlocks(block.id, newBlockId);
      }
    } catch (e: any) {
      // Some block types can't be created via API, skip them
      console.error(`  Skipped ${block.type}: ${e.message}`);
    }
  }
}

async function main() {
  try {
    // Get source page
    const sourcePage = await notion.pages.retrieve({ page_id: sourceId }) as any;
    const title = getTitle(sourcePage.properties);

    console.error(`Cloning: ${title}`);

    // Prepare properties for new page
    const properties: any = {};

    for (const [name, prop] of Object.entries(sourcePage.properties) as [string, any][]) {
      // Skip computed properties
      if (['formula', 'rollup', 'created_time', 'created_by', 'last_edited_time', 'last_edited_by', 'unique_id'].includes(prop.type)) {
        continue;
      }
      properties[name] = prop;
    }

    // Create new page
    let newPage: any;

    if (targetDbId) {
      newPage = await notion.pages.create({
        parent: { database_id: targetDbId },
        properties,
      });
    } else if (targetPageId) {
      // For page parent, we need title property
      const titleProp = Object.entries(properties).find(([_, p]: any) => p.type === 'title');
      newPage = await notion.pages.create({
        parent: { page_id: targetPageId },
        properties: titleProp ? { [titleProp[0]]: titleProp[1] } : {
          title: { title: [{ text: { content: title } }] },
        },
      });
    }

    console.error(`Created: ${newPage.url}`);

    // Clone content blocks
    console.error('Cloning content...');
    await cloneBlocks(sourceId, newPage.id);

    if (values.json) {
      console.log(JSON.stringify(newPage, null, 2));
    } else {
      console.log('✓ Clone complete');
      console.log(`  Source: ${sourceId}`);
      console.log(`  New page: ${newPage.id}`);
      console.log(`  URL: ${newPage.url}`);
    }
  } catch (error: any) {
    console.error('Error:', JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

function getTitle(props: any): string {
  for (const val of Object.values(props) as any[]) {
    if (val.type === 'title' && val.title?.[0]) {
      return val.title[0].plain_text;
    }
  }
  return 'Untitled';
}

main();

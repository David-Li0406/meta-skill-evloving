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

const { values, positionals } = parseArgs({
  options: {
    database: { type: 'string', short: 'd' },
    page: { type: 'string', short: 'p' },
    title: { type: 'string', short: 't' },
    json: { type: 'boolean', default: false },
  },
  allowPositionals: true,
});

const content = positionals.join(' ');

if ((!values.database && !values.page) || !values.title) {
  console.error(`Usage: quick-note.ts --database <DB_ID|URL> --title <text> [content]
       quick-note.ts --page <PAGE_ID|URL> --title <text> [content]

Rapidly create a new page with title and optional body content.

Options:
  --database, -d  Database to create in
  --page, -p      Parent page to create under
  --title, -t     Page title (required)
  --json          Output full response as JSON

Content can be passed as positional args or piped via stdin.

Examples:
  quick-note.ts -d abc123 -t "Meeting Notes" "Discussed Q4 roadmap"
  quick-note.ts -p abc123 -t "Ideas" "Random thoughts for later"
  echo "Long content here" | quick-note.ts -d abc123 -t "From stdin"
`);
  process.exit(1);
}

async function getContent(): Promise<string> {
  if (content) return content;

  // Check if stdin has data
  if (!process.stdin.isTTY) {
    const chunks: Buffer[] = [];
    for await (const chunk of process.stdin) {
      chunks.push(chunk);
    }
    return Buffer.concat(chunks).toString('utf-8').trim();
  }

  return '';
}

async function main() {
  try {
    const bodyContent = await getContent();

    let page: any;

    if (values.database) {
      const databaseId = extractId(values.database);

      // Get title property name
      const db = await notion.databases.retrieve({ database_id: databaseId });
      const titleProp = Object.entries(db.properties)
        .find(([_, p]: any) => p.type === 'title')?.[0] || 'Name';

      page = await notion.pages.create({
        parent: { database_id: databaseId },
        properties: {
          [titleProp]: {
            title: [{ text: { content: values.title! } }],
          },
        },
      });
    } else if (values.page) {
      const pageId = extractId(values.page);

      page = await notion.pages.create({
        parent: { page_id: pageId },
        properties: {
          title: {
            title: [{ text: { content: values.title! } }],
          },
        },
      });
    }

    // Add content if provided
    if (bodyContent) {
      const paragraphs = bodyContent.split('\n\n').filter(p => p.trim());

      const blocks = paragraphs.map(text => ({
        object: 'block' as const,
        type: 'paragraph' as const,
        paragraph: {
          rich_text: [{ type: 'text' as const, text: { content: text } }],
        },
      }));

      if (blocks.length > 0) {
        await notion.blocks.children.append({
          block_id: page.id,
          children: blocks,
        });
      }
    }

    if (values.json) {
      console.log(JSON.stringify(page, null, 2));
    } else {
      console.log('✓ Note created');
      console.log(`  Title: ${values.title}`);
      console.log(`  ID: ${page.id}`);
      console.log(`  URL: ${page.url}`);
    }
  } catch (error: any) {
    console.error('Error:', JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

main();

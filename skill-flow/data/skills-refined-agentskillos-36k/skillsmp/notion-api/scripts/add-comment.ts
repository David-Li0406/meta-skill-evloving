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
    page: { type: 'string', short: 'p' },
  },
  allowPositionals: true,
});

const comment = positionals.join(' ');

if (!values.page || !comment) {
  console.error('Usage: add-comment.ts --page <PAGE_ID|URL> "Your comment text"');
  process.exit(1);
}

const pageId = extractId(values.page);

async function main() {
  try {
    const result = await notion.comments.create({
      parent: { page_id: pageId },
      rich_text: [{ type: 'text', text: { content: comment } }],
    });

    console.log('Comment added:', (result as any).id);
  } catch (error: any) {
    console.error('Error:', JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

main();

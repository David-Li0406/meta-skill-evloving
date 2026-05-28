#!/usr/bin/env tsx
import { Client } from '@notionhq/client';
import { NotionToMarkdown } from 'notion-to-md';
import { parseArgs } from 'util';

const notion = new Client({ auth: process.env.NOTION_API_KEY });
const n2m = new NotionToMarkdown({ notionClient: notion });

function extractId(input: string): string {
  // If it's a URL, parse it
  if (input.includes('notion.so')) {
    const url = new URL(input);
    // Check for p= query param first (subpage)
    const pParam = url.searchParams.get('p');
    if (pParam) return pParam.replace(/-/g, '');
    // Otherwise extract from path (last 32 hex chars)
    const match = url.pathname.match(/([a-f0-9]{32})$/i)
      || url.pathname.match(/([a-f0-9-]{36})$/i)
      || url.pathname.match(/-([a-f0-9]{32})(?:\?|$)/i);
    if (match) return match[1].replace(/-/g, '');
  }
  // Already an ID, just clean it
  return input.replace(/-/g, '');
}

const { values } = parseArgs({
  options: {
    page: { type: 'string', short: 'p' },
    json: { type: 'boolean', default: false },
    'properties-only': { type: 'boolean', default: false },
  },
});

if (!values.page) {
  console.error('Usage: read-item.ts --page <PAGE_ID|URL> [--json] [--properties-only]');
  process.exit(1);
}

const pageId = extractId(values.page);

async function main() {
  try {
    // Get page metadata and properties
    const page = await notion.pages.retrieve({ page_id: pageId }) as any;

    if (values.json) {
      if (values['properties-only']) {
        console.log(JSON.stringify(page.properties, null, 2));
      } else {
        const blocks = await notion.blocks.children.list({ block_id: pageId });
        console.log(JSON.stringify({ page, blocks: blocks.results }, null, 2));
      }
      return;
    }

    // Format properties
    const props = page.properties;
    const title = getTitle(props);
    
    console.log(`# ${title}\n`);
    console.log('## Properties\n');
    
    for (const [key, val] of Object.entries(props) as [string, any][]) {
      const formatted = formatProperty(key, val);
      if (formatted) console.log(`- **${key}**: ${formatted}`);
    }
    
    if (!values['properties-only']) {
      // Get page content as markdown
      console.log('\n## Content\n');
      const mdBlocks = await n2m.pageToMarkdown(pageId);
      const mdString = n2m.toMarkdownString(mdBlocks);

      if (mdString.parent.trim()) {
        console.log(mdString.parent);
      } else {
        console.log('(No content)');
      }
    }

    // Show comments if any
    try {
      const comments = await notion.comments.list({ block_id: pageId });
      if (comments.results.length > 0) {
        console.log('\n## Comments\n');
        for (const comment of comments.results as any[]) {
          const author = comment.created_by?.name || 'Unknown';
          const text = comment.rich_text?.map((t: any) => t.plain_text).join('') || '';
          console.log(`- **${author}**: ${text}`);
        }
      }
    } catch {
      // Comments API might not be available
    }

  } catch (error: any) {
    console.error('Error:', JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

function getTitle(props: any): string {
  for (const [key, val] of Object.entries(props) as any[]) {
    if (val.type === 'title' && val.title?.[0]) {
      return val.title[0].plain_text;
    }
  }
  return '(Untitled)';
}

function formatProperty(key: string, prop: any): string | null {
  switch (prop.type) {
    case 'title':
      return null; // Already shown as header
    case 'rich_text':
      return prop.rich_text?.map((t: any) => t.plain_text).join('') || '(empty)';
    case 'number':
      return prop.number?.toString() ?? '(empty)';
    case 'select':
      return prop.select?.name || '(empty)';
    case 'multi_select':
      return prop.multi_select?.map((s: any) => s.name).join(', ') || '(empty)';
    case 'status':
      return prop.status?.name || '(empty)';
    case 'date':
      if (!prop.date) return '(empty)';
      return prop.date.end 
        ? `${prop.date.start} → ${prop.date.end}`
        : prop.date.start;
    case 'people':
      return prop.people?.map((p: any) => p.name).join(', ') || '(empty)';
    case 'checkbox':
      return prop.checkbox ? '✓' : '✗';
    case 'url':
      return prop.url || '(empty)';
    case 'email':
      return prop.email || '(empty)';
    case 'phone_number':
      return prop.phone_number || '(empty)';
    case 'formula':
      return formatFormula(prop.formula);
    case 'relation':
      return prop.relation?.length 
        ? `${prop.relation.length} linked item(s)`
        : '(empty)';
    case 'rollup':
      return formatRollup(prop.rollup);
    case 'created_time':
      return prop.created_time;
    case 'created_by':
      return prop.created_by?.name || '(unknown)';
    case 'last_edited_time':
      return prop.last_edited_time;
    case 'last_edited_by':
      return prop.last_edited_by?.name || '(unknown)';
    case 'files':
      return prop.files?.map((f: any) => f.name || f.url).join(', ') || '(empty)';
    case 'unique_id':
      return prop.unique_id?.prefix 
        ? `${prop.unique_id.prefix}-${prop.unique_id.number}`
        : prop.unique_id?.number?.toString() || '(empty)';
    default:
      return `(${prop.type})`;
  }
}

function formatFormula(formula: any): string {
  if (!formula) return '(empty)';
  switch (formula.type) {
    case 'string': return formula.string || '(empty)';
    case 'number': return formula.number?.toString() || '(empty)';
    case 'boolean': return formula.boolean ? '✓' : '✗';
    case 'date': return formula.date?.start || '(empty)';
    default: return '(formula)';
  }
}

function formatRollup(rollup: any): string {
  if (!rollup) return '(empty)';
  switch (rollup.type) {
    case 'number': return rollup.number?.toString() || '(empty)';
    case 'date': return rollup.date?.start || '(empty)';
    case 'array':
      if (!rollup.array?.length) return '(empty)';
      return rollup.array.map((item: any) => {
        if (item.type === 'title') return item.title?.[0]?.plain_text;
        if (item.type === 'rich_text') return item.rich_text?.[0]?.plain_text;
        return item[item.type];
      }).filter(Boolean).join(', ') || '(empty)';
    default:
      return '(rollup)';
  }
}

main();

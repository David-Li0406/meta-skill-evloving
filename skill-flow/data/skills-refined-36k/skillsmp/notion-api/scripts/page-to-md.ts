#!/usr/bin/env tsx
import { Client } from '@notionhq/client';
import { NotionToMarkdown } from 'notion-to-md';
import { parseArgs } from 'util';
import { writeFile } from 'fs/promises';

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
    output: { type: 'string', short: 'o' },
    'include-properties': { type: 'boolean', default: false },
  },
});

if (!values.page) {
  console.error(`Usage: page-to-md.ts --page <PAGE_ID|URL> [--output <file.md>] [--include-properties]

Fetch a Notion page and save as Markdown. Outputs to stdout if no --output specified.

Examples:
  page-to-md.ts --page abc123 --output notes.md
  page-to-md.ts --page 'https://notion.so/...' > page.md
`);
  process.exit(1);
}

const pageId = extractId(values.page);

async function main() {
  try {
    const page = await notion.pages.retrieve({ page_id: pageId }) as any;

    let output = '';

    // Get title
    const titleProp = Object.values(page.properties).find((p: any) => p.type === 'title') as any;
    const title = titleProp?.title?.[0]?.plain_text || '(Untitled)';
    output += `# ${title}\n\n`;

    // Include properties if requested
    if (values['include-properties']) {
      output += '## Properties\n\n';
      for (const [key, val] of Object.entries(page.properties) as [string, any][]) {
        if (val.type === 'title') continue;
        const formatted = formatProperty(val);
        if (formatted) output += `- **${key}**: ${formatted}\n`;
      }
      output += '\n';
    }

    // Get content as markdown
    const mdBlocks = await n2m.pageToMarkdown(pageId);
    const mdString = n2m.toMarkdownString(mdBlocks);

    if (mdString.parent.trim()) {
      output += mdString.parent;
    }

    if (values.output) {
      await writeFile(values.output, output);
      console.log(`Saved to ${values.output}`);
    } else {
      console.log(output);
    }
  } catch (error: any) {
    console.error('Error:', JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

function formatProperty(prop: any): string | null {
  switch (prop.type) {
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
      return prop.date.end ? `${prop.date.start} → ${prop.date.end}` : prop.date.start;
    case 'people':
      return prop.people?.map((p: any) => p.name).join(', ') || null;
    case 'checkbox':
      return prop.checkbox ? '✓' : '✗';
    case 'url':
      return prop.url || null;
    default:
      return null;
  }
}

main();

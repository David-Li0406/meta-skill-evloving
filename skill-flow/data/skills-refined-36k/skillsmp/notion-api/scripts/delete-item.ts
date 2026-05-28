#!/usr/bin/env tsx
import { Client } from "@notionhq/client";
import { parseArgs } from "util";

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
    page: { type: "string", short: "p" },
  },
});

if (!values.page) {
  console.error(`Usage: delete-item.ts --page <PAGE_ID|URL>

Deletes (archives) a Notion page. This is reversible in Notion's trash.

Examples:
  delete-item.ts --page abc123def456
  delete-item.ts -p abc123def456
`);
  process.exit(1);
}

const pageId = extractId(values.page);

async function main() {
  try {
    const page = (await notion.pages.retrieve({
      page_id: pageId,
    })) as any;
    const title =
      Object.values(page.properties).find((p: any) => p.type === "title")
        ?.title?.[0]?.plain_text || "(Untitled)";

    await notion.pages.update({
      page_id: pageId,
      archived: true,
    });

    console.log(`✓ Deleted "${title}"`);
    console.log(`  Page ID: ${pageId}`);
  } catch (error: any) {
    console.error("Error:", JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

main();

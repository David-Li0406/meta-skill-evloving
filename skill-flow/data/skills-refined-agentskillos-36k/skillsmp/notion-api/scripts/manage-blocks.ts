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
    action: { type: "string", short: "a" }, // list, delete, update
    block: { type: "string", short: "b" }, // block ID for delete/update
    text: { type: "string", short: "t" }, // new text for update
    json: { type: "boolean", default: false },
  },
});

if (!values.page || !values.action) {
  console.error(`Usage: manage-blocks.ts --page <PAGE_ID|URL> --action <ACTION> [options]

Actions:
  list              List all blocks on the page with their IDs
  delete --block    Delete a specific block by ID
  update --block    Update block text (for paragraphs, headings, bullets)

Examples:
  manage-blocks.ts --page abc123 --action list
  manage-blocks.ts --page abc123 --action delete --block def456
  manage-blocks.ts --page abc123 --action update --block def456 --text "New text"
`);
  process.exit(1);
}

const pageId = extractId(values.page);

async function listBlocks(pageId: string) {
  const response = await notion.blocks.children.list({
    block_id: pageId,
    page_size: 100,
  });

  if (values.json) {
    console.log(JSON.stringify(response.results, null, 2));
    return;
  }

  console.log(`Found ${response.results.length} blocks:\n`);

  for (const block of response.results as any[]) {
    const content = extractBlockText(block);
    const truncated =
      content.length > 60 ? content.slice(0, 60) + "..." : content;
    console.log(`[${block.type}] ${block.id}`);
    if (truncated) console.log(`  "${truncated}"`);
    console.log();
  }
}

function extractBlockText(block: any): string {
  const type = block.type;
  const data = block[type];

  if (data?.rich_text) {
    return data.rich_text.map((t: any) => t.plain_text).join("");
  }
  if (type === "divider") return "---";
  if (type === "embed") return `[embed: ${data?.url || ""}]`;
  if (type === "image")
    return `[image: ${data?.external?.url || data?.file?.url || ""}]`;
  return "";
}

async function deleteBlock(blockId: string) {
  await notion.blocks.delete({ block_id: blockId });
  console.log(`✓ Deleted block ${blockId}`);
}

async function updateBlock(blockId: string, newText: string) {
  // First get the block to know its type
  const block = (await notion.blocks.retrieve({ block_id: blockId })) as any;
  const type = block.type;

  const richTextTypes = [
    "paragraph",
    "heading_1",
    "heading_2",
    "heading_3",
    "bulleted_list_item",
    "numbered_list_item",
    "quote",
    "callout",
    "toggle",
  ];

  if (!richTextTypes.includes(type)) {
    console.error(`Cannot update block type: ${type}`);
    console.error(`Supported types: ${richTextTypes.join(", ")}`);
    process.exit(1);
  }

  await notion.blocks.update({
    block_id: blockId,
    [type]: {
      rich_text: [{ type: "text", text: { content: newText } }],
    },
  });

  console.log(`✓ Updated block ${blockId}`);
}

async function main() {
  try {
    switch (values.action) {
      case "list":
        await listBlocks(pageId);
        break;

      case "delete":
        if (!values.block) {
          console.error("--block required for delete action");
          process.exit(1);
        }
        await deleteBlock(values.block);
        break;

      case "update":
        if (!values.block || !values.text) {
          console.error("--block and --text required for update action");
          process.exit(1);
        }
        await updateBlock(values.block, values.text);
        break;

      default:
        console.error(`Unknown action: ${values.action}`);
        process.exit(1);
    }
  } catch (error: any) {
    console.error("Error:", JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

main();

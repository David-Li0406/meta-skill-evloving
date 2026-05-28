#!/usr/bin/env tsx
import { Client } from "@notionhq/client";
import { parseArgs } from "util";
import { Lexer, type Token, type Tokens } from "marked";

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
    page: { type: "string", short: "p" },
    file: { type: "string", short: "f" },
    after: { type: "string", short: "a" },
  },
  allowPositionals: true,
});

async function getMarkdown(): Promise<string> {
  if (positionals.length > 0) {
    return positionals.join(" ");
  }
  if (values.file) {
    const fs = await import("fs/promises");
    return fs.readFile(values.file, "utf-8");
  }
  const chunks: Buffer[] = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString("utf-8");
}

if (!values.page) {
  console.error(`Usage: append-content.ts --page <PAGE_ID|URL> [--after <BLOCK_ID>] [markdown]

Accepts markdown as:
  - Positional argument: --page abc123 "# Hello World"
  - File: --page abc123 --file content.md
  - Stdin (auto-detected, NO --file flag needed):
      echo "# Hello" | append-content.ts --page abc123
      append-content.ts --page abc123 << 'EOF'
      # Content here
      EOF

NOTE: Do NOT use --file - for stdin. Just pipe/heredoc without --file.

Options:
  --after, -a  Insert content after this block ID (instead of end of page)

Supported markdown:
  # h1, ## h2, ### h3, **bold**, *italic*, \`code\`, [links](url)
  - Bullets, 1. Numbered, - [ ] Todos, > Quotes, \`\`\`code blocks\`\`\`, ---

Examples:
  append-content.ts --page abc123 "# Hello World"
  append-content.ts --page abc123 --file notes.md
  echo "content" | append-content.ts --page abc123
  append-content.ts --page abc123 << 'EOF'
  # Heading
  - Item 1
  EOF
`);
  process.exit(1);
}

const pageId = extractId(values.page);

type RichTextItem = {
  type: "text";
  text: { content: string; link?: { url: string } };
  annotations?: {
    bold?: boolean;
    italic?: boolean;
    code?: boolean;
    strikethrough?: boolean;
  };
};

type Block = {
  object: "block";
  type: string;
  [key: string]: any;
};

// Convert marked inline tokens to Notion rich_text
function inlineTokensToRichText(tokens: Token[]): RichTextItem[] {
  const result: RichTextItem[] = [];

  for (const token of tokens) {
    switch (token.type) {
      case "text":
        result.push({
          type: "text",
          text: { content: token.text },
        });
        break;

      case "strong":
        // Recursively process children with bold annotation
        for (const child of inlineTokensToRichText(
          (token as Tokens.Strong).tokens || [],
        )) {
          result.push({
            ...child,
            annotations: { ...child.annotations, bold: true },
          });
        }
        break;

      case "em":
        for (const child of inlineTokensToRichText(
          (token as Tokens.Em).tokens || [],
        )) {
          result.push({
            ...child,
            annotations: { ...child.annotations, italic: true },
          });
        }
        break;

      case "codespan":
        result.push({
          type: "text",
          text: { content: (token as Tokens.Codespan).text },
          annotations: { code: true },
        });
        break;

      case "link":
        result.push({
          type: "text",
          text: {
            content: (token as Tokens.Link).text,
            link: { url: (token as Tokens.Link).href },
          },
        });
        break;

      case "del":
        for (const child of inlineTokensToRichText(
          (token as Tokens.Del).tokens || [],
        )) {
          result.push({
            ...child,
            annotations: { ...child.annotations, strikethrough: true },
          });
        }
        break;

      case "escape":
        result.push({
          type: "text",
          text: { content: (token as Tokens.Escape).text },
        });
        break;

      default:
        // Fallback for any unhandled token types
        if ("text" in token && typeof token.text === "string") {
          result.push({
            type: "text",
            text: { content: token.text },
          });
        }
    }
  }

  return result;
}

// Parse text with inline formatting using marked's inline lexer
function parseInlineFormatting(text: string): RichTextItem[] {
  const lexer = new Lexer();
  const tokens = lexer.inlineTokens(text);
  const richText = inlineTokensToRichText(tokens);
  return richText.length > 0
    ? richText
    : [{ type: "text", text: { content: text } }];
}

// Convert a list item token to Notion block(s)
function listItemToBlock(
  item: Tokens.ListItem,
  ordered: boolean,
): Block | null {
  // Check for checkbox (task list)
  if (item.task) {
    const textContent =
      item.tokens
        ?.filter((t) => t.type === "text" || t.type === "paragraph")
        .map((t) => ("text" in t ? t.text : ""))
        .join("") || item.text;

    return {
      object: "block",
      type: "to_do",
      to_do: {
        rich_text: parseInlineFormatting(textContent),
        checked: item.checked || false,
      },
    };
  }

  // Regular list item - get text content
  let textContent = "";
  const childBlocks: Block[] = [];

  for (const token of item.tokens || []) {
    if (token.type === "text") {
      textContent += token.text;
    } else if (token.type === "paragraph") {
      // For the first paragraph, use as main text
      if (!textContent) {
        textContent = (token as Tokens.Paragraph).text;
      }
    } else if (token.type === "list") {
      // Nested list - convert to children
      const nestedBlocks = listToBlocks(token as Tokens.List);
      childBlocks.push(...nestedBlocks);
    }
  }

  const blockType = ordered ? "numbered_list_item" : "bulleted_list_item";
  const block: Block = {
    object: "block",
    type: blockType,
    [blockType]: {
      rich_text: parseInlineFormatting(textContent),
    },
  };

  // Add children if there are nested items
  if (childBlocks.length > 0) {
    block[blockType].children = childBlocks;
  }

  return block;
}

// Convert a list token to Notion blocks
function listToBlocks(list: Tokens.List): Block[] {
  const blocks: Block[] = [];

  for (const item of list.items) {
    const block = listItemToBlock(item, list.ordered);
    if (block) {
      blocks.push(block);
    }
  }

  return blocks;
}

// Convert marked tokens to Notion blocks
function tokensToBlocks(tokens: Token[]): Block[] {
  const blocks: Block[] = [];

  for (const token of tokens) {
    switch (token.type) {
      case "heading": {
        const t = token as Tokens.Heading;
        const depth = Math.min(t.depth, 3);
        const headingType = `heading_${depth}` as
          | "heading_1"
          | "heading_2"
          | "heading_3";
        blocks.push({
          object: "block",
          type: headingType,
          [headingType]: {
            rich_text: parseInlineFormatting(t.text),
          },
        });
        break;
      }

      case "paragraph": {
        const t = token as Tokens.Paragraph;
        blocks.push({
          object: "block",
          type: "paragraph",
          paragraph: {
            rich_text: parseInlineFormatting(t.text),
          },
        });
        break;
      }

      case "list": {
        const listBlocks = listToBlocks(token as Tokens.List);
        blocks.push(...listBlocks);
        break;
      }

      case "blockquote": {
        const t = token as Tokens.Blockquote;
        // Recursively process blockquote content
        const quoteText = t.tokens
          ?.filter((bt) => bt.type === "paragraph")
          .map((bt) => (bt as Tokens.Paragraph).text)
          .join("\n");

        blocks.push({
          object: "block",
          type: "quote",
          quote: {
            rich_text: parseInlineFormatting(quoteText || t.text),
          },
        });
        break;
      }

      case "code": {
        const t = token as Tokens.Code;
        blocks.push({
          object: "block",
          type: "code",
          code: {
            rich_text: [{ type: "text", text: { content: t.text } }],
            language: t.lang || "plain text",
          },
        });
        break;
      }

      case "hr":
        blocks.push({
          object: "block",
          type: "divider",
          divider: {},
        });
        break;

      case "space":
        // Skip blank lines
        break;

      default:
        // For unknown types, try to extract text if available
        if ("text" in token && typeof token.text === "string" && token.text) {
          blocks.push({
            object: "block",
            type: "paragraph",
            paragraph: {
              rich_text: parseInlineFormatting(token.text),
            },
          });
        }
    }
  }

  return blocks;
}

function parseMarkdownToBlocks(markdown: string): Block[] {
  const lexer = new Lexer();
  const tokens = lexer.lex(markdown);
  return tokensToBlocks(tokens);
}

async function main() {
  const markdown = await getMarkdown();

  if (!markdown.trim()) {
    console.error("No content provided");
    process.exit(1);
  }

  const blocks = parseMarkdownToBlocks(markdown);

  if (blocks.length === 0) {
    console.error("No blocks generated from markdown");
    process.exit(1);
  }

  try {
    const appendParams: any = {
      block_id: pageId,
      children: blocks,
    };

    if (values.after) {
      appendParams.after = values.after;
    }

    await notion.blocks.children.append(appendParams);

    console.log(`✓ Added ${blocks.length} block(s) to page`);
  } catch (error: any) {
    console.error("Error:", JSON.stringify(error, null, 2));
    process.exit(1);
  }
}

main();

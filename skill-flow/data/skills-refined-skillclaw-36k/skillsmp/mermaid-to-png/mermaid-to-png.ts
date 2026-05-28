#!/usr/bin/env bun
/**
 * Extracts mermaid diagrams from a markdown file, renders them to PNGs via mermaid.ink,
 * and inserts image references after each mermaid block.
 *
 * Usage: bun mermaid-to-png.ts <markdown-file>
 */

import { readFile, writeFile, mkdir } from "fs/promises";
import { basename, dirname, join } from "path";

const MERMAID_REGEX = /```mermaid\n([\s\S]*?)```/g;

interface MermaidBlock {
  match: string;
  mermaidCode: string;
}

interface Replacement {
  original: string;
  replacement: string;
}

async function fetchPng(mermaidCode: string): Promise<Buffer> {
  const encoded = Buffer.from(mermaidCode).toString("base64");
  const url = `https://mermaid.ink/img/${encoded}?type=png&bgColor=white`;

  const response = await fetch(url, { redirect: "follow" });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const arrayBuffer = await response.arrayBuffer();
  return Buffer.from(arrayBuffer);
}

async function main(): Promise<void> {
  const filePath = process.argv[2];

  if (!filePath) {
    console.error("Usage: bun mermaid-to-png.ts <markdown-file>");
    process.exit(1);
  }

  const content = await readFile(filePath, "utf-8");
  const fileDir = dirname(filePath);
  const fileBasename = basename(filePath, ".md")
    .toLowerCase()
    .replace(/\s+/g, "-");

  const assetsDir = join(fileDir, "assets", fileBasename);
  await mkdir(assetsDir, { recursive: true });

  const mermaidBlocks: MermaidBlock[] = [];

  let match: RegExpExecArray | null;
  while ((match = MERMAID_REGEX.exec(content)) !== null) {
    mermaidBlocks.push({
      match: match[0],
      mermaidCode: match[1],
    });
  }

  console.log(`Found ${mermaidBlocks.length} mermaid diagrams`);

  const replacements: Replacement[] = [];

  for (let i = 0; i < mermaidBlocks.length; i++) {
    const block = mermaidBlocks[i];
    const diagramIndex = i + 1;
    const pngFilename = `diagram-${diagramIndex}.png`;
    const pngPath = join(assetsDir, pngFilename);
    const relativePngPath = `assets/${fileBasename}/${pngFilename}`;

    console.log(`Rendering diagram ${diagramIndex}...`);

    try {
      const pngData = await fetchPng(block.mermaidCode);
      await writeFile(pngPath, pngData);

      const replacement = `${block.match}\n\n![Diagram ${diagramIndex}](${relativePngPath})`;
      replacements.push({ original: block.match, replacement });

      console.log(`  -> ${relativePngPath}`);
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      console.error(`  Failed to render diagram ${diagramIndex}:`, message);
      replacements.push({ original: block.match, replacement: block.match });
    }
  }

  let newContent = content;
  for (const { original, replacement } of replacements) {
    newContent = newContent.replace(original, replacement);
  }

  await writeFile(filePath, newContent);
  console.log(`\nUpdated ${filePath}`);
  console.log(`PNGs saved to ${assetsDir}/`);
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});

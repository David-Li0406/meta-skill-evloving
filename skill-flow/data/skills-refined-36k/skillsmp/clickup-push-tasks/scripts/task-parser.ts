#!/usr/bin/env npx tsx
/**
 * Task File Parser
 * Parses task markdown files (docs/tasks/*.md) into structured data
 *
 * Usage:
 *   npx tsx task-parser.ts <taskFilePath>
 *
 * Output:
 *   JSON with title, clickupUrl, and phases with items
 */

import { readFileSync } from "fs";

export interface ParsedTaskItem {
  text: string;
  completed: boolean;
  file?: string;
}

export interface ParsedPhase {
  name: string;
  items: ParsedTaskItem[];
}

export interface ParsedTaskFile {
  title: string;
  clickupUrl?: string;
  type?: string;
  branch?: string;
  phases: ParsedPhase[];
}

// Sections that should stop task parsing (not part of task phases)
const NON_TASK_SECTIONS = [
  "Implementation Notes",
  "Verification",
  "Files Modified",
  "Files to Create/Modify",
  "References",
  "Notes",
  "Context",
  "Comments Summary",
  "Attachments",
];

/**
 * Parse a task file markdown content into structured data
 */
export function parseTaskContent(markdown: string): ParsedTaskFile {
  const lines = markdown.split("\n");

  let title = "";
  let clickupUrl: string | undefined;
  let type: string | undefined;
  let branch: string | undefined;
  const phases: ParsedPhase[] = [];

  let currentPhase: ParsedPhase | null = null;
  let lastItem: ParsedTaskItem | null = null;
  let inTasksSection = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Extract title: # Task: {title}
    const titleMatch = line.match(/^#\s+Task:\s*(.+)$/);
    if (titleMatch) {
      title = titleMatch[1].trim();
      continue;
    }

    // Extract ClickUp URL: **ClickUp:** {url}
    const clickupMatch = line.match(/^\*\*ClickUp:\*\*\s*(.+)$/);
    if (clickupMatch) {
      clickupUrl = clickupMatch[1].trim();
      continue;
    }

    // Extract type: **Type:** {type}
    const typeMatch = line.match(/^\*\*Type:\*\*\s*(.+)$/);
    if (typeMatch) {
      type = typeMatch[1].trim();
      continue;
    }

    // Extract branch: **Branch:** {branch}
    const branchMatch = line.match(/^\*\*Branch:\*\*\s*(.+)$/);
    if (branchMatch) {
      branch = branchMatch[1].trim();
      continue;
    }

    // Detect ## Tasks section header
    if (line.match(/^##\s+Tasks\s*$/)) {
      inTasksSection = true;
      continue;
    }

    // Detect other ## section headers (exit tasks section)
    const sectionMatch = line.match(/^##\s+(.+)$/);
    if (sectionMatch) {
      // Save current phase before leaving tasks section
      if (inTasksSection && currentPhase && currentPhase.items.length > 0) {
        phases.push(currentPhase);
        currentPhase = null;
        lastItem = null;
      }
      inTasksSection = false;
      continue;
    }

    // Detect phase headers: ### Phase N: {name} or ### {name}
    const phaseMatch = line.match(/^###\s+(?:Phase\s+\d+:\s*)?(.+)$/);
    if (phaseMatch) {
      const phaseName = phaseMatch[1].trim();

      // Check if this is a non-task section
      if (NON_TASK_SECTIONS.some(section => phaseName.toLowerCase().includes(section.toLowerCase()))) {
        // Save previous phase and exit
        if (currentPhase && currentPhase.items.length > 0) {
          phases.push(currentPhase);
          currentPhase = null;
          lastItem = null;
        }
        continue;
      }

      // Save previous phase if exists
      if (currentPhase && currentPhase.items.length > 0) {
        phases.push(currentPhase);
      }
      currentPhase = {
        name: phaseName,
        items: [],
      };
      lastItem = null;
      continue;
    }

    // Only parse task items if we're in a phase
    if (!currentPhase) continue;

    // Detect task items: - [ ] {text} or - [x] {text}
    const itemMatch = line.match(/^-\s+\[([ xX])\]\s+(.+)$/);
    if (itemMatch) {
      const completed = itemMatch[1].toLowerCase() === "x";
      const text = itemMatch[2].trim();

      lastItem = {
        text,
        completed,
      };
      currentPhase.items.push(lastItem);
      continue;
    }

    // Detect file metadata on continuation lines: - File: {path} or File: {path}
    if (lastItem) {
      const fileMatch = line.match(/^\s+[-*]?\s*File:\s*`?([^`]+)`?/);
      if (fileMatch) {
        // Extract just the file path, removing any line number suffix like :150-158
        const filePath = fileMatch[1].trim().split(":")[0];
        lastItem.file = filePath;
        continue;
      }
    }
  }

  // Don't forget the last phase
  if (currentPhase && currentPhase.items.length > 0) {
    phases.push(currentPhase);
  }

  return {
    title,
    clickupUrl,
    type,
    branch,
    phases,
  };
}

/**
 * Parse a task file from disk
 */
export function parseTaskFile(filePath: string): ParsedTaskFile {
  const content = readFileSync(filePath, "utf-8");
  return parseTaskContent(content);
}

/**
 * Extract task ID from ClickUp URL
 */
export function extractTaskId(clickupUrl: string): string | null {
  // Format: https://app.clickup.com/t/868h136ex
  const match = clickupUrl.match(/\/t\/([a-z0-9]+)$/i);
  return match ? match[1] : null;
}

// CLI entry point
if (import.meta.url === `file://${process.argv[1]}`) {
  const filePath = process.argv[2];

  if (!filePath) {
    console.error(JSON.stringify({ error: "Usage: task-parser.ts <taskFilePath>" }));
    process.exit(1);
  }

  try {
    const parsed = parseTaskFile(filePath);
    console.log(JSON.stringify(parsed, null, 2));
  } catch (err) {
    console.error(JSON.stringify({
      error: err instanceof Error ? err.message : String(err),
    }));
    process.exit(1);
  }
}

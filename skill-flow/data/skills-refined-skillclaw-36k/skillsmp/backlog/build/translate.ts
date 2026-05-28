#!/usr/bin/env bun
/**
 * Claude Code to OpenCode Plugin Translator
 *
 * Translates Claude Code plugin commands and agents to OpenCode format.
 *
 * Usage:
 *   bun run build/translate.ts
 *   # or
 *   ./build/translate.ts
 */

import { readdir, readFile, writeFile, mkdir } from "fs/promises";
import { existsSync } from "fs";
import { join, dirname } from "path";

// YAML frontmatter parser (simple implementation)
function parseFrontmatter(content: string): { frontmatter: Record<string, any>; body: string } {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) {
    return { frontmatter: {}, body: content };
  }

  const yamlStr = match[1];
  const body = match[2];
  const frontmatter: Record<string, any> = {};

  // Simple YAML parsing for our use case
  for (const line of yamlStr.split('\n')) {
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.slice(0, colonIndex).trim();
      const value = line.slice(colonIndex + 1).trim();
      frontmatter[key] = value;
    }
  }

  return { frontmatter, body };
}

// Transform Claude Code frontmatter to OpenCode format
function transformCommandFrontmatter(claudeFm: Record<string, any>): Record<string, any> {
  const opencodeFm: Record<string, any> = {};

  // description stays the same
  if (claudeFm.description) {
    opencodeFm.description = claudeFm.description;
  }

  // model needs provider prefix for OpenCode
  if (claudeFm.model) {
    const modelMap: Record<string, string> = {
      'sonnet': 'anthropic/claude-sonnet',
      'opus': 'anthropic/claude-opus',
      'haiku': 'anthropic/claude-haiku',
    };
    opencodeFm.model = modelMap[claudeFm.model] || `anthropic/${claudeFm.model}`;
  }

  // allowed-tools is not used in OpenCode commands (goes on agents)
  // argument-hint is handled differently in OpenCode (use $ARGUMENTS in body)

  return opencodeFm;
}

// Transform Claude Code agent frontmatter to OpenCode format
function transformAgentFrontmatter(claudeFm: Record<string, any>): Record<string, any> {
  const opencodeFm: Record<string, any> = {};

  // description is required in OpenCode
  if (claudeFm.description) {
    opencodeFm.description = claudeFm.description;
  }

  // OpenCode agents need explicit mode
  opencodeFm.mode = 'subagent';

  // model needs provider prefix
  if (claudeFm.model) {
    const modelMap: Record<string, string> = {
      'sonnet': 'anthropic/claude-sonnet',
      'opus': 'anthropic/claude-opus',
      'haiku': 'anthropic/claude-haiku',
    };
    opencodeFm.model = modelMap[claudeFm.model] || `anthropic/${claudeFm.model}`;
  }

  // Transform tools from string list to boolean object
  if (claudeFm.tools) {
    const toolList = claudeFm.tools.split(',').map((t: string) => t.trim().toLowerCase());
    const allTools = ['read', 'write', 'edit', 'bash', 'glob', 'grep', 'list', 'webfetch', 'todowrite', 'todoread'];

    opencodeFm.tools = {};
    for (const tool of allTools) {
      opencodeFm.tools[tool] = toolList.includes(tool);
    }
  }

  return opencodeFm;
}

// Generate YAML from object
function toYaml(obj: Record<string, any>, indent = 0): string {
  const spaces = '  '.repeat(indent);
  let yaml = '';

  for (const [key, value] of Object.entries(obj)) {
    if (typeof value === 'object' && value !== null) {
      yaml += `${spaces}${key}:\n${toYaml(value, indent + 1)}`;
    } else if (typeof value === 'boolean') {
      yaml += `${spaces}${key}: ${value}\n`;
    } else {
      yaml += `${spaces}${key}: ${value}\n`;
    }
  }

  return yaml;
}

// Update body content for OpenCode conventions
function transformBody(body: string): string {
  // Update command references from /up:xxx to /xxx format
  // OpenCode doesn't use plugin namespaces the same way
  let transformed = body;

  // Replace /up:plan with /plan, /up:prompt with /prompt, etc.
  transformed = transformed.replace(/\/up:(\w+)/g, '/$1');

  // Replace /backlog:xxx references
  transformed = transformed.replace(/\/backlog:(\w+)/g, '/$1');

  // Replace /design:xxx references
  transformed = transformed.replace(/\/design:(\w+)/g, '/$1');

  return transformed;
}

async function translateCommands(pluginDir: string) {
  const commandsDir = join(pluginDir, 'commands');
  const outputDir = join(pluginDir, '.opencode', 'commands');

  if (!existsSync(commandsDir)) {
    console.log('No commands directory found');
    return;
  }

  // Ensure output directory exists
  await mkdir(outputDir, { recursive: true });

  const files = await readdir(commandsDir);

  for (const file of files) {
    if (!file.endsWith('.md')) continue;

    const inputPath = join(commandsDir, file);
    const outputPath = join(outputDir, file);

    console.log(`Translating command: ${file}`);

    const content = await readFile(inputPath, 'utf-8');
    const { frontmatter, body } = parseFrontmatter(content);

    const opencodeFm = transformCommandFrontmatter(frontmatter);
    const transformedBody = transformBody(body);

    const output = `---\n${toYaml(opencodeFm)}---\n${transformedBody}`;

    await writeFile(outputPath, output);
    console.log(`  -> ${outputPath}`);
  }
}

async function translateAgents(pluginDir: string) {
  const agentsDir = join(pluginDir, 'agents');
  const outputDir = join(pluginDir, '.opencode', 'agents');

  if (!existsSync(agentsDir)) {
    console.log('No agents directory found');
    return;
  }

  // Ensure output directory exists
  await mkdir(outputDir, { recursive: true });

  const files = await readdir(agentsDir);

  for (const file of files) {
    if (!file.endsWith('.md')) continue;

    const inputPath = join(agentsDir, file);
    const outputPath = join(outputDir, file);

    console.log(`Translating agent: ${file}`);

    const content = await readFile(inputPath, 'utf-8');
    const { frontmatter, body } = parseFrontmatter(content);

    const opencodeFm = transformAgentFrontmatter(frontmatter);
    const transformedBody = transformBody(body);

    const output = `---\n${toYaml(opencodeFm)}---\n${transformedBody}`;

    await writeFile(outputPath, output);
    console.log(`  -> ${outputPath}`);
  }
}

async function main() {
  const pluginDir = process.cwd();

  console.log('═══════════════════════════════════════════════════════════════');
  console.log(' Claude Code -> OpenCode Plugin Translator');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log(`Plugin directory: ${pluginDir}`);
  console.log('');

  await translateCommands(pluginDir);
  console.log('');
  await translateAgents(pluginDir);

  console.log('');
  console.log('Translation complete!');
  console.log('');
  console.log('OpenCode files written to .opencode/ directory');
  console.log('To use with OpenCode, symlink or copy .opencode/ contents to your project.');
}

main().catch(console.error);

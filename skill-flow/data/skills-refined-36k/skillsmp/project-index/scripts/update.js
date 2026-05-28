#!/usr/bin/env node
/**
 * Incremental Update - Update CLAUDE.md based on git changes
 * Usage: node update.js [--diff HEAD~1] [--module path] [--silent] [--if-commit]
 *
 * --if-commit: Only run if last Bash command was git commit (for PostToolUse hook)
 */

import { promises as fs } from 'fs';
import path from 'path';
import { execSync } from 'child_process';

async function exists(p) {
  try { await fs.access(p); return true; } catch { return false; }
}

/**
 * Check if we should run based on hook context
 * PostToolUse hook sets CLAUDE_TOOL_INPUT with the command that was run
 */
function shouldRunInHookContext() {
  const toolInput = process.env.CLAUDE_TOOL_INPUT || '';
  // Check if the command contains 'git commit'
  return toolInput.includes('git commit');
}

function getChangedFiles(diffRef = 'HEAD~1') {
  try {
    const output = execSync(`git diff --name-only ${diffRef}`, { encoding: 'utf-8' });
    return output.trim().split('\n').filter(Boolean);
  } catch (e) {
    console.error('Error getting git diff:', e.message);
    return [];
  }
}

function getAffectedModules(changedFiles) {
  const modules = new Set();

  for (const file of changedFiles) {
    // Match module paths
    const match = file.match(/^(src\/(modules|features)\/[^/]+)/);
    if (match) {
      modules.add(match[1]);
    }

    // Match package paths
    const pkgMatch = file.match(/^(packages\/[^/]+)/);
    if (pkgMatch) {
      modules.add(pkgMatch[1]);
    }
  }

  return [...modules];
}

async function analyzeModuleChanges(modulePath, changedFiles, rootPath) {
  const moduleFiles = changedFiles.filter(f => f.startsWith(modulePath));

  const analysis = {
    added: [],
    modified: [],
    deleted: [],
  };

  try {
    const diffStat = execSync(`git diff --stat HEAD~1 -- ${modulePath}`, { encoding: 'utf-8' });

    for (const file of moduleFiles) {
      const fullPath = path.join(rootPath, file);
      if (await exists(fullPath)) {
        // Check if new file
        try {
          execSync(`git log -1 --diff-filter=A -- ${file}`, { encoding: 'utf-8' });
          analysis.added.push(file);
        } catch {
          analysis.modified.push(file);
        }
      } else {
        analysis.deleted.push(file);
      }
    }
  } catch (e) {
    // Fallback: assume all are modified
    analysis.modified = moduleFiles;
  }

  return analysis;
}

async function updateModuleClaude(modulePath, analysis, rootPath) {
  const claudePath = path.join(rootPath, modulePath, 'CLAUDE.md');

  if (!await exists(claudePath)) {
    console.log(`  ⚠ No CLAUDE.md found at ${modulePath}, skipping`);
    return false;
  }

  let content = await fs.readFile(claudePath, 'utf-8');
  let updated = false;

  // Add update timestamp
  const timestamp = new Date().toISOString().split('T')[0];
  if (!content.includes('Last updated:')) {
    content = content.replace(/^(# .+)$/m, `$1\n\n> Last updated: ${timestamp}`);
    updated = true;
  } else {
    content = content.replace(/Last updated: \d{4}-\d{2}-\d{2}/, `Last updated: ${timestamp}`);
    updated = true;
  }

  // Scan current files and update Core Files section
  const fullModulePath = path.join(rootPath, modulePath);
  const entries = await fs.readdir(fullModulePath, { withFileTypes: true });
  const currentFiles = entries
    .filter(e => e.isFile() && /\.(ts|js|tsx|jsx|py)$/.test(e.name))
    .filter(e => !e.name.includes('.test.') && !e.name.includes('.spec.'))
    .map(e => e.name);

  // Check if Core Files section needs update
  const coreFilesMatch = content.match(/## Core Files\n\n([\s\S]*?)(?=\n##|$)/);
  if (coreFilesMatch) {
    const existingFiles = coreFilesMatch[1].match(/`([^`]+)`/g)?.map(f => f.replace(/`/g, '')) || [];
    const newFiles = currentFiles.filter(f => !existingFiles.includes(f));
    const removedFiles = existingFiles.filter(f => !currentFiles.includes(f));

    if (newFiles.length > 0 || removedFiles.length > 0) {
      console.log(`  + New files: ${newFiles.join(', ') || 'none'}`);
      console.log(`  - Removed files: ${removedFiles.join(', ') || 'none'}`);
      updated = true;
    }
  }

  if (updated) {
    await fs.writeFile(claudePath, content);
    return true;
  }

  return false;
}

async function main() {
  const args = process.argv.slice(2);
  const rootPath = process.cwd();
  const silent = args.includes('--silent');
  const ifCommit = args.includes('--if-commit');

  // If --if-commit flag, check if this is a git commit context
  if (ifCommit && !shouldRunInHookContext()) {
    // Not a git commit, silently exit
    return;
  }

  const diffRef = args.includes('--diff') ? args[args.indexOf('--diff') + 1] : 'HEAD~1';
  const specificModule = args.includes('--module') ? args[args.indexOf('--module') + 1] : null;

  if (!silent) {
    console.log('Project Index - Incremental Update');
    console.log(`Checking changes since: ${diffRef}\n`);
  }

  // Get changed files
  const changedFiles = getChangedFiles(diffRef);

  if (changedFiles.length === 0) {
    if (!silent) console.log('No changes detected.');
    return;
  }

  if (!silent) {
    console.log(`Changed files: ${changedFiles.length}`);
  }

  // Get affected modules
  let modules = specificModule ? [specificModule] : getAffectedModules(changedFiles);

  if (modules.length === 0) {
    if (!silent) console.log('No module CLAUDE.md files need updating.');
    return;
  }

  if (!silent) {
    console.log(`Affected modules: ${modules.join(', ')}\n`);
  }

  // Update each module
  let updatedCount = 0;
  for (const modulePath of modules) {
    if (!silent) console.log(`Updating: ${modulePath}`);

    const analysis = await analyzeModuleChanges(modulePath, changedFiles, rootPath);
    const wasUpdated = await updateModuleClaude(modulePath, analysis, rootPath);

    if (wasUpdated) {
      updatedCount++;
      if (!silent) console.log(`  ✓ Updated ${modulePath}/CLAUDE.md`);
    }
  }

  // Check if root CLAUDE.md needs update
  const rootChanges = changedFiles.some(f =>
    f === 'package.json' ||
    f === 'tsconfig.json' ||
    f.match(/^(src\/(modules|features)\/[^/]+)$/) // New module added
  );

  if (rootChanges) {
    const rootClaude = path.join(rootPath, 'CLAUDE.md');
    if (await exists(rootClaude)) {
      let content = await fs.readFile(rootClaude, 'utf-8');
      const timestamp = new Date().toISOString().split('T')[0];
      content = content.replace(/Last updated: \d{4}-\d{2}-\d{2}/, `Last updated: ${timestamp}`);
      await fs.writeFile(rootClaude, content);
      if (!silent) console.log('✓ Updated root CLAUDE.md');
      updatedCount++;
    }
  }

  if (!silent) {
    console.log(`\nDone! Updated ${updatedCount} CLAUDE.md files.`);
  }
}

main().catch(console.error);

#!/usr/bin/env node
/**
 * Project Scanner - Analyze project structure and detect modules
 * Usage: node scan.js [path]
 */

import { promises as fs } from 'fs';
import path from 'path';

const IGNORE_DIRS = new Set([
  'node_modules', '.git', 'dist', 'build', '.next', '__pycache__',
  'venv', '.venv', 'target', 'vendor', '.cache', 'coverage'
]);

const MODULE_PATTERNS = [
  { pattern: /^src\/(modules|features)\/([^/]+)$/, type: 'feature' },
  { pattern: /^src\/components\/([^/]+)$/, type: 'component' },
  { pattern: /^src\/(services|api)\/([^/]+)$/, type: 'service' },
  { pattern: /^src\/(utils|lib|helpers)$/, type: 'utility' },
  { pattern: /^packages\/([^/]+)$/, type: 'package' },
  { pattern: /^apps\/([^/]+)$/, type: 'app' },
];

const TECH_INDICATORS = {
  'package.json': 'node',
  'tsconfig.json': 'typescript',
  'next.config.js': 'nextjs',
  'next.config.mjs': 'nextjs',
  'vite.config.js': 'vite',
  'nuxt.config.ts': 'nuxt',
  'pyproject.toml': 'python',
  'requirements.txt': 'python',
  'go.mod': 'go',
  'Cargo.toml': 'rust',
  'pom.xml': 'java',
  'build.gradle': 'java',
  'Gemfile': 'ruby',
  'composer.json': 'php',
};

async function exists(p) {
  try {
    await fs.access(p);
    return true;
  } catch {
    return false;
  }
}

async function detectTechStack(rootPath) {
  const stack = [];
  for (const [file, tech] of Object.entries(TECH_INDICATORS)) {
    if (await exists(path.join(rootPath, file))) {
      stack.push(tech);
    }
  }
  return [...new Set(stack)];
}

async function scanDir(dir, rootPath, depth = 0) {
  if (depth > 5) return [];

  const entries = await fs.readdir(dir, { withFileTypes: true });
  const modules = [];

  for (const entry of entries) {
    if (!entry.isDirectory() || IGNORE_DIRS.has(entry.name)) continue;

    const fullPath = path.join(dir, entry.name);
    const relativePath = path.relative(rootPath, fullPath);

    // Check if matches module pattern
    for (const { pattern, type } of MODULE_PATTERNS) {
      if (pattern.test(relativePath)) {
        const files = await fs.readdir(fullPath);
        modules.push({
          name: entry.name,
          path: relativePath,
          type,
          hasIndex: files.some(f => /^index\.(ts|js|tsx|jsx|py)$/.test(f)),
          hasClaude: files.includes('CLAUDE.md'),
          fileCount: files.filter(f => !f.startsWith('.')).length,
        });
        break;
      }
    }

    // Recurse
    const subModules = await scanDir(fullPath, rootPath, depth + 1);
    modules.push(...subModules);
  }

  return modules;
}

async function analyzeModule(modulePath, rootPath) {
  const files = await fs.readdir(modulePath, { withFileTypes: true });

  const analysis = {
    coreFiles: [],
    submodules: [],
    hasTests: false,
    hasTypes: false,
  };

  for (const entry of files) {
    const name = entry.name;

    if (entry.isDirectory() && !IGNORE_DIRS.has(name)) {
      analysis.submodules.push(name);
    } else if (entry.isFile()) {
      if (/\.(ts|js|tsx|jsx|py|go|rs)$/.test(name) && !name.includes('.test.') && !name.includes('.spec.')) {
        analysis.coreFiles.push(name);
      }
      if (name.includes('.test.') || name.includes('.spec.') || name === 'test' || name === 'tests') {
        analysis.hasTests = true;
      }
      if (name.endsWith('.d.ts') || name === 'types.ts') {
        analysis.hasTypes = true;
      }
    }
  }

  return analysis;
}

async function main() {
  const targetPath = process.argv[2] || process.cwd();
  const rootPath = path.resolve(targetPath);

  console.log(`Scanning: ${rootPath}\n`);

  // Detect tech stack
  const techStack = await detectTechStack(rootPath);
  console.log(`Tech Stack: ${techStack.join(', ') || 'Unknown'}\n`);

  // Check for existing root CLAUDE.md
  const hasRootClaude = await exists(path.join(rootPath, 'CLAUDE.md'));
  console.log(`Root CLAUDE.md: ${hasRootClaude ? '✓ exists' : '✗ missing'}\n`);

  // Scan for modules
  const modules = await scanDir(rootPath, rootPath);

  if (modules.length === 0) {
    console.log('No standard module structure detected.');
    console.log('Consider organizing code into src/modules/, src/features/, or packages/');
    return;
  }

  console.log(`Found ${modules.length} modules:\n`);

  // Group by type
  const byType = {};
  for (const mod of modules) {
    if (!byType[mod.type]) byType[mod.type] = [];
    byType[mod.type].push(mod);
  }

  for (const [type, mods] of Object.entries(byType)) {
    console.log(`${type.toUpperCase()}:`);
    for (const mod of mods) {
      const status = mod.hasClaude ? '✓' : '○';
      console.log(`  ${status} ${mod.name} (${mod.path}) - ${mod.fileCount} files`);
    }
    console.log();
  }

  // Summary
  const withClaude = modules.filter(m => m.hasClaude).length;
  console.log(`Coverage: ${withClaude}/${modules.length} modules have CLAUDE.md`);

  // Output JSON for programmatic use
  if (process.argv.includes('--json')) {
    console.log('\n--- JSON ---');
    console.log(JSON.stringify({ techStack, hasRootClaude, modules }, null, 2));
  }
}

main().catch(console.error);

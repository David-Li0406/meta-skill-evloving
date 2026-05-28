#!/usr/bin/env node
/**
 * CLAUDE.md Generator - Create layered index system
 * Usage: node generate.js [--layer 1|2|3] [--module path] [--auto]
 */

import { promises as fs } from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';

const CODE_EXTENSIONS = new Set([
  '.js', '.ts', '.jsx', '.tsx', '.mjs', '.cjs',
  '.py', '.go', '.rs', '.java', '.kt', '.rb', '.php'
]);

const IGNORE_DIRS = new Set([
  'node_modules', '.git', 'dist', 'build', 'coverage', '__pycache__'
]);

// Threshold for "large" directories that need their own CLAUDE.md
const LARGE_THRESHOLD = { files: 5, lines: 200 };

// Load templates
const TEMPLATES = {
  root: `# {PROJECT_NAME}

{DESCRIPTION}

## Tech Stack

{TECH_STACK}

## Module Index

When working on a specific module, read its CLAUDE.md for context:

{MODULE_INDEX}

## Global Conventions

- {CONVENTIONS}
`,

  module: `# {MODULE_NAME}

{DESCRIPTION}

## Core Files

{CORE_FILES}

## Key Concepts

{CONCEPTS}

## Submodule Index

{SUBMODULE_INDEX}

## Common Tasks

### Task 1
1. Step one
2. Step two

`,

  submodule: `# {SUBMODULE_NAME}

{DESCRIPTION}

## Core Files

{CORE_FILES}

## Implementation Details

{DETAILS}

## Configuration

{CONFIG}
`
};

async function exists(p) {
  try { await fs.access(p); return true; } catch { return false; }
}

async function readPackageJson(rootPath) {
  const pkgPath = path.join(rootPath, 'package.json');
  if (await exists(pkgPath)) {
    const content = await fs.readFile(pkgPath, 'utf-8');
    return JSON.parse(content);
  }
  return null;
}

async function detectProjectInfo(rootPath) {
  const pkg = await readPackageJson(rootPath);
  const dirName = path.basename(rootPath);

  return {
    name: pkg?.name || dirName,
    description: pkg?.description || 'Project description here.',
    version: pkg?.version || '0.0.0',
  };
}

async function detectTechStack(rootPath) {
  const stack = [];
  const checks = [
    ['package.json', async () => {
      const pkg = await readPackageJson(rootPath);
      if (pkg?.dependencies?.next || pkg?.devDependencies?.next) stack.push('Next.js');
      if (pkg?.dependencies?.react) stack.push('React');
      if (pkg?.dependencies?.vue) stack.push('Vue');
      if (pkg?.dependencies?.express) stack.push('Express');
      if (pkg?.devDependencies?.typescript) stack.push('TypeScript');
      if (pkg?.dependencies?.prisma || pkg?.devDependencies?.prisma) stack.push('Prisma');
      if (pkg?.dependencies?.tailwindcss || pkg?.devDependencies?.tailwindcss) stack.push('Tailwind CSS');
    }],
    ['pyproject.toml', () => stack.push('Python')],
    ['go.mod', () => stack.push('Go')],
    ['Cargo.toml', () => stack.push('Rust')],
  ];

  for (const [file, handler] of checks) {
    if (await exists(path.join(rootPath, file))) {
      await handler();
    }
  }

  return stack;
}

async function scanModules(rootPath) {
  const modules = [];
  const moduleDirs = ['src/modules', 'src/features', 'packages', 'apps'];

  for (const dir of moduleDirs) {
    const fullPath = path.join(rootPath, dir);
    if (await exists(fullPath)) {
      const entries = await fs.readdir(fullPath, { withFileTypes: true });
      for (const entry of entries) {
        if (entry.isDirectory() && !entry.name.startsWith('.')) {
          modules.push({
            name: entry.name,
            path: path.join(dir, entry.name),
            type: dir.includes('packages') ? 'package' : 'module',
          });
        }
      }
    }
  }

  return modules;
}

async function generateRootClaude(rootPath) {
  const info = await detectProjectInfo(rootPath);
  const techStack = await detectTechStack(rootPath);
  const modules = await scanModules(rootPath);

  let content = TEMPLATES.root
    .replace('{PROJECT_NAME}', info.name)
    .replace('{DESCRIPTION}', info.description)
    .replace('{TECH_STACK}', techStack.map(t => `- ${t}`).join('\n') || '- TODO: Add tech stack')
    .replace('{CONVENTIONS}', 'TODO: Add project conventions');

  // Generate module index
  if (modules.length > 0) {
    const index = modules.map(m =>
      `- **${m.name}**: \`${m.path}/CLAUDE.md\`\n  - TODO: Add description`
    ).join('\n\n');
    content = content.replace('{MODULE_INDEX}', index);
  } else {
    content = content.replace('{MODULE_INDEX}', '- No modules detected. Add modules to src/modules/ or packages/');
  }

  return content;
}

/**
 * Analyze a directory's code files
 * @param {string} dir - Full path to directory
 * @returns {Promise<{fileCount: number, lineCount: number, isLarge: boolean}>}
 */
async function analyzeDir(dir) {
  let fileCount = 0;
  let lineCount = 0;

  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const e of entries) {
      if (!e.isFile()) continue;
      const ext = path.extname(e.name).toLowerCase();
      if (!CODE_EXTENSIONS.has(ext)) continue;
      if (e.name.includes('.test.') || e.name.includes('.spec.')) continue;

      fileCount++;
      try {
        const content = await fs.readFile(path.join(dir, e.name), 'utf-8');
        lineCount += content.split('\n').length;
      } catch {}
    }
  } catch {}

  return {
    fileCount,
    lineCount,
    isLarge: fileCount >= LARGE_THRESHOLD.files || lineCount >= LARGE_THRESHOLD.lines
  };
}

/**
 * Find unindexed small subdirectories that parent should cover
 * @param {string} dir - Full path to parent directory
 * @returns {Promise<Array<{path: string, fileCount: number, lineCount: number, files: string[]}>>}
 */
async function findUnindexedSmallDirs(dir) {
  const results = [];

  async function scan(currentDir) {
    try {
      const entries = await fs.readdir(currentDir, { withFileTypes: true });

      for (const e of entries) {
        if (!e.isDirectory() || IGNORE_DIRS.has(e.name) || e.name.startsWith('.')) continue;

        const subDir = path.join(currentDir, e.name);
        const hasClaude = await exists(path.join(subDir, 'CLAUDE.md'));

        if (hasClaude) continue; // Has own index, skip

        const stats = await analyzeDir(subDir);
        if (stats.fileCount === 0) {
          // No code files, recurse into subdirs
          await scan(subDir);
          continue;
        }

        if (!stats.isLarge) {
          // Small directory without CLAUDE.md - parent should cover
          const files = (await fs.readdir(subDir, { withFileTypes: true }))
            .filter(f => f.isFile() && CODE_EXTENSIONS.has(path.extname(f.name).toLowerCase()))
            .filter(f => !f.name.includes('.test.') && !f.name.includes('.spec.'))
            .map(f => f.name);

          results.push({
            path: path.relative(dir, subDir),
            fileCount: stats.fileCount,
            lineCount: stats.lineCount,
            files
          });
        }

        // Recurse into subdirs
        await scan(subDir);
      }
    } catch {}
  }

  await scan(dir);
  return results;
}

/**
 * Generate prompt context for unindexed small directories
 * @param {string} modulePath - Module path relative to root
 * @param {string} rootPath - Project root
 * @returns {Promise<string>} Prompt fragment to inject
 */
async function generateUnindexedContext(modulePath, rootPath) {
  const fullPath = path.join(rootPath, modulePath);
  const unindexed = await findUnindexedSmallDirs(fullPath);

  if (unindexed.length === 0) return '';

  let context = `\n## 未索引的小子目录（需额外关注）\n\n`;
  context += `以下子目录没有独立的 CLAUDE.md，请在本文档中覆盖它们的功能说明：\n\n`;

  for (const d of unindexed) {
    context += `### ${d.path}\n`;
    context += `- 文件数: ${d.fileCount}, 代码行数: ${d.lineCount}\n`;
    context += `- 文件: ${d.files.join(', ')}\n\n`;
  }

  return context;
}

/**
 * Find all directories that need indexing/re-indexing
 * @param {string} rootPath - Project root
 * @param {string} scanPath - Path to scan (relative to root)
 * @returns {Promise<{needsUpdate: Array<{path: string, reason: string, smallChildren: number}>, needsCreate: Array<{path: string, fileCount: number, lineCount: number}>}>}
 */
export async function findDirsNeedingIndex(rootPath, scanPath) {
  const fullScanPath = path.join(rootPath, scanPath);
  const needsUpdate = []; // Parents with unindexed small children
  const needsCreate = []; // Large dirs without CLAUDE.md

  async function scan(dir) {
    try {
      const entries = await fs.readdir(dir, { withFileTypes: true });
      const hasClaude = await exists(path.join(dir, 'CLAUDE.md'));
      const stats = await analyzeDir(dir);
      const relativePath = path.relative(rootPath, dir);

      if (hasClaude) {
        // Check for unindexed small children
        const smallChildren = await findUnindexedSmallDirs(dir);
        if (smallChildren.length > 0) {
          needsUpdate.push({
            path: relativePath,
            reason: 'has_small_children',
            smallChildren: smallChildren.length
          });
        }
      } else if (stats.fileCount > 0 && stats.isLarge) {
        // Large directory without CLAUDE.md
        needsCreate.push({
          path: relativePath,
          fileCount: stats.fileCount,
          lineCount: stats.lineCount
        });
      }

      // Recurse
      for (const e of entries) {
        if (e.isDirectory() && !IGNORE_DIRS.has(e.name) && !e.name.startsWith('.')) {
          await scan(path.join(dir, e.name));
        }
      }
    } catch {}
  }

  await scan(fullScanPath);

  // Sort by line count (priority)
  needsCreate.sort((a, b) => b.lineCount - a.lineCount);
  needsUpdate.sort((a, b) => b.smallChildren - a.smallChildren);

  return { needsUpdate, needsCreate };
}

/**
 * Find all large directories that should have their own CLAUDE.md
 * @param {string} rootPath - Project root
 * @param {string} scanPath - Path to scan (relative to root)
 * @returns {Promise<Array<{path: string, fileCount: number, lineCount: number}>>}
 */
export async function findLargeDirs(rootPath, scanPath) {
  const fullScanPath = path.join(rootPath, scanPath);
  const results = [];

  async function scan(dir) {
    try {
      const entries = await fs.readdir(dir, { withFileTypes: true });
      const stats = await analyzeDir(dir);
      const relativePath = path.relative(rootPath, dir) || '.';

      if (stats.fileCount > 0 && stats.isLarge) {
        results.push({
          path: relativePath,
          fileCount: stats.fileCount,
          lineCount: stats.lineCount
        });
      }

      for (const e of entries) {
        if (e.isDirectory() && !IGNORE_DIRS.has(e.name) && !e.name.startsWith('.')) {
          await scan(path.join(dir, e.name));
        }
      }
    } catch {}
  }

  await scan(fullScanPath);

  // Sort by line count (priority)
  results.sort((a, b) => b.lineCount - a.lineCount);

  return results;
}

function getDepth(p) {
  return p.split(/[\\/]+/).filter(Boolean).length;
}

/**
 * Generate batch task list for codex parallel execution
 * @param {string} rootPath
 * @param {string} scanPath
 * @param {boolean} jsonOutput
 */
async function generateBatchTasks(rootPath, scanPath, jsonOutput = false) {
  const { needsUpdate, needsCreate } = await findDirsNeedingIndex(rootPath, scanPath);

  if (jsonOutput) {
    // Output JSON for programmatic use
    const tasks = [];

    for (const dir of needsUpdate) {
      const context = await generateUnindexedContext(dir.path, rootPath);
      tasks.push({
        id: `update_${dir.path.replace(/\//g, '_')}`,
        type: 'update',
        path: dir.path,
        reason: `${dir.smallChildren} unindexed small subdirs`,
        promptContext: context
      });
    }

    for (const dir of needsCreate) {
      tasks.push({
        id: `create_${dir.path.replace(/\//g, '_')}`,
        type: 'create',
        path: dir.path,
        reason: `${dir.fileCount} files, ${dir.lineCount} lines`,
        promptContext: ''
      });
    }

    tasks.sort((a, b) => {
      const depthA = getDepth(a.path || a.id);
      const depthB = getDepth(b.path || b.id);
      if (depthA !== depthB) return depthB - depthA;
      const pathA = a.path || a.id;
      const pathB = b.path || b.id;
      return pathA.localeCompare(pathB);
    });

    console.log(JSON.stringify({ tasks, summary: { update: needsUpdate.length, create: needsCreate.length } }, null, 2));
  } else {
    // Human-readable output
    console.log('=== 需要更新的目录（有未索引小子目录） ===\n');
    if (needsUpdate.length === 0) {
      console.log('  (无)\n');
    } else {
      for (const dir of needsUpdate) {
        console.log(`  📁 ${dir.path} (${dir.smallChildren} 个小子目录)`);
      }
      console.log('');
    }

    console.log('=== 需要新建索引的大目录 ===\n');
    if (needsCreate.length === 0) {
      console.log('  (无)\n');
    } else {
      for (const dir of needsCreate) {
        console.log(`  📄 ${dir.path} (${dir.fileCount} 文件, ${dir.lineCount} 行)`);
      }
      console.log('');
    }

    console.log('─'.repeat(50));
    console.log(`总计: 需更新 ${needsUpdate.length} | 需新建 ${needsCreate.length}`);
    console.log('\n使用 --batch --json 获取可供 codex --parallel 使用的任务列表');
  }
}

async function generateModuleClaude(modulePath, rootPath) {
  const moduleName = path.basename(modulePath);
  const fullPath = path.join(rootPath, modulePath);

  // Scan core files
  const entries = await fs.readdir(fullPath, { withFileTypes: true });
  const coreFiles = entries
    .filter(e => e.isFile() && /\.(ts|js|tsx|jsx|py)$/.test(e.name))
    .filter(e => !e.name.includes('.test.') && !e.name.includes('.spec.'))
    .map(e => `- \`${e.name}\``)
    .slice(0, 10);

  const submodules = entries
    .filter(e => e.isDirectory() && !e.name.startsWith('.') && e.name !== 'node_modules')
    .map(e => `- **${e.name}**: \`${modulePath}/${e.name}/CLAUDE.md\``);

  let content = TEMPLATES.module
    .replace('{MODULE_NAME}', moduleName.charAt(0).toUpperCase() + moduleName.slice(1) + ' Module')
    .replace('{DESCRIPTION}', 'TODO: Describe this module')
    .replace('{CORE_FILES}', coreFiles.join('\n') || '- TODO: List core files')
    .replace('{CONCEPTS}', '- TODO: Add key concepts')
    .replace('{SUBMODULE_INDEX}', submodules.length > 0 ? submodules.join('\n') : 'No submodules.');

  return content;
}

async function main() {
  const args = process.argv.slice(2);
  const rootPath = process.cwd();

  const layer = args.includes('--layer') ? args[args.indexOf('--layer') + 1] : null;
  const modulePath = args.includes('--module') ? args[args.indexOf('--module') + 1] : null;
  const auto = args.includes('--auto');
  const dryRun = args.includes('--dry-run');
  const promptContext = args.includes('--prompt-context');
  const batch = args.includes('--batch');
  const jsonOutput = args.includes('--json');
  const scanPath = args.includes('--scan') ? args[args.indexOf('--scan') + 1] : '.';

  if (!layer && !auto && !promptContext && !batch) {
    console.log('Usage:');
    console.log('  node generate.js --layer 1              # Generate root CLAUDE.md');
    console.log('  node generate.js --layer 2 --module src/modules/auth');
    console.log('  node generate.js --auto                 # Generate all layers');
    console.log('  node generate.js --auto --dry-run       # Preview without writing');
    console.log('  node generate.js --prompt-context --module js/agents/core');
    console.log('                                          # Output unindexed subdirs for codex prompt');
    console.log('  node generate.js --batch --scan js/agents');
    console.log('                                          # List dirs needing index update/creation');
    console.log('  node generate.js --batch --scan js/agents --json');
    console.log('                                          # Output JSON for codex --parallel');
    return;
  }

  // Batch mode: find dirs needing indexing
  if (batch) {
    await generateBatchTasks(rootPath, scanPath, jsonOutput);
    return;
  }

  // Generate prompt context for codex
  if (promptContext && modulePath) {
    const context = await generateUnindexedContext(modulePath, rootPath);
    if (context) {
      console.log(context);
    } else {
      console.log('# 该目录下没有未索引的小子目录');
    }
    return;
  }

  if (layer === '1' || auto) {
    console.log('Generating root CLAUDE.md...');
    const content = await generateRootClaude(rootPath);

    if (dryRun) {
      console.log('\n--- CLAUDE.md (preview) ---\n');
      console.log(content);
    } else {
      await fs.writeFile(path.join(rootPath, 'CLAUDE.md'), content);
      console.log('✓ Created CLAUDE.md');
    }
  }

  if (layer === '2' || auto) {
    const modules = await scanModules(rootPath);

    for (const mod of modules) {
      console.log(`Generating ${mod.path}/CLAUDE.md...`);
      const content = await generateModuleClaude(mod.path, rootPath);

      if (dryRun) {
        console.log(`\n--- ${mod.path}/CLAUDE.md (preview) ---\n`);
        console.log(content.slice(0, 500) + '...\n');
      } else {
        await fs.writeFile(path.join(rootPath, mod.path, 'CLAUDE.md'), content);
        console.log(`✓ Created ${mod.path}/CLAUDE.md`);
      }
    }
  }

  console.log('\nDone! Review and customize the generated CLAUDE.md files.');
}

const isDirectRun = process.argv[1] &&
  path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);

if (isDirectRun) {
  main().catch(console.error);
}

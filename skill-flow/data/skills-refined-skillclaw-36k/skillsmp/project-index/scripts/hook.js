#!/usr/bin/env node
/**
 * Hook Manager - Install/manage Claude Code hooks for project-index
 *
 * Usage:
 *   node hook.js init [--global]       Initialize project with all recommended hooks
 *   node hook.js install [--global]    Install PostToolUse hook (git commit trigger)
 *   node hook.js uninstall [--global]  Remove hooks
 *   node hook.js status                Check hook status
 *   node hook.js list                  List all installed hooks
 *   node hook.js toggle <hook> [on|off] Toggle specific hook
 *
 * Hook types:
 *   - post-commit: Update CLAUDE.md after git commit (PostToolUse)
 *   - stale-notify: Notify stale modules on session start (UserPromptSubmit)
 */

import { promises as fs } from 'fs';
import path from 'path';
import os from 'os';

const CLAUDE_SETTINGS_PATH = path.join(os.homedir(), '.claude', 'settings.json');
const PROJECT_SETTINGS_PATH = path.join(process.cwd(), '.claude', 'settings.json');
const STALE_CONFIG_PATH = path.join(process.cwd(), '.stale-config.json');

/**
 * Available hook definitions
 * Format: matcher is string (tool name regex), hooks is array
 * Note: For PostToolUse, we match "Bash" tool and filter git commit in the script
 */
const HOOKS = {
  'post-commit': {
    type: 'PostToolUse',
    config: {
      matcher: 'Bash',
      hooks: [{ type: 'command', command: 'node ~/.claude/skills/project-index/scripts/update.js --silent --if-commit' }]
    },
    description: 'Update CLAUDE.md after git commit'
  },
  'stale-notify': {
    type: 'UserPromptSubmit',
    config: {
      hooks: [{ type: 'command', command: 'node ~/.claude/skills/project-index/scripts/stale-notify.js' }]
    },
    description: 'Notify stale modules on session start'
  }
};

async function exists(p) {
  try { await fs.access(p); return true; } catch { return false; }
}

async function readSettings(settingsPath) {
  if (!await exists(settingsPath)) {
    return {};
  }
  const content = await fs.readFile(settingsPath, 'utf-8');
  return JSON.parse(content);
}

async function writeSettings(settingsPath, settings) {
  const dir = path.dirname(settingsPath);
  if (!await exists(dir)) {
    await fs.mkdir(dir, { recursive: true });
  }
  await fs.writeFile(settingsPath, JSON.stringify(settings, null, 2));
}

/**
 * Load .stale-config.json for hook configuration
 */
async function loadStaleConfig() {
  try {
    const content = await fs.readFile(STALE_CONFIG_PATH, 'utf-8');
    return JSON.parse(content);
  } catch {
    return {};
  }
}

/**
 * Check if a specific hook is installed (new format)
 * @param {object} settings
 * @param {string} hookName - 'post-commit' or 'stale-notify'
 */
function hasHook(settings, hookName) {
  const hookDef = HOOKS[hookName];
  if (!hookDef) return false;

  const hookList = settings.hooks?.[hookDef.type] || [];
  return hookList.some(h => {
    // Check if any sub-hook command contains 'project-index'
    const subHooks = h.hooks || [];
    return subHooks.some(sh => sh.command?.includes('project-index'));
  });
}

/**
 * Get all installed project-index hooks (new format)
 * @param {object} settings
 * @returns {{name: string, type: string, config: object}[]}
 */
function getInstalledHooks(settings) {
  const installed = [];
  for (const [name, def] of Object.entries(HOOKS)) {
    const hookList = settings.hooks?.[def.type] || [];
    const match = hookList.find(h => {
      const subHooks = h.hooks || [];
      return subHooks.some(sh => sh.command?.includes('project-index'));
    });
    if (match) {
      installed.push({ name, type: def.type, config: match });
    }
  }
  return installed;
}

/**
 * Install a specific hook
 * @param {string} hookName
 * @param {string} scope - 'project' or 'global'
 */
async function installHook(hookName, scope = 'project') {
  const hookDef = HOOKS[hookName];
  if (!hookDef) {
    console.log(`Unknown hook: ${hookName}`);
    console.log(`Available: ${Object.keys(HOOKS).join(', ')}`);
    return false;
  }

  const settingsPath = scope === 'global' ? CLAUDE_SETTINGS_PATH : PROJECT_SETTINGS_PATH;
  const settings = await readSettings(settingsPath);

  if (hasHook(settings, hookName)) {
    console.log(`Hook '${hookName}' already installed in ${scope} settings.`);
    return true;
  }

  if (!settings.hooks) settings.hooks = {};
  if (!settings.hooks[hookDef.type]) settings.hooks[hookDef.type] = [];

  settings.hooks[hookDef.type].push(hookDef.config);

  await writeSettings(settingsPath, settings);
  console.log(`✓ Hook '${hookName}' installed (${hookDef.description})`);
  return true;
}

/**
 * Remove a specific hook (new format)
 * @param {string} hookName
 * @param {string} scope
 */
async function removeHook(hookName, scope = 'project') {
  const hookDef = HOOKS[hookName];
  if (!hookDef) return false;

  const settingsPath = scope === 'global' ? CLAUDE_SETTINGS_PATH : PROJECT_SETTINGS_PATH;
  const settings = await readSettings(settingsPath);

  if (!settings.hooks?.[hookDef.type]) return false;

  const before = settings.hooks[hookDef.type].length;
  settings.hooks[hookDef.type] = settings.hooks[hookDef.type].filter(h => {
    const subHooks = h.hooks || [];
    return !subHooks.some(sh => sh.command?.includes('project-index'));
  });
  const after = settings.hooks[hookDef.type].length;

  if (before === after) return false;

  await writeSettings(settingsPath, settings);
  console.log(`✓ Hook '${hookName}' removed`);
  return true;
}

/**
 * Initialize project with all recommended hooks based on config
 */
async function init(scope = 'project') {
  const config = await loadStaleConfig();
  const notifyConfig = config.notify || {};

  console.log('Initializing project-index hooks...\n');

  // Always install post-commit hook
  await installHook('post-commit', scope);

  // Install stale-notify if enabled in config (default: true)
  if (notifyConfig.onSessionStart !== false) {
    await installHook('stale-notify', scope);
  } else {
    console.log('⊘ stale-notify disabled in .stale-config.json');
  }

  // Create .stale-config.json if not exists
  if (!await exists(STALE_CONFIG_PATH)) {
    const defaultConfig = {
      ignore: ['tests/**', 'test/**', 'docs/**', '*.test.js', '*.spec.js'],
      features: { doc: true, audit: true, kanban: true },
      notify: { enabled: true, threshold: 3, onSessionStart: true },
      concurrency: 6,
      timeout: 180000
    };
    await fs.writeFile(STALE_CONFIG_PATH, JSON.stringify(defaultConfig, null, 2));
    console.log('\n✓ Created .stale-config.json with default settings');
  }

  console.log('\n✓ Project initialized');
}

/**
 * List all installed hooks
 */
async function list() {
  console.log('Installed project-index hooks:\n');

  const projectSettings = await readSettings(PROJECT_SETTINGS_PATH);
  const globalSettings = await readSettings(CLAUDE_SETTINGS_PATH);

  const projectHooks = getInstalledHooks(projectSettings);
  const globalHooks = getInstalledHooks(globalSettings);

  if (projectHooks.length > 0) {
    console.log('Project (.claude/settings.json):');
    for (const h of projectHooks) {
      console.log(`  ✓ ${h.name} (${h.type})`);
    }
  }

  if (globalHooks.length > 0) {
    console.log('\nGlobal (~/.claude/settings.json):');
    for (const h of globalHooks) {
      console.log(`  ✓ ${h.name} (${h.type})`);
    }
  }

  if (projectHooks.length === 0 && globalHooks.length === 0) {
    console.log('  (none)');
    console.log('\nRun "node hook.js init" to set up recommended hooks.');
  }

  console.log('\nAvailable hooks:');
  for (const [name, def] of Object.entries(HOOKS)) {
    const installed = hasHook(projectSettings, name) || hasHook(globalSettings, name);
    console.log(`  ${installed ? '✓' : '○'} ${name} - ${def.description}`);
  }
}

/**
 * Toggle a specific hook on/off
 */
async function toggle(hookName, state, scope = 'project') {
  if (!HOOKS[hookName]) {
    console.log(`Unknown hook: ${hookName}`);
    console.log(`Available: ${Object.keys(HOOKS).join(', ')}`);
    return;
  }

  const settingsPath = scope === 'global' ? CLAUDE_SETTINGS_PATH : PROJECT_SETTINGS_PATH;
  const settings = await readSettings(settingsPath);
  const installed = hasHook(settings, hookName);

  if (state === 'on' || (state === undefined && !installed)) {
    await installHook(hookName, scope);
  } else if (state === 'off' || (state === undefined && installed)) {
    await removeHook(hookName, scope);
  }
}

async function status() {
  console.log('Project Index Hook Status\n');

  // Check project settings
  const projectSettings = await readSettings(PROJECT_SETTINGS_PATH);
  const globalSettings = await readSettings(CLAUDE_SETTINGS_PATH);

  console.log('Project (.claude/settings.json):');
  for (const [name, def] of Object.entries(HOOKS)) {
    const installed = hasHook(projectSettings, name);
    console.log(`  ${name}: ${installed ? '✓ installed' : '✗ not installed'}`);
  }

  console.log('\nGlobal (~/.claude/settings.json):');
  for (const [name, def] of Object.entries(HOOKS)) {
    const installed = hasHook(globalSettings, name);
    console.log(`  ${name}: ${installed ? '✓ installed' : '✗ not installed'}`);
  }

  // Check config
  const config = await loadStaleConfig();
  if (Object.keys(config).length > 0) {
    console.log('\nConfig (.stale-config.json):');
    console.log(`  notify.onSessionStart: ${config.notify?.onSessionStart ?? true}`);
    console.log(`  notify.threshold: ${config.notify?.threshold ?? 3}`);
  } else {
    console.log('\nNo .stale-config.json found. Run "node hook.js init" to create one.');
  }
}

/**
 * Uninstall all project-index hooks
 */
async function uninstall(scope = 'project') {
  console.log(`Removing all project-index hooks from ${scope}...\n`);
  let removed = 0;
  for (const name of Object.keys(HOOKS)) {
    if (await removeHook(name, scope)) removed++;
  }
  if (removed === 0) {
    console.log('No hooks found.');
  } else {
    console.log(`\n${removed} hook(s) removed.`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const scope = args.includes('--global') ? 'global' : 'project';

  switch (command) {
    case 'init':
      await init(scope);
      break;
    case 'install':
      // If specific hook name provided, install just that
      const hookToInstall = args.find(a => HOOKS[a]);
      if (hookToInstall) {
        await installHook(hookToInstall, scope);
      } else {
        await installHook('post-commit', scope);
      }
      break;
    case 'uninstall':
      const hookToRemove = args.find(a => HOOKS[a]);
      if (hookToRemove) {
        await removeHook(hookToRemove, scope);
      } else {
        await uninstall(scope);
      }
      break;
    case 'status':
      await status();
      break;
    case 'list':
      await list();
      break;
    case 'toggle':
      const hookName = args[1];
      const state = args[2]; // 'on', 'off', or undefined
      await toggle(hookName, state, scope);
      break;
    default:
      console.log('Usage:');
      console.log('  node hook.js init [--global]              Initialize with all recommended hooks');
      console.log('  node hook.js install [hook] [--global]    Install hook (default: post-commit)');
      console.log('  node hook.js uninstall [hook] [--global]  Remove hook(s)');
      console.log('  node hook.js status                       Check hook status');
      console.log('  node hook.js list                         List all hooks');
      console.log('  node hook.js toggle <hook> [on|off]       Toggle specific hook');
      console.log('\nHooks:');
      for (const [name, def] of Object.entries(HOOKS)) {
        console.log(`  ${name.padEnd(15)} ${def.description}`);
      }
  }
}

main().catch(console.error);

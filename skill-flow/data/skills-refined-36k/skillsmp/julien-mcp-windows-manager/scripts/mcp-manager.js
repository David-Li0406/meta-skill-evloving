#!/usr/bin/env node
/**
 * MCP Manager for Windows
 *
 * Add, remove, and list MCP servers with proper Windows configuration.
 * Handles cmd /c wrapper automatically for npx-based servers.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const GLOBAL_CONFIG = path.join(os.homedir(), '.claude.json');
const PROJECT_CONFIG = path.join(process.cwd(), '.mcp.json');

function loadConfig(configPath) {
    try {
        return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    } catch {
        return null;
    }
}

function saveConfig(configPath, config) {
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
}

function listMcps() {
    console.log('🔌 MCP Servers\n');

    // Global
    const global = loadConfig(GLOBAL_CONFIG);
    if (global?.mcpServers) {
        console.log('=== Global (~/.claude.json) ===');
        for (const [name, config] of Object.entries(global.mcpServers)) {
            const cmd = config.command + ' ' + (config.args || []).slice(0, 3).join(' ');
            console.log(`  • ${name}`);
            console.log(`    ${cmd}...`);
        }
    } else {
        console.log('=== Global ===\n  (none)');
    }

    console.log('');

    // Project
    const project = loadConfig(PROJECT_CONFIG);
    if (project?.mcpServers) {
        console.log('=== Project (.mcp.json) ===');
        for (const [name, config] of Object.entries(project.mcpServers)) {
            const cmd = config.command + ' ' + (config.args || []).slice(0, 3).join(' ');
            console.log(`  • ${name}`);
            console.log(`    ${cmd}...`);
        }
    } else {
        console.log('=== Project ===\n  (none or no .mcp.json)');
    }
}

function addMcp(name, packageName, options = {}) {
    const isGlobal = options.global !== false;
    const configPath = isGlobal ? GLOBAL_CONFIG : PROJECT_CONFIG;
    const scopeLabel = isGlobal ? 'global' : 'project';

    let config = loadConfig(configPath);

    if (!config) {
        if (isGlobal) {
            console.error(`❌ Global config not found: ${GLOBAL_CONFIG}`);
            process.exit(1);
        }
        config = { mcpServers: {} };
    }

    if (!config.mcpServers) {
        config.mcpServers = {};
    }

    // Check if already exists
    if (config.mcpServers[name]) {
        console.log(`⚠️  MCP "${name}" already exists in ${scopeLabel} config`);
        console.log('   Use --force to overwrite');
        if (!options.force) {
            process.exit(1);
        }
    }

    // Build Windows-compatible config
    const mcpConfig = {
        command: 'cmd',
        args: ['/c', 'npx', '-y', packageName]
    };

    // Add env if provided
    if (options.env) {
        mcpConfig.env = options.env;
    }

    config.mcpServers[name] = mcpConfig;
    saveConfig(configPath, config);

    console.log(`✅ Added MCP "${name}" to ${scopeLabel} config`);
    console.log(`   Package: ${packageName}`);
    console.log(`   Config: ${configPath}`);
    console.log('\n⚠️  Restart Claude Code to load the new MCP');
}

function removeMcp(name, options = {}) {
    let removed = false;

    // Try global first (unless project-only specified)
    if (options.project !== true) {
        const global = loadConfig(GLOBAL_CONFIG);
        if (global?.mcpServers?.[name]) {
            delete global.mcpServers[name];
            saveConfig(GLOBAL_CONFIG, global);
            console.log(`✅ Removed "${name}" from global config`);
            removed = true;
        }
    }

    // Try project
    if (options.global !== true) {
        const project = loadConfig(PROJECT_CONFIG);
        if (project?.mcpServers?.[name]) {
            delete project.mcpServers[name];
            saveConfig(PROJECT_CONFIG, project);
            console.log(`✅ Removed "${name}" from project config`);
            removed = true;
        }
    }

    if (!removed) {
        console.log(`❌ MCP "${name}" not found`);
        process.exit(1);
    }

    console.log('\n⚠️  Restart Claude Code to apply changes');
}

function showHelp() {
    console.log(`
🔌 MCP Manager for Windows

Usage:
  node mcp-manager.js <command> [options]

Commands:
  list                          List all MCPs (global + project)
  add <name> <package>          Add MCP server
  remove <name>                 Remove MCP server

Options:
  --global                      Target global config (~/.claude.json)
  --project                     Target project config (.mcp.json)
  --force                       Overwrite existing MCP

Examples:
  node mcp-manager.js list
  node mcp-manager.js add playwright @playwright/mcp@latest
  node mcp-manager.js add filesystem @modelcontextprotocol/server-filesystem
  node mcp-manager.js remove playwright --global
`);
}

// Parse arguments
const args = process.argv.slice(2);
const command = args[0];

const options = {
    global: args.includes('--global'),
    project: args.includes('--project'),
    force: args.includes('--force')
};

// Filter out flags
const positionalArgs = args.filter(a => !a.startsWith('--'));

switch (command) {
    case 'list':
        listMcps();
        break;
    case 'add':
        if (positionalArgs.length < 3) {
            console.error('❌ Usage: add <name> <package>');
            process.exit(1);
        }
        addMcp(positionalArgs[1], positionalArgs[2], options);
        break;
    case 'remove':
        if (positionalArgs.length < 2) {
            console.error('❌ Usage: remove <name>');
            process.exit(1);
        }
        removeMcp(positionalArgs[1], options);
        break;
    case 'help':
    case '--help':
    case '-h':
        showHelp();
        break;
    default:
        showHelp();
}

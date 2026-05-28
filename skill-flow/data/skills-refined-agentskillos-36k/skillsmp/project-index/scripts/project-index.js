#!/usr/bin/env node
/**
 * Project Index CLI - Unified entry point
 * Usage: project-index <command> [options]
 */

import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const COMMANDS = {
  scan: { script: 'scan.js', desc: 'Scan project structure and detect modules' },
  init: { script: 'generate.js', desc: 'Generate CLAUDE.md hierarchy', args: ['--auto'] },
  generate: { script: 'generate.js', desc: 'Generate CLAUDE.md files' },
  update: { script: 'update.js', desc: 'Incremental update based on git changes' },
  hook: { script: 'hook.js', desc: 'Manage Claude Code hooks' },
};

function showHelp() {
  console.log('Project Index - Layered CLAUDE.md System\n');
  console.log('Usage: project-index <command> [options]\n');
  console.log('Commands:');
  for (const [cmd, info] of Object.entries(COMMANDS)) {
    console.log(`  ${cmd.padEnd(12)} ${info.desc}`);
  }
  console.log('\nExamples:');
  console.log('  project-index scan              # Analyze project structure');
  console.log('  project-index init              # Generate all CLAUDE.md files');
  console.log('  project-index update            # Update after git changes');
  console.log('  project-index hook install      # Set up auto-update hook');
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h') {
    showHelp();
    return;
  }

  const cmdInfo = COMMANDS[command];
  if (!cmdInfo) {
    console.error(`Unknown command: ${command}`);
    console.error('Run "project-index --help" for usage.');
    process.exit(1);
  }

  const scriptPath = path.join(__dirname, cmdInfo.script);
  const scriptArgs = [...(cmdInfo.args || []), ...args.slice(1)];

  const child = spawn('node', [scriptPath, ...scriptArgs], {
    stdio: 'inherit',
    cwd: process.cwd(),
  });

  child.on('close', (code) => {
    process.exit(code || 0);
  });
}

main().catch(console.error);

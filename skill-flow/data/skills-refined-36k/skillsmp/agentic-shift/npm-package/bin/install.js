#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILL_NAME = 'agentic-shift';
const SKILL_DIR = path.join(os.homedir(), '.claude', 'skills', SKILL_NAME);

console.log('Installing The Agentic Shift...\n');

// Create skills directory
const skillsDir = path.join(os.homedir(), '.claude', 'skills');
if (!fs.existsSync(skillsDir)) {
  fs.mkdirSync(skillsDir, { recursive: true });
}

// Remove existing installation
if (fs.existsSync(SKILL_DIR)) {
  fs.rmSync(SKILL_DIR, { recursive: true });
}

// Copy skill files
const sourceDir = path.join(__dirname, '..', 'skill');
copyRecursive(sourceDir, SKILL_DIR);

console.log('Installed successfully!\n');
console.log('Start with:\n');
console.log('  claude /agentic-shift\n');

function copyRecursive(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

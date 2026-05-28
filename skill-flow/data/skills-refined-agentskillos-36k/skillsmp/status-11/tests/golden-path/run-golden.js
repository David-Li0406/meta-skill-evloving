#!/usr/bin/env node
const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');

const STORY_PATH = path.resolve(__dirname, '..', '..', 'web', 'stories', 'demo.ink');
const SCRIPT_PATH = path.resolve(__dirname, 'scripts', 'demo.golden.json');
const REPLAY_SCRIPT = path.resolve(__dirname, '..', '..', 'scripts', 'replay.js');
const TIMEOUT_MS = 30_000;

function ensurePaths() {
  if (!fs.existsSync(STORY_PATH)) {
    throw new Error(`Story not found at ${STORY_PATH}`);
  }
  if (!fs.existsSync(SCRIPT_PATH)) {
    throw new Error(`Golden script not found at ${SCRIPT_PATH}`);
  }
  if (!fs.existsSync(REPLAY_SCRIPT)) {
    throw new Error(`Replay harness not found at ${REPLAY_SCRIPT}`);
  }
}

function writeFailureLog(output) {
  try {
    const dir = path.join(__dirname, '..', '..', 'test-results', 'replay', String(Date.now()));
    fs.mkdirSync(dir, { recursive: true });
    const logPath = path.join(dir, 'logs.txt');
    fs.writeFileSync(logPath, output, 'utf8');
    return logPath;
  } catch (err) {
    return null;
  }
}

function run() {
  ensurePaths();
  const args = ['--story', STORY_PATH, '--script', SCRIPT_PATH];
  const child = execFile('node', [REPLAY_SCRIPT, ...args], { timeout: TIMEOUT_MS }, (error, stdout, stderr) => {
    if (error) {
      const combined = `stdout:\n${stdout}\n\nstderr:\n${stderr}\n\nerror:${error.message}`;
      const logPath = writeFailureLog(combined);
      if (logPath) {
        console.error(`Golden-path replay failed; logs saved to ${logPath}`);
      } else {
        console.error('Golden-path replay failed; unable to save logs');
      }
      console.error(combined);
      process.exitCode = error.code || 1;
      return;
    }
    process.stdout.write(stdout);
  });

  child.on('error', (err) => {
    const logPath = writeFailureLog(`spawn error: ${err.message}`);
    if (logPath) {
      console.error(`Golden-path replay spawn failed; logs saved to ${logPath}`);
    } else {
      console.error('Golden-path replay spawn failed; unable to save logs');
    }
    console.error(err);
    process.exit(1);
  });
}

if (require.main === module) {
  try {
    run();
  } catch (err) {
    const logPath = writeFailureLog(`setup error: ${err.message}`);
    if (logPath) {
      console.error(`Golden-path replay setup failed; logs saved to ${logPath}`);
    }
    console.error(err.message);
    process.exit(1);
  }
}

module.exports = { run };

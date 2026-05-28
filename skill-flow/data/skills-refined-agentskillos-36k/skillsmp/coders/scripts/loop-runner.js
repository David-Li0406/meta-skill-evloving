#!/usr/bin/env node

/**
 * Recursive Loop Runner for Coders
 *
 * Monitors promises and auto-spawns next task from todolist
 * Runs in background, orchestrator remains interactive
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';
const LOOP_STATE_KEY = 'coders:loop:state';
const PROMISE_KEY_PREFIX = 'coders:promise:';
const PANE_KEY_PREFIX = 'coders:pane:';
const USAGE_CAP_THRESHOLD = 90; // Switch tools if usage is above 90%

// Parse command line arguments
const args = process.argv.slice(2);
let todolistPath = null;
let cwd = null;
let tool = 'claude';
let model = null;
let maxConcurrent = 1;
let stopOnBlocked = false;
let loopId = `loop-${Date.now()}`;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--todolist' && args[i + 1]) {
    todolistPath = args[i + 1];
    i++;
  } else if (args[i] === '--cwd' && args[i + 1]) {
    cwd = args[i + 1];
    i++;
  } else if (args[i] === '--tool' && args[i + 1]) {
    tool = args[i + 1];
    i++;
  } else if (args[i] === '--model' && args[i + 1]) {
    model = args[i + 1];
    i++;
  } else if (args[i] === '--max-concurrent' && args[i + 1]) {
    maxConcurrent = parseInt(args[i + 1]);
    i++;
  } else if (args[i] === '--stop-on-blocked') {
    stopOnBlocked = true;
  } else if (args[i] === '--loop-id' && args[i + 1]) {
    loopId = args[i + 1];
    i++;
  }
}

if (!todolistPath || !cwd) {
  console.error('Usage: loop-runner.js --todolist <path> --cwd <dir> [options]');
  process.exit(1);
}

/**
 * Check if Claude has shown a usage warning in the session output
 * Returns true if we should switch to codex
 */
function checkForUsageWarning(sessionName) {
  try {
    // Capture recent output from the session
    const output = execSync(`tmux capture-pane -p -t "coder-${sessionName}" -S -100 2>/dev/null`, {
      encoding: 'utf-8',
      timeout: 5000
    });

    // Look for Claude's usage warning patterns
    // Examples:
    // "⚠️ You're approaching your usage limit"
    // "90% of your weekly limit"
    // "You've used 90% of your"
    const warningPatterns = [
      /approaching.*usage\s*limit/i,
      /9[0-9]%.*limit/i,
      /usage.*limit.*reached/i,
      /exceeded.*limit/i
    ];

    for (const pattern of warningPatterns) {
      if (pattern.test(output)) {
        return true;
      }
    }

    return false;
  } catch (e) {
    return false;
  }
}

/**
 * Parse todolist file to extract uncompleted tasks
 */
function parseTodolist(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  const tasks = [];

  for (const line of lines) {
    // Match uncompleted tasks: [ ] Task description
    const match = line.match(/^\[\ \]\s*(.+)$/);
    if (match) {
      tasks.push(match[1].trim());
    }
  }

  return tasks;
}

/**
 * Mark task as complete in todolist
 */
function markTaskComplete(filePath, taskDescription) {
  let content = fs.readFileSync(filePath, 'utf-8');
  // Replace first occurrence of [ ] task with [x] task
  const regex = new RegExp(`\\[\ \\]\\s*${taskDescription.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`);
  content = content.replace(regex, `[x] ${taskDescription}`);
  fs.writeFileSync(filePath, content);
}

/**
 * Spawn a coder session for a task
 */
function spawnTask(task, index, totalTasks, selectedTool) {
  const actualTool = selectedTool || tool;
  const sessionName = `${actualTool}-loop-task-${index + 1}`;
  const mainScript = path.join(__dirname, 'main.js');

  const spawnCmd = [
    'node', mainScript, 'spawn', actualTool,
    '--cwd', cwd,
    '--name', sessionName,
    '--task', `"${task}. When complete, commit changes and push to GitHub, then publish a completion promise."`
  ];

  if (model) {
    spawnCmd.push('--model', model);
  }

  console.log(`\n🚀 Spawning task ${index + 1}/${totalTasks}`);
  console.log(`📝 Task: ${task}`);
  console.log(`🔧 Command: ${spawnCmd.join(' ')}`);

  try {
    execSync(spawnCmd.join(' '), { stdio: 'inherit' });
    return sessionName;
  } catch (e) {
    console.error(`❌ Failed to spawn task: ${e.message}`);
    return null;
  }
}

/**
 * Monitor promises and return when new one detected
 */
async function waitForPromise(sessionName) {
  const { createClient } = await import('redis');
  const client = createClient({ url: REDIS_URL });
  await client.connect();

  const expectedKey = `${PROMISE_KEY_PREFIX}coder-${sessionName}`;

  console.log(`⏳ Waiting for promise from ${sessionName}...`);

  return new Promise((resolve) => {
    const checkInterval = setInterval(async () => {
      const promise = await client.get(expectedKey);
      if (promise) {
        clearInterval(checkInterval);
        const promiseData = JSON.parse(promise);
        console.log(`\n✅ Promise received from ${sessionName}`);
        console.log(`📋 Status: ${promiseData.status}`);
        console.log(`💬 Summary: ${promiseData.summary}`);
        await client.quit();
        resolve(promiseData);
      }
    }, 5000); // Check every 5 seconds
  });
}

/**
 * Save loop state to Redis
 */
async function saveLoopState(state) {
  const { createClient } = await import('redis');
  const client = createClient({ url: REDIS_URL });
  await client.connect();
  await client.set(`${LOOP_STATE_KEY}:${loopId}`, JSON.stringify(state));
  await client.quit();
}

/**
 * Main loop execution
 */
async function runLoop() {
  console.log('🔄 Starting Recursive Loop');
  console.log(`📂 Todolist: ${todolistPath}`);
  console.log(`📁 Working directory: ${cwd}`);
  console.log(`🤖 Tool: ${tool}`);
  console.log(`🆔 Loop ID: ${loopId}`);
  console.log('');

  // Parse todolist
  const tasks = parseTodolist(todolistPath);
  console.log(`📋 Found ${tasks.length} uncompleted tasks`);

  if (tasks.length === 0) {
    console.log('✅ All tasks already completed!');
    return;
  }

  // Execute tasks sequentially
  for (let i = 0; i < tasks.length; i++) {
    const task = tasks[i];

    // Save current state
    await saveLoopState({
      loopId,
      todolistPath,
      cwd,
      currentTaskIndex: i,
      totalTasks: tasks.length,
      currentTool: tool,
      status: 'running'
    });

    // Spawn task with current tool
    const sessionName = spawnTask(task, i, tasks.length, tool);
    if (!sessionName) {
      console.error('❌ Failed to spawn task, stopping loop');
      break;
    }

    // Wait for promise
    const promise = await waitForPromise(sessionName);

    // Check if blocked
    if (promise.status === 'blocked') {
      console.log(`\n🚫 Task blocked: ${promise.summary}`);
      if (stopOnBlocked) {
        console.log('⏸️  Stopping loop (--stop-on-blocked enabled)');
        break;
      }
      console.log('⚠️  Continuing despite blocked status...');
    }

    // Mark task as complete in todolist
    markTaskComplete(todolistPath, task);
    console.log(`✅ Task ${i + 1}/${tasks.length} completed`);

    // Check if Claude showed usage warning and switch to codex if needed
    if (tool === 'claude' && checkForUsageWarning(sessionName)) {
      console.log(`\n⚠️  Detected Claude usage warning - switching to codex for remaining tasks`);
      tool = 'codex';
    }

    // Small delay before next task
    await new Promise(resolve => setTimeout(resolve, 2000));
  }

  console.log('\n🎉 Loop completed!');
  await saveLoopState({
    loopId,
    todolistPath,
    cwd,
    currentTaskIndex: tasks.length,
    totalTasks: tasks.length,
    status: 'completed'
  });
}

// Handle graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n⏹️  Loop interrupted by user');
  await saveLoopState({
    loopId,
    status: 'paused'
  });
  process.exit(0);
});

// Run the loop
runLoop().catch((err) => {
  console.error('❌ Loop error:', err);
  process.exit(1);
});

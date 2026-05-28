#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const fg = require('fast-glob');
const inkjs = require('inkjs/full');

const { Story, Compiler } = inkjs;

const DEFAULT_GLOB = 'web/stories/**/*.ink';
const DEFAULT_MAX_STEPS = 1000;
const DEFAULT_STATE_FILE = '.validate-story-state.json';
const DEFAULT_MAX_RETRIES = 3;

function usage() {
  return `Usage: node scripts/validate-story.js [options]\n\n` +
    `Options:\n` +
    `  --story <path|glob>      Story file or glob (default: ${DEFAULT_GLOB})\n` +
    `  --seed <n>               Seed for deterministic choice selection\n` +
    `  --max-steps <n>          Maximum story steps (default: ${DEFAULT_MAX_STEPS})\n` +
    `  --output <stdout|path>   Output JSON to stdout or file (default: json/stdout)\n` +
    `  --state-file <path>      Path to rotation state file (default: ${DEFAULT_STATE_FILE})\n` +
    `  --clear-state            Clear stored state for the target story/stories before running\n` +
    `  --max-retries <n>        Attempts to find an alternate path (default: ${DEFAULT_MAX_RETRIES})\n` +
    `  --help                   Show this help\n`;
}

function parseArgs(argv) {
  const args = {
    story: DEFAULT_GLOB,
    seed: null,
    maxSteps: DEFAULT_MAX_STEPS,
    output: 'json',
    stateFile: DEFAULT_STATE_FILE,
    stateEnabled: true,
    clearState: false,
    maxRetries: DEFAULT_MAX_RETRIES,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    switch (arg) {
      case '--story':
        args.story = argv[++i];
        break;
      case '--seed': {
        const next = argv[++i];
        args.seed = next != null ? next : null;
        break;
      }
      case '--max-steps':
        args.maxSteps = parseInt(argv[++i], 10) || DEFAULT_MAX_STEPS;
        break;
      case '--output':
        args.output = argv[++i] || 'json';
        break;
      case '--state-file':
      case '--state':
        args.stateFile = argv[++i] || DEFAULT_STATE_FILE;
        args.stateEnabled = true;
        break;
      case '--state-file-default':
        args.stateFile = DEFAULT_STATE_FILE;
        args.stateEnabled = true;
        break;
      case '--clear-state':
        args.clearState = true;
        args.stateEnabled = true;
        if (!args.stateFile) args.stateFile = DEFAULT_STATE_FILE;
        break;
      case '--max-retries':
        args.maxRetries = parseInt(argv[++i], 10) || DEFAULT_MAX_RETRIES;
        break;
      case '--state-disabled':
      case '--no-state':
        args.stateEnabled = false;
        args.stateFile = null;
        break;
      case '--help':
      case '-h':
        args.help = true;
        break;
    default:
      break;
    }
  }

  return args;
}

function resolveStories(pattern) {

  const resolvedPath = path.resolve(pattern);
  if (fs.existsSync(resolvedPath)) {
    const stats = fs.statSync(resolvedPath);
    if (stats.isFile()) return [resolvedPath];
    if (stats.isDirectory()) {
      return fg.sync(path.join(resolvedPath, '**/*.ink'), { absolute: true });
    }
  }
  return fg.sync(pattern, { absolute: true });
}

function hashSeed(input) {
  const str = String(input);
  let hash = 0;
  for (let i = 0; i < str.length; i += 1) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash |= 0; // keep 32bit
  }
  return hash >>> 0;
}

function mulberry32(seed) {
  let s = seed >>> 0;
  return function rng() {
    s += 0x6d2b79f5;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function chooseIndex(choices, rng, depth, lastPath) {
  if (!choices.length) return null;
  const lastIndex = Array.isArray(lastPath) ? lastPath[depth] : undefined;
  // If there is only one choice, rotation is only possible when lastIndex is undefined.
  if (choices.length === 1) {
    if (typeof lastIndex === 'number') return null;
    return 0;
  }

  const candidates = choices.map((_, idx) => idx).filter((idx) => idx !== lastIndex);
  if (!candidates.length) return null;

  if (rng) {
    const idx = Math.floor(rng() * candidates.length);
    return candidates[idx];
  }

  // Deterministic rotation without seed: pick next index different from lastIndex.
  if (typeof lastIndex === 'number' && candidates.includes((lastIndex + 1) % choices.length)) {
    return (lastIndex + 1) % choices.length;
  }

  return candidates[0];
}

function readStateFile(stateFile) {
  if (!stateFile) return {};
  if (!fs.existsSync(stateFile)) return {};
  try {
    const raw = fs.readFileSync(stateFile, 'utf8');
    return JSON.parse(raw || '{}');
  } catch (err) {
    return {};
  }
}

function writeStateFile(stateFile, state) {
  if (!stateFile) return;
  const content = JSON.stringify(state, null, 2);
  const dir = path.dirname(stateFile);
  if (dir && dir !== '.' && !fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(stateFile, content, 'utf8');
}

function arraysEqual(a, b) {
  if (!Array.isArray(a) || !Array.isArray(b)) return false;
  if (a.length !== b.length) return false;
  for (let i = 0; i < a.length; i += 1) {
    if (a[i] !== b[i]) return false;
  }
  return true;
}

function runStoryOnce(filePath, opts, lastPath) {
  let compiled;
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    if (!Compiler) throw new Error('InkJS Compiler missing');
    compiled = new Compiler(content).Compile();
  } catch (err) {
    return {
      story: filePath,
      pass: false,
      steps: 0,
      path: [],
      error: `Parse/compile error: ${err.message}`,
      rotationOpportunity: false,
      exhausted: false,
    };
  }

  const story = new Story(compiled.ToJson());
  const seed = opts.seed != null ? hashSeed(opts.seed) : null;
  const rng = seed != null ? mulberry32(seed) : null;

  const choicePath = [];
  let steps = 0;
  let error = null;
  let rotationOpportunity = false;
  let exhausted = false;

  try {
    while (story.canContinue && steps < opts.maxSteps) {
      story.Continue();
      steps += 1;
    }

    while (story.currentChoices.length && steps < opts.maxSteps) {
      if (story.currentChoices.length > 1) rotationOpportunity = true;
      const idx = chooseIndex(story.currentChoices, rng, choicePath.length, lastPath);
      if (idx == null) {
        exhausted = true;
        break;
      }
      choicePath.push(idx);
      story.ChooseChoiceIndex(idx);
      steps += 1;
      while (story.canContinue && steps < opts.maxSteps) {
        story.Continue();
        steps += 1;
      }
    }
  } catch (err) {
    error = `Runtime error: ${err.message}`;
  }

  const pass = !error && !story.currentChoices.length && !story.canContinue && steps <= opts.maxSteps;

  return {
    story: filePath,
    pass,
    steps,
    path: choicePath,
    error: error || undefined,
    rotationOpportunity,
    exhausted,
  };
}

function runStoryWithRotation(filePath, opts, lastPath) {
  const maxRetries = Math.max(1, opts.maxRetries || DEFAULT_MAX_RETRIES);
  // When state is disabled, seeded runs remain deterministic and ignore previous paths.
  const rotationBaseline = opts.seed != null && opts.useState === false ? null : lastPath;

  for (let attempt = 0; attempt < maxRetries; attempt += 1) {
    const result = runStoryOnce(filePath, opts, rotationBaseline);

    if (result.error) return result;
    if (result.exhausted) {
      return {
        ...result,
        pass: false,
        error: `No alternative choices available for story ${filePath}`,
      };
    }

    if (!rotationBaseline || !arraysEqual(result.path, rotationBaseline)) {
      return result;
    }

    // No change and no rotation opportunity means all alternatives are exhausted.
    if (!result.rotationOpportunity) {
      return {
        ...result,
        pass: false,
        error: `No alternative path available for story ${filePath} (max retries reached)`,
      };
    }
  }

  return {
    story: filePath,
    pass: false,
    steps: 0,
    path: rotationBaseline || [],
    error: `Failed to find alternate path for story ${filePath} after ${opts.maxRetries} retries`,
  };
}

function outputResults(results, output) {
  const json = JSON.stringify(results, null, 2);
  if (output === 'stdout' || output === 'json' || !output) {
    console.log(json);
    return;
  }
  const outPath = path.resolve(output);
  // Ensure parent directory exists before writing to avoid ENOENT
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, json, 'utf8');
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log(usage());
    return;
  }

  const files = resolveStories(args.story);
  if (!files.length) {
    console.error(`No stories found for pattern: ${args.story}`);
    process.exitCode = 1;
    return;
  }

  const useState = args.stateEnabled;
  const stateFile = useState && (args.stateFile || DEFAULT_STATE_FILE)
    ? path.resolve(args.stateFile || DEFAULT_STATE_FILE)
    : null;
  const state = useState ? readStateFile(stateFile) : {};
  let stateChanged = false;

  if (useState && args.clearState) {
    files.forEach((file) => {
      if (state[file]) {
        delete state[file];
        stateChanged = true;
      }
    });
  }

  const results = files.map((file) => {
    const prev = useState ? state[file] : undefined;
    const result = runStoryWithRotation(file, {
      seed: args.seed,
      maxSteps: args.maxSteps,
      maxRetries: args.maxRetries,
      useState,
    }, prev?.lastPath);

    if (useState) {
      const runCount = prev?.runCount ? prev.runCount + 1 : 1;
      const lastPath = result.path;
      state[file] = {
        lastPath,
        lastRunAt: new Date().toISOString(),
        runCount,
      };
      stateChanged = true;
    }

    return result;
  });

  if (useState && stateChanged) writeStateFile(stateFile, state);

  outputResults(results, args.output);

  const allPass = results.length > 0 && results.every((r) => r.pass);
  if (!allPass) {
    process.exitCode = 1;
  }
}

main();

#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const inkjs = require('inkjs/full');

const DEFAULT_MAX_STEPS = 2000;

function usage() {
  return `Usage: node scripts/replay.js --story <path> --script <path> [--max-steps <n>] [--result-out <path>]\n\n` +
    `Runs an Ink story to completion using a scripted choice sequence.\n\n` +
    `Arguments:\n` +
    `  --story <path>       Path to .ink story file\n` +
    `  --script <path>      Path to JSON array of choices (indices or IDs)\n` +
    `  --max-steps <n>      Safety ceiling on total steps (default ${DEFAULT_MAX_STEPS})\n` +
    `  --result-out <path>  Optional path to write JSON result file (created parent dirs)\n` +
    `  --help               Show this message\n\n` +
    `Script format: JSON array. Each entry may be:\n` +
    `  - number: zero-based choice index\n` +
    `  - string: substring match against available choice text\n` +
    `Example: [0, 0, 0, 0]\n`;
}

function parseArgs(argv) {
  const args = { story: null, script: null, maxSteps: DEFAULT_MAX_STEPS, resultOut: null };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    switch (arg) {
      case '--story':
        args.story = argv[++i];
        break;
      case '--script':
        args.script = argv[++i];
        break;
      case '--max-steps':
        args.maxSteps = parseInt(argv[++i], 10) || DEFAULT_MAX_STEPS;
        break;
      case '--result-out':
        args.resultOut = argv[++i];
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

function loadStory(storyPath) {
  const abs = path.resolve(storyPath);
  if (!fs.existsSync(abs)) {
    throw new Error(`Story not found: ${abs}`);
  }
  const content = fs.readFileSync(abs, 'utf8');
  // If the story file contains compiled JSON (e.g. .ink.json), accept it directly.
  try {
    const parsed = JSON.parse(content);
    // Pass a JSON string to inkjs.Story (it accepts a JSON string of the compiled story).
    return new inkjs.Story(JSON.stringify(parsed));
  } catch (e) {
    // Not JSON, fall through to compile raw .ink source
  }
  if (!inkjs.Compiler) {
    throw new Error('InkJS Compiler missing (expected inkjs/full)');
  }
  const compiled = new inkjs.Compiler(content).Compile();
  return new inkjs.Story(compiled.ToJson());
}

function loadScript(scriptPath) {
  const abs = path.resolve(scriptPath);
  if (!fs.existsSync(abs)) {
    throw new Error(`Script not found: ${abs}`);
  }
  const raw = fs.readFileSync(abs, 'utf8');
  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    throw new Error(`Invalid JSON in script ${abs}: ${err.message}`);
  }
  if (!Array.isArray(parsed)) {
    throw new Error(`Script must be a JSON array. Got: ${typeof parsed}`);
  }
  return parsed;
}

function findChoiceIndex(choiceSpec, choices) {
  if (!choices || !choices.length) return { ok: false, error: 'No choices available' };

  if (typeof choiceSpec === 'number') {
    if (choiceSpec < 0 || choiceSpec >= choices.length) {
      return { ok: false, error: `Invalid choice index ${choiceSpec}; available: 0-${choices.length - 1}` };
    }
    return { ok: true, index: choiceSpec };
  }

  if (typeof choiceSpec === 'string') {
    const needle = choiceSpec.toLowerCase();
    const matchIdx = choices.findIndex((c) => (c.text || '').toLowerCase().includes(needle));
    if (matchIdx === -1) {
      return { ok: false, error: `Choice text containing "${choiceSpec}" not found among ${choices.length} choices` };
    }
    return { ok: true, index: matchIdx };
  }

  return { ok: false, error: `Unsupported choice spec type: ${typeof choiceSpec}` };
}

function runReplay({ storyPath, scriptPath, maxSteps = DEFAULT_MAX_STEPS }) {
  const story = loadStory(storyPath);
  const script = loadScript(scriptPath);

  let steps = 0;
  const pathTaken = [];
  let error = null;

  try {
    while (story.canContinue && steps < maxSteps) {
      story.Continue();
      steps += 1;
    }

    for (let i = 0; i < script.length; i += 1) {
      const choiceSpec = script[i];
      const currentChoices = story.currentChoices || [];
      if (!currentChoices.length) {
        error = `Script expects more choices, but story has none at step ${i}`;
        break;
      }
      const res = findChoiceIndex(choiceSpec, currentChoices);
      if (!res.ok) {
        error = res.error;
        break;
      }
      pathTaken.push(res.index);
      story.ChooseChoiceIndex(res.index);
      steps += 1;
      while (story.canContinue && steps < maxSteps) {
        story.Continue();
        steps += 1;
      }
    }

    // If script ended but story still has choices, consider failure.
    if (!error && story.currentChoices && story.currentChoices.length) {
      error = 'Script ended before story completion (choices remain)';
    }

    if (!error && (story.canContinue || (story.currentChoices && story.currentChoices.length))) {
      error = 'Story did not reach END within provided script';
    }

    if (!error && steps >= maxSteps) {
      error = `Reached max steps (${maxSteps}) before completion`;
    }
  } catch (err) {
    error = err.message;
  }

  const pass = !error;
  return {
    story: path.resolve(storyPath),
    pass,
    steps,
    path: pathTaken,
    error: pass ? undefined : error,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.story || !args.script) {
    console.log(usage());
    if (!args.story || !args.script) process.exitCode = 1;
    return;
  }

  try {
    const result = runReplay({ storyPath: args.story, scriptPath: args.script, maxSteps: args.maxSteps });

    // If a result-out path was provided, write the JSON result there (create parent dirs)
    if (args.resultOut) {
      try {
        const outPath = path.resolve(args.resultOut);
        const dir = path.dirname(outPath);
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(outPath, JSON.stringify(result, null, 2), 'utf8');
      } catch (werr) {
        console.error(`Failed to write result-out file: ${werr.message}`);
      }
    }

    console.log(JSON.stringify(result, null, 2));
    if (!result.pass) process.exitCode = 1;
  } catch (err) {
    const failure = { pass: false, error: err.message };
    console.error(JSON.stringify(failure));
    if (args.resultOut) {
      try {
        const outPath = path.resolve(args.resultOut);
        const dir = path.dirname(outPath);
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(outPath, JSON.stringify(failure, null, 2), 'utf8');
      } catch (werr) {
        console.error(`Failed to write result-out file: ${werr.message}`);
      }
    }
    process.exitCode = 1;
  }
}

if (require.main === module) {
  main();
}

module.exports = { runReplay };

#!/usr/bin/env node
const { spawn } = require("child_process");

const argv = process.argv.slice(2);
const subreddit = argv[0] || "";

if (!subreddit) {
  process.stderr.write("Missing required subreddit argument.\n");
  process.stdout.write(JSON.stringify({ ok: false, error: "missing_subreddit" }));
  process.exit(1);
}

const args = ["logs", subreddit];
let remaining = argv.slice(1);

if (remaining[0] && !remaining[0].startsWith("--")) {
  args.push(remaining[0]);
  remaining = remaining.slice(1);
}

if (remaining.length > 0) {
  args.push(...remaining);
}

process.stderr.write(
  `Streaming devvit logs for ${subreddit} (auto-exit after 5s)...\n`
);

const child = spawn("devvit", args, { stdio: ["ignore", "pipe", "pipe"] });

let stdout = "";
let stderr = "";
let done = false;
let debounceTimer = null;

const hardTimeoutMs = 5000;
const debounceMs = 500;

const hardTimer = setTimeout(() => finish("timeout"), hardTimeoutMs);

function finish(reason) {
  if (done) return;
  done = true;
  clearTimeout(hardTimer);
  if (debounceTimer) clearTimeout(debounceTimer);

  if (!child.killed) {
    child.kill("SIGINT");
    setTimeout(() => {
      if (!child.killed) child.kill("SIGKILL");
    }, 500);
  }

  const result = {
    ok: true,
    reason,
    exitCode: child.exitCode ?? null,
    signal: child.signalCode ?? null,
    stdout: stdout.trimEnd(),
    stderr: stderr.trimEnd(),
  };

  process.stdout.write(JSON.stringify(result, null, 2));
}

child.stdout.on("data", (chunk) => {
  stdout += chunk.toString("utf8");
  if (!debounceTimer) {
    debounceTimer = setTimeout(() => finish("debounce"), debounceMs);
  }
});

child.stderr.on("data", (chunk) => {
  stderr += chunk.toString("utf8");
});

child.on("error", (err) => {
  if (done) return;
  done = true;
  clearTimeout(hardTimer);
  if (debounceTimer) clearTimeout(debounceTimer);
  process.stdout.write(
    JSON.stringify(
      {
        ok: false,
        error: err.code === "ENOENT" ? "devvit_not_found" : err.message,
      },
      null,
      2
    )
  );
});

child.on("exit", () => {
  if (!done) finish("exit");
});

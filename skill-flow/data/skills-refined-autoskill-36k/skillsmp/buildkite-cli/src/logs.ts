#!/usr/bin/env tsx
/**
 * Get job logs (defaults to first failed job, or specify job index)
 * Usage: pnpm logs <url> [--job <index|name>] [--tail <lines>]
 */
import { getBuildRefFromArgs, apiFetch, parseArgs } from "./api.js";

interface Job {
  id: string;
  name: string;
  state: string;
  type: string;
}

const ref = await getBuildRefFromArgs();
const { flags } = parseArgs(process.argv.slice(2));

const build = await apiFetch<{ jobs: Job[] }>(
  `/organizations/${ref.org}/pipelines/${ref.pipeline}/builds/${ref.number}`
);

const jobs = build.jobs.filter((j) => j.type === "script");

let targetJob: Job | undefined;

if (flags.job) {
  const jobArg = flags.job as string;
  // Try by index first
  const idx = parseInt(jobArg, 10);
  if (!isNaN(idx) && idx >= 0 && idx < jobs.length) {
    targetJob = jobs[idx];
  } else {
    // Try by name match
    targetJob = jobs.find((j) => j.name.toLowerCase().includes(jobArg.toLowerCase()));
  }
} else {
  // Default: first failed job
  targetJob = jobs.find((j) => j.state === "failed" || j.state === "timed_out");
  if (!targetJob) {
    // Or last finished job
    targetJob = [...jobs].reverse().find((j) => j.state !== "scheduled");
  }
}

if (!targetJob) {
  console.error("❌ No matching job found");
  console.log("\nAvailable jobs:");
  jobs.forEach((j, i) => console.log(`  [${i}] ${j.state.padEnd(10)} ${j.name}`));
  process.exit(1);
}

console.log(`📜 Logs for: ${targetJob.name}\n`);

const log = await apiFetch<{ content: string }>(
  `/organizations/${ref.org}/pipelines/${ref.pipeline}/builds/${ref.number}/jobs/${targetJob.id}/log`
);

let content = log.content || "(no log content)";

// Tail if requested
const tail = parseInt(flags.tail as string, 10);
if (tail && !isNaN(tail)) {
  const lines = content.split("\n");
  content = lines.slice(-tail).join("\n");
}

console.log(content);

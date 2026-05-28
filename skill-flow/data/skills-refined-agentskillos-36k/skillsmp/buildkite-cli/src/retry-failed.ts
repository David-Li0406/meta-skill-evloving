#!/usr/bin/env tsx
/**
 * Retry failed jobs in a build
 * Usage: pnpm retry-failed <url> [--all]
 */
import { getBuildRefFromArgs, apiFetch, parseArgs, stateColors, reset } from "./api.js";

interface Job {
  id: string;
  name: string;
  state: string;
  type: string;
}

const ref = await getBuildRefFromArgs();
const { flags } = parseArgs(process.argv.slice(2));

console.log(`🔍 Fetching jobs for ${ref.org}/${ref.pipeline} #${ref.number}...`);

const build = await apiFetch<{ jobs: Job[] }>(
  `/organizations/${ref.org}/pipelines/${ref.pipeline}/builds/${ref.number}`
);

const failedJobs = build.jobs.filter(
  (j) => j.type === "script" && (j.state === "failed" || j.state === "timed_out")
);

if (!failedJobs.length) {
  console.log("✅ No failed jobs to retry");
  process.exit(0);
}

console.log(`\n📋 Failed jobs (${failedJobs.length}):`);
failedJobs.forEach((j) => {
  const color = stateColors[j.state] || "";
  console.log(`  ${color}${j.state}${reset} ${j.name}`);
});

console.log(`\n🔄 Retrying ${failedJobs.length} failed jobs...`);

for (const job of failedJobs) {
  try {
    await apiFetch(
      `/organizations/${ref.org}/pipelines/${ref.pipeline}/builds/${ref.number}/jobs/${job.id}/retry`,
      { method: "PUT" }
    );
    console.log(`  ✅ ${job.name}`);
  } catch (e: any) {
    console.log(`  ❌ ${job.name}: ${e.message}`);
  }
}

console.log("\n🔗 https://buildkite.com/" + `${ref.org}/${ref.pipeline}/builds/${ref.number}`);

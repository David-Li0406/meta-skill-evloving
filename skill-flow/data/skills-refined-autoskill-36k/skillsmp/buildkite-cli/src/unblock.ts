#!/usr/bin/env tsx
/**
 * Unblock a blocked build step
 * Usage: pnpm unblock <url> [--fields key=value,key2=value2]
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

const blockedJobs = build.jobs.filter(
  (j) => j.type === "manual" && j.state === "blocked"
);

if (!blockedJobs.length) {
  console.log("✅ No blocked jobs to unblock");
  process.exit(0);
}

// Parse fields if provided
const fieldsStr = flags.fields as string;
const fields: Record<string, string> = {};
if (fieldsStr) {
  for (const pair of fieldsStr.split(",")) {
    const [key, value] = pair.split("=");
    if (key && value) fields[key] = value;
  }
}

console.log(`🔓 Unblocking ${blockedJobs.length} blocked step(s)...`);

for (const job of blockedJobs) {
  try {
    await apiFetch(
      `/organizations/${ref.org}/pipelines/${ref.pipeline}/builds/${ref.number}/jobs/${job.id}/unblock`,
      {
        method: "PUT",
        body: JSON.stringify({ fields }),
      }
    );
    console.log(`  ✅ ${job.name}`);
  } catch (e: any) {
    console.log(`  ❌ ${job.name}: ${e.message}`);
  }
}

console.log(`\n🔗 https://buildkite.com/${ref.org}/${ref.pipeline}/builds/${ref.number}`);

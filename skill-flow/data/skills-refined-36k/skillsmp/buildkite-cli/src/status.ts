#!/usr/bin/env tsx
/**
 * Get build status with job details
 * Usage: pnpm status <url>
 */
import { getBuildRefFromArgs, apiFetch, stateColors, reset } from "./api.js";

interface Job {
  id: string;
  name: string;
  state: string;
  type: string;
  started_at: string | null;
  finished_at: string | null;
  exit_status: number | null;
}

interface Build {
  number: number;
  state: string;
  branch: string;
  commit: string;
  message: string;
  created_at: string;
  started_at: string | null;
  finished_at: string | null;
  web_url: string;
  jobs: Job[];
}

const ref = await getBuildRefFromArgs();

const build = await apiFetch<Build>(
  `/organizations/${ref.org}/pipelines/${ref.pipeline}/builds/${ref.number}`
);

const color = stateColors[build.state] || "";
const duration = build.finished_at && build.started_at
  ? Math.round((new Date(build.finished_at).getTime() - new Date(build.started_at).getTime()) / 1000)
  : null;

console.log(`
${color}■${reset} Build #${build.number} - ${color}${build.state.toUpperCase()}${reset}
  Branch: ${build.branch}
  Commit: ${build.commit.slice(0, 7)}
  Message: ${build.message.split("\n")[0].slice(0, 60)}
  ${duration ? `Duration: ${Math.floor(duration / 60)}m ${duration % 60}s` : ""}
`);

const jobs = build.jobs.filter((j) => j.type === "script");
if (jobs.length) {
  console.log("Jobs:");
  for (const job of jobs) {
    const jColor = stateColors[job.state] || "";
    const exit = job.exit_status !== null ? ` (exit ${job.exit_status})` : "";
    console.log(`  ${jColor}●${reset} ${job.state.padEnd(10)} ${job.name}${exit}`);
  }
}

console.log(`\n🔗 ${build.web_url}`);

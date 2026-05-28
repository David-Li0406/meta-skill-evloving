#!/usr/bin/env tsx
/**
 * List recent failed builds for a pipeline
 * Usage: pnpm list-failed [--pipeline name] [--limit n]
 */
import { apiFetch, parseArgs, stateColors, reset, DEFAULT_ORG } from "./api.js";

interface Build {
  number: number;
  state: string;
  branch: string;
  message: string;
  web_url: string;
  created_at: string;
}

const { flags } = parseArgs(process.argv.slice(2));

const org = DEFAULT_ORG || (flags.org as string);
const pipeline = (flags.pipeline as string) || process.env.BUILDKITE_PIPELINE;
const limit = parseInt(flags.limit as string, 10) || 10;

if (!org || !pipeline) {
  console.error("Usage: pnpm list-failed --pipeline <name> [--org <org>] [--limit <n>]");
  console.error("Or set BUILDKITE_ORG and BUILDKITE_PIPELINE env vars");
  process.exit(1);
}

console.log(`🔍 Recent failed builds for ${org}/${pipeline}...\n`);

const builds = await apiFetch<Build[]>(
  `/organizations/${org}/pipelines/${pipeline}/builds?state=failed&per_page=${limit}`
);

if (!builds.length) {
  console.log("✅ No recent failed builds!");
  process.exit(0);
}

for (const build of builds) {
  const date = new Date(build.created_at).toLocaleDateString();
  const msg = build.message.split("\n")[0].slice(0, 50);
  console.log(
    `${stateColors.failed}#${build.number}${reset} ${build.branch.padEnd(20)} ${date} ${msg}`
  );
  console.log(`   🔗 ${build.web_url}\n`);
}

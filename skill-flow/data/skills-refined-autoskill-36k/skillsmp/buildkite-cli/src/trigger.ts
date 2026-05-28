#!/usr/bin/env tsx
/**
 * Trigger a new build
 * Usage: pnpm trigger --pipeline <n> [--branch <b>] [--commit <c>] [--message <m>]
 */
import { apiFetch, parseArgs, DEFAULT_ORG } from "./api.js";

const { flags } = parseArgs(process.argv.slice(2));

const org = DEFAULT_ORG || (flags.org as string);
const pipeline = (flags.pipeline as string) || process.env.BUILDKITE_PIPELINE;
const branch = (flags.branch as string) || "main";
const commit = (flags.commit as string) || "HEAD";
const message = (flags.message as string) || `Manual trigger via CLI`;

if (!org || !pipeline) {
  console.error("Usage: pnpm trigger --pipeline <n> [--branch <b>] [--commit <c>] [--message <m>]");
  console.error("Or set BUILDKITE_ORG and BUILDKITE_PIPELINE env vars");
  process.exit(1);
}

console.log(`🚀 Triggering build for ${org}/${pipeline}...`);
console.log(`   Branch: ${branch}`);
console.log(`   Commit: ${commit}`);

const result = await apiFetch<{ web_url: string; number: number }>(
  `/organizations/${org}/pipelines/${pipeline}/builds`,
  {
    method: "POST",
    body: JSON.stringify({ branch, commit, message }),
  }
);

console.log(`\n✅ Created build #${result.number}`);
console.log(`🔗 ${result.web_url}`);

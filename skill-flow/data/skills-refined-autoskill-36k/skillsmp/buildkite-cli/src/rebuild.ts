#!/usr/bin/env tsx
/**
 * Rebuild a Buildkite build
 * Usage: pnpm rebuild <url>
 */
import { getBuildRefFromArgs, apiFetch } from "./api.js";

const ref = await getBuildRefFromArgs();

console.log(`🔄 Rebuilding ${ref.org}/${ref.pipeline} #${ref.number}...`);

const result = await apiFetch<{ web_url: string; number: number }>(
  `/organizations/${ref.org}/pipelines/${ref.pipeline}/builds/${ref.number}/rebuild`,
  { method: "PUT" }
);

console.log(`✅ Triggered build #${result.number}`);
console.log(`🔗 ${result.web_url}`);

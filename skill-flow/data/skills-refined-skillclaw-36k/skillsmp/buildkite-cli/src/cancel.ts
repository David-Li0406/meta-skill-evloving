#!/usr/bin/env tsx
/**
 * Cancel a running build
 * Usage: pnpm cancel <url>
 */
import { getBuildRefFromArgs, apiFetch } from "./api.js";

const ref = await getBuildRefFromArgs();

console.log(`⏹️  Canceling ${ref.org}/${ref.pipeline} #${ref.number}...`);

await apiFetch(
  `/organizations/${ref.org}/pipelines/${ref.pipeline}/builds/${ref.number}/cancel`,
  { method: "PUT" }
);

console.log("✅ Build canceled");

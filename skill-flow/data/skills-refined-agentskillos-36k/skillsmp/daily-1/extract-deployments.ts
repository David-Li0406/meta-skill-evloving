#!/usr/bin/env bun
/**
 * Extract deployment URLs from wrangler.jsonc files
 * Usage: bun extract-deployments.ts <repo-path> [repo-path...]
 *        bun extract-deployments.ts --from-repos repo1,repo2,repo3
 *
 * Output: Markdown table of deployments
 */

import { existsSync } from "fs";
import { join, basename, dirname } from "path";

interface WranglerRoute {
  pattern: string;
  custom_domain?: boolean;
}

interface WranglerEnv {
  routes?: WranglerRoute[];
}

interface WranglerConfig {
  name?: string;
  routes?: WranglerRoute[];
  env?: Record<string, WranglerEnv>;
}

interface Deployment {
  repo: string;
  name: string;
  staging?: string;
  production?: string;
  other?: string;
}

function extractDomain(routes?: WranglerRoute[]): string | undefined {
  if (!routes || routes.length === 0) return undefined;
  const customDomain = routes.find((r) => r.custom_domain);
  if (customDomain) return `https://${customDomain.pattern}`;
  // Fall back to first route pattern
  return routes[0]?.pattern;
}

async function extractDeployments(repoPath: string): Promise<Deployment | null> {
  const wranglerPath = join(repoPath, "wrangler.jsonc");
  const wranglerJsonPath = join(repoPath, "wrangler.json");

  let configPath: string | null = null;
  if (existsSync(wranglerPath)) {
    configPath = wranglerPath;
  } else if (existsSync(wranglerJsonPath)) {
    configPath = wranglerJsonPath;
  }

  if (!configPath) return null;

  try {
    // Bun can import JSONC files directly
    const config: WranglerConfig = await import(configPath);

    // Get repo name from path (org/repo format)
    const parts = repoPath.split("/");
    const repo = parts.slice(-2).join("/");

    const deployment: Deployment = {
      repo,
      name: config.name || basename(repoPath),
    };

    // Check for staging/production environments
    if (config.env?.staging) {
      deployment.staging = extractDomain(config.env.staging.routes);
    }
    if (config.env?.production) {
      deployment.production = extractDomain(config.env.production.routes);
    }

    // Check top-level routes (often used as default/production)
    const topLevel = extractDomain(config.routes);
    if (topLevel) {
      // If no production env but has top-level, use as production
      if (!deployment.production && !deployment.staging) {
        deployment.production = topLevel;
      } else if (!deployment.production) {
        deployment.other = topLevel;
      }
    }

    // Only return if we found at least one URL
    if (deployment.staging || deployment.production || deployment.other) {
      return deployment;
    }
    return null;
  } catch (e) {
    console.error(`Error parsing ${configPath}:`, e);
    return null;
  }
}

function formatMarkdownTable(deployments: Deployment[]): string {
  if (deployments.length === 0) return "";

  const lines: string[] = [
    "## Deployments",
    "",
    "| Project | Staging | Production |",
    "|---------|---------|------------|",
  ];

  for (const d of deployments) {
    const staging = d.staging ? `[${new URL(d.staging).hostname}](${d.staging})` : "-";
    const production = d.production
      ? `[${new URL(d.production).hostname}](${d.production})`
      : d.other
        ? `[${new URL(d.other).hostname}](${d.other})`
        : "-";
    lines.push(`| ${d.name} | ${staging} | ${production} |`);
  }

  return lines.join("\n");
}

// Main
const args = process.argv.slice(2);
let repoPaths: string[] = [];

if (args[0] === "--from-repos") {
  // Comma-separated list of org/repo names, resolved from ~/dev
  const devDir = join(process.env.HOME || "", "dev");
  repoPaths = args[1].split(",").map((r) => join(devDir, r.trim()));
} else if (args[0] === "--help" || args.length === 0) {
  console.log(`Usage:
  bun extract-deployments.ts <repo-path> [repo-path...]
  bun extract-deployments.ts --from-repos org/repo1,org/repo2

Output: Markdown table of deployment URLs extracted from wrangler.jsonc files`);
  process.exit(0);
} else {
  repoPaths = args;
}

const deployments: Deployment[] = [];

for (const repoPath of repoPaths) {
  const deployment = await extractDeployments(repoPath);
  if (deployment) {
    deployments.push(deployment);
  }
}

console.log(formatMarkdownTable(deployments));

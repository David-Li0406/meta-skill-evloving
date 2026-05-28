/**
 * Buildkite CLI Core - URL parsing and API helpers
 */

export interface BuildRef {
  org: string;
  pipeline: string;
  number: number;
}

export interface JobRef extends BuildRef {
  jobId: string;
}

const BUILDKITE_TOKEN = process.env.BUILDKITE_TOKEN;
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;

if (!BUILDKITE_TOKEN) {
  console.error("❌ BUILDKITE_TOKEN env var required");
  process.exit(1);
}

// Default org - set in env or override per-call
export const DEFAULT_ORG = process.env.BUILDKITE_ORG || "";

/**
 * Parse Buildkite build URL
 * Formats:
 *   https://buildkite.com/org/pipeline/builds/123
 *   https://buildkite.com/org/pipeline/builds/123#job-uuid
 */
export function parseBuildkiteUrl(url: string): BuildRef | null {
  const match = url.match(
    /buildkite\.com\/([^\/]+)\/([^\/]+)\/builds\/(\d+)/
  );
  if (!match) return null;
  return {
    org: match[1],
    pipeline: match[2],
    number: parseInt(match[3], 10),
  };
}

/**
 * Parse GitHub PR URL and find corresponding Buildkite build
 * Format: https://github.com/owner/repo/pull/123
 */
export function parseGithubPrUrl(url: string): { owner: string; repo: string; pr: number } | null {
  const match = url.match(/github\.com\/([^\/]+)\/([^\/]+)\/pull\/(\d+)/);
  if (!match) return null;
  return {
    owner: match[1],
    repo: match[2],
    pr: parseInt(match[3], 10),
  };
}

/**
 * Get PR head SHA from GitHub
 */
export async function getGithubPrHead(owner: string, repo: string, pr: number): Promise<string> {
  const headers: Record<string, string> = {
    Accept: "application/vnd.github.v3+json",
    "User-Agent": "buildkite-cli",
  };
  if (GITHUB_TOKEN) {
    headers.Authorization = `token ${GITHUB_TOKEN}`;
  }

  const res = await fetch(
    `https://api.github.com/repos/${owner}/${repo}/pulls/${pr}`,
    { headers }
  );
  if (!res.ok) throw new Error(`GitHub API error: ${res.status}`);
  const data = await res.json();
  return data.head.sha;
}

/**
 * Find Buildkite build by commit SHA
 */
export async function findBuildByCommit(
  org: string,
  pipeline: string,
  commit: string
): Promise<BuildRef | null> {
  const builds = await apiFetch<any[]>(
    `/organizations/${org}/pipelines/${pipeline}/builds?commit=${commit}&per_page=1`
  );
  if (!builds.length) return null;
  return { org, pipeline, number: builds[0].number };
}

/**
 * Parse any URL (Buildkite or GitHub PR) to BuildRef
 */
export async function parseAnyUrl(url: string, pipeline?: string): Promise<BuildRef | null> {
  // Try Buildkite URL first
  const bk = parseBuildkiteUrl(url);
  if (bk) return bk;

  // Try GitHub PR URL
  const gh = parseGithubPrUrl(url);
  if (gh) {
    if (!pipeline) {
      console.error("❌ Pipeline required for GitHub PR URLs. Use --pipeline or set BUILDKITE_PIPELINE");
      return null;
    }
    const org = DEFAULT_ORG;
    if (!org) {
      console.error("❌ Org required. Set BUILDKITE_ORG env var");
      return null;
    }
    const sha = await getGithubPrHead(gh.owner, gh.repo, gh.pr);
    console.log(`📍 PR #${gh.pr} → commit ${sha.slice(0, 7)}`);
    const build = await findBuildByCommit(org, pipeline, sha);
    if (!build) {
      console.error(`❌ No build found for commit ${sha.slice(0, 7)}`);
      return null;
    }
    console.log(`📍 Found build #${build.number}`);
    return build;
  }

  return null;
}

/**
 * REST API fetch helper
 */
export async function apiFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `https://api.buildkite.com/v2${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      Authorization: `Bearer ${BUILDKITE_TOKEN}`,
      "Content-Type": "application/json",
      ...options.headers,
    },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json();
}

/**
 * GraphQL query helper
 */
export async function graphql<T>(query: string, variables: Record<string, any> = {}): Promise<T> {
  const res = await fetch("https://graphql.buildkite.com/v1", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${BUILDKITE_TOKEN}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, variables }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`GraphQL error ${res.status}: ${text}`);
  }
  const data = await res.json();
  if (data.errors) {
    throw new Error(`GraphQL errors: ${JSON.stringify(data.errors)}`);
  }
  return data.data;
}

/**
 * Parse CLI args into simple key-value pairs
 */
export function parseArgs(args: string[]): { positional: string[]; flags: Record<string, string | boolean> } {
  const positional: string[] = [];
  const flags: Record<string, string | boolean> = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith("--")) {
        flags[key] = next;
        i++;
      } else {
        flags[key] = true;
      }
    } else if (arg.startsWith("-")) {
      flags[arg.slice(1)] = true;
    } else {
      positional.push(arg);
    }
  }

  return { positional, flags };
}

/**
 * Get BuildRef from CLI args (URL as first positional arg)
 */
export async function getBuildRefFromArgs(): Promise<BuildRef> {
  const { positional, flags } = parseArgs(process.argv.slice(2));
  const url = positional[0];

  if (!url) {
    console.error("Usage: pnpm <script> <buildkite-url|github-pr-url> [--pipeline name]");
    process.exit(1);
  }

  const pipeline = flags.pipeline as string || process.env.BUILDKITE_PIPELINE;
  const ref = await parseAnyUrl(url, pipeline);

  if (!ref) {
    console.error("❌ Could not parse URL:", url);
    process.exit(1);
  }

  return ref;
}

// Build state colors
export const stateColors: Record<string, string> = {
  passed: "\x1b[32m", // green
  failed: "\x1b[31m", // red
  canceled: "\x1b[33m", // yellow
  running: "\x1b[36m", // cyan
  scheduled: "\x1b[90m", // gray
  blocked: "\x1b[35m", // magenta
};
export const reset = "\x1b[0m";

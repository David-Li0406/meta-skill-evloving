import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

function run(cmd, args, opts = {}) {
  try {
    return execFileSync(cmd, args, {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
      ...opts,
    }).trim();
  } catch (err) {
    const stderr = err?.stderr?.toString?.() ?? "";
    const msg = [
      `Command failed: ${cmd} ${args.join(" ")}`,
      stderr ? `\n${stderr.trim()}` : "",
    ].join("");
    const e = new Error(msg);
    e.cause = err;
    throw e;
  }
}

function readStdinIfPresent() {
  try {
    if (process.stdin.isTTY) return null;
  } catch {
    return null;
  }
  const chunks = [];
  return new Promise((resolve, reject) => {
    process.stdin.on("data", (c) => chunks.push(c));
    process.stdin.on("end", () => resolve(Buffer.concat(chunks).toString("utf8").trim() || null));
    process.stdin.on("error", reject);
  });
}

function parseArgs(argv) {
  const out = {
    owner: null,
    repo: null,
    pr: null,
    maxPages: 50,
  };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--owner") out.owner = argv[++i];
    else if (a === "--repo") out.repo = argv[++i];
    else if (a === "--pr" || a === "--pull" || a === "-p") out.pr = Number(argv[++i]);
    else if (a === "--max-pages") out.maxPages = Number(argv[++i]);
    else if (a === "--help" || a === "-h") out.help = true;
    else throw new Error(`Unknown arg: ${a}`);
  }
  return out;
}

function printHelp() {
  process.stderr.write(
    [
      "fetch-review-threads.mjs",
      "",
      "Usage:",
      "  node scripts/fetch-review-threads.mjs [--owner <owner> --repo <repo> --pr <number>] [--max-pages <n>]",
      "",
      "Input:",
      "  - Optionally accepts JSON on stdin from discover-pr.mjs: { owner, repo, pullNumber }",
      "",
      "Output:",
      "  - Raw GraphQL pages wrapped as:",
      '    { "owner": "...", "repo": "...", "pullNumber": 123, "pages": [ <graphql-response>, ... ] }',
      "",
    ].join("\n")
  );
}

function getSkillRoot() {
  const __filename = fileURLToPath(import.meta.url);
  return path.resolve(path.dirname(__filename), "..");
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help) {
    printHelp();
    process.exit(0);
  }

  const stdin = await readStdinIfPresent();
  let input = null;
  if (stdin) {
    try {
      input = JSON.parse(stdin);
    } catch {
      throw new Error("Failed to parse stdin JSON. Expected output from discover-pr.mjs.");
    }
  }

  const owner = args.owner ?? input?.owner;
  const repo = args.repo ?? input?.repo;
  const pullNumber = args.pr ?? input?.pullNumber ?? input?.number;

  if (!owner || !repo || !Number.isInteger(pullNumber) || pullNumber <= 0) {
    throw new Error("Missing owner/repo/pr. Provide flags or pipe discover-pr.mjs output into this script.");
  }

  const skillRoot = getSkillRoot();
  const queryPath = path.join(skillRoot, "assets", "graphql", "pull_request_review_threads.gql");
  const query = readFileSync(queryPath, "utf8");

  const pages = [];
  let after = null;
  for (let page = 1; page <= args.maxPages; page++) {
    const ghArgs = [
      "api",
      "graphql",
      "-f",
      `query=${query}`,
      "-f",
      `owner=${owner}`,
      "-f",
      `repo=${repo}`,
      "-F",
      `number=${pullNumber}`,
    ];
    if (after === null) {
      ghArgs.push("-F", "after=null");
    } else {
      ghArgs.push("-f", `after=${after}`);
    }

    const raw = run("gh", ghArgs);
    const resp = JSON.parse(raw);
    pages.push(resp);

    const info =
      resp?.data?.repository?.pullRequest?.reviewThreads?.pageInfo ?? null;
    if (!info?.hasNextPage) break;
    if (!info?.endCursor) break;
    after = info.endCursor;
  }

  process.stdout.write(JSON.stringify({ owner, repo, pullNumber, pages }, null, 2));
}

main().catch((err) => {
  process.stderr.write(`${err?.message ?? String(err)}\n`);
  process.exit(1);
});

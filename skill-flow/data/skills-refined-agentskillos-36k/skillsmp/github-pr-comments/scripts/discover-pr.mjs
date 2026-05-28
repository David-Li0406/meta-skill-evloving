import { execFileSync } from "node:child_process";

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

function parseOwnerRepo(remoteUrl) {
  // Supports:
  // - https://github.com/OWNER/REPO.git
  // - https://github.com/OWNER/REPO
  // - git@github.com:OWNER/REPO.git
  // - ssh://git@github.com/OWNER/REPO.git
  const u = remoteUrl.trim();

  const https = u.match(/github\.com\/([^/]+)\/([^/.]+)(?:\.git)?$/i);
  if (https) return { owner: https[1], repo: https[2] };

  const ssh1 = u.match(/git@github\.com:([^/]+)\/([^/.]+)(?:\.git)?$/i);
  if (ssh1) return { owner: ssh1[1], repo: ssh1[2] };

  const ssh2 = u.match(/github\.com\/([^/]+)\/([^/.]+)(?:\.git)?$/i);
  if (ssh2) return { owner: ssh2[1], repo: ssh2[2] };

  throw new Error(`Unable to parse GitHub owner/repo from origin URL: ${remoteUrl}`);
}

function parseArgs(argv) {
  const out = { pr: null };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--pr" || a === "--pull" || a === "-p") {
      const v = argv[i + 1];
      if (!v) throw new Error("Missing value for --pr");
      out.pr = Number(v);
      if (!Number.isInteger(out.pr) || out.pr <= 0) {
        throw new Error(`Invalid --pr value: ${v}`);
      }
      i++;
      continue;
    }
    if (a === "--help" || a === "-h") {
      out.help = true;
      continue;
    }
    throw new Error(`Unknown arg: ${a}`);
  }
  return out;
}

function printHelp() {
  // Keep output stable: scripts chain by parsing stdout JSON.
  process.stderr.write(
    [
      "discover-pr.mjs",
      "",
      "Usage:",
      "  node scripts/discover-pr.mjs [--pr <number>]",
      "",
      "Outputs JSON:",
      '  { "owner": "...", "repo": "...", "pullNumber": 123, "headRefName": "branch-name", "url": "..." }',
      "",
    ].join("\n")
  );
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help) {
    printHelp();
    process.exit(0);
  }

  const branch = run("git", ["branch", "--show-current"]);
  const origin = run("git", ["remote", "get-url", "origin"]);
  const { owner, repo } = parseOwnerRepo(origin);

  let pullNumber = args.pr;
  let headRefName = branch;
  let url = null;

  if (!pullNumber) {
    // Prefer gh pr view because it maps current branch -> PR quickly.
    // Fallback to gh pr list --head if pr view fails.
    try {
      const json = run("gh", ["pr", "view", "--json", "number,headRefName,url"]);
      const parsed = JSON.parse(json);
      pullNumber = parsed.number;
      headRefName = parsed.headRefName ?? branch;
      url = parsed.url ?? null;
    } catch {
      const json = run("gh", ["pr", "list", "--head", branch, "--json", "number,headRefName,url", "--limit", "1"]);
      const parsed = JSON.parse(json);
      if (!Array.isArray(parsed) || parsed.length === 0) {
        throw new Error(
          `Could not find an open PR for branch '${branch}'. Provide --pr <number> or ensure the PR exists and gh is authenticated.`
        );
      }
      pullNumber = parsed[0].number;
      headRefName = parsed[0].headRefName ?? branch;
      url = parsed[0].url ?? null;
    }
  }

  if (!Number.isInteger(pullNumber) || pullNumber <= 0) {
    throw new Error("Failed to determine pull request number. Provide --pr <number>.");
  }

  const out = { owner, repo, pullNumber, headRefName, url };
  process.stdout.write(JSON.stringify(out, null, 2));
}

main().catch((err) => {
  process.stderr.write(`${err?.message ?? String(err)}\n`);
  process.exit(1);
});

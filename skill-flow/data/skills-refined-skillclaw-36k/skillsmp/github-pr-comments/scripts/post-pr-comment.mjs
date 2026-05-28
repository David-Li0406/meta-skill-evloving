import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";

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

function parseArgs(argv) {
  const out = { pr: null, bodyFile: null, help: false };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--pr" || a === "--pull" || a === "-p") out.pr = Number(argv[++i]);
    else if (a === "--body-file" || a === "-F") out.bodyFile = argv[++i];
    else if (a === "--help" || a === "-h") out.help = true;
    else throw new Error(`Unknown arg: ${a}`);
  }
  return out;
}

function printHelp() {
  process.stderr.write(
    [
      "post-pr-comment.mjs",
      "",
      "Usage:",
      "  node scripts/post-pr-comment.mjs --pr <number> --body-file <path>",
      "",
      "Notes:",
      "  - Uses `gh pr comment` to post a top-level PR comment.",
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
  if (!Number.isInteger(args.pr) || args.pr <= 0) {
    throw new Error("Missing/invalid --pr <number>.");
  }
  if (!args.bodyFile) {
    throw new Error("Missing --body-file <path>.");
  }

  const body = readFileSync(args.bodyFile, "utf8");
  if (!body.trim()) throw new Error("Body file is empty.");

  // gh pr comment requires being in a repo (or GH_REPO env var set).
  run("gh", ["pr", "comment", String(args.pr), "--body-file", args.bodyFile]);
  process.stdout.write(`OK: posted comment to PR #${args.pr}\n`);
}

main().catch((err) => {
  process.stderr.write(`${err?.message ?? String(err)}\n`);
  process.exit(1);
});

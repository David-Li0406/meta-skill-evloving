import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

function readStdin() {
  const chunks = [];
  return new Promise((resolve, reject) => {
    process.stdin.on("data", (c) => chunks.push(c));
    process.stdin.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    process.stdin.on("error", reject);
  });
}

function parseArgs(argv) {
  const out = { template: null, help: false };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--template") out.template = argv[++i];
    else if (a === "--help" || a === "-h") out.help = true;
    else throw new Error(`Unknown arg: ${a}`);
  }
  return out;
}

function printHelp() {
  process.stderr.write(
    [
      "render-summary.mjs",
      "",
      "Usage:",
      "  node scripts/render-summary.mjs [--template <relative-path>] < normalized.json",
      "",
      "Default template:",
      "  assets/templates/review-comments-summary.md",
      "",
      "Output:",
      "  Markdown summary to stdout.",
      "",
    ].join("\n")
  );
}

function getSkillRoot() {
  const __filename = fileURLToPath(import.meta.url);
  return path.resolve(path.dirname(__filename), "..");
}

function escapeMd(s) {
  return String(s ?? "")
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n")
    .trim();
}

function splitByStatus(threads) {
  const unresolved = [];
  const outdated = [];
  const resolved = [];
  for (const t of threads ?? []) {
    const isResolved = Boolean(t.isResolved);
    const isOutdated = Boolean(t.isOutdated);
    if (!isResolved && !isOutdated) unresolved.push(t);
    else if (!isResolved && isOutdated) outdated.push(t);
    else resolved.push(t);
  }
  return { unresolved, outdated, resolved };
}

function renderList(items) {
  if (!items.length) return "_None_\n";
  return items
    .map((t) => {
      const loc = t.path
        ? `**File:** \`${escapeMd(t.path)}\`${t.line ? ` (Line ${t.line})` : ""}`
        : "**File:** _Unknown_";
      const author = t.author ? `@${escapeMd(t.author)}` : "_Unknown_";
      const body = t.body ? escapeMd(t.body) : "_No comment body_";
      const url = t.url ? escapeMd(t.url) : "_No link_";
      return [
        `- ${loc}`,
        `  - **Author:** ${author}`,
        `  - **Comment:** ${body}`,
        `  - **Link:** ${url}`,
      ].join("\n");
    })
    .join("\n\n") + "\n";
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help) {
    printHelp();
    process.exit(0);
  }

  const stdin = (await readStdin()).trim();
  if (!stdin) throw new Error("No input provided on stdin.");
  const input = JSON.parse(stdin);

  const { unresolved, outdated, resolved } = splitByStatus(input.threads);

  // We keep a simple renderer (no external deps). The template file exists mainly
  // as a reference/asset; this script outputs a stable summary format.
  const pullUrl = input.pullUrl ?? "(unknown)";

  const md = [
    "## PR Review Comments Summary",
    "",
    `PR: ${pullUrl}`,
    "",
    `### Unresolved Comments (${unresolved.length})`,
    "",
    renderList(unresolved),
    `### Unresolved but Outdated (${outdated.length})`,
    "",
    renderList(outdated),
    `### Resolved Comments (${resolved.length})`,
    "",
    renderList(resolved),
  ].join("\n");

  // If a template was requested, verify it exists so errors are clearer.
  if (args.template) {
    const skillRoot = getSkillRoot();
    const p = path.resolve(skillRoot, args.template);
    readFileSync(p, "utf8");
  } else {
    const skillRoot = getSkillRoot();
    const p = path.resolve(skillRoot, "assets/templates/review-comments-summary.md");
    readFileSync(p, "utf8");
  }

  process.stdout.write(md);
}

main().catch((err) => {
  process.stderr.write(`${err?.message ?? String(err)}\n`);
  process.exit(1);
});

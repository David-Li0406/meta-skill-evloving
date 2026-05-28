function readStdin() {
  const chunks = [];
  return new Promise((resolve, reject) => {
    process.stdin.on("data", (c) => chunks.push(c));
    process.stdin.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    process.stdin.on("error", reject);
  });
}

function parseArgs(argv) {
  const out = { help: false };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--help" || a === "-h") out.help = true;
    else throw new Error(`Unknown arg: ${a}`);
  }
  return out;
}

function printHelp() {
  process.stderr.write(
    [
      "normalize-threads.mjs",
      "",
      "Usage:",
      "  node scripts/normalize-threads.mjs < raw-pages.json",
      "",
      "Input:",
      '  { owner, repo, pullNumber, pages: [ { data: { repository: { pullRequest: { reviewThreads: { nodes: [...] }}}}} ] }',
      "",
      "Output:",
      '  { owner, repo, pullNumber, pullUrl, threads: [ { path, line, originalLine, isResolved, isOutdated, author, body, createdAt, url, diffHunk } ] }',
      "",
    ].join("\n")
  );
}

function flattenThreads(pages) {
  const all = [];
  for (const p of pages ?? []) {
    const nodes = p?.data?.repository?.pullRequest?.reviewThreads?.nodes ?? [];
    for (const n of nodes) all.push(n);
  }
  return all;
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help) {
    printHelp();
    process.exit(0);
  }

  const stdin = (await readStdin()).trim();
  if (!stdin) throw new Error("No input provided on stdin.");

  let input;
  try {
    input = JSON.parse(stdin);
  } catch {
    throw new Error("Failed to parse stdin JSON.");
  }

  const owner = input.owner;
  const repo = input.repo;
  const pullNumber = input.pullNumber;
  const pullUrl = input.pages?.[0]?.data?.repository?.pullRequest?.url ?? null;

  if (!owner || !repo || !Number.isInteger(pullNumber) || pullNumber <= 0) {
    throw new Error("Input missing owner/repo/pullNumber.");
  }

  const rawThreads = flattenThreads(input.pages);

  const threads = rawThreads.map((t) => {
    const comments = t?.comments?.nodes ?? [];
    // Prefer the most recent comment for the summary body, but keep diffHunk/path/line from thread.
    const last = comments.length ? comments[comments.length - 1] : null;
    const author = last?.author?.login ?? null;
    const body = last?.body ?? null;
    const url = last?.url ?? null;
    const createdAt = last?.createdAt ?? null;

    return {
      id: t?.id ?? null,
      isResolved: Boolean(t?.isResolved),
      isOutdated: Boolean(t?.isOutdated),
      path: t?.path ?? null,
      line: t?.line ?? null,
      originalLine: t?.originalLine ?? null,
      diffHunk: t?.diffHunk ?? null,
      author,
      body,
      url,
      createdAt,
      commentCount: comments.length,
    };
  });

  process.stdout.write(JSON.stringify({ owner, repo, pullNumber, pullUrl, threads }, null, 2));
}

main().catch((err) => {
  process.stderr.write(`${err?.message ?? String(err)}\n`);
  process.exit(1);
});

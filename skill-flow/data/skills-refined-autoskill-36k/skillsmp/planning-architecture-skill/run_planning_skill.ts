// run_planning_skill.ts
// This script implements the Planning & Architecture skill defined in SKILL.md.
// It performs the following steps:
// 1. Locate the repository root (assumes this script resides within the repo).
// 2. Read documentation files from the docs/ directory.
// 3. Perform web searches for modern UI/UX design patterns (placeholder implementation).
// 4. Synthesize the information into a structured implementation plan.
// 5. Write the plan to output/plan.md.

const fs = require("fs").promises;
const path = require("path");

// Helper to locate repo root by walking up until a package.json is found.
async function findRepoRoot(startDir: string): Promise<string> {
  let dir = startDir;
  while (true) {
    const pkgPath = path.join(dir, "package.json");
    try {
      await fs.access(pkgPath);
      return dir;
    } catch {
      const parent = path.dirname(dir);
      if (parent === dir) throw new Error("Repository root not found");
      dir = parent;
    }
  }
}

// Read a documentation file if it exists.
async function readDocFile(
  repoRoot: string,
  relativePath: string,
): Promise<string> {
  const fullPath = path.join(repoRoot, "docs", relativePath);
  try {
    const content = await fs.readFile(fullPath, "utf8");
    return content;
  } catch (e) {
    return `**Missing documentation:** ${relativePath}`;
  }
}

// Placeholder for web search – in a real environment this would call a search API.
async function performWebSearch(query: string): Promise<string> {
  // For now, return a static placeholder.
  return `Web search results for "${query}" (placeholder).`;
}

async function main() {
  const repoRoot = await findRepoRoot(__dirname);
  const projectOverview = await readDocFile(repoRoot, "PROJECT_OVERVIEW.md");
  const designSystem = await readDocFile(repoRoot, "DESIGN_SYSTEM.md");

  const searchResults = await performWebSearch(
    "modern web app design patterns",
  );

  const plan = `# Implementation Plan for Tenzzen App

## Repository Root
${repoRoot}

## Documentation Summary
### PROJECT_OVERVIEW.md
${projectOverview}

### DESIGN_SYSTEM.md
${designSystem}

## Web Design Inspiration
${searchResults}

## Suggested Architecture
- Use Next.js App Router for pages.
- Leverage Convex for backend data and functions.
- Organize UI components under \`components/\` with a design system.
- Apply modern UI/UX patterns such as glassmorphism, dark mode, and micro‑animations.

## Next Steps
1. Refine the architecture diagram.
2. Break down tasks into granular tickets.
3. Implement UI components following the design inspiration.
`;

  const outputDir = path.join(repoRoot, "output");
  await fs.mkdir(outputDir, { recursive: true });
  const planPath = path.join(outputDir, "plan.md");
  await fs.writeFile(planPath, plan, "utf8");
  console.log(`Implementation plan written to ${planPath}`);
}

main().catch((err) => {
  console.error("Error executing planning skill:", err);
  process.exit(1);
});

#!/usr/bin/env node
/**
 * Generate Documentation Links for semantic-release notes
 * SHAREABLE: Works with any repository via dynamic repo URL detection
 *
 * Usage: node generate-doc-notes.mjs [lastTag]
 * Output: Markdown section written to stdout (or nothing if no docs changed)
 *
 * ADR: 2025-12-06-release-notes-adr-linking
 * Scope Expansion: 2025-12-21 - Extended to all markdown documentation
 * Enhancement: 2025-12-23 - Added line count delta (+N/-M) and rename context tracking
 */

import { execSync } from "child_process";
import { readFileSync, existsSync } from "fs";

// ADR: 2025-12-08-mise-env-centralized-config
// Configuration via environment variables with defaults for backward compatibility
const ADR_DIR = process.env.ADR_DIR || "docs/adr";
const DESIGN_DIR = process.env.DESIGN_DIR || "docs/design";

// Category patterns in priority order (first match wins)
const CATEGORY_MATCHERS = [
  {
    id: "adr",
    pattern: /^docs\/adr\/(\d{4}-\d{2}-\d{2}-[\w-]+)\.md$/,
    label: "ADRs",
  },
  {
    id: "designSpec",
    pattern: /^docs\/design\/(\d{4}-\d{2}-\d{2}-[\w-]+)\/spec\.md$/,
    label: "Design Specs",
  },
  {
    id: "skill",
    pattern: /^plugins\/([\w-]+)\/skills\/([\w-]+)\/SKILL\.md$/,
    label: "Skills",
  },
  {
    id: "pluginReadme",
    pattern: /^plugins\/([\w-]+)\/README\.md$/,
    label: "Plugin READMEs",
  },
  {
    id: "skillReference",
    pattern: /^plugins\/([\w-]+)\/skills\/([\w-]+)\/references\/([\w-]+)\.md$/,
    label: "Skill References",
  },
  {
    id: "pluginSkill",
    pattern: /^plugins\/([\w-]+)\/SKILL\.md$/,
    label: "Plugin Skills",
  },
  {
    id: "command",
    pattern: /^plugins\/([\w-]+)\/commands\/([\w-]+)\.md$/,
    label: "Commands",
  },
  {
    id: "rootDocs",
    pattern: /^(CLAUDE|README|CHANGELOG)\.md$/,
    label: "Root Documentation",
  },
  {
    id: "generalDocs",
    pattern: /^docs\/(?!adr\/|design\/)([\w-]+)\.md$/,
    label: "General Documentation",
  },
  {
    id: "assets",
    pattern: /^plugins\/.*\/assets\/.*\.md$/,
    label: "Assets",
  },
];

// Exclusion patterns
const EXCLUDE_PATTERNS = [
  /^tmp\//, // Gitignored temp directory
  /^node_modules\//, // Dependencies
  /^\.git\//, // Git internals
  /^\.claude\//, // Claude workspace
];

// ADR reference in commit messages: ADR: YYYY-MM-DD-slug
const ADR_COMMIT_REF_PATTERN = /ADR:\s*(\d{4}-\d{2}-\d{2}-[\w-]+)/g;

// Dynamic repo URL detection (works for any repo)
function getRepoUrl() {
  try {
    const remoteUrl = execSync("git remote get-url origin", {
      encoding: "utf8",
    }).trim();
    return remoteUrl
      // Handle custom SSH host aliases (e.g., git@github.com-username:owner/repo)
      .replace(/^git@github\.com[^:]*:/, "https://github.com/")
      .replace(/\.git$/, "");
  } catch {
    throw new Error("Failed to get git remote URL");
  }
}

const REPO_URL = getRepoUrl();
const LAST_TAG = process.argv[2] || "";

/**
 * Parse git diff --numstat output for line count statistics
 */
function parseNumstat(output) {
  if (!output) return {};
  const stats = {};
  for (const line of output.split("\n")) {
    if (!line.trim()) continue;
    const [added, deleted, ...pathParts] = line.split("\t");
    const path = pathParts.join("\t");
    if (path) {
      stats[path] = {
        added: added === "-" ? 0 : parseInt(added, 10),
        deleted: deleted === "-" ? 0 : parseInt(deleted, 10),
      };
    }
  }
  return stats;
}

/**
 * Get changed files with change type via git diff
 * For first release (no tag), uses git ls-files to get all tracked files
 * Enhanced: Includes line count delta and old path for renames
 */
function getChangedFilesWithType() {
  try {
    // A=Added, C=Copied, M=Modified, R=Renamed, D=Deleted
    const cmd = LAST_TAG
      ? `git diff ${LAST_TAG}..HEAD --name-status --diff-filter=ACDMR`
      : `git ls-files`;

    const output = execSync(cmd, { encoding: "utf8" }).trim();
    if (!output) return [];

    // Get line count statistics
    let lineStats = {};
    if (LAST_TAG) {
      try {
        const numstatCmd = `git diff ${LAST_TAG}..HEAD --numstat`;
        const numstatOutput = execSync(numstatCmd, { encoding: "utf8" }).trim();
        lineStats = parseNumstat(numstatOutput);
      } catch {
        // Silently continue without line stats
      }
    }

    if (!LAST_TAG) {
      // First release: all files are "Added"
      return output
        .split("\n")
        .filter((path) => path.endsWith(".md"))
        .map((path) => ({
          path,
          changeType: "new",
          linesAdded: lineStats[path]?.added || 0,
          linesDeleted: lineStats[path]?.deleted || 0,
        }));
    }

    return output
      .split("\n")
      .map((line) => {
        const parts = line.split("\t");
        const status = parts[0];

        // Handle renames: R100\told-path\tnew-path
        if (status.startsWith("R")) {
          const oldPath = parts[1];
          const newPath = parts[2];
          return {
            path: newPath,
            oldPath: oldPath, // Preserve old path for context
            changeType: "renamed",
            renameScore: parseInt(status.substring(1), 10),
            linesAdded: lineStats[newPath]?.added || 0,
            linesDeleted: lineStats[newPath]?.deleted || 0,
          };
        }

        const path = parts.slice(1).join("\t");
        const changeType =
          {
            A: "new",
            C: "new",
            M: "updated",
            D: "deleted",
          }[status[0]] || "updated";

        return {
          path,
          changeType,
          linesAdded: lineStats[path]?.added || 0,
          linesDeleted: lineStats[path]?.deleted || 0,
        };
      })
      .filter(({ path }) => path.endsWith(".md"));
  } catch {
    return [];
  }
}

/**
 * Parse commit messages for ADR references
 * Looks for patterns like "ADR: 2025-12-06-slug" in commit bodies
 */
function parseCommitMessages() {
  try {
    const cmd = LAST_TAG
      ? `git log ${LAST_TAG}..HEAD --format="%B"`
      : `git log HEAD --format="%B"`;
    const output = execSync(cmd, { encoding: "utf8" });
    const matches = [...output.matchAll(ADR_COMMIT_REF_PATTERN)];
    return matches.map((m) => m[1]);
  } catch {
    return [];
  }
}

/**
 * Categorize a file path
 * Returns { category, match } or null if excluded/not markdown
 */
function categorizeFile(path) {
  // Check exclusions first
  for (const exclude of EXCLUDE_PATTERNS) {
    if (exclude.test(path)) return null;
  }

  // Check categories in order
  for (const { id, pattern } of CATEGORY_MATCHERS) {
    const match = path.match(pattern);
    if (match) {
      return { category: id, match };
    }
  }

  // Catch-all for other .md files
  if (/\.md$/.test(path)) {
    return { category: "other", match: [path] };
  }

  return null;
}

/**
 * Extract title based on file type
 * - ADRs: H1 after frontmatter (e.g., "# ADR: Ralph RSSI...")
 * - SKILLs: YAML name field or H1
 * - READMEs: H1 or directory name
 * - Design Specs: H1 or parent directory slug
 */
function extractTitle(filePath, category) {
  if (!existsSync(filePath)) return null;

  try {
    const content = readFileSync(filePath, "utf8");

    // For SKILLs: try YAML name field first
    if (category === "skill" || category === "pluginSkill") {
      const yamlMatch = content.match(/^---\n([\s\S]*?)\n---/);
      if (yamlMatch) {
        const nameMatch = yamlMatch[1].match(/^name:\s*(.+)$/m);
        if (nameMatch) return nameMatch[1].trim();
      }
    }

    // Default: extract H1 after frontmatter
    const lines = content.split("\n");
    let inFrontmatter = false;
    for (const line of lines) {
      if (line.trim() === "---") {
        inFrontmatter = !inFrontmatter;
        continue;
      }
      if (!inFrontmatter && line.startsWith("# ")) {
        // Strip "ADR: " prefix if present
        return line.replace(/^# (?:ADR:\s*)?/, "").trim();
      }
    }
  } catch {
    // Fallback handled by caller
  }

  return null;
}

/**
 * Extract status from YAML frontmatter
 */
function extractStatus(filePath) {
  if (!existsSync(filePath)) return "unknown";
  try {
    const content = readFileSync(filePath, "utf8");
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return "unknown";
    const statusMatch = match[1].match(/^status:\s*(\w+)/m);
    return statusMatch ? statusMatch[1] : "unknown";
  } catch {
    return "unknown";
  }
}

/**
 * Check if corresponding design spec exists for an ADR slug
 */
function findDesignSpec(adrSlug) {
  const specPath = `${DESIGN_DIR}/${adrSlug}/spec.md`;
  return existsSync(specPath) ? specPath : null;
}

/**
 * Get fallback title from path
 */
function getFallbackTitle(path, category) {
  const filename = path.split("/").pop().replace(/\.md$/, "");

  switch (category) {
    case "adr":
    case "designSpec":
      // Extract slug from YYYY-MM-DD-slug pattern
      const slug = path.match(/(\d{4}-\d{2}-\d{2}-([\w-]+))/)?.[2];
      return slug
        ? slug.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())
        : filename;
    case "skill":
    case "pluginSkill":
      return path.match(/skills\/([\w-]+)\/SKILL\.md$/)?.[1] || filename;
    case "pluginReadme":
      return path.match(/plugins\/([\w-]+)\/README\.md$/)?.[1] || filename;
    case "skillReference":
      return (
        path.match(/references\/([\w-]+)\.md$/)?.[1]?.replace(/-/g, " ") ||
        filename
      );
    case "command":
      return path.match(/commands\/([\w-]+)\.md$/)?.[1] || filename;
    default:
      return filename;
  }
}

/**
 * Render ADR section with status table
 */
function renderAdrSection(files) {
  let output = "\n### ADRs\n\n";
  output += "| Status | ADR | Change |\n";
  output += "|--------|-----|--------|\n";

  for (const file of files.sort((a, b) => a.path.localeCompare(b.path))) {
    const { path, changeType } = file;
    const title = extractTitle(path, "adr") || getFallbackTitle(path, "adr");
    const status = extractStatus(path);
    const url = getFileUrl(path, changeType);
    output += `| ${status} | [${title}](${url}) | ${formatChangeInfo(file)} |\n`;
  }

  return output;
}

/**
 * Render Design Specs section
 */
function renderDesignSpecSection(files) {
  let output = "\n### Design Specs\n\n";

  for (const file of files.sort((a, b) => a.path.localeCompare(b.path))) {
    const { path, changeType } = file;
    const title =
      extractTitle(path, "designSpec") || getFallbackTitle(path, "designSpec");
    const url = getFileUrl(path, changeType);
    output += `- [${title}](${url}) - ${formatChangeInfo(file)}\n`;
  }

  return output;
}

/**
 * Render Skills section grouped by plugin
 */
function renderSkillsSection(files) {
  let output = "\n### Skills\n\n";

  // Group by plugin
  const byPlugin = {};
  for (const file of files) {
    const plugin = file.match?.[1];
    if (!plugin) continue;
    if (!byPlugin[plugin]) byPlugin[plugin] = [];
    byPlugin[plugin].push(file);
  }

  // Render each plugin group
  for (const plugin of Object.keys(byPlugin).sort()) {
    const pluginFiles = byPlugin[plugin];
    output += `<details>\n<summary><strong>${plugin}</strong> (${pluginFiles.length} ${pluginFiles.length === 1 ? "change" : "changes"})</summary>\n\n`;

    for (const file of pluginFiles.sort((a, b) =>
      a.path.localeCompare(b.path)
    )) {
      const { path, changeType } = file;
      const skillName = path.match(/skills\/([\w-]+)\/SKILL\.md$/)?.[1];
      const title =
        extractTitle(path, "skill") ||
        skillName?.replace(/-/g, " ") ||
        getFallbackTitle(path, "skill");
      const url = getFileUrl(path, changeType);
      output += `- [${title}](${url}) - ${formatChangeInfo(file)}\n`;
    }

    output += "\n</details>\n\n";
  }

  return output;
}

/**
 * Render Skill References section with collapsible groups
 */
function renderSkillReferencesSection(files) {
  let output = "\n### Skill References\n\n";

  // Group by plugin/skill
  const bySkill = {};
  for (const file of files) {
    const plugin = file.match?.[1];
    const skill = file.match?.[2];
    if (!plugin || !skill) continue;
    const key = `${plugin}/${skill}`;
    if (!bySkill[key]) bySkill[key] = [];
    bySkill[key].push(file);
  }

  // Render each skill group
  for (const key of Object.keys(bySkill).sort()) {
    const skillFiles = bySkill[key];
    output += `<details>\n<summary><strong>${key}</strong> (${skillFiles.length} ${skillFiles.length === 1 ? "file" : "files"})</summary>\n\n`;

    for (const file of skillFiles.sort((a, b) =>
      a.path.localeCompare(b.path)
    )) {
      const { path, changeType } = file;
      const refName = path.match(/references\/([\w-]+)\.md$/)?.[1];
      const title =
        extractTitle(path, "skillReference") ||
        refName?.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()) ||
        getFallbackTitle(path, "skillReference");
      const url = getFileUrl(path, changeType);
      output += `- [${title}](${url}) - ${formatChangeInfo(file)}\n`;
    }

    output += "\n</details>\n\n";
  }

  return output;
}

/**
 * Render Commands section grouped by plugin
 */
function renderCommandsSection(files) {
  let output = "\n### Commands\n\n";

  // Group by plugin
  const byPlugin = {};
  for (const file of files) {
    const plugin = file.match?.[1];
    if (!plugin) continue;
    if (!byPlugin[plugin]) byPlugin[plugin] = [];
    byPlugin[plugin].push(file);
  }

  // Render each plugin group
  for (const plugin of Object.keys(byPlugin).sort()) {
    const pluginFiles = byPlugin[plugin];
    output += `<details>\n<summary><strong>${plugin}</strong> (${pluginFiles.length} ${pluginFiles.length === 1 ? "command" : "commands"})</summary>\n\n`;

    for (const file of pluginFiles.sort((a, b) =>
      a.path.localeCompare(b.path)
    )) {
      const { path, changeType } = file;
      const cmdName = path.match(/commands\/([\w-]+)\.md$/)?.[1];
      const title =
        extractTitle(path, "command") || cmdName || getFallbackTitle(path, "command");
      const url = getFileUrl(path, changeType);
      output += `- [${title}](${url}) - ${formatChangeInfo(file)}\n`;
    }

    output += "\n</details>\n\n";
  }

  return output;
}

/**
 * Format change info with line counts and rename context
 * Examples: "new (+152)", "updated (+5/-3)", "renamed from `old/path`"
 * Note: Deleted files show no line counts (file no longer exists)
 */
function formatChangeInfo(file) {
  const { changeType, linesAdded, linesDeleted, oldPath } = file;

  // For deleted files, just show "deleted" without line stats
  // (line counts for deleted files are meaningless - the file is gone)
  if (changeType === "deleted") {
    return "deleted";
  }

  // Build line delta string for non-deleted files
  let lineDelta = "";
  if (linesAdded > 0 || linesDeleted > 0) {
    if (linesAdded > 0 && linesDeleted > 0) {
      lineDelta = ` (+${linesAdded}/-${linesDeleted})`;
    } else if (linesAdded > 0) {
      lineDelta = ` (+${linesAdded})`;
    } else if (linesDeleted > 0) {
      lineDelta = ` (-${linesDeleted})`;
    }
  }

  // Special handling for renames
  if (changeType === "renamed" && oldPath) {
    return `renamed from \`${oldPath}\`${lineDelta}`;
  }

  return `${changeType}${lineDelta}`;
}

/**
 * Generate URL for a file, using historical tag for deleted files
 */
function getFileUrl(path, changeType) {
  if (changeType === "deleted" && LAST_TAG) {
    // Deleted files link to the last tag where they existed
    return `${REPO_URL}/blob/${LAST_TAG}/${path}`;
  }
  return `${REPO_URL}/blob/main/${path}`;
}

/**
 * Render simple list for categories without grouping
 */
function renderSimpleList(header, files) {
  let output = `\n### ${header}\n\n`;

  for (const file of files.sort((a, b) => a.path.localeCompare(b.path))) {
    const { path, category, changeType } = file;
    const title =
      extractTitle(path, category) || getFallbackTitle(path, category);
    const url = getFileUrl(path, changeType);
    output += `- [${title}](${url}) - ${formatChangeInfo(file)}\n`;
  }

  return output;
}

// Main logic
const changedFiles = getChangedFilesWithType();

// Categorize all changed files (preserve line stats and rename info)
const categorizedFiles = [];
for (const file of changedFiles) {
  const result = categorizeFile(file.path);
  if (result) {
    categorizedFiles.push({
      ...file, // Preserves path, changeType, linesAdded, linesDeleted, oldPath, renameScore
      category: result.category,
      match: result.match,
    });
  }
}

// Get ADR references from commit messages
const commitSlugs = parseCommitMessages();

// Add ADRs referenced in commits that weren't changed
for (const slug of commitSlugs) {
  const adrPath = `${ADR_DIR}/${slug}.md`;
  if (
    existsSync(adrPath) &&
    !categorizedFiles.some((f) => f.path === adrPath)
  ) {
    categorizedFiles.push({
      path: adrPath,
      changeType: "referenced",
      category: "adr",
      match: [adrPath, slug],
    });
  }
}

// COUPLING: If design spec changed, include corresponding ADR
for (const file of [...categorizedFiles]) {
  if (file.category === "designSpec") {
    const slug = file.path.match(/(\d{4}-\d{2}-\d{2}-[\w-]+)\/spec\.md$/)?.[1];
    if (slug) {
      const adrPath = `${ADR_DIR}/${slug}.md`;
      if (
        existsSync(adrPath) &&
        !categorizedFiles.some((f) => f.path === adrPath)
      ) {
        categorizedFiles.push({
          path: adrPath,
          changeType: "coupled",
          category: "adr",
          match: [adrPath, slug],
        });
      }
    }
  }
}

// Also add corresponding design specs for changed ADRs
for (const file of [...categorizedFiles]) {
  if (file.category === "adr") {
    const slug = file.path.match(/(\d{4}-\d{2}-\d{2}-[\w-]+)\.md$/)?.[1];
    if (slug) {
      const specPath = findDesignSpec(slug);
      if (specPath && !categorizedFiles.some((f) => f.path === specPath)) {
        categorizedFiles.push({
          path: specPath,
          changeType: "coupled",
          category: "designSpec",
          match: [specPath, slug],
        });
      }
    }
  }
}

// Exit silently if nothing found
if (categorizedFiles.length === 0) {
  process.exit(0);
}

// Group by category
const groups = {};
for (const file of categorizedFiles) {
  if (!groups[file.category]) groups[file.category] = [];
  groups[file.category].push(file);
}

// Generate output
let output = "\n---\n\n## Documentation Changes\n";

// Architecture Decisions section
if (groups.adr || groups.designSpec) {
  output += "\n## Architecture Decisions\n";

  if (groups.adr) {
    output += renderAdrSection(groups.adr);
  }

  if (groups.designSpec) {
    output += renderDesignSpecSection(groups.designSpec);
  }
}

// Plugin Documentation section
if (
  groups.skill ||
  groups.pluginReadme ||
  groups.pluginSkill ||
  groups.skillReference ||
  groups.command
) {
  output += "\n## Plugin Documentation\n";

  if (groups.skill) {
    output += renderSkillsSection(groups.skill);
  }

  if (groups.pluginSkill) {
    output += renderSimpleList("Plugin Skills", groups.pluginSkill);
  }

  if (groups.pluginReadme) {
    output += renderSimpleList("Plugin READMEs", groups.pluginReadme);
  }

  if (groups.skillReference) {
    output += renderSkillReferencesSection(groups.skillReference);
  }

  if (groups.command) {
    output += renderCommandsSection(groups.command);
  }
}

// Repository Documentation section
if (groups.rootDocs || groups.generalDocs) {
  output += "\n## Repository Documentation\n";

  if (groups.rootDocs) {
    output += renderSimpleList("Root Documentation", groups.rootDocs);
  }

  if (groups.generalDocs) {
    output += renderSimpleList("General Documentation", groups.generalDocs);
  }
}

// Other section
if (groups.assets || groups.other) {
  output += "\n## Other Documentation\n";

  if (groups.assets) {
    output += renderSimpleList("Assets", groups.assets);
  }

  if (groups.other) {
    output += renderSimpleList("Other", groups.other);
  }
}

process.stdout.write(output);

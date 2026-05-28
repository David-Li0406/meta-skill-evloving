#!/usr/bin/env -S deno run --allow-read --allow-env

/**
 * Analyze Source Documents
 *
 * Reads markdown files from a directory and proposes a course structure.
 * Identifies units based on subdirectories, lessons based on files.
 *
 * Usage:
 *   deno run --allow-read --allow-env scripts/analyze-sources.ts /path/to/sources
 *   deno run --allow-read --allow-env scripts/analyze-sources.ts /path/to/sources --json
 *   deno run --allow-read --allow-env scripts/analyze-sources.ts /path/to/sources --plan
 */

import { parseArgs, showHelp } from "./api-client.ts";

// === TYPES ===

interface SourceFile {
  path: string;
  filename: string;
  title: string;
  description: string;
  headings: string[];
  wordCount: number;
  directory: string;
}

interface ProposedLesson {
  sourceFile: string;
  title: string;
  description: string;
  order: number;
  audienceLayer?: "general" | "practitioner" | "specialist";
}

interface ProposedUnit {
  title: string;
  description: string;
  sourceDirectory: string;
  lessons: ProposedLesson[];
  order: number;
}

interface CoursePlan {
  suggestedTitle: string;
  description: string;
  sourceDirectory: string;
  units: ProposedUnit[];
  suggestedCompetencies: string[];
  totalLessons: number;
  totalWordCount: number;
}

// === FILE ANALYSIS ===

async function readMarkdownFile(path: string): Promise<string> {
  try {
    return await Deno.readTextFile(path);
  } catch (error) {
    console.error(`Error reading ${path}: ${error}`);
    return "";
  }
}

function extractTitle(content: string, filename: string): string {
  // Try to find H1 heading
  const h1Match = content.match(/^#\s+(.+)$/m);
  if (h1Match) {
    return h1Match[1].trim();
  }
  // Fall back to filename
  return filename
    .replace(/\.md$/, "")
    .replace(/[-_]/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function extractDescription(content: string): string {
  // Find first paragraph after title
  const lines = content.split("\n");
  let foundHeading = false;
  let paragraphLines: string[] = [];

  for (const line of lines) {
    if (line.startsWith("#")) {
      if (foundHeading && paragraphLines.length > 0) break;
      foundHeading = true;
      continue;
    }
    if (foundHeading && line.trim()) {
      if (line.startsWith("-") || line.startsWith("|") || line.startsWith("```")) {
        break;
      }
      paragraphLines.push(line.trim());
    } else if (foundHeading && paragraphLines.length > 0) {
      break;
    }
  }

  const description = paragraphLines.join(" ");
  return description.length > 200 ? description.slice(0, 197) + "..." : description;
}

function extractHeadings(content: string): string[] {
  const headings: string[] = [];
  const lines = content.split("\n");
  for (const line of lines) {
    const match = line.match(/^(#{1,3})\s+(.+)$/);
    if (match) {
      headings.push(match[2].trim());
    }
  }
  return headings;
}

function countWords(content: string): number {
  // Remove markdown syntax and count words
  const text = content
    .replace(/```[\s\S]*?```/g, "")
    .replace(/`[^`]+`/g, "")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/[#*_~|]/g, "");
  return text.split(/\s+/).filter((w) => w.length > 0).length;
}

async function analyzeFile(
  path: string,
  rootDir: string
): Promise<SourceFile | null> {
  const content = await readMarkdownFile(path);
  if (!content) return null;

  const filename = path.split("/").pop() || "";
  if (filename.toLowerCase() === "readme.md") {
    return null; // Skip READMEs, they're usually navigation
  }

  // Get relative directory
  const relativePath = path.replace(rootDir, "").replace(/^\//, "");
  const parts = relativePath.split("/");
  const directory = parts.length > 1 ? parts.slice(0, -1).join("/") : "";

  return {
    path,
    filename,
    title: extractTitle(content, filename),
    description: extractDescription(content),
    headings: extractHeadings(content),
    wordCount: countWords(content),
    directory,
  };
}

// === DIRECTORY SCANNING ===

async function findMarkdownFiles(dir: string): Promise<string[]> {
  const files: string[] = [];

  async function scan(currentDir: string): Promise<void> {
    try {
      for await (const entry of Deno.readDir(currentDir)) {
        const path = `${currentDir}/${entry.name}`;
        if (entry.isDirectory) {
          await scan(path);
        } else if (entry.name.endsWith(".md")) {
          files.push(path);
        }
      }
    } catch (error) {
      console.error(`Error scanning ${currentDir}: ${error}`);
    }
  }

  await scan(dir);
  return files.sort();
}

// === COURSE STRUCTURE INFERENCE ===

function inferAudienceLayer(
  directory: string,
  title: string
): "general" | "practitioner" | "specialist" | undefined {
  const lowerDir = directory.toLowerCase();
  const lowerTitle = title.toLowerCase();

  if (
    lowerDir.includes("foundation") ||
    lowerDir.includes("layer-1") ||
    lowerDir.includes("basic") ||
    lowerTitle.includes("introduction") ||
    lowerTitle.includes("getting started")
  ) {
    return "general";
  }

  if (
    lowerDir.includes("effective") ||
    lowerDir.includes("layer-2") ||
    lowerDir.includes("intermediate") ||
    lowerTitle.includes("advanced") ||
    lowerTitle.includes("techniques")
  ) {
    return "practitioner";
  }

  if (
    lowerDir.includes("technical") ||
    lowerDir.includes("layer-3") ||
    lowerDir.includes("expert") ||
    lowerTitle.includes("architecture") ||
    lowerTitle.includes("implementation")
  ) {
    return "specialist";
  }

  return undefined;
}

function formatUnitTitle(directory: string): string {
  if (!directory) return "General";

  // Handle layer-style directories
  const layerMatch = directory.match(/layer-(\d+)-(\w+)/i);
  if (layerMatch) {
    const [, num, name] = layerMatch;
    return `Layer ${num}: ${name.charAt(0).toUpperCase() + name.slice(1)}`;
  }

  // Otherwise, format the directory name
  return directory
    .split("/")
    .pop()!
    .replace(/[-_]/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function buildCoursePlan(
  files: SourceFile[],
  sourceDir: string
): CoursePlan {
  // Group files by directory
  const byDirectory = new Map<string, SourceFile[]>();
  for (const file of files) {
    const dir = file.directory || "";
    if (!byDirectory.has(dir)) {
      byDirectory.set(dir, []);
    }
    byDirectory.get(dir)!.push(file);
  }

  // Build units
  const units: ProposedUnit[] = [];
  let unitOrder = 1;

  // Sort directories to maintain consistent ordering
  const sortedDirs = [...byDirectory.keys()].sort();

  for (const dir of sortedDirs) {
    const dirFiles = byDirectory.get(dir)!;

    // Sort files within directory
    dirFiles.sort((a, b) => a.filename.localeCompare(b.filename));

    const lessons: ProposedLesson[] = dirFiles.map((file, index) => ({
      sourceFile: file.path,
      title: file.title,
      description: file.description,
      order: index + 1,
      audienceLayer: inferAudienceLayer(dir, file.title),
    }));

    units.push({
      title: formatUnitTitle(dir),
      description: `Content from ${dir || "root directory"}`,
      sourceDirectory: dir,
      lessons,
      order: unitOrder++,
    });
  }

  // Try to infer course title from README or directory name
  let suggestedTitle = "New Course";
  const dirName = sourceDir.split("/").pop();
  if (dirName) {
    suggestedTitle = dirName
      .replace(/[-_]/g, " ")
      .replace(/\b\w/g, (c) => c.toUpperCase());
  }

  // Extract potential competencies from all headings
  const allHeadings = files.flatMap((f) => f.headings);
  const competencyKeywords = [
    "understand",
    "learn",
    "know",
    "skill",
    "ability",
    "can",
    "will be able",
  ];
  const suggestedCompetencies = allHeadings
    .filter((h) =>
      competencyKeywords.some((k) => h.toLowerCase().includes(k))
    )
    .slice(0, 10);

  const totalWordCount = files.reduce((sum, f) => sum + f.wordCount, 0);

  return {
    suggestedTitle,
    description: `Course generated from ${files.length} source documents`,
    sourceDirectory: sourceDir,
    units,
    suggestedCompetencies,
    totalLessons: files.length,
    totalWordCount,
  };
}

// === OUTPUT FORMATTING ===

function formatPlan(plan: CoursePlan): string {
  const lines: string[] = [];

  lines.push(`# Course Plan: ${plan.suggestedTitle}`);
  lines.push("");
  lines.push(`**Source:** ${plan.sourceDirectory}`);
  lines.push(
    `**Total:** ${plan.totalLessons} lessons, ~${plan.totalWordCount.toLocaleString()} words`
  );
  lines.push("");

  lines.push("## Proposed Structure");
  lines.push("");

  for (const unit of plan.units) {
    lines.push(`### ${unit.order}. ${unit.title}`);
    lines.push("");
    for (const lesson of unit.lessons) {
      const layer = lesson.audienceLayer
        ? ` [${lesson.audienceLayer}]`
        : "";
      lines.push(`- **${lesson.title}**${layer}`);
      if (lesson.description) {
        lines.push(`  ${lesson.description}`);
      }
    }
    lines.push("");
  }

  if (plan.suggestedCompetencies.length > 0) {
    lines.push("## Suggested Competencies");
    lines.push("");
    for (const comp of plan.suggestedCompetencies) {
      lines.push(`- ${comp}`);
    }
    lines.push("");
  }

  lines.push("---");
  lines.push(
    "*Generated by teach-course-builder. Review and modify as needed.*"
  );

  return lines.join("\n");
}

// === MAIN ===

async function main(): Promise<void> {
  const args = parseArgs(Deno.args);

  if (args.has("help") || args.has("h") || Deno.args.includes("-h")) {
    showHelp(
      "Analyze Source Documents",
      "Usage: deno run --allow-read --allow-env scripts/analyze-sources.ts <directory>",
      `  <directory>  Source directory containing markdown files`
    );
    Deno.exit(0);
  }

  const sourceDir = args.get("_positional") as string;
  if (!sourceDir) {
    console.error("Error: Please specify a source directory");
    console.error(
      "Usage: deno run --allow-read --allow-env scripts/analyze-sources.ts <directory>"
    );
    Deno.exit(1);
  }

  // Check if directory exists
  try {
    const stat = await Deno.stat(sourceDir);
    if (!stat.isDirectory) {
      console.error(`Error: ${sourceDir} is not a directory`);
      Deno.exit(1);
    }
  } catch {
    console.error(`Error: Directory ${sourceDir} does not exist`);
    Deno.exit(1);
  }

  // Find and analyze files
  const files = await findMarkdownFiles(sourceDir);
  if (files.length === 0) {
    console.error(`No markdown files found in ${sourceDir}`);
    Deno.exit(1);
  }

  console.error(`Found ${files.length} markdown files`);

  // Analyze each file
  const analyzed: SourceFile[] = [];
  for (const file of files) {
    const result = await analyzeFile(file, sourceDir);
    if (result) {
      analyzed.push(result);
    }
  }

  console.error(`Analyzed ${analyzed.length} content files`);

  // Build course plan
  const plan = buildCoursePlan(analyzed, sourceDir);

  // Output
  if (args.has("json")) {
    console.log(JSON.stringify(plan, null, 2));
  } else {
    console.log(formatPlan(plan));
  }
}

main();

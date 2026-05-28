#!/usr/bin/env -S deno run --allow-read

/**
 * Analyze Framework
 *
 * Extracts structure from a framework SKILL.md for agent conversion.
 * Outputs JSON with diagnostic states, vocabulary, processes, and integrations.
 *
 * Usage:
 *   deno run --allow-read scripts/analyze-framework.ts path/to/SKILL.md
 *   deno run --allow-read scripts/analyze-framework.ts path/to/SKILL.md --json
 *   deno run --allow-read scripts/analyze-framework.ts path/to/SKILL.md --output analysis.json
 */

// === INTERFACES ===

interface DiagnosticState {
  id: string;
  name: string;
  symptoms: string[];
  test: string;
  intervention: string;
}

interface VocabularyTerm {
  term: string;
  context: string;
  depth: "introductory" | "working" | "expert";
}

interface ProcessPhase {
  phaseId: string;
  name: string;
  description: string;
}

interface Integration {
  skill: string;
  connectionType: string;
  description: string;
}

interface AntiPattern {
  name: string;
  symptom: string;
  fix: string;
}

interface FrameworkAnalysis {
  frameworkId: string;
  frameworkName: string;
  states: DiagnosticState[];
  vocabulary: VocabularyTerm[];
  processes: ProcessPhase[];
  integrations: Integration[];
  antiPatterns: AntiPattern[];
  analyzedAt: string;
}

// === PARSING ===

function extractFrontmatter(content: string): Record<string, unknown> {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};

  const frontmatter: Record<string, unknown> = {};
  const lines = match[1].split("\n");

  for (const line of lines) {
    const colonIndex = line.indexOf(":");
    if (colonIndex > 0) {
      const key = line.slice(0, colonIndex).trim();
      const value = line.slice(colonIndex + 1).trim();
      frontmatter[key] = value.replace(/^["']|["']$/g, "");
    }
  }

  return frontmatter;
}

function extractDiagnosticStates(content: string): DiagnosticState[] {
  const states: DiagnosticState[] = [];

  // Look for state patterns like "### R1: Name" or "### State X1: Name"
  const statePattern =
    /###\s+(?:State\s+)?([A-Z0-9.]+):\s*(.+?)\n([\s\S]*?)(?=###\s+(?:State\s+)?[A-Z0-9.]+:|##\s|$)/g;

  let match;
  while ((match = statePattern.exec(content)) !== null) {
    const [, id, name, body] = match;

    // Extract symptoms
    const symptomsMatch = body.match(
      /\*\*Symptoms?:\*\*\s*([\s\S]*?)(?=\*\*(?:Test|Key Questions?|Intervention)|\n###|\n##|$)/i
    );
    const symptoms = symptomsMatch
      ? symptomsMatch[1]
          .split(/[-*]\s+/)
          .map((s) => s.trim())
          .filter(Boolean)
      : [];

    // Extract test
    const testMatch = body.match(
      /\*\*(?:Test|Key Questions?):\*\*\s*([\s\S]*?)(?=\*\*(?:Symptoms?|Intervention)|\n###|\n##|$)/i
    );
    const test = testMatch ? testMatch[1].trim() : "";

    // Extract intervention
    const interventionMatch = body.match(
      /\*\*Intervention:\*\*\s*([\s\S]*?)(?=\*\*(?:Test|Symptoms?)|\n###|\n##|$)/i
    );
    const intervention = interventionMatch
      ? interventionMatch[1].trim()
      : "";

    states.push({
      id: id.trim(),
      name: name.trim(),
      symptoms: symptoms.length > 0 ? symptoms : [body.slice(0, 100).trim()],
      test,
      intervention,
    });
  }

  return states;
}

function extractVocabulary(content: string): VocabularyTerm[] {
  const vocabulary: VocabularyTerm[] = [];

  // Look for bold terms with definitions
  const boldPattern = /\*\*([^*]+)\*\*[:\s]+([^*\n]+)/g;

  let match;
  while ((match = boldPattern.exec(content)) !== null) {
    const [, term, context] = match;

    // Skip common non-vocabulary items
    const skipTerms = [
      "symptoms",
      "test",
      "intervention",
      "problem",
      "fix",
      "use when",
    ];
    if (skipTerms.some((s) => term.toLowerCase().includes(s))) continue;
    if (term.length > 50) continue; // Likely not a term

    // Guess depth based on context
    let depth: "introductory" | "working" | "expert" = "working";
    if (context.toLowerCase().includes("technical") || context.toLowerCase().includes("expert")) {
      depth = "expert";
    } else if (
      context.toLowerCase().includes("basic") ||
      context.toLowerCase().includes("introduct")
    ) {
      depth = "introductory";
    }

    vocabulary.push({
      term: term.trim(),
      context: context.trim().slice(0, 200),
      depth,
    });
  }

  // Deduplicate
  const seen = new Set<string>();
  return vocabulary.filter((v) => {
    const key = v.term.toLowerCase();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function extractProcessPhases(content: string): ProcessPhase[] {
  const phases: ProcessPhase[] = [];

  // Look for phase patterns
  const phasePattern =
    /(?:Phase|Step)\s+(\d+(?:\.\d+)?)[:\s]+([^\n]+)\n([\s\S]*?)(?=(?:Phase|Step)\s+\d|##\s|$)/gi;

  let match;
  while ((match = phasePattern.exec(content)) !== null) {
    const [, id, name, body] = match;

    phases.push({
      phaseId: id.trim(),
      name: name.trim(),
      description: body.trim().slice(0, 200),
    });
  }

  return phases;
}

function extractIntegrations(content: string): Integration[] {
  const integrations: Integration[] = [];

  // Look for integration section
  const integrationSection = content.match(
    /##\s+Integration[^\n]*\n([\s\S]*?)(?=##\s|$)/i
  );
  if (!integrationSection) return integrations;

  // Look for skill references
  const skillPattern = /\*\*([^*]+)\*\*[:\s|]+([^\n|]+)/g;

  let match;
  while ((match = skillPattern.exec(integrationSection[1])) !== null) {
    const [, skill, description] = match;

    integrations.push({
      skill: skill.trim().toLowerCase().replace(/\s+/g, "-"),
      connectionType: "integration",
      description: description.trim(),
    });
  }

  return integrations;
}

function extractAntiPatterns(content: string): AntiPattern[] {
  const antiPatterns: AntiPattern[] = [];

  // Look for anti-pattern section
  const antiPatternSection = content.match(
    /##\s+Anti-?Patterns?\s*\n([\s\S]*?)(?=##\s|$)/i
  );
  if (!antiPatternSection) return antiPatterns;

  // Look for pattern definitions
  const patternPattern =
    /###\s+(?:The\s+)?([^\n]+)\n([\s\S]*?)(?=###|$)/g;

  let match;
  while ((match = patternPattern.exec(antiPatternSection[1])) !== null) {
    const [, name, body] = match;

    const problemMatch = body.match(/\*\*Problem:\*\*\s*([^\n]+)/i);
    const symptomMatch = body.match(/\*\*Symptom[s]?:\*\*\s*([^\n]+)/i);
    const fixMatch = body.match(/\*\*Fix:\*\*\s*([^\n]+)/i);

    antiPatterns.push({
      name: name.trim(),
      symptom: (symptomMatch || problemMatch)?.[1]?.trim() || "",
      fix: fixMatch?.[1]?.trim() || "",
    });
  }

  return antiPatterns;
}

function analyzeFramework(content: string, filePath: string): FrameworkAnalysis {
  const frontmatter = extractFrontmatter(content);

  const frameworkId =
    (frontmatter.name as string) ||
    filePath
      .split("/")
      .pop()
      ?.replace(/\.md$/, "")
      .toLowerCase()
      .replace(/\s+/g, "-") ||
    "unknown";

  // Extract title from first heading
  const titleMatch = content.match(/^#\s+([^\n]+)/m);
  const frameworkName = titleMatch?.[1] || frameworkId;

  return {
    frameworkId,
    frameworkName,
    states: extractDiagnosticStates(content),
    vocabulary: extractVocabulary(content),
    processes: extractProcessPhases(content),
    integrations: extractIntegrations(content),
    antiPatterns: extractAntiPatterns(content),
    analyzedAt: new Date().toISOString(),
  };
}

// === FORMATTING ===

function formatAnalysis(analysis: FrameworkAnalysis): string {
  const lines: string[] = [];

  lines.push(`Framework Analysis: ${analysis.frameworkName}`);
  lines.push(`ID: ${analysis.frameworkId}`);
  lines.push(`Analyzed: ${analysis.analyzedAt}`);
  lines.push("");

  lines.push(`## Diagnostic States (${analysis.states.length})`);
  for (const state of analysis.states) {
    lines.push(`  ${state.id}: ${state.name}`);
    lines.push(`    Symptoms: ${state.symptoms.slice(0, 2).join("; ")}`);
    if (state.intervention) {
      lines.push(`    Intervention: ${state.intervention.slice(0, 80)}`);
    }
  }
  lines.push("");

  lines.push(`## Vocabulary (${analysis.vocabulary.length} terms)`);
  for (const term of analysis.vocabulary.slice(0, 10)) {
    lines.push(`  ${term.term} [${term.depth}]`);
  }
  if (analysis.vocabulary.length > 10) {
    lines.push(`  ... and ${analysis.vocabulary.length - 10} more`);
  }
  lines.push("");

  lines.push(`## Process Phases (${analysis.processes.length})`);
  for (const phase of analysis.processes) {
    lines.push(`  Phase ${phase.phaseId}: ${phase.name}`);
  }
  lines.push("");

  lines.push(`## Integrations (${analysis.integrations.length})`);
  for (const integration of analysis.integrations) {
    lines.push(`  ${integration.skill}: ${integration.description.slice(0, 60)}`);
  }
  lines.push("");

  lines.push(`## Anti-Patterns (${analysis.antiPatterns.length})`);
  for (const ap of analysis.antiPatterns) {
    lines.push(`  ${ap.name}`);
  }

  return lines.join("\n");
}

// === MAIN ===

async function main(): Promise<void> {
  const args = Deno.args;

  // Help
  if (args.includes("--help") || args.includes("-h") || args.length === 0) {
    console.log(`Analyze Framework

Extracts structure from a framework SKILL.md for agent conversion.

Usage:
  deno run --allow-read scripts/analyze-framework.ts <path-to-SKILL.md> [options]

Options:
  --json           Output as JSON
  --output <file>  Write JSON output to file
  --help, -h       Show this help

Examples:
  deno run --allow-read scripts/analyze-framework.ts skills/research/SKILL.md
  deno run --allow-read scripts/analyze-framework.ts skills/research/SKILL.md --json
  deno run --allow-read scripts/analyze-framework.ts skills/research/SKILL.md --output analysis.json
`);
    Deno.exit(0);
  }

  // Parse arguments
  const jsonOutput = args.includes("--json");
  const outputIndex = args.indexOf("--output");
  const outputFile = outputIndex !== -1 ? args[outputIndex + 1] : null;

  // Find file path
  let filePath: string | null = null;
  const skipIndices = new Set<number>();
  if (outputIndex !== -1) {
    skipIndices.add(outputIndex);
    skipIndices.add(outputIndex + 1);
  }

  for (let i = 0; i < args.length; i++) {
    if (!args[i].startsWith("--") && !skipIndices.has(i)) {
      filePath = args[i];
      break;
    }
  }

  if (!filePath) {
    console.error("Error: No file path provided");
    Deno.exit(1);
  }

  // Read file
  let content: string;
  try {
    content = await Deno.readTextFile(filePath);
  } catch (e) {
    console.error(`Error reading file: ${e}`);
    Deno.exit(1);
  }

  // Analyze
  const analysis = analyzeFramework(content, filePath);

  // Output
  if (outputFile) {
    await Deno.writeTextFile(outputFile, JSON.stringify(analysis, null, 2));
    console.log(`Analysis written to: ${outputFile}`);
  } else if (jsonOutput) {
    console.log(JSON.stringify(analysis, null, 2));
  } else {
    console.log(formatAnalysis(analysis));
  }
}

main();

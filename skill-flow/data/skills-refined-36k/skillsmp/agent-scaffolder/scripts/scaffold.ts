#!/usr/bin/env -S deno run --allow-read --allow-write
// deno-lint-ignore-file no-console no-await-in-loop

/**
 * Agent Scaffolder Script
 *
 * Generates a new Climpt agent structure from templates.
 *
 * Usage:
 *   deno run -A ${CLAUDE_PLUGIN_ROOT}/skills/agent-scaffolder/scripts/scaffold.ts \
 *     --name my-agent \
 *     --description "My agent description" \
 *     --completion-type externalState
 */

import { parse } from "https://deno.land/std@0.224.0/flags/mod.ts";
import { ensureDir } from "https://deno.land/std@0.224.0/fs/mod.ts";
import {
  dirname,
  fromFileUrl,
  join,
} from "https://deno.land/std@0.224.0/path/mod.ts";

interface ScaffoldOptions {
  name: string;
  description: string;
  completionType: string;
  displayName?: string;
  dryRun?: boolean;
}

const COMPLETION_TYPES = [
  "externalState",
  "iterationBudget",
  "keywordSignal",
  "stepMachine",
] as const;

function toDisplayName(kebabName: string): string {
  return kebabName
    .split("-")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function replaceTemplateVars(
  content: string,
  vars: Record<string, string>,
): string {
  let result = content;
  for (const [key, value] of Object.entries(vars)) {
    result = result.replaceAll(`{{${key}}}`, value);
  }
  return result;
}

async function readTemplate(templatePath: string): Promise<string> {
  const scriptDir = dirname(fromFileUrl(import.meta.url));
  const fullPath = join(scriptDir, "..", "templates", templatePath);
  return await Deno.readTextFile(fullPath);
}

async function writeFile(
  path: string,
  content: string,
  dryRun: boolean,
): Promise<void> {
  if (dryRun) {
    console.log(`[DRY-RUN] Would create: ${path}`);
    console.log("---");
    console.log(
      content.substring(0, 500) + (content.length > 500 ? "..." : ""),
    );
    console.log("---\n");
    return;
  }

  await ensureDir(dirname(path));
  await Deno.writeTextFile(path, content);
  console.log(`Created: ${path}`);
}

async function scaffold(options: ScaffoldOptions): Promise<void> {
  const {
    name,
    description,
    completionType,
    displayName = toDisplayName(name),
    dryRun = false,
  } = options;

  // Validate agent name
  if (!/^[a-z][a-z0-9-]*$/.test(name)) {
    console.error(
      "Error: Agent name must be lowercase kebab-case (e.g., my-agent)",
    );
    Deno.exit(1);
  }

  // Validate completion type
  if (
    !COMPLETION_TYPES.includes(
      completionType as typeof COMPLETION_TYPES[number],
    )
  ) {
    console.error(
      `Error: Invalid completion type. Must be one of: ${
        COMPLETION_TYPES.join(", ")
      }`,
    );
    Deno.exit(1);
  }

  const baseDir = `.agent/${name}`;
  const vars: Record<string, string> = {
    AGENT_NAME: name,
    DISPLAY_NAME: displayName,
    DESCRIPTION: description,
    COMPLETION_TYPE: completionType,
    ROLE_DESCRIPTION: "performs automated tasks",
  };

  console.log(`\nScaffolding agent: ${name}`);
  console.log(`  Display Name: ${displayName}`);
  console.log(`  Completion Type: ${completionType}`);
  console.log(`  Output Directory: ${baseDir}`);
  if (dryRun) {
    console.log("  Mode: DRY-RUN\n");
  } else {
    console.log("");
  }

  // Create directory structure
  const dirs = [
    `${baseDir}/schemas`,
    `${baseDir}/prompts/steps/initial/default`,
    `${baseDir}/prompts/steps/continuation/default`,
    `${baseDir}/prompts/steps/verification/default`,
    `${baseDir}/prompts/steps/closure/default`,
  ];

  if (!dryRun) {
    for (const dir of dirs) {
      await ensureDir(dir);
    }
  }

  // Generate files from templates
  const files: Array<{ template: string; output: string }> = [
    { template: "agent.json.tmpl", output: `${baseDir}/agent.json` },
    {
      template: "steps_registry.json.tmpl",
      output: `${baseDir}/steps_registry.json`,
    },
    {
      template: "step_outputs.schema.json.tmpl",
      output: `${baseDir}/schemas/step_outputs.schema.json`,
    },
    {
      template: "prompts/system.md.tmpl",
      output: `${baseDir}/prompts/system.md`,
    },
    {
      template: "prompts/steps/initial.md.tmpl",
      output: `${baseDir}/prompts/steps/initial/default/f_default.md`,
    },
    {
      template: "prompts/steps/continuation.md.tmpl",
      output: `${baseDir}/prompts/steps/continuation/default/f_default.md`,
    },
    {
      template: "prompts/steps/verification.md.tmpl",
      output: `${baseDir}/prompts/steps/verification/default/f_default.md`,
    },
    {
      template: "prompts/steps/closure.md.tmpl",
      output: `${baseDir}/prompts/steps/closure/default/f_default.md`,
    },
  ];

  for (const { template, output } of files) {
    const templateContent = await readTemplate(template);
    const content = replaceTemplateVars(templateContent, vars);
    await writeFile(output, content, dryRun);
  }

  console.log("\nScaffolding complete!");
  console.log("\nNext steps:");
  console.log(
    `  1. Edit ${baseDir}/prompts/system.md to define the agent's role`,
  );
  console.log(`  2. Customize prompts in ${baseDir}/prompts/steps/`);
  console.log(`  3. Add parameters to ${baseDir}/agent.json if needed`);
  console.log(
    `  4. Verify with: deno run -A agents/scripts/run-agent.ts --agent ${name} --dry-run`,
  );
}

// Main
if (import.meta.main) {
  const args = parse(Deno.args, {
    string: ["name", "description", "completion-type", "display-name"],
    boolean: ["dry-run", "help"],
    default: {
      "completion-type": "externalState",
      description: "A new Climpt agent",
    },
    alias: {
      n: "name",
      d: "description",
      c: "completion-type",
      h: "help",
    },
  });

  if (args.help || !args.name) {
    console.log(`
Agent Scaffolder - Generate a new Climpt agent structure

Usage:
  deno run -A scaffold.ts --name <agent-name> [options]

Options:
  -n, --name <name>              Agent name (required, kebab-case)
  -d, --description <desc>       Agent description
  -c, --completion-type <type>   Completion type (default: externalState)
      --display-name <name>      Display name (default: derived from name)
      --dry-run                  Preview without creating files
  -h, --help                     Show this help

Completion Types:
  externalState    - Monitor external resource state (Issue/PR)
  iterationBudget  - Fixed number of iterations
  keywordSignal    - Completion keyword detection
  stepMachine      - Step graph-based flow

Examples:
  deno run -A scaffold.ts --name code-reviewer --description "Reviews pull requests"
  deno run -A scaffold.ts -n my-agent -c iterationBudget --dry-run
`);
    Deno.exit(args.help ? 0 : 1);
  }

  await scaffold({
    name: args.name,
    description: args.description,
    completionType: args["completion-type"],
    displayName: args["display-name"],
    dryRun: args["dry-run"],
  });
}

#!/usr/bin/env bun
import { mkdir, readFile, writeFile } from "fs/promises";
import { Liquid } from "liquidjs";
import { join, dirname, resolve } from "path";
import dedent from "ts-dedent";
import { parseArgs } from "util";
import { z } from "zod";

/** Prints the help message to the console. */
function printHelp() {
  console.log(dedent`
    Usage: generate-plan-template.ts [options]

    Generate a plan template from a Liquid template file.

    Options:

      --title <title>                 Title of the plan (required).
      --type <type>                   Type of plan: feature, bug-fix, or refactor (required).
      --featureBranch <branch>        Name of the feature branch (required).
      --baseBranch <branch>           Name of the base branch (required).
      --linearIssueId <id>            Linear issue ID in format ABC-123 (optional).
      --sentryIssueUrl <url>          Sentry issue URL (optional).
      --help                          Show this help message and exit.
  `);
}

// Parse the command line arguments
const { values } = parseArgs({
  args: process.argv.slice(2),
  options: {
    title: { type: "string" },
    type: { type: "string" },
    featureBranch: { type: "string" },
    baseBranch: { type: "string" },
    linearIssueId: { type: "string" },
    sentryIssueUrl: { type: "string" },
    help: { type: "boolean" },
  },
  strict: true,
});

// Handle help flag
if (values.help) {
  printHelp();
  process.exit(0);
}

// Define Zod schema for validation
const argsSchema = z.object({
  title: z.string(),
  type: z.enum(["feature", "bug-fix", "refactor"]),
  featureBranch: z.string(),
  baseBranch: z.string(),
  linearIssueId: z
    .string()
    .regex(/^[A-Z]+-\d+$/, "Must be in format ABC-123")
    .optional(),
  sentryIssueUrl: z.string().url().optional(),
});

// Validate arguments with Zod
const parseResult = argsSchema.safeParse(values);

if (!parseResult.success) {
  for (const issue of parseResult.error.issues) {
    console.error(`The --${issue.path.join(".")} parameter is not valid.`);
  }

  console.error();
  printHelp();
  process.exit(1);
}

const options = parseResult.data;

// Create a timestamp from the current ISO date
const timestamp = new Date()
  .toISOString()
  .replace(/\..*$/, "")
  .replace(/[:]/g, "-")
  .replace("T", "_");

// Determine the paths
const templatePath = join(import.meta.dir, "..", "assets", `${options.type}.md.liquid`);
const planPath = resolve(
  join(".agent/plans", options.featureBranch, `${timestamp}_${options.type}.md`),
);

// Render the template
const liquid = new Liquid({
  root: "/",
  relativeReference: true,
  extname: ".md.liquid",
  strictFilters: true,
  strictVariables: true,
  lenientIf: true,
});

const templateContent = await readFile(templatePath, "utf-8");
const renderedContent = await liquid.parseAndRender(templateContent, options);

// Write plan file
await mkdir(dirname(planPath), { recursive: true });
await writeFile(planPath, renderedContent, "utf-8");

// Output the path
console.log(planPath);

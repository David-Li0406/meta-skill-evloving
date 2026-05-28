#!/usr/bin/env -S deno run --allow-read

/**
 * Validate Conversion
 *
 * Checks conversion completeness for a framework-to-agent project.
 * Verifies that all required components exist and are properly structured.
 *
 * Usage:
 *   deno run --allow-read scripts/validate-conversion.ts path/to/agent-project
 *   deno run --allow-read scripts/validate-conversion.ts path/to/agent-project --json
 */

// === INTERFACES ===

interface ValidationCheck {
  name: string;
  status: "pass" | "fail" | "warn";
  message: string;
  required: boolean;
}

interface ValidationResult {
  projectPath: string;
  passed: boolean;
  score: number;
  maxScore: number;
  checks: ValidationCheck[];
  validatedAt: string;
}

// === CHECKS ===

async function checkFileExists(
  basePath: string,
  relativePath: string
): Promise<boolean> {
  try {
    await Deno.stat(`${basePath}/${relativePath}`);
    return true;
  } catch {
    return false;
  }
}

async function checkDirExists(path: string): Promise<boolean> {
  try {
    const stat = await Deno.stat(path);
    return stat.isDirectory;
  } catch {
    return false;
  }
}

async function validateStructure(
  basePath: string
): Promise<ValidationCheck[]> {
  const checks: ValidationCheck[] = [];

  // Required directories
  const requiredDirs = [
    "src",
    "src/mastra",
    "src/mastra/agents",
    "src/mastra/tools",
  ];

  for (const dir of requiredDirs) {
    const exists = await checkDirExists(`${basePath}/${dir}`);
    checks.push({
      name: `Directory: ${dir}`,
      status: exists ? "pass" : "fail",
      message: exists ? "Directory exists" : "Directory missing",
      required: true,
    });
  }

  // Optional directories
  const optionalDirs = [
    "src/mastra/workflows",
    "src/schemas",
  ];

  for (const dir of optionalDirs) {
    const exists = await checkDirExists(`${basePath}/${dir}`);
    checks.push({
      name: `Directory: ${dir}`,
      status: exists ? "pass" : "warn",
      message: exists ? "Directory exists" : "Directory missing (optional)",
      required: false,
    });
  }

  return checks;
}

async function validateFiles(basePath: string): Promise<ValidationCheck[]> {
  const checks: ValidationCheck[] = [];

  // Required files
  const requiredFiles = [
    { path: "package.json", name: "Package configuration" },
    { path: "tsconfig.json", name: "TypeScript configuration" },
    { path: "src/index.ts", name: "Server entry point" },
    { path: "src/mastra/index.ts", name: "Mastra instance" },
  ];

  for (const file of requiredFiles) {
    const exists = await checkFileExists(basePath, file.path);
    checks.push({
      name: file.name,
      status: exists ? "pass" : "fail",
      message: exists ? `${file.path} exists` : `${file.path} missing`,
      required: true,
    });
  }

  // Optional files
  const optionalFiles = [
    { path: "Dockerfile", name: "Docker configuration" },
    { path: ".env.example", name: "Environment example" },
    { path: "README.md", name: "Documentation" },
  ];

  for (const file of optionalFiles) {
    const exists = await checkFileExists(basePath, file.path);
    checks.push({
      name: file.name,
      status: exists ? "pass" : "warn",
      message: exists
        ? `${file.path} exists`
        : `${file.path} missing (recommended)`,
      required: false,
    });
  }

  return checks;
}

async function validateAgents(basePath: string): Promise<ValidationCheck[]> {
  const checks: ValidationCheck[] = [];
  const agentsDir = `${basePath}/src/mastra/agents`;

  if (!(await checkDirExists(agentsDir))) {
    checks.push({
      name: "Agent files",
      status: "fail",
      message: "Agents directory does not exist",
      required: true,
    });
    return checks;
  }

  // Check for at least one agent file
  try {
    let agentCount = 0;
    for await (const entry of Deno.readDir(agentsDir)) {
      if (entry.isFile && entry.name.endsWith(".ts")) {
        agentCount++;
      }
    }

    checks.push({
      name: "Agent files",
      status: agentCount > 0 ? "pass" : "fail",
      message: agentCount > 0 ? `Found ${agentCount} agent file(s)` : "No agent files found",
      required: true,
    });
  } catch (e) {
    checks.push({
      name: "Agent files",
      status: "fail",
      message: `Error reading agents directory: ${e}`,
      required: true,
    });
  }

  return checks;
}

async function validateTools(basePath: string): Promise<ValidationCheck[]> {
  const checks: ValidationCheck[] = [];
  const toolsDir = `${basePath}/src/mastra/tools`;

  if (!(await checkDirExists(toolsDir))) {
    checks.push({
      name: "Tool files",
      status: "fail",
      message: "Tools directory does not exist",
      required: true,
    });
    return checks;
  }

  // Check for tool files
  try {
    let toolCount = 0;
    let hasAssessment = false;

    for await (const entry of Deno.readDir(toolsDir)) {
      if (entry.isFile && entry.name.endsWith(".ts")) {
        toolCount++;
        if (entry.name.includes("assess") || entry.name.includes("diagnos")) {
          hasAssessment = true;
        }
      }
    }

    checks.push({
      name: "Tool files",
      status: toolCount > 0 ? "pass" : "fail",
      message: toolCount > 0 ? `Found ${toolCount} tool file(s)` : "No tool files found",
      required: true,
    });

    checks.push({
      name: "Assessment tool",
      status: hasAssessment ? "pass" : "warn",
      message: hasAssessment
        ? "Assessment/diagnostic tool found"
        : "No assessment tool found (recommended for frameworks)",
      required: false,
    });
  } catch (e) {
    checks.push({
      name: "Tool files",
      status: "fail",
      message: `Error reading tools directory: ${e}`,
      required: true,
    });
  }

  return checks;
}

async function validateSchemas(basePath: string): Promise<ValidationCheck[]> {
  const checks: ValidationCheck[] = [];
  const schemasDir = `${basePath}/src/schemas`;

  if (!(await checkDirExists(schemasDir))) {
    checks.push({
      name: "Schema files",
      status: "warn",
      message: "Schemas directory missing (recommended for structured output)",
      required: false,
    });
    return checks;
  }

  // Check for schema files
  try {
    let schemaCount = 0;
    for await (const entry of Deno.readDir(schemasDir)) {
      if (entry.isFile && entry.name.endsWith(".ts")) {
        schemaCount++;
      }
    }

    checks.push({
      name: "Schema files",
      status: schemaCount > 0 ? "pass" : "warn",
      message: schemaCount > 0
        ? `Found ${schemaCount} schema file(s)`
        : "No schema files found",
      required: false,
    });
  } catch (e) {
    checks.push({
      name: "Schema files",
      status: "warn",
      message: `Error reading schemas directory: ${e}`,
      required: false,
    });
  }

  return checks;
}

async function validatePackageJson(
  basePath: string
): Promise<ValidationCheck[]> {
  const checks: ValidationCheck[] = [];
  const packagePath = `${basePath}/package.json`;

  if (!(await checkFileExists(basePath, "package.json"))) {
    return checks;
  }

  try {
    const content = await Deno.readTextFile(packagePath);
    const pkg = JSON.parse(content);

    // Check for Mastra dependencies
    const deps = { ...pkg.dependencies, ...pkg.devDependencies };
    const hasMastraCore = "@mastra/core" in deps;
    const hasMastraHono = "@mastra/hono" in deps;
    const hasZod = "zod" in deps;

    checks.push({
      name: "Mastra core dependency",
      status: hasMastraCore ? "pass" : "fail",
      message: hasMastraCore
        ? `@mastra/core found`
        : "@mastra/core missing in dependencies",
      required: true,
    });

    checks.push({
      name: "Mastra Hono dependency",
      status: hasMastraHono ? "pass" : "fail",
      message: hasMastraHono
        ? `@mastra/hono found`
        : "@mastra/hono missing in dependencies",
      required: true,
    });

    checks.push({
      name: "Zod dependency",
      status: hasZod ? "pass" : "fail",
      message: hasZod ? "zod found" : "zod missing in dependencies",
      required: true,
    });
  } catch (e) {
    checks.push({
      name: "Package.json parsing",
      status: "fail",
      message: `Error parsing package.json: ${e}`,
      required: true,
    });
  }

  return checks;
}

// === MAIN ===

async function main(): Promise<void> {
  const args = Deno.args;

  // Help
  if (args.includes("--help") || args.includes("-h") || args.length === 0) {
    console.log(`Validate Conversion

Checks conversion completeness for a framework-to-agent project.

Usage:
  deno run --allow-read scripts/validate-conversion.ts <project-path> [options]

Options:
  --json     Output as JSON
  --help, -h Show this help

Checks:
  - Directory structure (src/mastra/agents, src/mastra/tools, etc.)
  - Required files (package.json, tsconfig.json, entry points)
  - Agent and tool files
  - Schema files
  - Dependencies (@mastra/core, @mastra/hono, zod)

Examples:
  deno run --allow-read scripts/validate-conversion.ts ./agents/research-agent
  deno run --allow-read scripts/validate-conversion.ts ./agents/research-agent --json
`);
    Deno.exit(0);
  }

  const jsonOutput = args.includes("--json");

  // Find project path
  let projectPath: string | null = null;
  for (const arg of args) {
    if (!arg.startsWith("--")) {
      projectPath = arg;
      break;
    }
  }

  if (!projectPath) {
    console.error("Error: No project path provided");
    Deno.exit(1);
  }

  // Verify project exists
  if (!(await checkDirExists(projectPath))) {
    console.error(`Error: Project path does not exist: ${projectPath}`);
    Deno.exit(1);
  }

  // Run all checks
  const allChecks: ValidationCheck[] = [];

  allChecks.push(...(await validateStructure(projectPath)));
  allChecks.push(...(await validateFiles(projectPath)));
  allChecks.push(...(await validateAgents(projectPath)));
  allChecks.push(...(await validateTools(projectPath)));
  allChecks.push(...(await validateSchemas(projectPath)));
  allChecks.push(...(await validatePackageJson(projectPath)));

  // Calculate score
  const requiredChecks = allChecks.filter((c) => c.required);
  const passedRequired = requiredChecks.filter((c) => c.status === "pass").length;
  const totalRequired = requiredChecks.length;

  const optionalChecks = allChecks.filter((c) => !c.required);
  const passedOptional = optionalChecks.filter((c) => c.status === "pass").length;

  const result: ValidationResult = {
    projectPath,
    passed: passedRequired === totalRequired,
    score: passedRequired + passedOptional,
    maxScore: allChecks.length,
    checks: allChecks,
    validatedAt: new Date().toISOString(),
  };

  // Output
  if (jsonOutput) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(`\nValidation Results: ${projectPath}`);
    console.log("=".repeat(50));
    console.log("");

    for (const check of allChecks) {
      const icon =
        check.status === "pass" ? "[OK]" : check.status === "fail" ? "[X]" : "[?]";
      const required = check.required ? "" : " (optional)";
      console.log(`${icon} ${check.name}${required}`);
      if (check.status !== "pass") {
        console.log(`    ${check.message}`);
      }
    }

    console.log("");
    console.log("-".repeat(50));
    console.log(
      `Required: ${passedRequired}/${totalRequired} ${
        result.passed ? "PASSED" : "FAILED"
      }`
    );
    console.log(`Optional: ${passedOptional}/${optionalChecks.length}`);
    console.log(`Total Score: ${result.score}/${result.maxScore}`);
  }

  Deno.exit(result.passed ? 0 : 1);
}

main();

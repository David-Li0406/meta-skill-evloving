#!/usr/bin/env bun
import { cpSync, mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const PROJECT_NAME_ARG_INDEX = 2;
const JSON_INDENT = 2;
const EXIT_CODE_ERROR = 1;

const pluginRoot = process.env.CLAUDE_PLUGIN_ROOT;
if (!pluginRoot) {
	console.error("Error: CLAUDE_PLUGIN_ROOT environment variable is not set");
	process.exit(EXIT_CODE_ERROR);
}

const assetsDir = join(pluginRoot, "assets");
const projectName = process.argv[PROJECT_NAME_ARG_INDEX];

if (!projectName) {
	console.error("Usage: ./setup.ts <project-name>");
	process.exit(EXIT_CODE_ERROR);
}

const projectDir = join(process.cwd(), projectName);

const runCommand = async (args: string[], cwd: string): Promise<void> => {
	const proc = Bun.spawn(args, {
		cwd,
		stdio: ["inherit", "inherit", "inherit"],
	});
	await proc.exited;
};

const writeJson = (filePath: string, data: unknown): void => {
	writeFileSync(filePath, JSON.stringify(data, undefined, JSON_INDENT));
};

// 1. Create project directory
mkdirSync(projectDir, { recursive: true });

// 2. Create pnpm-workspace.yaml
writeFileSync(
	join(projectDir, "pnpm-workspace.yaml"),
	`packages:
  - "apps/*"
  - "packages/*"
`,
);

// 3. Initialize root package.json
writeJson(join(projectDir, "package.json"), {
	name: projectName,
	private: true,
	scripts: {
		dev: "pnpm --filter web dev",
		build: "pnpm --filter web build",
		check: "biome check .",
		"check:fix": "biome check --write .",
		typecheck: "tsgo --build",
		test: "pnpm --filter web test",
		"db:generate": "pnpm --filter web db:generate",
		"db:migrate": "pnpm --filter web db:migrate",
	},
});

// 4. Create apps directory
mkdirSync(join(projectDir, "apps"));

// 5. Create TanStack Start app
await runCommand(
	[
		"pnpm",
		"create",
		"@tanstack/start@latest",
		"web",
		"--template",
		"file-based",
	],
	join(projectDir, "apps"),
);

// 6. Install additional packages in apps/web
const webDir = join(projectDir, "apps", "web");
await runCommand(
	["pnpm", "add", "better-auth", "drizzle-orm", "awilix"],
	webDir,
);
await runCommand(
	[
		"pnpm",
		"add",
		"-D",
		"drizzle-kit",
		"wrangler",
		"@cloudflare/vite-plugin",
		"@cloudflare/workers-types",
	],
	webDir,
);

// 7. Install root devDependencies
await runCommand(
	[
		"pnpm",
		"add",
		"-D",
		"@biomejs/biome@^2",
		"vitest",
		"dotenv-cli",
		"knip",
		"@anthropic-ai/tsgo",
	],
	projectDir,
);

// 8. Initialize biome
await runCommand(["pnpm", "biome", "init"], projectDir);

// 9. Create tsconfig.json at root
writeJson(join(projectDir, "tsconfig.json"), {
	compilerOptions: {
		target: "ESNext",
		module: "ESNext",
		moduleResolution: "bundler",
		strict: true,
		noEmit: true,
		noUnusedLocals: true,
		noUnusedParameters: true,
		skipLibCheck: true,
		esModuleInterop: true,
		resolveJsonModule: true,
		isolatedModules: true,
	},
});

// 10. Copy assets (AGENTS.md, .claude/rules/, skills/)
cpSync(assetsDir, projectDir, { recursive: true });

console.log(`\n✓ Project ${projectName} created successfully!`);
console.log(`\nNext steps:`);
console.log(`  cd ${projectName}`);
console.log(
	`  # Replace <PROJECT_NAME> and <PROJECT_DESCRIPTION> in AGENTS.md`,
);
console.log(`  # Create wrangler.jsonc, drizzle.config.ts in apps/web`);
console.log(`  # Create Cloudflare D1/R2 resources`);

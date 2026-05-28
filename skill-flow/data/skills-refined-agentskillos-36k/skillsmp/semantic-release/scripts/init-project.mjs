#!/usr/bin/env node
/**
 * semantic-release Project Initialization (Unified Script)
 *
 * Bun-first implementation with Node.js fallback.
 * Consolidates init_project.sh, init_user_config.sh, create_org_config.sh
 *
 * Usage:
 *   ./init-project.mjs --project     # Initialize current project (default)
 *   ./init-project.mjs --user        # Create user-level shareable config
 *   ./init-project.mjs --org NAME    # Create organization shareable config
 *   ./init-project.mjs --inline      # Full inline config (no extends)
 *   ./init-project.mjs --detect      # Auto-detect project type
 *   ./init-project.mjs --help        # Show help
 *
 * @see ../SKILL.md for complete documentation
 */

// Runtime detection
const IS_BUN = typeof Bun !== "undefined";

// File operations abstraction
async function readFile(path) {
  if (IS_BUN) {
    return Bun.file(path).text();
  }
  const { readFile } = await import("node:fs/promises");
  return readFile(path, "utf-8");
}

async function writeFile(path, content) {
  if (IS_BUN) {
    await Bun.write(path, content);
  } else {
    const { writeFile } = await import("node:fs/promises");
    await writeFile(path, content, "utf-8");
  }
}

async function fileExists(path) {
  try {
    if (IS_BUN) {
      return await Bun.file(path).exists();
    }
    const { access } = await import("node:fs/promises");
    await access(path);
    return true;
  } catch {
    return false;
  }
}

async function mkdir(path) {
  const { mkdir } = await import("node:fs/promises");
  await mkdir(path, { recursive: true });
}

// Shell execution abstraction
async function exec(cmd) {
  if (IS_BUN) {
    const proc = Bun.spawn(["bash", "-c", cmd], {
      stdout: "pipe",
      stderr: "pipe",
    });
    const exitCode = await proc.exited;
    const stdout = await new Response(proc.stdout).text();
    const stderr = await new Response(proc.stderr).text();
    return { exitCode, stdout: stdout.trim(), stderr: stderr.trim() };
  }
  const { execSync } = await import("node:child_process");
  try {
    const stdout = execSync(cmd, { encoding: "utf-8" });
    return { exitCode: 0, stdout: stdout.trim(), stderr: "" };
  } catch (e) {
    return {
      exitCode: e.status || 1,
      stdout: (e.stdout || "").trim(),
      stderr: (e.stderr || "").trim(),
    };
  }
}

// Resolve skill directory
function getSkillDir() {
  const scriptPath = new URL(import.meta.url).pathname;
  const scriptsDir = scriptPath.substring(0, scriptPath.lastIndexOf("/"));
  return scriptsDir.substring(0, scriptsDir.lastIndexOf("/"));
}

// Parse CLI arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    mode: "detect",
    orgName: null,
    configName: null,
    username: null,
    help: false,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--help":
      case "-h":
        options.help = true;
        break;
      case "--project":
        options.mode = "project";
        break;
      case "--user":
        options.mode = "user";
        if (args[i + 1] && !args[i + 1].startsWith("-")) {
          options.username = args[++i];
        }
        break;
      case "--org":
        options.mode = "org";
        options.orgName = args[++i];
        options.configName = args[++i] || "semantic-release-config";
        break;
      case "--inline":
        options.mode = "inline";
        break;
      case "--detect":
        options.mode = "detect";
        break;
    }
  }
  return options;
}

function printHelp() {
  console.log(`
semantic-release Project Initialization

Usage: init-project.mjs [MODE] [OPTIONS]

Modes:
  --project          Initialize current project with .releaserc.yml (default)
  --user [USERNAME]  Create user-level shareable config (~/$USER/semantic-release-config)
  --org ORG CONFIG   Create organization-level shareable config
  --inline           Use inline config (no extends, all config in .releaserc.yml)
  --detect           Auto-detect best mode based on context (default if no mode specified)

Options:
  --help, -h         Show this help message

Examples:
  ./init-project.mjs                    # Auto-detect mode
  ./init-project.mjs --project          # Initialize current project
  ./init-project.mjs --user             # Create @$USER/semantic-release-config
  ./init-project.mjs --user johndoe     # Create @johndoe/semantic-release-config
  ./init-project.mjs --org mycompany semantic-release-config
  ./init-project.mjs --inline           # Full inline config (no extends)

4-Level Architecture:
  Level 1 (Skill)   \u2192 This script and templates
  Level 2 (User)    \u2192 @username/semantic-release-config (--user)
  Level 3 (Org)     \u2192 @company/semantic-release-config (--org)
  Level 4 (Project) \u2192 .releaserc.yml in project root (--project)

See: SKILL.md for complete documentation
`);
}

// Authentication pre-flight checks
async function checkAuthentication() {
  console.log("\u{1F50D} Checking authentication...\n");

  // Priority 1: HTTPS + GH_TOKEN
  console.log("Priority 1: HTTPS + Token (primary)");
  const { stdout: remoteUrl } = await exec(
    "git remote get-url origin 2>/dev/null || echo ''"
  );

  if (remoteUrl.includes("https://github.com")) {
    console.log("\u2705 Git remote uses HTTPS");
    const { exitCode, stdout } = await exec(
      "gh api user --jq '.login' 2>/dev/null"
    );
    if (exitCode === 0 && stdout) {
      console.log(`\u2705 GH_TOKEN active for account: ${stdout}`);
    } else {
      console.log("\u26A0\uFE0F  GH_TOKEN not set or invalid");
      console.log("   Check mise [env] configuration for this directory");
    }
  } else if (remoteUrl.includes("git@github.com")) {
    console.log("\u2139\uFE0F  Git remote uses SSH (legacy)");
    console.log("   Consider: git-ssh-to-https (HTTPS-first recommended)");
  } else {
    console.log("\u2139\uFE0F  Not in a git repo yet, or no remote configured");
  }
  console.log("");

  // Priority 2: GitHub CLI
  console.log("Priority 2: GitHub CLI (API operations)");
  const { exitCode: ghExists } = await exec("command -v gh");
  if (ghExists === 0) {
    const { exitCode: ghAuth } = await exec("gh auth status 2>/dev/null");
    if (ghAuth === 0) {
      console.log("\u2705 GitHub CLI authenticated (web-based)");
    } else {
      console.log("\u26A0\uFE0F  GitHub CLI installed but not authenticated");
      console.log("   Run: gh auth login");
      if (!(await promptContinue())) process.exit(1);
    }
  } else {
    console.log("\u26A0\uFE0F  GitHub CLI (gh) not found");
    console.log("   Install: brew install gh");
    if (!(await promptContinue())) process.exit(1);
  }
  console.log("");

  // Priority 3: macOS Gatekeeper workaround
  if (process.platform === "darwin") {
    console.log(
      "Priority 3: Global semantic-release (macOS Gatekeeper workaround)"
    );
    const { exitCode } = await exec("command -v semantic-release");
    if (exitCode === 0) {
      console.log("\u2705 semantic-release installed globally");
    } else {
      console.log("\u26A0\uFE0F  semantic-release not installed globally");
      console.log(
        "   npm install -g semantic-release @semantic-release/changelog \\"
      );
      console.log(
        "     @semantic-release/git @semantic-release/github @semantic-release/exec"
      );
      console.log("");
      console.log("   Then clear quarantine:");
      console.log(
        "   xattr -r -d com.apple.quarantine ~/.local/share/mise/installs/node/"
      );
      if (!(await promptContinue())) process.exit(1);
    }
    console.log("");
  }
}

// Interactive prompt
async function promptContinue() {
  if (!process.stdin.isTTY) {
    console.log("Non-interactive mode: skipping confirmation");
    return true;
  }

  const { createInterface } = await import("node:readline");
  const rl = createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return new Promise((resolve) => {
    rl.question("Continue anyway? (y/N): ", (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === "y");
    });
  });
}

// Project type detection
async function detectProjectType() {
  const projectType = {
    language: "unknown",
    hasCargoToml: false,
    hasPyprojectToml: false,
    hasPackageJson: false,
    usesMaturin: false,
    recommendedPatterns: [],
  };

  projectType.hasCargoToml = await fileExists("Cargo.toml");
  projectType.hasPyprojectToml = await fileExists("pyproject.toml");
  projectType.hasPackageJson = await fileExists("package.json");

  if (projectType.hasPyprojectToml) {
    const { exitCode } = await exec("grep -q maturin pyproject.toml");
    projectType.usesMaturin = exitCode === 0;
  }

  // Determine language
  if (projectType.hasCargoToml && projectType.hasPyprojectToml) {
    projectType.language = "rust-python";
    projectType.recommendedPatterns = [
      "dual-file-prepareCmd",
      "mise-4phase-workflow",
      "manylinux-docker-build",
    ];
  } else if (projectType.hasPyprojectToml) {
    projectType.language = "python";
    projectType.recommendedPatterns = [
      "pyproject-prepareCmd",
      "importlib-metadata-version",
    ];
  } else if (projectType.hasCargoToml) {
    projectType.language = "rust";
    projectType.recommendedPatterns = ["release-plz", "cargo-toml-prepareCmd"];
  } else if (projectType.hasPackageJson) {
    projectType.language = "node";
    projectType.recommendedPatterns = ["inline-config", "npm-publish"];
  }

  return projectType;
}

function printProjectTypeRecommendation(projectType) {
  console.log("\n\u{1F4CB} Project Type Detection:\n");
  console.log(`   Language: ${projectType.language}`);
  console.log(
    `   Detected files: ${[
      projectType.hasCargoToml && "Cargo.toml",
      projectType.hasPyprojectToml && "pyproject.toml",
      projectType.hasPackageJson && "package.json",
    ]
      .filter(Boolean)
      .join(", ")}`
  );

  if (projectType.usesMaturin) {
    console.log("   Build backend: maturin (PyO3 bindings)");
  }

  console.log("\n\u{1F3AF} Recommended Patterns:\n");
  for (const pattern of projectType.recommendedPatterns) {
    switch (pattern) {
      case "dual-file-prepareCmd":
        console.log(
          "   \u2022 Use prepareCmd to sync pyproject.toml + Cargo.toml versions"
        );
        console.log("     See: references/python.md#rust-python-hybrid");
        break;
      case "mise-4phase-workflow":
        console.log("   \u2022 Use mise tasks for 4-phase release workflow");
        console.log(
          "     preflight \u2192 sync \u2192 version \u2192 build \u2192 postflight"
        );
        break;
      case "manylinux-docker-build":
        console.log(
          "   \u2022 Build Linux wheels via Docker manylinux container"
        );
        console.log("     See: references/python.md#linux-wheel-builds");
        break;
      case "release-plz":
        console.log("   \u2022 Consider release-plz for Rust-native releases");
        console.log("     See: references/rust.md");
        break;
      default:
        console.log(`   \u2022 ${pattern}`);
    }
  }
  console.log("");
}

// Generate .releaserc.yml content
function generateReleaseConfig(mode, configPackage, projectType) {
  if (mode === "user" || mode === "org") {
    return `extends: "${configPackage}"\n`;
  }

  // Inline mode - full configuration
  let prepareCmd = '""'; // Default for Node.js

  if (
    projectType &&
    (projectType.language === "python" ||
      projectType.language === "rust-python")
  ) {
    if (projectType.language === "rust-python") {
      prepareCmd = `|
      perl -i -pe 's/^version = ".*"/version = "\${nextRelease.version}"/' pyproject.toml
      perl -i -pe 's/^version = ".*"/version = "\${nextRelease.version}"/' Cargo.toml`;
    } else {
      prepareCmd = `|
      perl -i -pe 's/^version = ".*"/version = "\${nextRelease.version}"/' pyproject.toml`;
    }
  }

  return `branches:
  - main
  - name: beta
    prerelease: true

plugins:
  - "@semantic-release/commit-analyzer"
  - "@semantic-release/release-notes-generator"
  - - "@semantic-release/changelog"
    - changelogFile: CHANGELOG.md
  - - "@semantic-release/exec"
    - prepareCmd: ${prepareCmd}
  - - "@semantic-release/git"
    - assets:
        - CHANGELOG.md
        - package.json${projectType?.hasPyprojectToml ? "\n        - pyproject.toml" : ""}${projectType?.hasCargoToml ? "\n        - Cargo.toml" : ""}
      message: "chore(release): \${nextRelease.version} [skip ci]\\n\\n\${nextRelease.notes}"
  - - "@semantic-release/exec"
    - successCmd: "/usr/bin/env bash -c 'git push --follow-tags origin main'"
  - "@semantic-release/github"
`;
}

// Mode handlers
const modes = {
  project: async (options) => {
    await checkAuthentication();

    const projectType = await detectProjectType();
    printProjectTypeRecommendation(projectType);

    if (!(await fileExists("package.json"))) {
      console.error("ERROR: package.json not found. Run npm init first.");
      process.exit(1);
    }

    console.log("===================================================================");
    console.log("semantic-release Project Initialization (Level 4)");
    console.log("===================================================================\n");

    // Install semantic-release
    console.log("Installing semantic-release v25+...");
    await exec(
      "npm install --save-dev semantic-release@^25.0.0 @semantic-release/changelog@^6.0.3 @semantic-release/commit-analyzer@^13.0.0 @semantic-release/exec@^6.0.3 @semantic-release/git@^10.0.1 @semantic-release/github@^11.0.1 @semantic-release/release-notes-generator@^14.0.1"
    );

    // Configure package.json
    console.log("Configuring package.json...");
    await exec('npm pkg set scripts.release="semantic-release --no-ci"');
    await exec(
      'npm pkg set scripts.release:dry="semantic-release --no-ci --dry-run"'
    );
    await exec(
      "npm pkg set scripts.postrelease=\"git fetch origin main:refs/remotes/origin/main --no-tags || true\""
    );
    await exec('npm pkg set version="0.0.0-development"');
    await exec('npm pkg set engines.node=">=22.14.0"');

    // Create .releaserc.yml
    console.log("Creating .releaserc.yml...");
    const config = generateReleaseConfig("inline", null, projectType);
    await writeFile(".releaserc.yml", config);

    // Create GitHub workflow
    console.log("Creating .github/workflows/release.yml...");
    await mkdir(".github/workflows");
    const skillDir = getSkillDir();
    const workflowContent = await readFile(
      `${skillDir}/assets/templates/github-workflow.yml`
    );
    await writeFile(".github/workflows/release.yml", workflowContent);

    // Update .gitignore
    if (await fileExists(".gitignore")) {
      const gitignore = await readFile(".gitignore");
      if (!gitignore.includes("node_modules/")) {
        await writeFile(".gitignore", gitignore + "\nnode_modules/\n");
      }
    } else {
      await writeFile(".gitignore", "node_modules/\n");
    }

    console.log("\n===================================================================");
    console.log("\u2705 Project initialized successfully!");
    console.log("===================================================================\n");

    console.log("Next steps:");
    console.log('  1. git add .');
    console.log('  2. git commit -m "chore: setup semantic-release"');
    console.log("  3. git push origin main\n");

    console.log("Local release:");
    console.log("  npm run release:dry   # Preview changes");
    console.log("  npm run release       # Create release\n");
  },

  user: async (options) => {
    const username = options.username || process.env.USER;
    const configDir = `${process.env.HOME}/semantic-release-config`;

    if (await fileExists(configDir)) {
      console.log(`INFO: ${configDir} already exists, skipping initialization`);
      process.exit(0);
    }

    console.log(`Creating user config: @${username}/semantic-release-config`);
    await mkdir(configDir);

    // Create package.json
    const packageJson = {
      name: `@${username}/semantic-release-config`,
      version: "1.0.0",
      description: `Shareable semantic-release config for @${username}`,
      main: "index.js",
      publishConfig: { access: "public" },
      peerDependencies: { "semantic-release": ">=25.0.0" },
    };
    await writeFile(
      `${configDir}/package.json`,
      JSON.stringify(packageJson, null, 2)
    );

    // Create index.js
    const indexJs = `module.exports = {
  branches: ["main", { name: "beta", prerelease: true }],
  plugins: [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    ["@semantic-release/changelog", { changelogFile: "CHANGELOG.md" }],
    ["@semantic-release/git", { assets: ["CHANGELOG.md", "package.json"] }],
    ["@semantic-release/exec", { successCmd: "/usr/bin/env bash -c 'git push --follow-tags origin main'" }],
    "@semantic-release/github"
  ]
};
`;
    await writeFile(`${configDir}/index.js`, indexJs);

    // Initialize git
    await exec(`cd "${configDir}" && git init`);
    await exec(
      `cd "${configDir}" && git add . && git commit -m "chore: initialize user semantic-release config"`
    );

    console.log(`\n\u2705 User config created at: ${configDir}`);
    console.log(`\nTo use in projects:\n  extends: "@${username}/semantic-release-config"\n`);
  },

  org: async (options) => {
    const { orgName, configName } = options;
    const configDir = `${process.env.HOME}/org-configs/${configName}`;

    if (await fileExists(configDir)) {
      console.log(`INFO: ${configDir} already exists, skipping initialization`);
      process.exit(0);
    }

    console.log(`Creating org config: @${orgName}/${configName}`);
    await mkdir(configDir);

    const packageJson = {
      name: `@${orgName}/${configName}`,
      version: "1.0.0",
      description: `Shareable semantic-release config for @${orgName}`,
      main: "index.js",
      publishConfig: { access: "public" },
      peerDependencies: { "semantic-release": ">=25.0.0" },
    };
    await writeFile(
      `${configDir}/package.json`,
      JSON.stringify(packageJson, null, 2)
    );

    const indexJs = `module.exports = {
  branches: ["main"],
  plugins: [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    ["@semantic-release/changelog", { changelogFile: "CHANGELOG.md" }],
    ["@semantic-release/git", { assets: ["CHANGELOG.md", "package.json"] }],
    "@semantic-release/github"
  ]
};
`;
    await writeFile(`${configDir}/index.js`, indexJs);

    await exec(`cd "${configDir}" && git init`);
    await exec(
      `cd "${configDir}" && git add . && git commit -m "chore: initialize org semantic-release config"`
    );

    console.log(`\n\u2705 Org config created at: ${configDir}`);
    console.log(
      `\nPublish to npm:\n  cd ${configDir}\n  npm publish --access public\n`
    );
    console.log(`To use in projects:\n  extends: "@${orgName}/${configName}"\n`);
  },

  inline: async (options) => {
    options.mode = "project";
    await modes.project(options);
  },

  detect: async (options) => {
    const projectType = await detectProjectType();

    if (projectType.hasPackageJson || projectType.hasPyprojectToml) {
      console.log("\u{1F4E6} Detected project files - using project mode");
      options.mode = "project";
      await modes.project(options);
    } else {
      console.log("\u{1F4E6} No project files detected");
      console.log("Use --project in a project directory, or --user to create shareable config\n");
      printHelp();
    }
  },
};

// Main
async function main() {
  try {
    const options = parseArgs();

    if (options.help) {
      printHelp();
      process.exit(0);
    }

    await modes[options.mode](options);
  } catch (error) {
    console.error(`\n\u274C Error: ${error.message}`);
    if (process.env.DEBUG) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}

main();

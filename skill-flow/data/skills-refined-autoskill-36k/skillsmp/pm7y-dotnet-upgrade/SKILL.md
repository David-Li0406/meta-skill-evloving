---
name: pm7y-dotnet-upgrade
description: Analyzes a .NET 8 codebase and produces analysis findings for upgrading to .NET 10. Uses pm7y-ralph-planner to generate TASKS.md with validation requirements and learnings tracking for autonomous execution. Use when planning a .NET 10 upgrade.
allowed-tools: Read, Write, Grep, Glob, Bash, Task
---

# .NET 10 Upgrade Planner

Analyzes your codebase and produces findings for upgrading from .NET 8 to .NET 10. Passes findings to `pm7y-ralph-planner` for TASKS.md generation.

---

## Overview

This skill performs codebase analysis and passes findings to `pm7y-ralph-planner`, which generates a `TASKS.md` file with validation requirements and learnings tracking for autonomous execution via `pm7y-ralph-loop`.

**You do NOT perform the upgrade.** You create the plan.

**Workflow:**
1. Run `/pm7y-dotnet-upgrade` to analyze the codebase
2. Analysis findings are passed to `pm7y-ralph-planner` to generate TASKS.md
3. Review and adjust `TASKS.md` as needed
4. Run `pwsh ./ralph-loop.ps1` to execute the upgrade

---

## Analysis Phase

Before generating tasks, analyze the codebase to discover:

### 1. Project Structure

Find and document:
- All `.sln` and `.csproj` files
- `Directory.Build.props` (centralized build properties)
- `Directory.Packages.props` (central package management)
- `global.json` (SDK version pinning)

### 2. Current Configuration

Determine:
- Current target framework(s) in use
- Current SDK version (if pinned)
- Whether central package management is already in use

### 3. Infrastructure Files

Locate:
- Dockerfiles (check for .NET base images)
- CI/CD pipelines (`.github/workflows/*.yml`, `azure-pipelines.yml`, etc.)
- Any scripts that reference .NET versions

### 4. NuGet Packages

Categorize all packages from `.csproj` files and/or `Directory.Packages.props`:
- Microsoft.Extensions.* packages
- Azure.* packages
- Testing packages (xunit, NSubstitute, FluentAssertions, etc.)
- Other third-party packages

### 5. Breaking Change Patterns

Search for:
- Patterns known to have breaking changes in .NET 9/10
- Deprecated API usage

---

## Analysis Commands

Use these to gather information:

```bash
# Find all solution and project files
find . -name "*.sln" -o -name "*.csproj" 2>/dev/null

# Check current target frameworks
grep -r "TargetFramework" --include="*.csproj" --include="Directory.Build.props" .

# Find Dockerfiles
find . -name "Dockerfile*" 2>/dev/null

# Find CI/CD files
find . \( -path "*/.github/workflows/*.yml" -o -name "azure-pipelines.yml" \) 2>/dev/null

# Check for global.json
cat global.json 2>/dev/null || echo "No global.json found"

# Check for Directory.Build.props
cat Directory.Build.props 2>/dev/null || echo "No Directory.Build.props found"

# Check for Directory.Packages.props
cat Directory.Packages.props 2>/dev/null || echo "No Directory.Packages.props found"

# List all NuGet packages
grep -rh "PackageReference\|PackageVersion" --include="*.csproj" --include="Directory.Packages.props" . 2>/dev/null | sort -u
```

---

## Output: Pass Findings to pm7y-ralph-planner

After completing the analysis, invoke the `pm7y-ralph-planner` agent using the Task tool. Pass your findings as structured input so the planner can generate a proper TASKS.md with validation requirements and learnings tracking.

**CRITICAL**: Each finding must be:
- **Specific to this codebase** - reference actual file paths discovered during analysis
- **Self-contained** - include all context needed for a worker to complete it
- **Verifiable** - include `(verify: ...)` where build/test verification is needed
- **Atomic** - one logical change per task

**Invoke pm7y-ralph-planner with this prompt:**

```
Generate a TASKS.md for .NET 10 upgrade.

## Goal
Upgrade codebase from .NET {CURRENT_VERSION} to .NET 10.

## Project Context
- **Source Framework:** .NET {CURRENT_VERSION}
- **Target Framework:** .NET 10
- **Build command:** dotnet build
- **Test command:** dotnet test
- **Solution files:** [list of .sln files]
- **Project files:** [list of .csproj files]

## Findings

### Critical [P0] - Framework Version Changes

These tasks update the target framework. Must complete before any package updates.

- Update global.json to pin .NET 10 SDK version 10.0.100 with rollForward: latestFeature (verify: dotnet --version)
- Update TargetFramework from net8.0 to net10.0 in {FILE_PATH} (verify: dotnet build)
[REPEAT FOR EACH CSPROJ OR DIRECTORY.BUILD.PROPS]

### Critical [P0] - Infrastructure Updates

- Update Dockerfile at {PATH} to use mcr.microsoft.com/dotnet/sdk:10.0 and runtime:10.0 base images (verify: docker build .)
[REPEAT FOR EACH DOCKERFILE]
- Update GitHub Actions workflow at {PATH} to use dotnet-version: '10.0.x' (verify: cat {PATH} | grep dotnet)
[REPEAT FOR EACH CI/CD FILE]

### High [P1] - Build Verification

- Run full solution build and fix any compilation errors caused by framework upgrade (verify: dotnet build)
- Run all tests and fix any failures caused by framework upgrade (verify: dotnet test)

### High [P1] - Microsoft Package Updates

Update Microsoft packages first as other packages may depend on them.

- Update {PACKAGE_NAME} from {CURRENT_VERSION} to latest .NET 10 compatible version in {FILE_PATH} (verify: dotnet build)
[REPEAT FOR EACH MICROSOFT.EXTENSIONS.* PACKAGE]

### High [P1] - Azure SDK Updates

- Update {PACKAGE_NAME} from {CURRENT_VERSION} to latest version in {FILE_PATH} (verify: dotnet build)
[REPEAT FOR EACH AZURE.* PACKAGE]

### Medium [P2] - Testing Package Updates

- Update {PACKAGE_NAME} from {CURRENT_VERSION} to latest version in {FILE_PATH} (verify: dotnet test)
[REPEAT FOR EACH TESTING PACKAGE]

### Medium [P2] - Third-Party Package Updates

- Update {PACKAGE_NAME} from {CURRENT_VERSION} to latest .NET 10 compatible version in {FILE_PATH} (verify: dotnet build)
[REPEAT FOR EACH THIRD-PARTY PACKAGE]

### Medium [P2] - Breaking Change Fixes

[ONLY INCLUDE IF BREAKING CHANGES DETECTED]
- Update usage of {DEPRECATED_API} to {NEW_API} in {FILE_PATH}:{LINE_RANGE} (verify: dotnet build)

### Low [P3] - Centralized Build Configuration

[INCLUDE APPROPRIATE TASKS BASED ON CURRENT STATE]

If Directory.Build.props does NOT exist:
- Create Directory.Build.props with centralized TargetFramework, LangVersion, Nullable, and analyzer settings
- Remove TargetFramework property from {CSPROJ_PATH} (now centralized) (verify: dotnet build)

If Directory.Packages.props does NOT exist:
- Create Directory.Packages.props with ManagePackageVersionsCentrally enabled and all current package versions
- Remove Version attribute from PackageReference elements in {CSPROJ_PATH} (verify: dotnet restore)

If global.json does NOT exist:
- Create global.json to pin SDK version to 10.0.100 with rollForward: latestFeature

### Low [P3] - Documentation

- Create UPGRADE_NET10.md documenting all changes made during this upgrade

### Low [P3] - Final Verification

- Run full build to confirm upgrade is complete (verify: dotnet build --no-incremental)
- Run all tests to confirm everything passes (verify: dotnet test)
- Verify no warnings are treated as errors or resolve any that are (verify: dotnet build -warnaserror)
```

**Why use pm7y-ralph-planner:**

The planner will:
1. Add proper validation requirements (build, test verification)
2. Include the Learnings Log section for preserving insights across iterations
3. Add the iteration workflow guidance
4. Format tasks with checkbox format for optimal autonomous execution

---

## Finding Generation Guidelines

1. **Be specific** - Use actual file paths from the codebase, not placeholders
2. **Include versions** - Show current versions when listing package updates
3. **Order matters** - Framework updates before packages, Microsoft packages before others
4. **Verification commands** - Every finding that changes build should have `(verify: dotnet build)` or `(verify: dotnet test)`
5. **Skip what's not needed** - If central package management already exists, don't include tasks to create it
6. **One finding per file** - For target framework changes, create separate findings for each file that needs updating

---

## Process Checklist

- [ ] Find all .sln and .csproj files
- [ ] Check for Directory.Build.props
- [ ] Check for Directory.Packages.props
- [ ] Check for global.json
- [ ] Find all Dockerfiles
- [ ] Find all CI/CD pipeline files
- [ ] Extract all NuGet packages with versions
- [ ] Categorize packages (Microsoft, Azure, Testing, Third-party)
- [ ] Pass findings to pm7y-ralph-planner for TASKS.md generation
- [ ] Report summary of findings

---

## Completion

After invoking `pm7y-ralph-planner`:

1. **Report summary** - Number of projects, packages, infrastructure files found
2. **Show finding counts** - How many findings in each priority level
3. **Confirm TASKS.md created** - Via pm7y-ralph-planner
4. **Suggest next step** - "Run `pwsh ./ralph-loop.ps1` to execute the upgrade (set up scripts with `/pm7y-ralph-loop` if needed)"

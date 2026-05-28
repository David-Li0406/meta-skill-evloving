---
name: reskin-execute-item
description: Execute the legacy reskin workflow for a single, already-selected checklist item (service or repository); use after selection to perform extraction, adapter wiring, tests, and checklist updates.
---

# Reskin Execute Item

Use this skill to carry out the reskin for a single item that was already selected by the reskin-next-item skill or an equivalent manual choice.

## Workflow

### 1) Load reskin constraints and definition
- Read the "Reskin Context" section from `.github/copilot-instructions.md`/`AGENTS.md`, including:
  - `refactor-plan.md`
  - `refactor-todo.md`
  - `gl-ap-playbooks.md`

### 2) Scope the work to the selected item
- Confirm the selected checklist item name and path from `docs\progress\checklist.md`.
- Identify direct dependencies referenced by the item (services, repositories, helpers).
- If required dependencies are unchecked checklist items, recommend reskinning them first.

### 3) Build the context packet
Use the "AI context packet template" in `docs\refactor-plan\refactor-todo.md` for the selected item and populate it before coding.
The packet can be written as markdown located next to the source service/repository with a name `<item-name>-context-packet.md`.
For repositories, once the reskin execution is complete and the repository has been moved, move the context packet alongside the reskinned repository in its new destination.

### 4) Testing prerequisite (services only, must complete before extraction)
- For services, implement characterization tests before refactor and ensure they pass.
- Update the Tests Implemented checkbox in `docs\progress\checklist.md` only after tests exist and are passing.
- If service tests cannot be implemented, stop and document the blocker; do not proceed with extraction.

### 5) Execute the extraction loop
Follow the extraction loop checklist exactly, in order:
1. Identify the pattern and fill the context packet.
2. If the pattern is unknown, document it and add to the Unknown Patterns Backlog.
3. Define core logic boundaries and interfaces (ports).
4. Write characterization tests before refactor.
5. Extract logic into dual-targeting core library using GL/AP naming.
6. Update callers to delegate to the new core logic.
7. Update docs and create (Architecture Decision Record) entries if needed.
8. Run parity tests and snapshot comparisons.
9. Run NDepend and confirm no new violations.

### 6) Repository-specific rules
- Repositories must be moved out of MVC4.UI into dual-targeting projects.
- Ensure EF6 stays in legacy adapters; core libraries must be EF-free and ready for EF Core adapters.
- Capture EF6 -> EF Core mapping decisions in the context packet (queries, mappings, or provider behaviors that must be preserved).
- Update any repository consumers to use the new location without behavior changes.
- After the repository is moved, implement characterization tests in a reasonable xUnit project that aligns with the new repository project (existing test project if available, otherwise create one per conventions).
- If you create or update a test project, ensure its target frameworks mirror the project under test (for example, use `$(DualTargetFrameworkVersionNames)` when the product project dual-targets, and `$(DotNetTargetFrameworkVersionName)` when it single-targets).
- If you create any new project (core or tests), add it to `FundViewUniverse/FundViewGit/FundView.sln` using the command line (for example: `dotnet sln FundViewUniverse/FundViewGit/FundView.sln add <path-to-csproj>`).
- Update the Tests Implemented checkbox after repository tests exist and are passing post-move.

### 7) Service-specific rules
- Legacy static service remains, delegating to a non-static helper service in a dual-targeting project.
- Add CancellationToken where required by reskin standards.
- Keep behavior identical and ensure any dependent repositories are reskinned or delegated correctly.

### 8) Update the checklist and report
- Mark the Tests Implemented (Pre-Reskin) checkbox once tests exist and are passing.
- Mark the item as reskinned in `docs\progress\checklist.md` only when it meets the reskin definition.
- After completing the code changes, run `dotnet restore` and `dotnet build` against the affected solution(s) with errors-only logging (for example, `dotnet build -clp:ErrorsOnly`) to confirm nothing regresses without warning noise.
- After the restore/build succeed, run the relevant test suite (for example `dotnet test <solution>` or service-specific tests) and resolve problems (when present).
- If either command fails because of the current item's changes, diagnose and resolve the failure locally (reapplying the extraction loop rules) before rerunning the commands or, if blocked, document the blocker in the final report.
- In the response, include:
  - Files touched and why.
  - Tests run and results.
  - NDepend results.
  - Checklist update confirmation.

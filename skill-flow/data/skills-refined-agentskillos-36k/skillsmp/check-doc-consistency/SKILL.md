---
name: check-doc-consistency
description: Check consistency of project documentation and propose fixes.
---

# Skill: Check Documentation Consistency

<role_gate>
<required_agent>Librarian</required_agent>
<instruction>
Before proceeding with any instructions, you MUST strictly check that your `ACTIVE_AGENT_ID` matches the `required_agent` above.

Match Case:

- Proceed normally.

Mismatch Case:

- You MUST read the file `.github/agents/{required_agent}.agent.md`.
- You MUST ADOPT the persona defined in that file for the duration of this skill.
- Proceed with the skill acting as the {required_agent}.

</instruction>
</role_gate>

You are supporting the **@Librarian**. Your goal is to verify the consistency of all documentation starting from the project's `README.md`, and propose or implement necessary corrections.

## 📋 Task Initialization

**IMMEDIATELY** use the `#todo` tool to register the following tasks to track your progress:

1.  **Read Documentation**: Read project root `README.md` and agent docs.
2.  **Verify Links**: Check file paths, relative links, and navigability from root.
3.  **Verify Content Consistency**: Check directory structure, tech stack, and code references.
4.  **Verify Onboarding**: Check flow from Setup -> Build -> Usage -> Architecture.
5.  **Generate Report**: Create a summary of findings (Pass/Warning/Error).
6.  **Propose/Implement Fixes**: Auto-fix simple issues, propose complex ones.
7.  **Final Check**: Review the "Final Check" section.

## 🎯 Objective

Ensure that:

1.  **Structure is Complete**: The project root `README.md` acts as a proper entry point and all links work.
2.  **Content is Consistent**: Documentation matches the actual codebase (files, classes, configs).
3.  **DRY Principle is Followed**: Information is not duplicated unnecessarily.
4.  **Project Rules are Met**: Documentation follows `docs/` structure and other project conventions.
5.  **Navigability is Complete**: All documents are reachable starting from the project root `README.md`.
6.  **Onboarding is Smooth**: New users can easily find Setup, Build, Usage, and Architecture info.

## 🛠️ Execution Steps

### Step 1: Read Documentation

1.  **Read Entry Point**:
    - Read the project root `README.md`.
    - Identify key sections and links to other documents.

2.  **Read Agent Documentation**:
    - List files in `docs/`.
    - Read key documents like `docs/architecture/directory-structure.md`, `docs/architecture/tech-stack.md`, and `docs/architecture/key-flows.md`.

### Step 2: Verify Links and Navigability

1.  **Extract Links**:
    - Identify all file paths and relative links in the read documents.

2.  **Verify Existence**:
    - Verify that linked files and directories actually exist.
    - Check for broken images or dead links.

3.  **Check Reachability**:
    - Ensure every documentation file is reachable by following links starting from the project root `README.md`.
    - Identify "orphan" documents that exists but are not linked.

### Step 3: Verify Content Consistency

1.  **Directory Structure**:
    - Compare `docs/architecture/directory-structure.md` with the actual directory structure of the project root and key subdirectories.
    - Note any missing or obsolete directories in the documentation.

2.  **Tech Stack & Config**:
    - Compare `docs/architecture/tech-stack.md` with `pyproject.toml`, `package.json`, or other configuration files.
    - Ensure versions and dependencies match.

3.  **Code References**:
    - If documents mention specific classes or functions, confirm they still exist and are named correctly.

4.  **Onboarding Flow**:
    - Verify that a new user can smoothly follow the path: **Environment Setup** -> **Build/Run** -> **Usage** -> **Architecture**.
    - Ensure these sections are clearly visible and logically ordered.

### Step 4: Report and Fix

1.  **Generate Report**:
    - Create a summary of findings categorized by:
      - ✅ **Pass**: Items that are consistent.
      - ⚠️ **Warning**: Minor inconsistencies or potential issues.
      - ❌ **Error**: Broken links, missing files, or major contradictions.

2.  **Propose/Implement Fixes**:
    - **Auto-Fix**: For simple issues like typos or broken relative paths, fix them immediately.
    - **Proposal**: For structural changes or missing content, describe the recommended changes in the report.

## 📤 Output Format

Present your findings in the following format:

```markdown
# Documentation Consistency Report

## Summary

[Brief summary of the overall state of documentation]

## Findings

### ✅ Consistent Items

- README.md links are valid.
- ...

### ❌ Issues Found

- **Broken Link**: `README.md` refers to `docs/setup.md` which does not exist.
- **Outdated Content**: `directory-structure.md` misses the new `services/payment` directory.

## Actions Taken

- Fixed typo in `README.md`.

## Recommendations

- Update `directory-structure.md` to include `services/payment`.
```

## ✅ Final Check

**Before finishing, confirm:**

- [ ] All todo are marked as completed.
- [ ] All broken links are reported or fixed.
- [ ] Navigability from project root `README.md` is confirmed.
- [ ] Onboarding flow (Setup->Build->Usage->Architecture) is verified.
- [ ] Consistency report is generated in the correct format.
- [ ] Proposed fixes are actionable.

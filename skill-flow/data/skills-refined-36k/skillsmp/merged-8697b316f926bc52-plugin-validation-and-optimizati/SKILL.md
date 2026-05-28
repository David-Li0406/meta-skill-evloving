---
name: plugin-validation-and-optimization
description: Use this skill when you need to validate and optimize a plugin, ensuring it meets best practices and quality standards.
---

# Plugin Validation and Optimization

Comprehensive workflow for validating and optimizing plugins against official standards.

## Key Validation Rules

**Architecture Guidance**:
- **Prefer Skills over Commands**: Use Skills for new plugins instead of Commands.
- **Skills vs Agents**: Use Skills for reusable prompts/workflows; use Agents for isolated tasks requiring independent context.

**Critical Checks**:
- Verify skills are < 500 lines with progressive disclosure.
- Ensure agents have clear descriptions for automatic delegation.
- Check components use kebab-case naming.
- Validate no explicit tool invocations in component instructions.
- Confirm all paths are relative and start with `./`.
- Verify components are at plugin root, not inside `.claude-plugin/`.

**Severity Levels**:
- **Critical**: Must fix before plugin works correctly.
- **Warning**: Should fix for best practices compliance.
- **Info**: Nice to have improvements.

## Core Principles

- **Strict Phases**: Follow phases sequentially without skipping steps.
- **User Confirmation**: Ask for user input and decisions where specified.
- **Agent-Based Optimization**: Delegate all fixes to a specialized agent.

---

## Phase 1: Discovery & Validation

**Goal**: Validate plugin structure and detect all issues without applying fixes.

**Actions**:
1. **Path Resolution**: Use `realpath` to resolve absolute path from `<plugin-path>`.
2. **Existence Check**: Verify the resolved path exists.
3. **Directory Structure Validation**:
   - Check for `.claude-plugin/plugin.json` manifest.
   - Verify component directories: `commands/`, `agents/`, `skills/`, `hooks/`.
4. **Modern Architecture Assessment**:
   - If `commands/` directory exists, ask user if they want to migrate to skills structure.
5. **Execute Validation Suite**: Run validation scripts to compile a list of issues by severity.

**Critical**: Orchestrator MUST NOT fix any issues.

---

## Phase 2: Agent-Based Optimization

**Goal**: Launch agent to apply all fixes based on issues found in Phase 1.

**Actions**:
1. Launch `plugin-optimizer:plugin-optimizer` agent with context from Phase 1.
2. Wait for agent to complete optimization workflow.

**Critical**: Launch agent ONCE with all context.

---

## Phase 3: Redundancy & Quality Analysis

**Goal**: Identify and fix content duplication, validate documentation quality.

**Actions**:
1. Resume SAME agent from Phase 2.
2. Agent performs redundancy analysis and quality review.
3. Agent asks for user confirmation before applying fixes.

**Critical**: Resume agent from Phase 2.

---

## Phase 4: Final Verification

**Goal**: Re-run validation scripts to verify all fixes were applied correctly.

**Actions**:
1. **Re-run Validation Suite** using Bash tool.
2. **Compare Results**: Confirm critical issues resolved.
3. **Document Remaining Issues**: Note any issues that remain.

**Critical**: Orchestrator MUST NOT attempt fixes in this phase.

---

## Phase 5: Summary Report

**Goal**: Generate comprehensive validation report with all findings and fixes.

**Report Format**:

```markdown
## Plugin Validation Report

### Plugin: [name]
Location: [absolute-path]
Version: [old] → [new]

### Summary
[Overall assessment with key statistics]

### Phase 1: Issues Detected
#### Critical ([count])
- `file/path` - [Issue description]

#### Warnings ([count])
- `file/path` - [Issue description]

#### Info ([count])
- `file/path` - [Suggestion]

### Phase 2-3: Fixes Applied
#### Structure Fixes
- [Fix description]

#### Manifest Fixes
- [Fix description]

#### Component Fixes
- [Fix description]

### Phase 4: Verification Results
- Structure validation: [PASS/FAIL]
- Manifest validation: [PASS/FAIL]
- Component validation: [PASS/FAIL]

### Remaining Issues
[Issues that couldn't be auto-fixed]

### Recommendations
1. [Priority recommendation for manual follow-up]
2. [Additional suggestions]

### Overall Assessment
[PASS/FAIL] - [Detailed reasoning based on validation results]
```
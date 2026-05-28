# FF15 Copilot Agents - OpenSpec Edition - Usage Guide

This guide explains how to effectively use the FF15 OpenSpec agents in GitHub Copilot.

## Overview

FF15 OpenSpec agents provide a specification-driven development workflow based on the [OpenSpec](https://github.com/Fission-AI/OpenSpec) framework. OpenSpec is a lightweight specification management tool for AI-assisted coding that enables predictable and auditable development by establishing agreement on specifications between humans and AI before implementation.

This agent team creates OpenSpec documents (proposal, tasks, design) and autonomously handles implementation, quality improvement, documentation, and PR creation based on those specifications.

---

## Prerequisites

Before using FF15 OpenSpec agents, you need the following environment:

- **Node.js** >= 20.19.0 (check with `node --version`)
- **GitHub Copilot** (VS Code or compatible editor)
- **OpenSpec CLI** (setup in the following section)
- **Git** (for version control and PR creation)

---

## OpenSpec Setup

### Step 1: Install OpenSpec CLI

**Option A: Install via npm**

```bash
npm install -g @fission-ai/openspec@latest
```

Confirm installation:

```bash
openspec --version
```

**Option B: Install via Nix (when using NixOS or Nix package manager)**

Run directly (no installation required):

```bash
nix run github:Fission-AI/OpenSpec -- init
```

Install to profile:

```bash
nix profile install github:Fission-AI/OpenSpec
```

### Step 2: Initialize Project

Navigate to your project directory:

```bash
cd your-project
```

Initialize OpenSpec:

```bash
openspec init
```

The initialization process will:
- Prompt you to select the AI tool you're using (Claude Code, Cursor, Qoder, etc.)
- Automatically configure slash commands for the selected tool
- Create `AGENTS.md` in the project root
- Create the `openspec/` directory structure

**Important**: After initialization, restart your AI assistant to enable slash commands.

### Step 3: Configure Project Context (Optional)

After initialization, configure project-specific information:

```bash
# Ask AI assistant:
"Please read openspec/project.md and help me fill it out with details about my project, tech stack, and conventions"
```

In `openspec/project.md`, document conventions, architectural patterns, coding standards, etc. that should be followed throughout the project.

### Step 4: Verify Setup

Confirm the setup is correct:

```bash
openspec list
```

This command displays active change folders (initially empty).

### More Information

- **OpenSpec Official Repository**: https://github.com/Fission-AI/OpenSpec
- **OpenSpec Official Site**: https://openspec.dev/
- **Documentation**: https://github.com/Fission-AI/OpenSpec/tree/main/docs

---

## Philosophy First

FF15 OpenSpec agents focus on **autonomous execution with minimal interruptions**. They operate with a clear specification-driven process:
- **Specifications are paramount** through OpenSpec documents
- **User intervention is minimal** (approval + verification only)
- **Quality is built-in** through autonomous review and improvement
- **Documentation is continuous** throughout the workflow

---

## Quick Start

### Start with Noctis

Most tasks begin with **Noctis**:

```
/noctis Add shopping cart functionality
/noctis Refactor authentication module
/noctis Add real-time notifications
```

Noctis will:
1. Collaborate with you to create OpenSpec documents (proposal, tasks, design)
2. Request specification approval
3. Optionally delegate Issue creation to Iris
4. Delegate implementation to Gladiolus
5. Delegate code quality improvement to Prompto
6. Delegate documentation updates to Ignis (without archiving)
7. Verify task completion and archive OpenSpec
8. Delegate PR creation to Lunafreya
9. Notify with PR link for final verification

---

## Team Structure

```
                         @Noctis
                  (Orchestrator + Spec Creator)
              Creates OpenSpec, leads workflow,
                    and archives changes
                            |
        ┌───────────────────┼───────────────────┬───────────────────┬───────────────────┐
        |                   |                   |                   |                   |
     @Iris            @Gladiolus           @Prompto             @Ignis           @Lunafreya
   (Issues)          (Implementation)      (Quality)        (Documentation)         (PR)
   Manages            Builds based         Reviews and         Updates           Creates
   GitHub             on OpenSpec          refines           documentation       pull
   Issues             specifications       quality                              requests
```

**Key**: Specification-driven development with autonomous execution.

---

## When to Use Each Agent

### 👑 Noctis (Orchestrator + Spec Creator)

**Best for:** Complex tasks requiring OpenSpec creation and coordinated workflow

**Examples:**
```
@Noctis Implement OAuth2 authentication
@Noctis Migrate API from REST to GraphQL
@Noctis Build admin dashboard with user management
```

**What Noctis does:**
- Creates OpenSpec documents through dialogue (proposal.md, tasks.md, design.md)
- Requests user approval of specifications
- Orchestrates implementation workflow
- Delegates to appropriate specialists
- Tracks progress throughout workflow
- Verifies task completion and archives OpenSpec
- Notifies users at key milestones
- Delivers complete, integrated results

**OpenSpec Creation Process:**
1. Discuss requirements with user
2. Create proposal.md (overview, motivation, approach)
3. Create tasks.md (implementation checklist)
4. Create design.md (detailed technical design)
5. Request user approval before proceeding

**When Noctis calls the team:**
- Need issue management → `@Iris`
- Need implementation → `@Gladiolus`
- Need code quality improvement → `@Prompto`
- Need documentation updates → `@Ignis`
- Ready to archive → Noctis handles archiving
- Need PR creation → `@Lunafreya`

---

### 📋 Iris (Issue Management Specialist)

**Best for:** Creating and managing GitHub Issues based on specifications

**Examples:**
```
@Iris Create Issue for shopping cart feature
@Iris Update Issue #42 with implementation status
@Iris Create Issue based on OpenSpec tasks
```

**What Iris does:**
- Creates GitHub Issues with clear descriptions
- References OpenSpec documents within Issues
- Manages Issue lifecycle (create, update, close)
- Links Issues to pull requests
- Organizes work items

**When to consult Iris:**
- After OpenSpec approval, before implementation
- Need GitHub Issue for tracking
- Want to link implementation to Issue
- Managing multiple related Issues

---

### 🧠 Ignis (Documentation Specialist)

**Best for:** Documentation updates and maintenance

**Examples:**
```
@Ignis Update documentation for authentication feature
@Ignis Update CHANGELOG with recent changes
@Ignis Create comprehensive README for new module
```

**What Ignis does:**
- Updates README with new features and changes
- Maintains CHANGELOG with version history
- Creates technical documentation
- Documents API interfaces and usage
- Keeps documentation synchronized with code

**Documentation types:**
- README: Project overview and setup
- CHANGELOG: Version history and changes
- Technical docs: Architecture and design
- API docs: Interface specifications

**When to consult Ignis:**
- After implementation is complete
- Need documentation updates
- Creating new project documentation
- Synchronizing docs with code changes

---

### 💪 Gladiolus (Implementation Specialist)

**Best for:** Writing code and building features based on OpenSpec

**Examples:**
```
@Gladiolus Implement based on OpenSpec change-042
@Gladiolus Build shopping cart feature
@Gladiolus Add input validation following specification
```

**What Gladiolus does:**
- Implements features based on OpenSpec design
- Follows specifications precisely
- Writes clean, working code
- Tests features thoroughly
- Executes to completion
- Reports progress and blockers

**Implementation philosophy:**
- Follows OpenSpec design.md as blueprint
- Maintains code quality standards
- Tests as part of implementation
- No scope creep beyond specifications
- Speaks up about blocking issues

**When to consult Gladiolus:**
- After OpenSpec approval
- Need direct implementation
- Building features from clear specifications
- Bug fixes with clear requirements

---

### ✨ Prompto (Code Quality Specialist)

**Best for:** Code quality improvement, OpenSpec compliance, refactoring

**Examples:**
```
@Prompto Review and improve authentication code
@Prompto Ensure OpenSpec compliance in recent changes
@Prompto Refactor for improved maintainability
```

**What Prompto does:**
- Verifies OpenSpec compliance (checks against design.md)
- Enforces review-policy guidelines
- Performs code quality reviews
- Refactors for clarity and maintainability
- Identifies improvement opportunities
- Ensures consistent code patterns
- Safe refactoring without breaking functionality

**Quality improvement focus:**
- **OpenSpec Compliance**: Implementation matches design
- **Review Policy**: Follows project review guidelines
- **Code Clarity**: Readable and maintainable
- **Pattern Consistency**: Follows established patterns
- **Best Practices**: Adheres to language standards

**Refactoring approach:**
- Clarity over cleverness
- Consistency in naming and patterns
- Maintainability without changing behavior
- Safe transformations with tests

**When to consult Prompto:**
- After implementation, before documentation
- Need quality improvement
- Ensure OpenSpec compliance
- Code readability concerns
- Refactor for better maintainability

---

### 🌙 Lunafreya (PR Creation Specialist)

**Best for:** Pull request creation and finalization

**Examples:**
```
@Lunafreya Create PR for authentication implementation
@Lunafreya Finalize PR with proper description
@Lunafreya Create PR linked to Issue #42
```

**What Lunafreya does:**
- Creates pull requests with clear descriptions
- Links PR to related Issues
- References OpenSpec documents
- Verifies CI passes
- Ensures all changes are committed
- Prepares for merge and deployment

**PR creation checklist:**
1. All code changes are committed
2. Tests pass (CI is green)
3. Documentation is updated
4. CHANGELOG is updated
5. OpenSpec is archived
6. Issue references are included

**When to consult Lunafreya:**
- After documentation and archiving complete
- Ready to create pull request
- Need PR for completed work
- Finalize implementation delivery

---

## Typical Workflows

### Feature Implementation (OpenSpec-driven)

```
User: @Noctis Add shopping cart functionality

Workflow:
1. Noctis: Creates OpenSpec (proposal, tasks, design) with user
2. User: Approves specification
3. Iris: Creates GitHub Issue (if requested)
4. Gladiolus: Implements based on OpenSpec design
5. Prompto: Reviews OpenSpec compliance and quality
6. Ignis: Updates documentation (without archiving)
7. Noctis: Verifies task completion and archives OpenSpec
8. Lunafreya: Creates PR with proper description
9. Noctis: Notifies user and requests verification
10. User: Verifies and approves merge
```

### Bug Fix with OpenSpec

```
User: @Noctis Fix session timeout issue

Workflow:
1. Noctis: Creates minimal OpenSpec (proposal + tasks)
2. User: Approves fix approach
3. Gladiolus: Implements fix
4. Prompto: Reviews quality
5. Ignis: Updates CHANGELOG
6. Noctis: Archives OpenSpec
7. Lunafreya: Creates PR
8. Noctis: Notifies completion
```

### Direct Agent Usage

```
User: @Iris Create Issue for CSV export feature
→ Direct Issue creation

User: @Gladiolus Implement following OpenSpec change-042
→ Direct implementation

User: @Prompto Improve code quality in authentication module
→ Direct quality improvement

User: @Lunafreya Create PR for completed work
→ Direct PR creation
```

---

## Best Practices

### Do's

✅ **Start with Noctis for new features** - Let it create OpenSpec
✅ **Approve specifications before implementation** - Ensure clarity upfront
✅ **Trust autonomous workflow** - Minimal intervention is sufficient
✅ **Verify final results** - Check PR before merge
✅ **Use direct agents for simple tasks** - Skip orchestration when appropriate

### Don'ts

❌ **Don't skip OpenSpec for complex features** - Prevents scope creep
❌ **Don't micromanage workflow** - Trust the process
❌ **Don't skip quality review** - Prompto catches important issues
❌ **Don't skip documentation** - Ignis keeps everything current

---

## Examples by Task Type

### New Feature
```
@Noctis Add two-factor authentication
```
→ Full OpenSpec workflow with team coordination

### Bug Fix
```
@Noctis Fix payment processing timeout
```
→ Minimal OpenSpec with direct fix

### Issue Creation
```
@Iris Create Issue for search optimization feature
```
→ Direct to Iris for issue management

### Implementation
```
@Gladiolus Implement following OpenSpec change-042
```
→ Direct to Gladiolus with clear specifications

### Code Quality
```
@Prompto Review and improve authentication module
```
→ Direct to Prompto for quality improvement

### Documentation
```
@Ignis Update documentation with recent changes
```
→ Direct to Ignis for documentation updates

### PR Creation
```
@Lunafreya Create PR for authentication implementation
```
→ Direct to Lunafreya when ready

---

## エージェント選択クイックリファレンス

| Need | Call |
|------|------|
| Complex feature with OpenSpec | `@Noctis` |
| Create/manage GitHub Issues | `@Iris` |
| Implement from OpenSpec | `@Gladiolus` |
| Code quality improvement | `@Prompto` |
| Documentation updates | `@Ignis` |
| Archive OpenSpec | `@Noctis` |
| Pull request creation | `@Lunafreya` |
| Workflow orchestration | `@Noctis` |
| Quick bug fix | `@Noctis` (minimal spec) |

---

## OpenSpec Documents

The workflow revolves around three main documents:

### proposal.md
- **Overview**: What are we building?
- **Motivation**: Why are we building it?
- **Approach**: How will we build it?
- **Scope**: What's included and what's excluded?

### tasks.md
- **Checklist**: Step-by-step implementation tasks
- **Progress tracking**: Mark completed items
- **Dependencies**: Task ordering

### design.md
- **Technical design**: Detailed implementation plan
- **Architecture**: System structure
- **API contracts**: Interfaces and data models
- **Edge cases**: Error handling and validation

---

**Remember**: Specification-driven development with autonomous execution and minimal user interruption.

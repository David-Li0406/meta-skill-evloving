---
title: Skill Quality Review Framework
description: Comprehensive 7-category quality review framework with automated validation, manual checklists, scoring rubrics, and approval criteria for skill creation
keywords: quality review, validation, testing, scoring, checklists, frontmatter, structure, documentation, references, scripts, artifact type
skill: creating-skills
---

# Skill Quality Review

Comprehensive quality review framework for skill creation. Use this before packaging or deploying any skill.

## Overview

This review process ensures skills meet production standards through systematic validation, scoring, and testing. The review is organized into **7 scoring categories**, each containing specific checklist items. Scores are determined by the percentage of checks passed within each category.

**Target**: All categories ≥4/5 for approval.

---

## Review Workflow

Follow these 4 steps for every skill review:

### Step 1: Automated Pre-Flight Gate

**Purpose**: Catch structural and syntactic errors before manual review.

Execute the comprehensive validation script:

```bash
python3 scripts/validate_skill.py /path/to/skill-folder --check all
```

**Desired outcome**: ≥95% pass rate on SKILL.md validation (22+/23 checks).

**Understanding Errors vs Warnings:**
- **Errors** (✗ red): Block validation, must be fixed to pass
- **Warnings** (⚠ yellow): Review manually, not blocking, may be acceptable
- **Skipped** (⊘ yellow): Not applicable to this skill

**Context Matters:**
The validation script performs pattern-based analysis and may flag content that is contextually appropriate. Use good judgement.

Separation of concerns check (domain boundaries, no duplication)
```bash
python3 scripts/check_soc_violations.py /path/to/artifact-folder
```

### Step 2: Manual Quality Review

**Purpose**: Deep assessment of skill quality, usability, and completeness.

**IMPORTANT**: This review requires contextual interpretation. The automated script performs pattern-based analysis and may flag content that is contextually appropriate (e.g., anti-pattern examples, technical terms like "current branch", quoted incorrect usage). Always apply judgment when reviewing flagged items.

For each of the 7 categories in "Scoring Categories" below:

1. **Review all checklist items** - Read each item carefully
2. **Mark as pass (✓) or fail (✗)** - Some items reference Step 1 automated results, most require manual judgment
3. **Apply contextual analysis** - Understand WHY something was flagged before marking as fail
4. **Calculate percentage** - (items passed / total items) × 100
5. **Assign score** - Use rubric below based on percentage
6. **Document issues** - Note specific problems for any failed items

**Scoring Rubric (applies to all 7 categories):**

- **5 (Excellent)**: 90-100% of checks pass
- **4 (Good)**: 75-89% of checks pass
- **3 (Acceptable)**: 60-74% of checks pass
- **2 (Needs Work)**: 40-59% of checks pass
- **1 (Poor)**: <40% of checks pass

**Target**: All categories score ≥4/5 for approval.

### Step 3: Test the Skill

Skills have no side effects and should always be tested:

```bash
# Structure check
ls -la ~/.claude/skills/skill-name/
head -20 skill-name/SKILL.md
ls skill-name/references/ skill-name/scripts/ skill-name/assets/ skill-name/templates/

# Functionality test
Skill(command="skill-name")

# Observe:
# - Loads correctly?
# - Provides expected guidance?
# - References accessible?
# - Scripts functional (if applicable)?
```

**Reference validation:**
- Read key reference files for quality
- Verify discoverability from SKILL.md
- Check no duplication with SKILL.md
- Assess LLM-first density (see Category 4)

### Step 4: Apply Recommendation Logic

Based on scores from Step 2:

- **APPROVE** - All scores ≥4, ready for packaging
- **NEEDS_REVISION** - Any score <4, requires improvements
- **CONSIDER_DIFFERENT_TYPE** - Artifact Type score ≤2, might be better as command/subagent

Document all issues with:
- Category affected
- Severity: critical (1-2), major (3), minor (4)
- Specific problem description
- Actionable improvement suggestion

---

## Scoring Categories

**How to use these checklists:**

Each category below contains checklist items for manual review. Some items were already validated by the automated script in Step 1 (syntax, structure, required fields) - mark these as ✓ if Step 1 passed. Other items require manual judgment (quality, clarity, appropriateness) - carefully assess these during review.

**Review each category:**
1. Go through all checklist items
2. Mark ✓ (pass) or ✗ (fail) for each
3. Calculate: (items passed / total items) × 100
4. Assign score 1-5 using rubric from Step 2
5. Document issues in "Issues identified" section

---

### Category 1: Frontmatter & Discovery

The YAML frontmatter determines when Claude invokes the skill. Quality here directly impacts discoverability.

#### Checklist Items

**Name (required)**
- [ ] `name` field present
- [ ] Name is 64 characters or less
- [ ] Name uses gerund form (e.g., "processing-pdfs", "analyzing-data", "managing-workflows")
- [ ] Name is descriptive and action-oriented
- [ ] Name avoids generic terms like "Helper", "Utils", "Tools"

**Description (required)**
- [ ] `description` field present
- [ ] Description is 1024 characters or less
- [ ] Description written in third person (injected into system prompt)
- [ ] Description includes WHAT the skill does
- [ ] Description includes WHEN to use it
- [ ] Description includes specific keywords/triggers for discovery
- [ ] No first person ("I can...") or second person ("You should...")
- [ ] Description is specific enough for Claude to know when to invoke the skill

**Total checks**: 13

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 2: Structure & Organization

Proper file structure enables progressive disclosure and efficient context management.

#### Checklist Items

**File Size & Organization**
- [ ] SKILL.md is under 500 lines
- [ ] Content exceeding 500 lines split into separate files
- [ ] File structure is clear and logical
- [ ] File names are descriptive
- [ ] Files organized by domain or feature

**Path Conventions**
- [ ] Directory uses forward slashes (/)
- [ ] No Windows-style paths (backslashes)
- [ ] File references are one level deep (e.g., `reference/guide.md`)
- [ ] No deep nesting (e.g., NOT `reference/api/v2/endpoints/auth.md`)

**Progressive Disclosure**
- [ ] Large content split across multiple files
- [ ] SKILL.md contains core instructions only
- [ ] Additional details in reference files
- [ ] References clearly indicated (e.g., "See reference/api.md")
- [ ] Reference files organized logically
- [ ] Scripts in scripts/ directory
- [ ] Documentation in reference/ directory
- [ ] Assets in assets/ directory (if applicable)

**Total checks**: 17

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 3: Instructions & Workflows

Clear, actionable instructions ensure Claude can execute the skill effectively.

#### Checklist Items

**Writing Style**
- [ ] Content is concise - assumes Claude's intelligence
- [ ] Uses imperative/infinitive form (not second person)
- [ ] No explanations of basic concepts Claude already knows
- [ ] No explanations of what common file formats are (PDF, CSV, etc.)
- [ ] No over-explanation of libraries or programming concepts
- [ ] Terminology is consistent throughout
- [ ] No time-sensitive information (dates, version numbers)
- [ ] No "current" or "as of 2024" type statements

**Workflow Quality**
- [ ] Workflows have clear, numbered steps
- [ ] Each step has concrete commands or code
- [ ] Steps include verification/validation
- [ ] Inputs and outputs clearly specified
- [ ] Expected results documented
- [ ] Error handling explained
- [ ] Troubleshooting guidance provided
- [ ] Complex operations broken into sequential steps with checkpoints

**Degrees of Freedom**
- [ ] High freedom tasks use text instructions (multiple valid approaches)
- [ ] Medium freedom tasks use templates/pseudocode (preferred patterns)
- [ ] Low freedom tasks use exact scripts (fragile operations)
- [ ] Specificity level appropriate for task fragility

**Total checks**: 20

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 4: Reference Materials & LLM-First Design

Reference files should be information-dense, structured, and optimized for LLM consumption.

#### Checklist Items

**Reference Organization**
- [ ] Sufficient docs in `references/` (if needed)
- [ ] Well organized and discoverable
- [ ] No duplication with SKILL.md
- [ ] Progressive disclosure followed
- [ ] References use strict heading hierarchy (H1→H2→H3, never skip)
- [ ] Sections are self-contained with necessary context
- [ ] Explicit language (avoid vague pronouns like "it", "this", "they")
- [ ] Code examples in proper code blocks with language tags
- [ ] Prerequisites stated explicitly

**Reference Frontmatter** (if references/ exists)
- [ ] All reference .md files have YAML frontmatter
- [ ] Frontmatter is valid YAML
- [ ] Each has required fields: `title`, `description`
- [ ] Title field ≤100 characters
- [ ] Description field ≤500 characters
- [ ] Frontmatter includes `keywords` for enhanced discoverability (recommended)
- [ ] Frontmatter enables file discovery in tooling

**LLM-First Design Principles**

*High-density patterns (seek these):*
- [ ] Uses comparison tables for related concepts
- [ ] Uses decision trees for conditional logic
- [ ] Uses rule checklists for validation
- [ ] Assumes LLM knowledge (no explaining basic concepts)
- [ ] Contains domain-specific information only

*Bloat indicators (avoid these):*
- [ ] Does NOT explain general concepts (TDD, Git, REST, etc.)
- [ ] Does NOT include pedagogical scaffolding ("Let's understand...")
- [ ] Does NOT have multiple redundant examples
- [ ] Does NOT include background/motivation sections
- [ ] Does NOT include tutorials for concepts Claude knows

**Density Assessment** (for skills with references/)
- [ ] Content is primarily structured data (tables, trees, checklists)
- [ ] Prose is minimal and directive
- [ ] No verbose explanations
- [ ] Information density is high (target: 7+/10)

**Total checks**: 26 (N/A if no references/ directory - score 5/5)

**Score**: _____ /5 (based on % passed, or 5/5 if N/A)

**Issues identified**:

---

### Category 5: Code & Scripts

Scripts must be complete, functional, and solve problems deterministically.

#### Checklist Items

**Dependencies & Setup**
- [ ] All required packages explicitly listed
- [ ] Installation commands provided
- [ ] Import statements shown
- [ ] No assumed installations
- [ ] Package sources identified (npm, PyPI, etc.)
- [ ] Version requirements specified (if critical)
- [ ] Platform-specific notes included (if relevant)
- [ ] Environment variables documented (if needed)

**Script Quality**
- [ ] Scripts are complete and functional
- [ ] Scripts solve problems (don't punt to Claude)
- [ ] Scripts have error handling
- [ ] Error messages are specific and helpful
- [ ] No "magic numbers" or unexplained constants
- [ ] All values justified or configurable
- [ ] Scripts have clear documentation
- [ ] Script purpose explained
- [ ] Usage examples provided
- [ ] Exit codes documented (if applicable)

**Code in SKILL.md**
- [ ] Examples are concrete, not abstract
- [ ] Code examples are complete and runnable
- [ ] No pseudocode where real code would be clearer
- [ ] Code blocks properly formatted
- [ ] Syntax highlighting specified where relevant

**Total checks**: 23 (N/A if no scripts/ - adjust total accordingly)

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 6: Integration & Separation of Concerns

Skills should integrate well with other skills/tools and maintain clear domain boundaries.

#### Checklist Items

**Skill Integration**
- [ ] Properly references other skills when appropriate
- [ ] Uses Skill() invocation pattern correctly
- [ ] Leverages existing skills instead of duplicating content
- [ ] No duplication of content from other skills

**Tool Integration**
- [ ] MCP tools use fully qualified names (ServerName:tool_name)
- [ ] Server names capitalized correctly
- [ ] No bare tool names without server prefix (if using MCP tools)
- [ ] Tool requirements clearly stated
- [ ] Restrictions explained
- [ ] Usage patterns documented

**Domain Boundaries**
- [ ] Clear domain boundaries defined
- [ ] No content overlap with other skills
- [ ] Responsibilities well-defined
- [ ] Implementation matches documentation
- [ ] Scope is appropriate (not too broad or narrow)

**Total checks**: 15

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 7: Examples & Documentation Standards

Quality examples and documentation enable effective skill usage.

#### Checklist Items

**Examples**
- [ ] At least one complete working example
- [ ] Examples use realistic data
- [ ] Examples show common use cases
- [ ] Examples are copy-pasteable
- [ ] Examples include both input AND expected output (I/O pairs)
- [ ] Examples demonstrate desired style and detail level
- [ ] Edge cases covered in examples
- [ ] Examples are concrete, not abstract or placeholder-heavy

**Documentation Standards**
- [ ] Clear section headers
- [ ] Logical content flow
- [ ] No orphaned sections
- [ ] Cross-references are accurate
- [ ] Links/references are valid
- [ ] Table of contents included for files exceeding 100 lines

**Accessibility & Usability**
- [ ] Clear, scannable headers
- [ ] Logical information hierarchy
- [ ] Quick start section for new users (if needed)
- [ ] Progressive detail (simple → complex)
- [ ] Search-friendly terminology
- [ ] Consistent formatting
- [ ] Minimal cognitive load
- [ ] No jargon without explanation

**Error Handling & Troubleshooting**
- [ ] Error messages are specific
- [ ] Error messages suggest solutions
- [ ] Error messages include context
- [ ] Common issues documented
- [ ] Troubleshooting section present (if needed)
- [ ] Recovery procedures explained (if applicable)

**Total checks**: 27

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

## Additional Validation Checks

These are yes/no gates that must pass regardless of category scores.

### Security Considerations
- [ ] No hardcoded credentials
- [ ] Environment variables for secrets (if applicable)
- [ ] Security best practices mentioned (if relevant)
- [ ] Input validation recommended (where needed)
- [ ] Safe file handling practices

### Artifact Type Validation
- [ ] Skill is the appropriate artifact type (not better as command/subagent)
- [ ] Skill has complexity warranting skill structure (>200 lines or needs bundled resources)
- [ ] Not better suited as a simple command (<200 lines, single file, manual trigger)
- [ ] Not better suited as a subagent (separate domain, autonomous sub-tasks)

### Final Verification
- [ ] All file references are valid (no broken links)
- [ ] All code examples run correctly
- [ ] All commands execute correctly
- [ ] JSON/YAML syntax is valid
- [ ] No critical typos in documentation

---

## Score Summary

Complete after scoring all categories:

| Category | Score | Status |
|----------|-------|--------|
| 1. Frontmatter & Discovery | ___/5 | ___ |
| 2. Structure & Organization | ___/5 | ___ |
| 3. Instructions & Workflows | ___/5 | ___ |
| 4. Reference Materials & LLM-First | ___/5 | ___ |
| 5. Code & Scripts | ___/5 | ___ |
| 6. Integration & SoC | ___/5 | ___ |
| 7. Examples & Documentation | ___/5 | ___ |
| **Average** | **___/5** | ___ |

**Status codes**: ✓ Pass (≥4) | ⚠ Review (3) | ✗ Fail (<3)

---

## Final Recommendation

Based on scores and validation checks:

**[ ] APPROVE** - All scores ≥4, all validation checks pass
- Skill is ready for packaging and deployment
- Package with: `python3 scripts/package_skill.py /path/to/skill-folder`

**[ ] NEEDS_REVISION** - Any score <4 or validation checks fail
- Address all issues documented in category reviews
- Re-run quality review after improvements
- Focus on categories with scores <4

**[ ] CONSIDER_DIFFERENT_TYPE** - Artifact Type validation concerns
- Consider if skill would be better as command or subagent
- Commands: Simple workflow (<200 lines), single file, manual trigger
- Subagents: Separate domain, autonomous sub-tasks, dedicated scope

---

## Common Anti-Patterns

Watch for these frequent mistakes:

**Frontmatter Issues**
- ✗ Not using gerund form in name
- ✗ Description too vague or generic
- ✗ Description in first/second person
- ✗ Missing trigger keywords

**Structure Issues**
- ✗ SKILL.md over 500 lines without splitting
- ✗ Deep file nesting (more than one level)
- ✗ Windows-style paths (backslashes)
- ✗ Duplication between SKILL.md and references

**Content Issues**
- ✗ Over-explaining basic concepts
- ✗ Abstract examples instead of concrete code
- ✗ Inconsistent terminology
- ✗ Time-sensitive information
- ✗ Second person language ("you should...")

**Code Issues**
- ✗ Missing package installation instructions
- ✗ Assuming tools are pre-installed
- ✗ Scripts without error messages
- ✗ Magic numbers without explanation

**Integration Issues**
- ✗ MCP tools without server prefix
- ✗ Duplicating content from other skills
- ✗ No troubleshooting section when needed
- ✗ Unclear domain boundaries

---

## Quality Standards Summary

A production-ready skill must be:

1. **Discoverable** - Clear name and description with triggers
2. **Concise** - Respects context window, uses progressive disclosure
3. **Concrete** - Real code and examples, not abstractions
4. **Complete** - All dependencies listed, all references valid
5. **Correct** - Tested and verified to work
6. **Clear** - Well-organized, scannable, AI-readable
7. **Coherent** - Clear boundaries, proper integration with other skills

**Minimum standard**: All categories score 4+/5, all validation checks pass.

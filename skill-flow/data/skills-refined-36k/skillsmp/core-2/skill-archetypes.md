# Skill Archetypes

**Directory structure patterns for Minimal, Standard, and Complex skills**

This document defines the three skill archetypes used in Qara based on analysis of 29 production skills. Choose the archetype that matches your skill's complexity and requirements.

**See also:**
- [skill-structure.md](./skill-structure.md) - Mandatory structure requirements and canonical template
- [routing-patterns.md](./routing-patterns.md) - The 4-level routing hierarchy and routing patterns

---

## Overview: Three Skill Archetypes

Based on analysis of 29 production skills in Qara, three clear organizational patterns emerged:

| Archetype | File Count | Complexity | Use Case |
|-----------|-----------|------------|----------|
| **Minimal** | 3-7 files | Low | Single-purpose, 1-3 workflows |
| **Standard** | 10-50 files | Medium | Multi-workflow, clear domain |
| **Complex** | 40-7000+ files | High | Multi-domain, stateful, embedded apps |

---

## Archetype 1: Minimal Skill

**Use Case:** Simple, single-purpose skills with 1-3 workflows

**Examples:** `be-creative`, `social-xpost`, `newsletter-content`

```
skill-name/
├── SKILL.md                    # REQUIRED - Skill definition
└── [OPTIONAL ONE OF:]
    ├── assets/                 # For templates/resources
    │   └── *.md
    └── workflows/              # For 1-3 workflows
        └── *.md
```

**Required Elements:**
- `SKILL.md` - Skill definition, description, usage triggers

**Optional Elements:**
- `assets/` OR `workflows/` (pick one based on skill type)
- Maximum 2-3 workflow files if using workflows
- Maximum 2-3 template files if using assets

**When to Use:**
- Single clear purpose
- 1-3 primary workflows
- No complex state management
- No external dependencies

**Real Example: be-creative**
```
be-creative/
├── SKILL.md
└── assets/
    ├── creative-writing-template.md
    └── idea-generation-template.md
```

**Routing Pattern:** Direct keyword routing in SKILL.md to template assets

---

## Archetype 2: Standard Skill

**Use Case:** Multi-workflow skills with clear domain boundaries

**Examples:** `research`, `blogging`, `media`, `story-explanation`, `images-ulart`

```
skill-name/
├── SKILL.md                    # REQUIRED - Skill definition
├── [OPTIONAL: MIGRATION-*.md]  # Migration documentation
├── tools/                      # OPTIONAL - TypeScript/executable tools
│   └── *.ts
├── examples/                   # OPTIONAL - Example files
│   └── *.json
├── documentation/              # OPTIONAL - Structured docs
│   └── *.md
├── workflows/                  # REQUIRED - Primary workflows
│   ├── *.md                    # Flat for <10 workflows
│   └── category/               # Nested for 10+ workflows
│       └── *.md
└── [OPTIONAL ONE OF:]
    ├── tools/                  # Executable automation
    ├── assets/                 # Templates/resources
    └── references/             # Reference documentation
```

**Required Elements:**
- `SKILL.md` - Skill definition
- `workflows/` - At least 3-15 workflow files

**Optional Elements:**
- `documentation/` - For complex documentation needs
- `tools/` - For executable automation scripts
- `assets/` - For templates and resources
- `references/` - For reference documentation
- `MIGRATION-*.md` - For change tracking

**Workflow Organization:**
- **Flat** (<10 workflows): All .md files in workflows/
- **Nested** (10+ workflows): Subdirectories by category

**When to Use:**
- 3-15 distinct workflows
- Clear domain boundaries
- Minimal external state
- Some documentation needs

**Real Example: research**
```
research/
├── SKILL.md
├── MIGRATION-NOTES.md
└── workflows/
    ├── analyze-ai-trends.md
    ├── claude-research.md
    ├── conduct.md
    ├── enhance.md
    ├── extract-alpha.md
    ├── extract-knowledge.md
    ├── fabric.md
    ├── interview-research.md
    ├── perplexity-research.md
    ├── retrieve.md
    ├── web-scraping.md
    └── youtube-extraction.md
```

**Routing Pattern:** SKILL.md lists workflows by category, routes based on request keywords

---

## Archetype 3: Complex Skill

**Use Case:** Multi-domain, stateful, or application-embedded skills

**Examples:** `system`, `development`, `business`, `CORE`, `telos`

```
skill-name/
├── SKILL.md                    # REQUIRED - Skill definition
├── CONSTITUTION.md             # OPTIONAL - System architecture and philosophy
├── METHODOLOGY.md              # OPTIONAL - Process methodology
├── *.md                        # OPTIONAL - Root reference docs
├── .archive/                   # OPTIONAL - Historical artifacts
│   └── [dated-directories]/
├── documentation/              # RECOMMENDED - Organized docs
│   ├── README.md
│   ├── [category]/             # Nested by topic (DEPRECATED for CORE)
│   │   └── *.md
│   └── *.md                    # CORE uses flat structure ONLY
├── references/                 # OPTIONAL - Reference docs
│   └── *.md
├── workflows/                  # REQUIRED - Nested workflows
│   ├── *.md                    # Core workflows (flat)
│   └── [category]/             # Specialized workflows
│       └── *.md
├── state/                      # OPTIONAL - Runtime state
│   └── *.json, *.cache
├── tools/                      # OPTIONAL - Automation scripts
│   └── *.ts, *.sh
├── testing/                    # OPTIONAL - Test infrastructure
│   └── *.md
├── [domain-directories]/       # OPTIONAL - Domain-specific tools
│   └── [domain structure]
└── [app-directory]/            # OPTIONAL - Embedded applications
    ├── package.json
    ├── src/
    └── [app structure]
```

**Required Elements:**
- `SKILL.md` - Skill definition
- `workflows/` - Nested structure with 15+ workflows

**Recommended Elements:**
- `documentation/` - Organized documentation tree
- Root-level reference .md files for key concepts

**Optional Elements:**
- `CONSTITUTION.md` - For system architecture and philosophy
- `METHODOLOGY.md` - For development methodology
- `.archive/` - For historical artifacts (dated subdirectories)
- `references/` - For reference documentation
- `state/` - For runtime state (.json, .cache files)
- `tools/` - For executable automation
- `testing/` - For test infrastructure
- Domain-specific directories (e.g., `consulting-templates/`)
- Embedded applications (e.g., `dashboard-template/`)

**When to Use:**
- 15+ workflows across multiple domains
- Requires state management
- Has embedded applications or tools
- Needs extensive documentation
- Complex methodology or architecture
- Long-term skill with evolution history

**Real Example: development**
```
development/
├── SKILL.md
├── METHODOLOGY.md
├── TESTING-PHILOSOPHY.md
├── MIGRATION-2025-10-31.md
├── .archive/
│   └── [old-implementations]/
├── design-standards/
│   ├── design-principles.md
│   ├── saas-dashboard-checklist.md
│   └── style-guide.md
├── references/
│   ├── cli-testing-standards.md
│   ├── plan-subagent-guide.md
│   └── stack-integrations.md
└── workflows/
    ├── sdd-workflow.md
    ├── sdd-specify.md
    ├── sdd-implement.md
    ├── product-discovery.md
    └── [15+ more workflows]
```

**Routing Pattern:** Multi-level routing with state awareness, methodology phases, and workflow categories

**CRITICAL ARCHITECTURAL REQUIREMENT (CORE Skill Only):**

The CORE skill uses a **completely flat structure** - ALL documentation files are at the CORE root:

```
CORE/
├── SKILL.md
├── CONSTITUTION.md           # PRIMARY - System architecture and philosophy
├── MY_DEFINITIONS.md         # Canonical definitions
├── agent-guide.md            # Agent hierarchy and roles
├── contacts.md
├── history-system.md
├── hook-system.md
├── testing-guide.md
├── ... (all other docs at CORE root)
└── workflows/
    └── ... (flat or nested as needed)
```

**Why Completely Flat Structure for CORE:**
- CORE documentation is reference material, not workflow-based
- Simpler to maintain and discover
- Files organized by naming convention only
- Reduces path complexity in skill references (no subdirectories)
- Easier to link and reference from other skills

**Other Complex Skills:** May use nested documentation/ structure (with subdirectories) as shown in examples above

---

## Workflow Organization

### Workflow Discovery Mechanisms

**How Qara finds and invokes workflows:**

1. **Explicit Reference in SKILL.md**
   ```markdown
   Use `perplexity-research.md` for web research with Perplexity API
   ```
   → Qara reads the workflow file and executes steps

2. **Category Listing**
   ```markdown
   ### Research Workflows
   - perplexity-research.md
   - claude-research.md
   - extract-alpha.md
   ```
   → Agent selects appropriate workflow from list

3. **Directory Scanning**
   ```markdown
   See workflows/ directory for all available research workflows
   ```
   → Qara scans directory and presents options

4. **Paired Documentation**
   ```
   workflows/
   ├── post-to-x.md        # Documentation
   └── post-to-x.ts        # Implementation
   ```
   → Qara reads .md for instructions, executes .ts for automation

### Flat vs Nested Workflows

**Flat Workflows** (All files in workflows/ directory)

**Use when:**
- 5-10 workflows
- All workflows at similar abstraction level
- No natural category groupings

**Example: research skill**
```
workflows/
├── analyze-ai-trends.md
├── claude-research.md
├── conduct.md
├── extract-alpha.md
└── perplexity-research.md
```

**Nested Workflows** (Subdirectories by category)

**Use when:**
- 10+ workflows
- Clear category boundaries
- Different abstraction levels

**Example: business skill**
```
workflows/
├── consulting/
│   ├── create-proposal.md
│   └── generate-deliverable.md
├── finances/
│   ├── check-balance.md
│   └── track-expenses.md
└── hormozi/
    ├── create-offer.md
    └── value-equation.md
```

**Hybrid Workflows** (Core flat + specialized nested)

**Use when:**
- Some workflows are core/universal
- Others are category-specific

**Example: system skill**
```
workflows/
├── check-sensitive.md          # Core (flat)
├── update-qara-repo.md          # Core (flat)
├── website/                    # Category (nested)
│   ├── get-analytics.md
│   └── sync-content.md
└── observability/              # Category (nested)
    └── update-dashboard.md
```

---

## Skill Structure Decision Tree

```
How many workflows?
├─ 0-3 → MINIMAL SKILL
│  └─ SKILL.md + (assets/ OR workflows/)
│
├─ 3-15 → STANDARD SKILL
│  ├─ <10 workflows → Flat workflows/
│  └─ 10-15 workflows → Nested workflows/
│
└─ 15+ → COMPLEX SKILL
   ├─ documentation/
   ├─ workflows/ (nested)
   └─ Optional: state/, tools/, references/, etc.
```

## Workflow Organization Rules

| Workflow Count | Organization | Structure |
|----------------|--------------|-----------|
| 0-5 | Flat | `workflows/*.md` |
| 5-10 | Flat (consider categories) | `workflows/*.md` |
| 10-20 | Nested by category | `workflows/category/*.md` |
| 20+ | Nested + hybrid | `workflows/*.md` + `workflows/category/*.md` |

---

## File Naming Cheat Sheet

| Element | Format | Example |
|---------|--------|---------|
| Root skill file | `SKILL.md` | `SKILL.md` |
| Root docs | `UPPERCASE.md` | `METHODOLOGY.md` |
| Workflows | `kebab-case.md` | `create-blog-post.md` |
| Tools | `kebab-case.ts` | `update-content.ts` |
| Migrations | `MIGRATION-DATE.md` | `MIGRATION-2025-11-10.md` |
| State files | `kebab-case.json` | `content-state.json` |
| Container dirs | `plural-lowercase` | `workflows/`, `tools/` |
| Content dirs | `singular-lowercase` | `state/`, `documentation/` |

---

## Common Patterns Reference

**Minimal Skill (be-creative):**
```
skill/
├── SKILL.md
└── assets/
    └── *.md
```

**Standard Skill (research):**
```
skill/
├── SKILL.md
└── workflows/
    └── *.md
```

**Complex Skill (development):**
```
skill/
├── SKILL.md
├── METHODOLOGY.md
├── documentation/
│   └── category/
│       └── *.md
├── workflows/
│   └── category/
│       └── *.md
└── references/
    └── *.md
```

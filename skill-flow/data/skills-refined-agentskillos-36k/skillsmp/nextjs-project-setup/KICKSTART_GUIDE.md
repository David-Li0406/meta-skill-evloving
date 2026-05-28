# Next.js Project Setup - Kickstart Guide

**Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Production Ready

---

## Overview

This guide provides a step-by-step walkthrough of the Next.js Project Setup skill, showing exactly which components are invoked at each stage and what deliverables are produced.

**Skill Components**:
- **1 Skill**: `.claude/skills/nextjs-project-setup/SKILL.md` (auto-discovered by Claude)
- **7 Sub-agents**: `.claude/agents/nextjs-*.md` (delegated via Task tool)
- **4 Templates**: `.claude/skills/nextjs-project-setup/templates/` (output formatting)
- **0 Slash Commands**: None currently (skill is auto-invoked)

---

## How Users Trigger the Skill

### Auto-Discovery (Recommended)

Claude Code automatically invokes this skill when users request Next.js project setup:

```
User: "I want to set up a new Next.js project for a SaaS dashboard with Supabase authentication"
```

**Behind the scenes**:
1. Claude reads skill `description` field in YAML frontmatter
2. Matches user intent to skill capability
3. Loads `SKILL.md` instructions
4. Begins execution

### Explicit Mention (Alternative)

```
User: "Use the nextjs-project-setup skill to create my project"
```

---

## Execution Paths

The skill adapts to project complexity:

### Path 1: Simple Setup (15-30 minutes)

**Indicators**: Standard website, no database, single tenant, simple design

**Workflow**:
```
User Request
    ↓
Complexity Assessment → [SIMPLE]
    ↓
Load @docs/simple-setup.md
    ↓
Execute: Template → Components → Design → Docs
    ↓
Deliverables: Basic project structure
```

**Components Used**:
- **Skill**: SKILL.md (orchestration)
- **Documentation**: docs/simple-setup.md
- **MCP Tools**: Vercel, Shadcn
- **Sub-agents**: None (direct execution)

---

### Path 2: Complex Setup (2-4 hours)

**Indicators**: Database, auth, multi-tenant, complex design, e-commerce

**Workflow**:
```
User Request
    ↓
Complexity Assessment → [COMPLEX]
    ↓
Phase 1: Research (Parallel) ∥ 4 agents
    ↓
Phase 2: Template Selection
    ↓
Phase 3: Specification
    ↓
Phase 4: Design System (Agent + User Feedback)
    ↓
Phase 5: Wireframes (Agent + User Feedback)
    ↓
Phase 6: Implementation (Parallel) ∥ TDD
    ↓
Phase 7: QA Validation (Parallel) ∥
    ↓
Phase 8: Documentation Audit
    ↓
Final: Production-Ready Project
```

---

## Detailed Phase Breakdown (Complex Path)

### Phase 1: Research (Parallel Execution)

**Purpose**: Gather foundational knowledge without bloating main context

**Duration**: ~5 minutes (parallel execution)

**Components**:
- **Sub-agents** (4 launched simultaneously):
  - `nextjs-research-vercel.md` → Reports Next.js templates
  - `nextjs-research-shadcn.md` → Reports Shadcn patterns
  - `nextjs-research-supabase.md` → Reports auth & RLS patterns
  - `nextjs-research-design.md` → Reports 2025 design trends

**How It Works**:
1. Main skill delegates to 4 agents using Task tool
2. Each agent operates in isolated context (separate conversation)
3. Agents write reports to `/reports/*.md` (~2000 tokens each)
4. Main skill reads reports (8,000 total tokens vs 140,000 if read all docs)

**Token Efficiency**: 94% savings (8K vs 140K)

**Deliverables**:
```
/reports/
├── vercel-templates.md       (Next.js template analysis)
├── shadcn-best-practices.md  (Component patterns)
├── supabase-patterns.md      (Auth & RLS)
└── design-systems.md         (Color palettes, typography)
```

**User Action**: None (automatic)

---

### Phase 2: Template Selection

**Purpose**: Choose optimal Next.js template

**Duration**: ~10 minutes

**Components**:
- **Documentation**: @docs/complex/phase-2-template.md
- **MCP Tools**: Vercel MCP
- **Prerequisites**: /reports/vercel-templates.md

**How It Works**:
1. Analyze user requirements
2. Query Vercel MCP: `mcp__vercel__list_templates`
3. Match features to requirements
4. Present top 3 options with pros/cons
5. User selects template
6. Install: `npx create-next-app --example <template>`

**Deliverables**:
```
project-root/              (installed template)
/docs/template-selection.md  (rationale, features, setup notes)
```

**User Action**: Select template from 3 options

---

### Phase 3: Specification

**Purpose**: Define complete product requirements

**Duration**: ~20 minutes

**Components**:
- **Documentation**: @docs/complex/phase-3-spec.md
- **Referenced Skills**: product-skill, constitution-skill (from main toolkit)

**How It Works**:
1. Invoke product definition skill (creates product-spec.md)
2. Invoke constitution generation (creates constitution.md)
3. Define features with acceptance criteria
4. Document architecture decisions

**Deliverables**:
```
/docs/
├── product-spec.md     (User personas, stories, pain points)
├── constitution.md     (Technical principles, constraints)
├── features.md         (Feature breakdown with ACs)
└── architecture.md     (System design, data model)
```

**User Action**: Review and approve specifications

---

### Phase 4: Design System Ideation

**Purpose**: Generate multiple design options with expert evaluation

**Duration**: ~30 minutes (includes user feedback iterations)

**Components**:
- **Sub-agent**: `nextjs-design-ideator.md`
- **Template**: templates/design-showcase.md
- **MCP Tools**: Shadcn MCP, 21st Dev MCP
- **Documentation**: @docs/complex/phase-4-design.md
- **Prerequisites**: Specifications, research reports

**How It Works**:
1. **Brainstorm** (agent generates 3-5 design options):
   - Color palettes (WCAG-compliant HSL variables)
   - Typography systems (font pairs, scales)
   - Component styles (button variants, card layouts)
   - Layout patterns (grid systems, spacing)

2. **Showcase** (template formats options):
   - Visual comparison table
   - Expert evaluation scores (UX, conversion, A11y, mobile, SEO)
   - Color swatches with contrast ratios
   - Component previews

3. **User Feedback Loop**:
   - Present showcase
   - Discuss trade-offs
   - Iterate on selected option
   - Refine until approved

4. **Finalize**:
   - Document chosen system
   - Configure Tailwind CSS (CSS variables only, no hardcoded colors)
   - Set up Shadcn structure
   - Import base components via Shadcn MCP workflow

**Shadcn MCP Workflow** (enforced):
```
Search → View → Examples → Install
(NEVER skip Examples step)
```

**Deliverables**:
```
/docs/design-system.md
tailwind.config.ts          (CSS variables configured)
components.json             (Shadcn registries: @ui, @magicui)
components/ui/              (Base components installed)
```

**User Action**: Select design option, provide feedback, approve final

---

### Phase 5: Wireframes & Asset Management

**Purpose**: Create detailed layout wireframes with image asset management

**Duration**: ~30 minutes (includes user feedback)

**Components**:
- **Template**: templates/wireframe-template.md
- **Documentation**: @docs/complex/phase-5-wireframes.md
- **Prerequisites**: Design system, specifications

**How It Works**:

**5.1 Image Asset Management** (if user provides images):
1. Inventory all images
2. Describe each image (AI analysis)
3. Rename with descriptive filenames
4. Categorize by purpose (hero, feature, testimonial, etc.)
5. Document in /assets/inventory.md
6. Reference in wireframes

**5.2 Wireframe Generation**:
1. Create 2-3 layout variations per major page
2. Use text-based ASCII art wireframes
3. Reference design system components
4. Include image placeholders with @asset references
5. Expert evaluation (UX, conversion, A11y, mobile, SEO)
6. User feedback loop
7. Iterate until approved

**Deliverables**:
```
/docs/wireframes/
├── landing-page.md         (Multiple layout options)
├── dashboard.md            (Admin interface)
├── product-page.md         (Product details)
└── checkout.md             (E-commerce flow)

/assets/inventory.md        (If images provided)
```

**User Action**: Review wireframes, select layouts, provide feedback

---

### Phase 6: Implementation

**Purpose**: Build application with TDD and parallel execution

**Duration**: 1-2 hours (depends on features)

**Components**:
- **Documentation**: @docs/complex/phase-6-implement.md
- **MCP Tools**: Shadcn MCP, Supabase MCP
- **Referenced Skills**: implement-and-verify (from main toolkit)
- **Prerequisites**: Wireframes, design system, template

**Core Principles**:
1. **TDD Mandatory**: Tests before implementation (RED-GREEN-REFACTOR)
2. **Visual Validation**: Every page reviewed before marking complete
3. **Interaction Testing**: All links, buttons, animations validated
4. **Parallel Execution**: Independent features via sub-agents

**Component Management**:
- Use Shadcn MCP for all components
- Follow workflow: Search → View → Example → Install
- Use global Tailwind CSS variables (no hardcoded colors)
- Prefer @ui registry for core, @magicui for enhanced

**Database Setup** (if applicable):
- Use Supabase MCP tools ONLY (never CLI)
- Start with staging environment
- Define schema with RLS policies
- Implement Server Actions for mutations
- Multi-tenant: tenant_id foreign keys

**Deliverables**:
```
Complete codebase:
├── app/                    (Next.js App Router)
├── components/             (UI components)
├── lib/                    (Utilities, Supabase client)
├── __tests__/              (Test suite)
└── supabase/               (Migrations, RLS policies)
```

**User Action**: Review implementation progress, provide feedback

---

### Phase 7: QA Validation (Parallel with Implementation)

**Purpose**: Continuous quality validation across 5 dimensions

**Duration**: Runs continuously during implementation

**Components**:
- **Sub-agent**: `nextjs-qa-validator.md` (runs continuously)
- **MCP Tools**: Chrome DevTools MCP (optional for E2E testing)
- **Documentation**: @docs/complex/phase-7-qa.md

**Validation Dimensions**:
1. **Functional** (12 criteria): Auth, DB operations, UI rendering
2. **Accessibility** (16 criteria): Color contrast ≥4.5:1, keyboard nav, ARIA
3. **Performance** (12 criteria): Build size, image optimization, Core Web Vitals
4. **Security** (12 criteria): RLS policies, input validation, env vars
5. **Compatibility** (8 criteria): Browser support, responsive design, TypeScript

**Process**:
1. QA agent validates continuously
2. Reports issues immediately (blocks task completion)
3. Implementation agents fix
4. Re-validate
5. No task marked complete until QA ✓

**Deliverables**:
```
/reports/qa-validation.md
- Overall quality score (percentage)
- Pass/fail per dimension
- Issue tracking
- Resolution verification
```

**User Action**: None (automatic validation, blocking failures)

---

### Phase 8: Documentation & Audit

**Purpose**: Comprehensive documentation and completeness audit

**Duration**: ~20 minutes

**Components**:
- **Sub-agent**: `nextjs-doc-auditor.md`
- **Documentation**: @docs/complex/phase-8-docs.md
- **Prerequisites**: Implementation complete, QA passing

**Documentation Structure Generated**:
```
project-root/
├── CLAUDE.md                # Main context (comprehensive)
├── README.md                # User-facing setup guide
├── DEVELOPMENT.md           # Developer guide
├── API.md                   # API documentation (if applicable)
├── DEPLOYMENT.md            # Deployment instructions
└── TROUBLESHOOTING.md       # Common issues & solutions
```

**Audit Checklist**:
- [ ] CLAUDE.md completeness (10 required sections)
- [ ] README.md quality (12 sections)
- [ ] API documentation (if endpoints exist)
- [ ] Deployment guide (Vercel, env vars, database)
- [ ] Code documentation (JSDoc, TypeScript types)
- [ ] Test documentation (coverage, running tests)

**Deliverables**:
```
Complete documentation suite
/reports/documentation-audit.md (coverage metrics, missing sections)
```

**User Action**: Review documentation, request clarifications if needed

---

## Final Output Structure

After completing all phases, the project structure is:

```
project-root/
├── app/                     # Next.js App Router
│   ├── (auth)/             # Auth routes
│   ├── (dashboard)/        # Protected routes
│   ├── api/                # API routes
│   ├── layout.tsx          # Root layout
│   └── globals.css         # Tailwind CSS (CSS variables)
│
├── components/
│   ├── ui/                 # Shadcn components
│   ├── custom/             # Project-specific components
│   └── layouts/            # Layout components
│
├── lib/
│   ├── supabase/           # Supabase client (server, client, admin)
│   ├── utils/              # Utilities
│   └── validators/         # Input validation
│
├── __tests__/              # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── e2e/                # End-to-end tests (optional)
│
├── supabase/
│   ├── migrations/         # Database migrations
│   └── seed.sql            # Seed data (optional)
│
├── docs/
│   ├── product-spec.md     # Product definition
│   ├── constitution.md     # Technical principles
│   ├── design-system.md    # Design documentation
│   ├── wireframes/         # Layout documentation
│   └── template-selection.md
│
├── reports/                # Generated during setup (can be deleted)
│   ├── vercel-templates.md
│   ├── shadcn-best-practices.md
│   ├── supabase-patterns.md
│   ├── design-systems.md
│   ├── qa-validation.md
│   └── documentation-audit.md
│
├── CLAUDE.md               # Main Claude context
├── README.md               # User-facing guide
├── DEVELOPMENT.md          # Developer guide
├── API.md                  # API documentation
├── DEPLOYMENT.md           # Deployment guide
├── TROUBLESHOOTING.md      # Common issues
├── tailwind.config.ts      # Tailwind configuration
├── components.json         # Shadcn configuration
├── next.config.mjs         # Next.js configuration
└── package.json            # Dependencies
```

---

## System Component Reference

### 1. Skill (SKILL.md)

**Location**: `.claude/skills/nextjs-project-setup/SKILL.md`

**Purpose**: Main orchestration file that Claude auto-discovers

**Structure**:
```yaml
---
name: nextjs-project-setup
description: Comprehensive Next.js project setup... (auto-discovery trigger)
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__*
---

# Instructions (Markdown content)
```

**How Invoked**: Auto-discovered by Claude based on `description` field

**Key Features**:
- Complexity assessment logic
- Phase orchestration
- Sub-agent delegation via Task tool
- Progressive disclosure (loads only needed docs/agents)

---

### 2. Sub-Agents (7 total)

**Location**: `.claude/agents/nextjs-*.md`

**Purpose**: Specialized AI assistants with isolated context

**Structure**:
```yaml
---
name: nextjs-research-supabase
description: Research Supabase auth patterns... (agent discovery)
model: inherit
tools: mcp__supabase__*, mcp__Ref__*, Read, Write
---

# System Prompt (Markdown content)
```

**How Invoked**: Delegated by skill using Task tool

**Key Features**:
- Separate context window (prevents main context pollution)
- Token budget: ~2500 per agent
- Write reports (~2000 tokens each)
- Parallel execution capability

**Agent Inventory**:
1. `nextjs-research-vercel.md` - Next.js templates
2. `nextjs-research-shadcn.md` - Component patterns
3. `nextjs-research-supabase.md` - Auth & RLS
4. `nextjs-research-design.md` - Design trends
5. `nextjs-design-ideator.md` - Design system generation
6. `nextjs-qa-validator.md` - Quality validation
7. `nextjs-doc-auditor.md` - Documentation audit

---

### 3. Templates (4 total)

**Location**: `.claude/skills/nextjs-project-setup/templates/`

**Purpose**: Structured output formats for consistency

**Template Inventory**:

#### spec-template.md
- Complete project specification
- User stories, personas, acceptance criteria
- Functional & non-functional requirements
- Data model, success criteria

#### wireframe-template.md
- ASCII art wireframe layouts
- Component references, image placeholders
- Responsive breakpoints, interaction notes

#### design-showcase.md
- Design system comparison table
- Expert evaluation matrix (UX, conversion, A11y, mobile, SEO)
- Color palettes, typography, component styles

#### report-template.md
- Standardized agent report format
- Executive summary, findings, recommendations, evidence
- Token budget: ≤2500 tokens

**How Used**: Referenced via `@templates/` in skill and agent instructions

---

### 4. Documentation (Phase Guides)

**Location**: `.claude/skills/nextjs-project-setup/docs/`

**Purpose**: Detailed workflow instructions for each phase

**Structure**:
```
docs/
├── simple-setup.md          # Simple path workflow
└── complex/
    ├── phase-2-template.md  # Template selection
    ├── phase-3-spec.md      # Specification
    ├── phase-4-design.md    # Design system
    ├── phase-5-wireframes.md # Wireframes
    ├── phase-6-implement.md # Implementation
    ├── phase-7-qa.md        # QA validation
    └── phase-8-docs.md      # Documentation
```

**How Used**: Loaded via `@docs/` references when needed (progressive disclosure)

---

### 5. MCP Tools Integration

**Purpose**: External service integration without leaving Claude

**Tools Used**:
- **mcp__vercel__***: List Next.js templates, deployment info
- **mcp__shadcn__***: Search, view, install components
- **mcp__supabase__***: Query schema, create tables, RLS policies
- **mcp__21st-dev__***: Design inspiration, component discovery
- **mcp__Ref__***: Documentation lookup (Next.js, Shadcn, Supabase)
- **mcp__firecrawl__***: Web scraping for research
- **mcp__chrome-devtools__***: E2E testing (optional)

**Configuration**: Defined in `allowed-tools` field of YAML frontmatter

---

## Token Efficiency Breakdown

**Traditional Approach** (read all documentation):
- Next.js docs: 50,000 tokens
- Shadcn docs: 30,000 tokens
- Supabase docs: 40,000 tokens
- Design resources: 20,000 tokens
- **Total**: 140,000 tokens

**Optimized Approach** (this skill):
- Research reports: 8,000 tokens (4 agents × 2,000 each)
- Main skill context: 3,000 tokens
- Phase docs (progressive): 2,600 tokens
- **Total**: 13,600 tokens

**Token Savings**: 90.3% (126,400 tokens saved)

---

## User Interaction Points

Throughout the workflow, users are prompted for decisions:

1. **Complexity Assessment** (Phase 0): Confirm simple vs complex path
2. **Template Selection** (Phase 2): Choose from 3 template options
3. **Specification Review** (Phase 3): Approve product spec and features
4. **Design Selection** (Phase 4): Choose from 3-5 design options, iterate
5. **Wireframe Review** (Phase 5): Select layouts, provide feedback
6. **Implementation Review** (Phase 6): Review progress, test features
7. **Final Review** (Phase 8): Approve documentation, request changes

---

## Troubleshooting

### Issue: Skill Not Auto-Discovered

**Symptom**: User request doesn't trigger skill

**Solutions**:
1. Check YAML frontmatter has `description` field
2. Verify `.claude/skills/nextjs-project-setup/SKILL.md` exists
3. Try explicit invocation: "Use nextjs-project-setup skill"

---

### Issue: Sub-Agent Not Found

**Symptom**: Error "agent not found" during phase execution

**Solutions**:
1. Verify all 7 agents exist in `.claude/agents/`
2. Check filenames: `nextjs-*.md`
3. Verify YAML `name:` field matches filename

---

### Issue: MCP Tools Not Available

**Symptom**: Error "MCP tool not found"

**Solutions**:
1. Check `.mcp.json` configuration
2. Verify MCP servers running
3. Test MCP connection: `/mcp`

---

## Performance Metrics

**Execution Time**:
- Simple path: 15-30 minutes
- Complex path: 2-4 hours (with user feedback)

**Token Usage**:
- Simple path: ~4,000 tokens
- Complex path: ~13,600 tokens

**Cost** (Claude Sonnet 3.5):
- Simple path: ~$0.05
- Complex path: ~$0.24

**Output Quality**:
- 100% specification coverage
- All wireframes with expert evaluation
- 3-5 design options evaluated
- 100% QA validation pass rate

---

## Next Steps

After project setup completion:

1. **Implementation**: Use `/implement` command (from Intelligence Toolkit)
2. **Testing**: Run test suite, fix failures
3. **Deployment**: Follow DEPLOYMENT.md guide
4. **Iteration**: Request changes, refine features

---

**Guide Status**: ✅ Complete
**Last Updated**: 2025-10-29
**Skill Version**: 1.0.0

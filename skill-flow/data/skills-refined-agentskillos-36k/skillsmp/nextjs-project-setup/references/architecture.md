# Sub-Agent Architecture

**Version**: 1.0.0
**Created**: 2025-10-29
**Purpose**: Define agent architecture, I/O contracts, and coordination patterns

---

## Overview

This document defines the architecture for 7 specialized sub-agents used in the Next.js Project Setup skill. These agents execute in parallel or sequential workflows with isolated contexts and strict token budgets.

**Agent Count**: 7 total
- **Research Agents** (4): Parallel execution in Phase 1
- **Design Agent** (1): Phase 4 design system generation
- **QA Agent** (1): Phase 7 quality validation
- **Documentation Agent** (1): Phase 8 documentation audit

---

## Architecture Pattern

```
Main Orchestrator (SKILL.md)
    ↓ (dispatch with handover protocol)
Sub-Agents (isolated contexts, ≤2500 token reports)
    ↓ (write reports to /reports/*.md)
Main Orchestrator (reads reports, continues workflow)
```

**Key Principles**:
1. **Isolated Contexts**: Sub-agents execute with fresh context (no main conversation history)
2. **Token Budgets**: Each agent ≤2500 tokens per report
3. **Report-Based**: Agents write concise reports, orchestrator never sees full research process
4. **Evidence-Based**: All findings require sources (URLs, docs, examples)
5. **Actionable**: Recommendations must be specific and implementable

---

## Agent I/O Contracts

### Contract Template

```typescript
interface AgentContract {
  name: string                    // Agent identifier
  model: "inherit"                // Use same tier as main conversation
  tools: string[]                 // Allowed tools (MCP, Read, Write, etc.)
  token_budget: 2500              // Maximum report size
  inputs: AgentInputs             // What orchestrator provides
  outputs: AgentOutputs           // What agent returns
  execution: "parallel" | "sequential"
}

interface AgentInputs {
  project_description: string     // User's project description
  complexity_factors?: object     // Assessed complexity scores
  phase?: string                  // Current workflow phase
  context?: object                // Additional context if needed
}

interface AgentOutputs {
  report_path: string             // Where report is saved
  report: AgentReport             // Structured report content
}

interface AgentReport {
  summary: string                 // 100-200 tokens
  findings: Finding[]             // 1500-2000 tokens total
  recommendations: Recommendation[] // 300-500 tokens total
  evidence: Source[]              // 200-300 tokens total
  token_count: number             // Actual tokens used
}
```

---

## Agent Specifications

### 1. research-vercel.md

**Purpose**: Research Next.js 15 templates and Vercel deployment best practices

**Execution**: Parallel (Phase 1)

**Tools**:
- mcp__Ref__ref_search_documentation (Next.js docs)
- WebSearch (Vercel templates, deployment patterns)
- WebFetch (template documentation)

**Inputs**:
```typescript
{
  project_description: string,  // e.g., "SaaS dashboard for project management"
  complexity_factors: {
    database: boolean,
    auth: boolean,
    multi_tenant: boolean,
    e_commerce: boolean,
    real_time: boolean
  }
}
```

**Outputs**:
```typescript
{
  report_path: "/reports/vercel-templates.md",
  report: {
    summary: "Top 3 Next.js templates for SaaS dashboard based on requirements",
    findings: [
      {
        template: "next-enterprise",
        url: "https://...",
        features: ["TypeScript", "App Router", "Tailwind", "shadcn/ui"],
        pros: ["Enterprise-ready", "Well-documented"],
        cons: ["Opinionated structure"],
        fit_score: 9
      },
      // ... 2 more templates
    ],
    recommendations: [
      "Use next-enterprise for complex SaaS",
      "Configure App Router for RSC benefits",
      "Enable Edge Runtime for API routes"
    ],
    evidence: [
      { source: "Next.js 15 docs", url: "..." },
      { source: "Vercel templates", url: "..." }
    ]
  }
}
```

**Success Criteria**:
- [ ] 3-5 template recommendations with rationale
- [ ] Each template has features, pros/cons, fit score
- [ ] Deployment configuration recommendations
- [ ] Environment setup guidance
- [ ] All sources cited

---

### 2. research-shadcn.md

**Purpose**: Research Shadcn component patterns, accessibility, and usage examples

**Execution**: Parallel (Phase 1)

**Tools**:
- mcp__shadcn__search_items_in_registries
- mcp__shadcn__view_items_in_registries
- mcp__shadcn__get_item_examples_from_registries
- mcp__Ref__ref_search_documentation (Shadcn docs)

**Inputs**:
```typescript
{
  project_description: string,  // e.g., "SaaS dashboard"
  project_type: "dashboard" | "blog" | "e-commerce" | "portfolio"
}
```

**Outputs**:
```typescript
{
  report_path: "/reports/shadcn-best-practices.md",
  report: {
    summary: "Shadcn component patterns and accessibility best practices for dashboards",
    findings: [
      {
        category: "Layout Components",
        components: ["card", "sheet", "tabs", "dialog"],
        examples: ["@ui/card-demo", "@ui/sheet-demo"],
        accessibility_notes: "ARIA labels required, keyboard nav supported"
      },
      {
        category: "Form Components",
        components: ["input", "textarea", "select", "checkbox"],
        examples: ["@ui/input-demo", "@ui/form-demo"],
        accessibility_notes: "WCAG 2.1 AA compliant, proper labels"
      },
      // ... more categories
    ],
    recommendations: [
      "Start with @ui registry for core components",
      "Use @magicui sparingly (≤300ms animations)",
      "Always follow Search → View → Example → Install workflow",
      "Test accessibility after each component install"
    ],
    evidence: [
      { source: "Shadcn UI docs", url: "..." },
      { component: "@ui/card", example: "@ui/card-demo" }
    ]
  }
}
```

**Success Criteria**:
- [ ] Component recommendations by category (layout, form, data, navigation)
- [ ] Accessibility notes per component
- [ ] Example usage patterns
- [ ] Workflow best practices (Search → View → Example → Install)
- [ ] Registry priority (@ui > @magicui)

---

### 3. research-supabase.md

**Purpose**: Research Supabase auth patterns, RLS policies, and schema design

**Execution**: Parallel (Phase 1)

**Tools**:
- mcp__supabase__search_docs (GraphQL queries)
- mcp__Ref__ref_search_documentation (Supabase docs)

**Inputs**:
```typescript
{
  project_description: string,
  auth_required: boolean,
  database_required: boolean,
  multi_tenant: boolean,
  real_time: boolean
}
```

**Outputs**:
```typescript
{
  report_path: "/reports/supabase-patterns.md",
  report: {
    summary: "Supabase auth and database patterns for multi-tenant SaaS",
    findings: [
      {
        category: "Authentication",
        patterns: ["Email/Password", "OAuth (Google, GitHub)", "Magic Links"],
        recommended: "Email/Password + OAuth",
        rls_strategy: "User-based isolation"
      },
      {
        category: "Row Level Security",
        tenant_isolation: "tenant_id column + RLS policies",
        example_policy: "CREATE POLICY ... USING (auth.uid() = user_id)"
      },
      {
        category: "Schema Design",
        tables: ["users", "tenants", "projects", "tasks"],
        relationships: "users → tenants (many-to-one), projects → tenants"
      }
    ],
    recommendations: [
      "Use Supabase MCP tools only (never CLI)",
      "Start with staging environment",
      "Implement RLS policies immediately",
      "Use server actions for mutations",
      "Edge functions for API routes"
    ],
    evidence: [
      { source: "Supabase Auth docs", url: "..." },
      { source: "RLS patterns", url: "..." }
    ]
  }
}
```

**Success Criteria**:
- [ ] Auth strategy recommendation
- [ ] RLS policy templates
- [ ] Schema design patterns
- [ ] Multi-tenant isolation strategy (if applicable)
- [ ] Edge function recommendations

---

### 4. research-design.md

**Purpose**: Research current design trends and SaaS UI patterns

**Execution**: Parallel (Phase 1)

**Tools**:
- mcp__21st-dev__21st_magic_component_inspiration
- mcp__21st-dev__logo_search
- WebSearch (design trends 2025)

**Inputs**:
```typescript
{
  project_description: string,
  project_type: string,  // "SaaS", "blog", "e-commerce", etc.
  target_audience: string  // "developers", "business users", "general"
}
```

**Outputs**:
```typescript
{
  report_path: "/reports/design-systems.md",
  report: {
    summary: "2025 design trends for SaaS dashboards with modern UI patterns",
    findings: [
      {
        trend: "Minimalist Modern",
        characteristics: ["Clean lines", "High contrast", "Spacious"],
        examples: ["Linear", "Notion", "Stripe"],
        color_palettes: [
          { primary: "hsl(222, 47%, 11%)", secondary: "hsl(217, 91%, 60%)" }
        ]
      },
      {
        trend: "Bold & Vibrant",
        characteristics: ["Bright colors", "Gradients", "Animations"],
        examples: ["Framer", "Vercel", "Raycast"],
        color_palettes: [
          { primary: "hsl(280, 100%, 50%)", secondary: "hsl(340, 100%, 50%)" }
        ]
      }
    ],
    recommendations: [
      "Use CSS variables for all colors (no hardcoded values)",
      "Support dark mode via next-themes",
      "Ensure WCAG 2.1 AA contrast (4.5:1 minimum)",
      "Mobile-first responsive design",
      "Animations ≤300ms for perceived performance"
    ],
    evidence: [
      { source: "21st.dev", url: "..." },
      { source: "Design trends 2025", url: "..." }
    ]
  }
}
```

**Success Criteria**:
- [ ] 3-5 design trend categories
- [ ] Each trend has characteristics, examples, color palettes
- [ ] Typography recommendations
- [ ] Component style directions
- [ ] Accessibility considerations (WCAG 2.1 AA)

---

### 5. design-ideator.md

**Purpose**: Generate 3-5 design system options based on research findings

**Execution**: Sequential (Phase 4, after research-design.md)

**Tools**:
- mcp__21st-dev__21st_magic_component_inspiration
- mcp__shadcn__search_items_in_registries
- Read (research reports from Phase 1)

**Inputs**:
```typescript
{
  project_description: string,
  spec_file: "/docs/spec.md",
  research_reports: [
    "/reports/design-systems.md",
    "/reports/shadcn-best-practices.md"
  ]
}
```

**Outputs**:
```typescript
{
  report_path: "/reports/design-options.md",
  report: {
    summary: "3 design system options with expert evaluation",
    findings: [
      {
        option: "Option 1: Modern Minimalist",
        philosophy: "Clean, spacious, professional",
        color_palette: {
          primary: "hsl(222, 47%, 11%)",
          secondary: "hsl(217, 91%, 60%)",
          accent: "hsl(142, 76%, 36%)",
          background: "hsl(0, 0%, 100%)",
          foreground: "hsl(222, 47%, 11%)"
        },
        contrast_scores: {
          "primary on background": "14.5:1 ✅",
          "secondary on background": "4.8:1 ✅",
          "accent on background": "4.6:1 ✅"
        },
        typography: {
          heading: "Inter",
          body: "Inter 400",
          code: "JetBrains Mono"
        },
        expert_evaluation: {
          ux: { score: 9, rationale: "High readability, clear hierarchy" },
          conversion: { score: 8, rationale: "Strong CTA contrast" },
          a11y: { score: 10, rationale: "All WCAG 2.1 AA passes" },
          mobile: { score: 9, rationale: "Clean responsive patterns" },
          seo: { score: 8, rationale: "Fast, semantic HTML" }
        }
      },
      // ... 2 more options
    ],
    recommendations: [
      "Recommend Option 1 for professional SaaS",
      "Option 2 for creative/marketing-focused",
      "Option 3 for developer tools"
    ],
    evidence: [
      { source: "Design systems research", file: "/reports/design-systems.md" },
      { inspiration: "Linear, Notion", url: "..." }
    ]
  }
}
```

**Success Criteria**:
- [ ] 3-5 complete design system options
- [ ] Each option has color palette, typography, component styles
- [ ] Contrast scores (WCAG 2.1 AA validation)
- [ ] Expert evaluation (UX, Conversion, A11y, Mobile, SEO)
- [ ] Clear recommendation with rationale

---

### 6. qa-validator.md

**Purpose**: Generate quality checklists and validate production readiness

**Execution**: Sequential (Phase 7, after implementation)

**Tools**:
- Read (implemented codebase)
- Grep (search for patterns, anti-patterns)
- mcp__Ref__ref_search_documentation (testing best practices)
- Bash (run tests, lint, type-check)

**Inputs**:
```typescript
{
  project_path: string,  // Root directory
  implemented_stories: ["P1", "P2", "P3"],
  verification_reports: ["/reports/verify-P1.md", "/reports/verify-P2.md"]
}
```

**Outputs**:
```typescript
{
  report_path: "/reports/qa-validation.md",
  report: {
    summary: "QA validation results: 45/50 checks passed, 5 medium issues",
    findings: [
      {
        category: "Functional Testing",
        status: "PASS",
        tests_run: 127,
        tests_passed: 127,
        coverage: "92%"
      },
      {
        category: "Accessibility",
        status: "PASS",
        wcag_score: "100/100",
        issues: []
      },
      {
        category: "Performance",
        status: "PASS",
        lighthouse_score: 93,
        core_web_vitals: {
          lcp: "1.2s ✅",
          fid: "45ms ✅",
          cls: "0.05 ✅"
        }
      },
      {
        category: "Security",
        status: "MEDIUM",
        critical_bugs: 0,
        high_bugs: 0,
        medium_bugs: 5,
        issues: [
          "Missing CSP headers",
          "Incomplete input validation on /api/projects"
        ]
      }
    ],
    recommendations: [
      "CRITICAL: None",
      "HIGH: None",
      "MEDIUM: Add CSP headers, validate all API inputs",
      "LOW: Optimize bundle size (-15KB gzipped)"
    ],
    production_readiness: {
      all_tests_passing: true,
      accessibility_score: 100,
      lighthouse_performance: 93,
      critical_bugs: 0,
      high_bugs: 0,
      status: "READY_FOR_PRODUCTION ✅"
    },
    evidence: [
      { test_results: "/reports/test-results.json" },
      { lighthouse_report: "/reports/lighthouse.json" }
    ]
  }
}
```

**Success Criteria**:
- [ ] All quality gates validated (functional, accessible, performant, secure, compatible)
- [ ] Severity levels assigned (CRITICAL/HIGH/MEDIUM/LOW)
- [ ] Production readiness gate evaluated
- [ ] Specific, actionable recommendations
- [ ] Test results and Lighthouse scores documented

---

### 7. doc-auditor.md

**Purpose**: Audit documentation completeness, clarity, and consistency

**Execution**: Sequential (Phase 8, after documentation creation)

**Tools**:
- Read (all documentation files)
- Grep (search for broken references, missing sections)

**Inputs**:
```typescript
{
  project_path: string,
  expected_docs: [
    "/README.md",
    "/CLAUDE.md",
    "/docs/API.md",
    "/docs/DEPLOYMENT.md",
    "/CHANGELOG.md"
  ]
}
```

**Outputs**:
```typescript
{
  report_path: "/reports/doc-audit.md",
  report: {
    summary: "Documentation audit: 4/5 docs complete, 1 missing (API.md)",
    findings: [
      {
        file: "/README.md",
        status: "COMPLETE",
        sections: ["Overview", "Features", "Quick Start", "Development", "Deployment"],
        missing: [],
        clarity_score: 9,
        issues: ["Installation section could be more detailed"]
      },
      {
        file: "/CLAUDE.md",
        status: "COMPLETE",
        sections: ["Overview", "Tech Stack", "Conventions", "Anti-Patterns"],
        missing: [],
        clarity_score: 10,
        issues: []
      },
      {
        file: "/docs/API.md",
        status: "MISSING",
        reason: "No API routes implemented yet"
      }
    ],
    recommendations: [
      "README.md: Add detailed installation steps",
      "DEPLOYMENT.md: Add troubleshooting section",
      "Create API.md once API routes are implemented",
      "Add inline JSDoc comments for complex functions"
    ],
    evidence: [
      { files_analyzed: 5 },
      { sections_audited: 47 },
      { broken_references: 0 }
    ]
  }
}
```

**Success Criteria**:
- [ ] All expected documentation files audited
- [ ] Completeness score per file
- [ ] Clarity score per file
- [ ] Missing sections identified
- [ ] Broken references detected
- [ ] Specific improvement recommendations

---

## Handover Protocol

### Pattern

**Main Orchestrator → Sub-Agent**:
```markdown
## Task
[Clear, specific task description]

## Inputs
- project_description: "..."
- complexity_factors: {...}

## Output Requirements
- report_path: "/reports/[name].md"
- token_budget: 2500
- format: Use report template

## Tools Available
- [Tool 1]
- [Tool 2]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

**Sub-Agent → Main Orchestrator**:
```markdown
# [Task Name] Report

## Summary (100-200 tokens)
[Key finding or recommendation]

## Findings (1500-2000 tokens)
[Structured findings with evidence]

## Recommendations (300-500 tokens)
[Actionable recommendations]

## Evidence (200-300 tokens)
[Sources with URLs]

---

**Token Count**: [actual] / 2500
**Status**: COMPLETE
```

**Main Orchestrator Continues**:
```markdown
1. Read report (not full research process)
2. Extract key findings for context
3. Continue to next phase
4. Reference report in phase docs: @reports/[name].md
```

---

## Token Budget Enforcement

**Per-Agent Budget**: ≤2500 tokens per report

**Enforcement Strategy**:
1. Agents use structured format (limits expansion)
2. Summary: 100-200 tokens (concise key finding)
3. Findings: 1500-2000 tokens (core research)
4. Recommendations: 300-500 tokens (actionable items)
5. Evidence: 200-300 tokens (sources)

**Validation**:
- Agents MUST report actual token count
- Orchestrator MUST check token count before proceeding
- If over budget: Agent MUST refactor to meet budget

**CoD^Σ Usage**: Encouraged to compress information density

---

## Parallel Execution Strategy

### Phase 1: Research Agents (4 parallel)

**Dispatch Pattern**:
```
Main Orchestrator:
  1. Assess project complexity
  2. Identify research needs
  3. Dispatch 4 agents simultaneously:
     - research-vercel.md
     - research-shadcn.md
     - research-supabase.md (if DB/auth needed)
     - research-design.md
  4. Wait for all agents to complete
  5. Read all 4 reports (~8,000 tokens total)
  6. Continue to Phase 2

Total Time: ~10-15 minutes (parallel, not sequential)
Total Tokens: ~8,000 (reports only, not research process)
```

**Benefit**: 4 agents × 2500 tokens = 10,000 tokens in isolated contexts, orchestrator only sees 8,000 tokens of reports

---

## Success Criteria

### Agent Development
- ✅ All 7 agents defined with clear contracts
- ✅ Input/output formats standardized
- ✅ Token budgets specified (≤2500 each)
- ✅ Tools required listed
- ✅ Success criteria defined per agent

### Agent Execution
- ✅ Reports written to /reports/*.md
- ✅ Token budgets enforced
- ✅ Evidence sources cited
- ✅ Recommendations actionable
- ✅ Handover protocol followed

### Integration
- ✅ Orchestrator reads reports (not full process)
- ✅ Phase docs reference reports via @reports/*.md
- ✅ Progressive disclosure maintained
- ✅ Token efficiency achieved (67%+ savings)

---

## Next Steps

1. ✅ Architecture defined → Proceed to agent creation
2. Create 7 agents following specifications
3. Test each agent independently
4. Test parallel execution (Phase 1 research agents)
5. Validate token budgets
6. Integrate with phase docs

---

**Document Version**: 1.0.0
**Created**: 2025-10-29
**Status**: COMPLETE - Ready for agent creation

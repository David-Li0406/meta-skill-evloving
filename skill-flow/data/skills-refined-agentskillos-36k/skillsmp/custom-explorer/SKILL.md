---
name: custom-explorer
description: Evaluate custom stack combinations against requirements. Use when user proposes their own technology combination or asks to compare a specific stack against alternatives.
---

# Custom Stack Combination Explorer

Evaluate user-proposed stack combinations against project requirements.

## Standalone Usage

Can be invoked directly:
- "Evaluate this stack: React + Fastify + MongoDB + Vercel"
- "Would Next.js + PlanetScale + Clerk work for my project?"
- "Compare my proposed stack against the recommendations"

## Process

### Step 1: Capture Components

Document the proposed stack:

```yaml
proposed_stack:
  frontend: "<technology>"
  backend: "<technology>"
  database: "<technology>"
  auth: "<technology>"
  hosting: "<platform>"
  other:
    - "<additional component>"
```

### Step 2: Gather Requirements (if not provided)

Key questions:
- What's the expected traffic/scale?
- What's the team's ops maturity?
- What's the budget range?
- Any compliance requirements?
- Cloud preference?

### Step 3: Fit Assessment

Evaluate against requirements:

| Requirement | Fit | Notes |
|-------------|-----|-------|
| Budget | ✓/✗/~ | Cost comparison |
| Ops maturity | ✓/✗/~ | Team capability match |
| Compliance | ✓/✗/~ | Meets requirements? |
| Scalability | ✓/✗/~ | Handles workload? |
| Team skills | ✓/✗/~ | Learning curve? |
| Local dev | ✓/✗/~ | Good DX possible? |

### Step 4: Pros/Cons Analysis

Compare to conventional alternatives.

### Step 5: Cost Estimate

Use relevant cost evaluator skills.

### Step 6: Local Dev Assessment

Use local-dev-evaluator skill.

## Output Contract

```yaml
custom_evaluation:
  stack_name: "<descriptive name>"

  proposed_components:
    frontend:
      technology: "<tech>"
      hosting: "<platform>"
    backend:
      technology: "<tech>"
      hosting: "<platform>"
    database:
      technology: "<tech>"
      hosting: "<managed|self-hosted>"
    auth:
      provider: "<solution>"
    other: []

  fit_assessment:
    overall_score: "<strong|moderate|weak>"
    fits_budget: true|false
    fits_ops_maturity: true|false
    fits_compliance: true|false
    fits_scalability: true|false
    fits_team_skills: true|false
    notes: "<explanation>"

  pros:
    - "<advantage 1>"
    - "<advantage 2>"

  cons:
    - "<disadvantage 1>"
    - "<disadvantage 2>"

  risks:
    - risk: "<risk>"
      severity: "<high|medium|low>"
      mitigation: "<how to mitigate>"

  cost_estimate:
    baseline_monthly: "<$X>"
    at_10x_scale: "<$X>"
    cost_drivers:
      - "<driver 1>"

  local_dev:
    recommended_approach: "<approach>"
    complexity: "<low|medium|high>"
    time_to_first_run: "<estimate>"
    parity_notes: "<what differs from prod>"

  comparison_to_conventional:
    conventional_option: "<what would typically be recommended>"
    better_at:
      - "<where custom stack wins>"
    worse_at:
      - "<where custom stack loses>"

  verdict: "<proceed|reconsider|avoid>"
  verdict_reason: "<explanation>"

  recommendations:
    - "<recommendation if proceeding>"
```

## Example: React + Fastify + MongoDB + Railway

```yaml
custom_evaluation:
  stack_name: "React + Fastify + MongoDB on Railway"

  proposed_components:
    frontend:
      technology: "React (Vite)"
      hosting: "Railway (static)"
    backend:
      technology: "Fastify (Node.js)"
      hosting: "Railway"
    database:
      technology: "MongoDB"
      hosting: "Railway (managed)"
    auth:
      provider: "Auth0"

  fit_assessment:
    overall_score: "moderate"
    fits_budget: true      # Railway is cost-effective
    fits_ops_maturity: true # Minimal ops needed
    fits_compliance: false  # MongoDB on Railway - SOC2?
    fits_scalability: true  # Scales well
    fits_team_skills: true  # Common technologies
    notes: "Good fit for startups, verify compliance needs"

  pros:
    - "Simple deployment (Railway handles everything)"
    - "Cost-effective for small-medium scale"
    - "Fastify is very performant"
    - "MongoDB flexible for changing schema"
    - "Good local dev story"

  cons:
    - "MongoDB querying less flexible than SQL"
    - "Railway smaller ecosystem than AWS/GCP"
    - "Auth0 adds per-MAU cost"
    - "Less enterprise compliance options"

  risks:
    - risk: "MongoDB data modeling mistakes"
      severity: "medium"
      mitigation: "Plan schema carefully, consider relationships"
    - risk: "Railway vendor lock-in"
      severity: "low"
      mitigation: "Standard containers, easy to migrate"

  cost_estimate:
    baseline_monthly: "$25-50"
    at_10x_scale: "$200-400"
    cost_drivers:
      - "Railway compute (based on usage)"
      - "Auth0 (if > 7k MAU)"

  local_dev:
    recommended_approach: "docker-compose"
    complexity: "low"
    time_to_first_run: "5-10 minutes"
    parity_notes: "Local MongoDB vs Railway MongoDB (identical)"

  comparison_to_conventional:
    conventional_option: "Next.js + Vercel + Supabase"
    better_at:
      - "Backend flexibility (custom Fastify vs API routes)"
      - "Document-oriented data (if schema is flexible)"
    worse_at:
      - "DX simplicity (more moving parts)"
      - "SQL querying (if needed)"
      - "Built-in auth (Supabase includes auth)"

  verdict: "proceed"
  verdict_reason: "Good fit for the requirements. Consider Supabase if SQL would be beneficial."

  recommendations:
    - "Set up proper MongoDB indexes early"
    - "Use Mongoose for schema validation"
    - "Consider Supabase if relational queries become important"
```

## Evaluation Questions

When assessing custom stacks, ask:

1. **Why this combination?** - Understanding motivation helps assessment
2. **Team experience?** - Familiarity reduces risk
3. **Specific requirements?** - Something driving unconventional choice?
4. **Flexibility needed?** - Can components be swapped later?
5. **Budget constraints?** - Cost-driven decisions?

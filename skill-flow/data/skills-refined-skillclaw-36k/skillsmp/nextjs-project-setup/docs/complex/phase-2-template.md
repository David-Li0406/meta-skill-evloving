# Phase 2: Template Selection (Complex Path)

**Duration**: 20-30 minutes
**Prerequisites**: Phase 1 research reports completed
**Next Phase**: Phase 3 (Specification)

---

## Overview

**Purpose**: Select optimal Next.js template based on project requirements and research findings

**Inputs**:
- User requirements (from initial conversation)
- Research reports:
  - `/reports/vercel-templates.md` (template analysis)
  - `/reports/shadcn-best-practices.md` (component patterns)
  - `/reports/supabase-patterns.md` (if database needed)

**Outputs**:
- Installed Next.js template
- `/docs/template-selection.md` (rationale and features)
- Environment setup checklist

---

## Tools Required

- **Vercel MCP**: Template discovery and comparison
- **File System**: Template installation and verification
- **Bash**: Installation commands

---

## Workflow (CoD^Σ)

```
Requirements ∧ Research_Reports → Analysis
  ↓
Vercel_MCP(filter, compare) → Candidates[3]
  ↓
User_Selection → Install
  ↓
Verification ∧ Documentation → Complete
```

---

## Detailed Steps

### Step 1: Analyze Requirements

Review user requirements against template features:

**Database Requirements**:
```
IF database_required THEN
  IF database = Supabase THEN
    Filter := {Supabase_Starter, Stripe_Subscription_Starter}
  ELSE
    Alternative_Recommendation
ELSE
  Filter := No_DB_Templates
```

**Feature Matrix**:
| Requirement | Template Candidates |
|-------------|-------------------|
| Auth + DB | Supabase Starter |
| SaaS + Payments | Stripe Subscription Starter |
| E-commerce | Next.js Commerce |
| Blog/Content | Blog Starter, Portfolio |
| Enterprise | Enterprise Boilerplate |
| Multi-tenant | ⚠️ Requires custom implementation on Supabase base |

### Step 2: Load Research Report

Read `/reports/vercel-templates.md` for:
- Template comparison matrix
- Pro/con analysis
- Setup requirements
- Known issues or limitations

**Evidence Required** (Constitution Article II):
- Template features (file:line from vercel-templates.md)
- Setup complexity assessment
- Integration compatibility

### Step 3: Template Comparison

**Use Vercel MCP**:
```typescript
// Search templates by feature
mcp__vercel__list_templates(filter: {
  framework: "nextjs",
  features: ["database", "auth", "typescript"]
})

// Get detailed template info
mcp__vercel__get_template_info(template_id)
```

**Present Top 3 Options**:

**Format**:
```markdown
### Option 1: [Template Name]
**Best for**: [Use case]
**Features**: [Key features]
**Tech Stack**: [Core technologies]
**Pros**:
- [Advantage 1]
- [Advantage 2]
**Cons**:
- [Limitation 1]
- [Limitation 2]
**Setup Time**: [Estimate]
**GitHub**: [Repository URL]
```

### Step 4: User Selection

Present options and ask user to select. Consider:
- **Project requirements** alignment
- **Team expertise** with tech stack
- **Setup complexity** vs timeline
- **Maintenance** and community support
- **Extensibility** for future features

### Step 5: Install Template

**Recommended Installation**:
```bash
# Method 1: NPM (fastest)
npx create-next-app@latest project-name --example [template-url]
cd project-name

# Method 2: Vercel CLI (if deploying immediately)
npx vercel init [template-name]

# Verify installation
npm install
npm run dev
```

**Verification Checklist**:
- [ ] Template cloned successfully
- [ ] Dependencies installed (package.json complete)
- [ ] Development server starts without errors
- [ ] Template structure matches documentation
- [ ] Environment variables template exists (.env.example)

### Step 6: Environment Setup

**Create `.env.local` based on template requirements**:

**Supabase Template Example**:
```bash
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=your-anon-key
```

**Stripe Subscription Template Example**:
```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=your-stripe-key
STRIPE_SECRET_KEY=your-stripe-secret
STRIPE_WEBHOOK_SECRET_LIVE=your-webhook-secret
```

**⚠️ Security Note**: NEVER commit `.env.local` to git. Verify `.gitignore` includes it.

---

## Sub-Agents

**None required for this phase** - Uses research from Phase 1 agents

Optional: If custom template evaluation needed, dispatch `template-analyzer` agent

---

## Quality Checks

### Pre-Installation
- [ ] Requirements clearly documented
- [ ] Research reports reviewed
- [ ] Template matches ≥80% of requirements
- [ ] No deal-breaker limitations identified

### Post-Installation
- [ ] Project structure correct (app/ or pages/ directory)
- [ ] TypeScript configured (`tsconfig.json` present)
- [ ] Tailwind CSS set up (`tailwind.config.ts` present)
- [ ] Development server runs successfully
- [ ] No dependency errors in console
- [ ] Environment variables documented

### Template-Specific (Supabase)
- [ ] Supabase client initialized
- [ ] Auth middleware configured
- [ ] Database types generated (if applicable)
- [ ] Row Level Security (RLS) enabled

---

## Outputs

### 1. Installed Template
**Location**: Project root directory
**Status**: Running on http://localhost:3000

### 2. Template Selection Document
**Location**: `/docs/template-selection.md`
**Content**:
```markdown
# Template Selection: [Template Name]

## Decision Rationale
[Why this template was chosen]

## Key Features
- [Feature 1]
- [Feature 2]
- [Feature 3]

## Tech Stack
- Framework: Next.js [version]
- Database: [Supabase | None]
- Auth: [Method]
- Styling: Tailwind CSS + [Component library]
- Language: TypeScript

## Setup Notes
[Installation steps taken, environment variables, special configuration]

## Known Limitations
[Any identified constraints or workarounds needed]

## Next Steps
Phase 3: Product Specification
```

### 3. Environment Checklist
Document all required environment variables and setup steps for team members.

---

## Next Phase Handover

**Prerequisites for Phase 3 (Specification)**:
- ✅ Template installed and running
- ✅ Environment variables configured
- ✅ Development server operational
- ✅ Template features documented
- ✅ Known limitations identified

**Handover Context**:
- Template name and repository URL
- Tech stack summary
- Key template patterns (auth, data fetching, routing)
- Constraints or conventions to follow

**Continue with**: `phase-3-spec.md`

---

## Common Issues & Solutions

### Issue: Template installation fails
**Cause**: Network issues, npm version mismatch, template deprecated
**Solution**:
- Check npm version: `npm --version` (should be ≥8.0)
- Try alternative installation method
- Verify template URL is correct
- Check GitHub repo for known issues

### Issue: Dependencies won't install
**Cause**: Lock file conflicts, peer dependency issues
**Solution**:
```bash
rm -rf node_modules package-lock.json
npm install
```
Or try different package manager (pnpm, yarn)

### Issue: Development server won't start
**Cause**: Port in use, missing environment variables, configuration error
**Solution**:
- Check port 3000: `lsof -i :3000`
- Verify required env vars in `.env.local`
- Check console for specific error messages
- Review template documentation for setup requirements

### Issue: Template doesn't match requirements
**Cause**: Incorrect template selected, requirements changed
**Solution**: Stop and re-evaluate. It's better to select correct template now than migrate later.

---

## Evidence Requirements (Constitution Article II)

All template selections MUST document:
- **Requirements**: Specific user needs (file:line from conversation)
- **Research**: Reference to vercel-templates.md analysis
- **Comparison**: Why this template vs alternatives
- **Validation**: Installation verification steps completed

**Bad**: "Selected Supabase Starter because it seems good"
**Good**: "Selected Supabase Starter because requirements include: auth (conversation:line 5), PostgreSQL database (conversation:line 12), and multi-tenant patterns (research-supabase.md:line 45 confirms template supports this via RLS)"

---

## Success Criteria

- ✅ Template installed successfully
- ✅ All dependencies resolved
- ✅ Development server running
- ✅ Selection rationale documented with evidence
- ✅ Environment setup checklist created
- ✅ Team can replicate setup from documentation
- ✅ Ready to proceed with specification phase

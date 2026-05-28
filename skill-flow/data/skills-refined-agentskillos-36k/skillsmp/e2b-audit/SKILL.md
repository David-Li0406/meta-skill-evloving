---
name: e2b-audit
description: Run accessibility and SEO audits in isolated e2b cloud sandboxes
triggers:
  - accessibility audit
  - seo audit
  - lighthouse audit
  - axe audit
  - pa11y audit
  - wcag compliance
  - a11y check
---

# E2B Audit Skill

Run comprehensive accessibility and SEO audits in isolated e2b cloud sandboxes using Lighthouse, axe-core, and pa11y.

## When to Use

Activate this skill when:
- User asks for accessibility audit/check
- User asks for SEO audit/analysis
- User mentions WCAG compliance
- User wants to run Lighthouse, axe, or pa11y
- User says "audit my site" or similar

## Prerequisites Check

Before running, verify:

```bash
# Check for API key
echo $E2B_API_KEY
```

If not set, inform user:
> E2B_API_KEY is required. Get your key at https://e2b.dev/dashboard

## Workflow

### Step 1: Prepare

1. Check for `e2b-tools.config.ts` in project root
2. If not present, ask user about their dev server setup:
   - What command starts the dev server? (default: `npm run dev`)
   - What port does it run on? (default: 4321)

### Step 2: Run Audit

Execute the audit CLI:

```bash
npx e2b-audit run --verbose
```

Or with specific options:

```bash
# Specific tools only
npx e2b-audit run --tools lighthouse,axe --verbose

# Custom dev server
npx e2b-audit run --dev-command "npm run dev" --dev-port 3000 --verbose

# Custom output location
npx e2b-audit run --output docs/accessibility --verbose
```

### Step 3: Review Results

After audit completes, results are in `docs/audits/`:
- `lighthouse.json` - Performance, accessibility, SEO scores
- `axe.json` - Detailed accessibility violations
- `pa11y.json` - Additional accessibility issues

Read and summarize findings:

```bash
# Check what was generated
ls -la docs/audits/
```

### Step 4: Report Summary

Provide user with:

1. **Scores** (from Lighthouse):
   - Performance: X/100
   - Accessibility: X/100
   - Best Practices: X/100
   - SEO: X/100

2. **Critical Issues** (severity: critical/serious):
   - List top issues from axe/pa11y
   - Include affected elements/selectors

3. **Recommendations**:
   - Prioritized fixes
   - WCAG criteria affected

### Step 5: Offer Remediation

Ask user:
> Would you like me to generate remediation specs for these issues?

If yes, create specs in `docs/accessibility/specs/` or `docs/seo/specs/` following the project's spec format.

## Configuration

If user needs custom config, help create `e2b-tools.config.ts`:

```typescript
import { defineConfig } from '@e2b-tools/core';

export default defineConfig({
  base: {
    sandbox: {
      timeout: 300, // 5 minutes
    },
    devServer: {
      port: 4321,
      command: 'npm run dev',
    },
  },
  audit: {
    tools: {
      lighthouse: true,
      axe: true,
      pa11y: true,
    },
    output: {
      dir: 'docs/audits',
      format: 'json',
    },
  },
});
```

## Troubleshooting

### Sandbox timeout
Increase timeout in config or CLI:
```bash
npx e2b-audit run --timeout 600
```

### Dev server not starting
Check the command and port match your project's setup.

### Missing API key
```bash
export E2B_API_KEY=your_key_here
```

## Example Interaction

**User:** "Can you audit my site for accessibility issues?"

**Assistant:**
1. Check E2B_API_KEY is set
2. Run `npx e2b-audit run --verbose`
3. Wait for completion
4. Read results from `docs/audits/`
5. Summarize findings
6. Offer to create remediation specs

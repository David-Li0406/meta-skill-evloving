---
name: dead-code-cleanup
description: Safely detects and removes truly dead/unused code in Next.js + TypeScript projects. Invoked only via prompt-classifier SEQUENCE (e.g. after verification-guardian flags unused items or explicit "clean dead code" prompt). Prioritizes automation via knip, tiered risk classification, batched proposals, strict safety rails. Goal: high-confidence incremental cleanup with zero breakage.
priority: medium (post-verification or explicit request)
triggers: none (classifier only)
---

# Dead Code Cleanup – Safe & Automated Entropy Fighter

You are the guardian against codebase bloat. Invoke **only** when called by classifier (e.g. "dead-code-cleanup <scope>"). Never decide to run yourself.

## Core Safety Rails – HARD ENFORCED (NEVER violate)
- NEVER remove or suggest removal of:
  - app/**/page.tsx, app/**/layout.tsx, app/**/loading.tsx, app/**/error.tsx, app/**/not-found.tsx
  - app/**/route.ts, app/api/**/route.ts (API entry points)
  - files exporting generateStaticParams, generateMetadata, generateViewport
  - dynamic routes: [param], [...catchAll], [[...optional]]
  - parallel/intercepting routes: @folder, (.)intercept
  - server actions referenced via form action=""
  - barrel files (index.ts) unless confirmed zero side-effects AND no string refs
  - test files, mocks, stories, .stories.tsx unless explicit request
  - anything string-referenced (grep filename without extension)
  - public APIs/exports if project is published as package
- Assume Vercel/Next.js 15+ conventions: app/ and pages/ are magic-routed

## Process (Strict – follow every time)
1. Determine scope from classifier call (whole project, folder, or file)
2. Prefer automated detection:
   - shell "npx knip --include files,exports,types,dependencies --strict --json" → parse JSON
   - If knip missing/not json-capable: shell "npx knip --include exports,types,files"
   - Fallback: shell "tsc --noEmit --noUnusedLocals --noUnusedParameters --pretty"
3. Classify findings into tiers:
   - Tier 1 (very safe): unused imports, locals, parameters
   - Tier 2 (medium risk): unused exports (non-barrel), small helpers
   - Tier 3 (high risk): unused files, dependencies, barrels with potential side-effects
4. Propose batched changes (prefer Tier 1 first; Tier 2/3 only if user approves higher risk)
5. Show git-style diffs or clear edit descriptions
6. After approval: apply → re-run knip/tsc → verification-guardian (scoped)
7. If new dead code surfaces post-removal → continue chain

## Tool Integration
- classifier vocab: dead-code-cleanup <scope>
- use: shell "npx knip ...", read <file>, edit <file> "remove: <reason>", diff <file>, ask-approval, verification-guardian
- search-code for string refs / dependents when needed

## Output Format (Exact)
Scope: <project | folder | file>

Detection Source: knip | tsc | manual

Findings Summary:
- Tier 1 (very safe): X items
- Tier 2 (medium): Y items
- Tier 3 (high risk): Z items

Proposed Changes:
1. edit src/lib/utils.ts "remove unused import { foo } from 'bar'"
   Reason: unused import – zero risk
   Diff: -import { foo } from 'bar';
2. edit app/components/Button.tsx "remove unused prop variant?: string"
   Reason: unused parameter – safe
...

Risk Notes / Exclusions:
- app/api/users/route.ts: API entry – protected
- lib/index.ts: barrel – manual review required

Approval:
- Apply Tier 1 only? [y/n]
- Review / apply Tier 2? [y/n]
- Skip Tier 3? [y/n]

After any change: verification-guardian will run scoped checks.

## Examples

Classifier calls: dead-code-cleanup app/components/
→ Scope: app/components/
  Findings Summary:
  - Tier 1: 7 unused imports/locals
  - Tier 2: 2 unused exports
  - Tier 3: 1 potentially unused file (Button_old.tsx)
  Proposed Changes:
  1. edit app/components/Card.tsx "remove unused import clsx"
  ...
  Approval: Apply Tier 1 only? [y/n]

Explicit prompt: "clean up dead code in lib/"
→ Same structured output, scoped to lib/

Never mass-delete without explicit tiered approval.
Never bypass safety rails.
Safety > speed. Always chain to verification-guardian.
# org standards

development standards and principles from AGENTS.md and CLAUDE.md.

## exploration-first

**never read files blind.** always: `layer` → `outline` → `Read`

| intent | action |
|--------|--------|
| explore codebase | layer → outline → Read |
| find usages | outline --callers=X |
| trace deps | outline --callees=X |
| pre-refactor | layer --check-cycles + --callers |
| review PR | outline --pr=URL |
| review changes | outline --diff=HEAD~1 |

**audit check:** look for layer/outline in recent command history before file reads.

## commit message style

pattern: `feat(ISSUE-123): description`

| prefix | when |
|--------|------|
| feat | new feature |
| fix | bug fix |
| refactor | code restructuring |
| test | adding tests |
| docs | documentation |
| chore | maintenance |

**audit check:** `git log --oneline -20` should show issue references (ARB-, SIP-, etc.)

## issue integration

always reference Linear issues:

- luke-labs: ARB-xxx, KUM-xxx, KOT-xxx, SIN-xxx, WEB-xxx
- spottedinprod: SIP-xxx

**audit check:** commits should reference issues, branches should be named after issues.

## TDD workflow

test-first development:

1. write failing test
2. implement to pass
3. refactor
4. verify with `verify --format=summary`

**audit check:** test files should exist, ideally with git history showing tests before impl.

## voice and style

- lowercase except acronyms (API, LLM, CLI)
- file paths always in backticks: `src/AuthProvider.tsx`
- no corporate speak
- concise, direct

**audit check:** docs and comments should follow style.

## known repositories

### personal (convex stack)

| repo | path | focus |
|------|------|-------|
| arbor | ~/Developer/arbor/arbor-xyz | agents, chat, TDD |
| koto | ~/Developer/koto/koto-xyz | pipedream, onboarding |
| kumori | ~/Developer/kumori/kumori-xyz | notifications, media |
| sine | ~/Developer/sine/sine-xyz | convex↔iOS, media |
| webs | ~/Developer/webs/webs-xyz | web agents, workflows |

**convex stack:** Next.js 16, React 19, Convex, Clerk, Turborepo

## patterns to inherit

from mature projects:

### arbor patterns
- TDD with convex-test
- test colocation (*.test.ts next to source)
- turborepo apps/packages structure
- comprehensive typing

### koto patterns
- pipedream integration
- onboarding flows
- env handling (.env.example)

### kumori patterns
- notification systems
- media/image generation
- AI queue patterns

### webs patterns
- web agent architecture
- reactive client subscriptions
- TDD with playwright

## anti-patterns to avoid

| anti-pattern | why bad | correct |
|--------------|---------|---------|
| reading files blind | wastes context | explore first |
| commits without issues | loses traceability | always reference |
| tests after impl | less effective | TDD |
| corporate speak | unclear | direct voice |
| hardcoded paths | fragile | use conventions |

## audit scoring

| standard | 0 | 1 | 2 |
|----------|---|---|---|
| exploration-first | never | sometimes | always |
| commit messages | no refs | some refs | all refs |
| TDD | no tests | tests exist | tests first |
| voice | corporate | mixed | correct |
| issue integration | none | partial | full |

**passing score:** 7+/10

# flywheel patterns

two flywheels depending on work type:
- **code work**: scope → test → change → test → verify
- **domain work**: research → synthesize → validate → integrate

## code flywheel

the core loop: scope → test → change → test → verify

## scope phase

understand what to build before building:

```bash
# find relevant code
outline --search=featureName src/
outline --callers=functionName

# understand architecture
layer .
layer . --focus="packages/relevant" --depth=2

# check recent changes
outline --diff=HEAD~5
git log --oneline -10 -- relevant/path/
```

**scope questions**:
- what's the smallest valuable increment?
- what tests need to exist?
- what patterns should i follow?
- what might break?

## test phase

write/update tests before or alongside implementation:

### when to test-first

| situation | approach |
|-----------|----------|
| new feature, clear behavior | test-first |
| bug fix | reproduce with test, then fix |
| refactor | ensure coverage, then change |
| experimental | implement, then add tests |
| non-code work | skip |

### test patterns

```bash
# run tests
verify --format=summary

# run specific tests
pnpm --filter @repo/backend test -- --grep="feature"

# check coverage
verify --coverage
```

### test scaffolding

```typescript
// convex function test (convex-test)
it('does the thing', async () => {
  const t = convexTest(schema)
  const asUser = t.withIdentity({ name: 'Luke', subject: 'user_123' })

  // arrange
  // act
  // assert
})

// react component test (@testing-library/react)
it('renders correctly', () => {
  render(<Component />)
  expect(screen.getByText('expected')).toBeInTheDocument()
})
```

## change phase

implement the actual change:

```bash
# read patterns first
outline src/similar-feature/ --format=yaml

# then edit
# Edit tool for targeted changes
# Write tool for new files
```

**change principles**:
- smallest working increment
- follow existing patterns
- don't refactor while implementing
- commit atomic pieces

## verify phase

confirm the change works:

```bash
# core verification
verify --format=summary    # tests
pnpm lint                  # style
pnpm build                 # compilation
pnpm typecheck             # types

# review changes
git diff --stat
outline --diff=HEAD~1      # structural changes
```

**verification checklist**:
- [ ] tests pass (new and existing)
- [ ] no lint errors
- [ ] build succeeds
- [ ] types check
- [ ] no unintended changes

## commit phase

persist the progress:

```bash
git add -A
git commit -m "feat: description

- what was done
- why it was done

🤖 Generated with Claude Code"
```

**commit principles**:
- atomic (one logical change per commit)
- well-messaged (what and why)
- frequent (git is persistent memory)

## full cycle example

```
1. SCOPE
   - outline --search=userAuth src/
   - read existing auth patterns
   - identify: need new middleware

2. TEST
   - write test: it('blocks unauthenticated users')
   - verify --format=summary → RED

3. CHANGE
   - implement authMiddleware.ts
   - follow pattern from existing middleware

4. TEST
   - verify --format=summary → GREEN

5. VERIFY
   - pnpm lint ✅
   - pnpm build ✅
   - pnpm typecheck ✅

6. COMMIT
   - git commit -m "feat: add auth middleware for protected routes"

7. REPEAT
   - next smallest increment
```

## code flywheel anti-patterns

- **skipping scope**: implementing without understanding
- **skipping tests**: "i'll add them later" (you won't)
- **big changes**: doing too much before verifying
- **skipping verify**: assuming tests are enough
- **batching commits**: losing the ability to bisect

---

## domain flywheel

the core loop: research → synthesize → validate → integrate

### research phase

gather from primary sources, not summaries:

```bash
# live documentation
ref_search_documentation "{library} {feature} guide"
ref_read_url "{authoritative_doc_url}"

# actual code
# read source repos (sonner, vaul, etc.)

# talks and articles
# find author's own words, not third-party summaries
```

**research questions**:
- what are the primary sources? (not blog posts, actual docs/code)
- what does the author themselves say?
- what's the current version/state?
- what are experts using in practice?

**minimum bar**:
- 2-3 `ref_search_documentation` calls
- 1-2 `ref_read_url` calls to actual docs
- github repo exploration for code-heavy domains

### synthesize phase

distill into actionable patterns:

```
while researching:
  1. extract decision trees (if X then Y)
  2. identify concrete values (300ms, ease-out, etc.)
  3. note anti-patterns with examples
  4. find integration points with user's tools
```

**synthesis questions**:
- can someone use this without re-reading sources?
- are there if/then rules, not just philosophy?
- are values concrete (numbers, timings, easings)?
- would an expert recognize this as informed?

### validate phase

external check before declaring done:

```bash
# pair quick check
copilot -p --model gemini-3-pro \
  "Domain skill depth check.

   Task: {description}
   Sources consulted: {ref_calls_made}
   Artifacts: {file_list}

   Validate:
   - Primary sources used? (not just web scrapes)
   - Decision trees present? (not just philosophy)
   - Concrete values? (numbers, timings)
   - Would expert recognize as informed?

   Output JSON: {pass, depth_score, issues[], missing_sources[], confidence, escalate}"
```

**routing**:
- confidence >= 8: proceed to integrate
- confidence 5-7: escalate to pair thorough
- confidence < 5: more research needed

### integrate phase

connect to user's existing workflow:

```bash
# find user's patterns
outline ~/Developer/components --search=similar
layer ~/Developer/arbor/arbor-xyz

# reference in skill
# "works with your existing X pattern"
# "integrate with ~/Developer/components/Y"
```

**integration questions**:
- does this reference user's actual tools?
- can they apply this tomorrow?
- what's the first thing they'd do with this?

## domain full cycle example

```
1. RESEARCH
   - ref_search_documentation "framer motion animation"
   - ref_read_url "https://www.framer.com/motion/animation/"
   - read sonner source: github.com/emilkowalski/sonner
   - find Emil's talks/articles

2. SYNTHESIZE
   - extract timing values (200-250ms)
   - create decision trees (if toast → slide, if modal → scale)
   - note anti-patterns (bounce without purpose)
   - map to user's component lib

3. VALIDATE (pair quick)
   - check: primary sources used? yes (3 ref calls, repo read)
   - check: decision trees? yes (if/then for each component)
   - check: concrete values? yes (ms, easings)
   - confidence: 8 → proceed

4. INTEGRATE
   - reference ~/Developer/components patterns
   - add "works with your Radix setup"
   - include code samples that match their stack

5. AGENTIC REVIEW (pair thorough if needed)
   - final depth check
   - catch any blind spots

6. USER CONFIRMS DONE
```

## domain flywheel anti-patterns

- **surface research**: web scrapes instead of primary sources
- **philosophy only**: no decision trees or concrete values
- **no integration**: generic patterns that don't fit user's stack
- **skipping validate**: self-review misses blind spots
- **declaring done early**: user hasn't confirmed

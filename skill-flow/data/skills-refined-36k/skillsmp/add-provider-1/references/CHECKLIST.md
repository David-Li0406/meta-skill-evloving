# Comprehensive Checklists: Provider Integration Verification

Complete verification steps for all 6 work streams, plus pre-implementation research.

---

## ⚠️ PRE-IMPLEMENTATION: Research & Capability Audit

**Do this BEFORE starting Stream 1. This is critical for correct implementation.**

### Research Phase
- [ ] Read [RESEARCH-GUIDE.md](RESEARCH-GUIDE.md) completely
- [ ] Visited provider's official documentation site
- [ ] Identified official config file locations (project-level and global)
- [ ] Tested config files yourself (if possible)

### Capability Audit (All 11 Primitives)
- [ ] Agent Mode: support level documented with evidence
- [ ] Skills / Workflows: support level documented with evidence
- [ ] Tool Integrations (MCP): support level documented with evidence
- [ ] Persistent Instructions: support level documented with evidence
- [ ] Global Instructions: support level documented with evidence
- [ ] Path-Scoped Rules: support level documented with evidence
- [ ] Slash Commands: support level documented with evidence
- [ ] Custom Agents: support level documented with evidence
- [ ] Permissions & Guardrails: support level documented with evidence
- [ ] Lifecycle Hooks: support level documented with evidence
- [ ] Verification / Evals: support level documented with evidence

### Documentation
- [ ] Created research summary with links to official docs
- [ ] Each primitive has a support level decision (full/partial/diy/none)
- [ ] Each support level decision has evidence (link to docs)
- [ ] All config file locations are from official sources, not guesses
- [ ] Verified no overlaps or conflicts between primitives

**⚠️ Do NOT proceed to Stream 1 until this section is 100% complete.**

---

## Stream 1: Type System Verification

### Provider Union Types
- [ ] `site/src/data/primitives.ts` - Added new provider to `Provider` type
- [ ] `site/src/data/fileTree.ts` - Added new provider to `Provider` type
- [ ] `site/src/data/comparison.ts` - Added new provider to `Provider` type (check interface)
- [ ] Verify all type names use exact same casing (lowercase)
- [ ] Run `npm run typecheck` - Should show errors about missing data (expected)

### UI Provider Labels
- [ ] `site/src/components/PrimitiveCards/PrimitiveCard.tsx` - Added to `providerLabels` Record
- [ ] Label is human-readable (e.g., "Cursor", "GitHub Copilot", "Claude Code")
- [ ] No duplicate labels

### TypeScript Configuration
- [ ] No import errors
- [ ] Provider type is imported in all files that reference it
- [ ] No "Cannot find type" errors

---

## Stream 2: Data Layer Verification

### Primitives Implementations
- [ ] `site/src/data/primitives.ts` - Added provider entry for ALL 11 primitives:
  - [ ] Agent Mode
  - [ ] Skills / Workflows
  - [ ] Tool Integrations (MCP)
  - [ ] Persistent Instructions
  - [ ] Global Instructions
  - [ ] Path-Scoped Rules
  - [ ] Slash Commands
  - [ ] Custom Agents
  - [ ] Permissions & Guardrails
  - [ ] Lifecycle Hooks
  - [ ] Verification / Evals

**For each primitive entry, verify:**
- [ ] `provider` field matches exact type name
- [ ] `implementation` is 1-2 sentences, descriptive
- [ ] `location` is either file path or feature name
- [ ] `support` is one of: 'full' | 'partial' | 'diy' (not 'none')

### Comparison Matrix
- [ ] `site/src/data/comparison.ts` - Added provider field to ALL 11 `ComparisonRow` entries

**For each comparison row, verify:**
- [ ] `primitiveId` matches a primitive id from primitives.ts
- [ ] Provider object has all 3 fields:
  - [ ] `level` is 'full' | 'partial' | 'none'
  - [ ] `implementation` matches primitives.ts (or is very similar)
  - [ ] `location` matches primitives.ts (or is very similar)
- [ ] Support levels are consistent between primitives.ts and comparison.ts

### File Tree Structure
- [ ] `site/src/data/fileTree.ts` - Added `{provider}Tree` constant
- [ ] `site/src/data/fileTree.ts` - Added `{provider}GlobalTree` constant
- [ ] `site/src/data/fileTree.ts` - Added provider to `trees` mapping
- [ ] `site/src/data/fileTree.ts` - Added provider to `globalTrees` mapping

**For file tree entries, verify:**
- [ ] `id` attributes are unique across all file nodes
- [ ] File paths follow provider's actual documentation (not guesses)
- [ ] Labels are descriptive (e.g., "Project Instructions", "Global Settings")
- [ ] `loadOrder` is consistent (1 for base, 2+ for specialized)
- [ ] Examples are valid and helpful
- [ ] Exact syntax matches official docs (frontmatter fields, file names, etc.)

**File Tree Completeness Check:**
- [ ] Demonstrates ALL primitives with full/partial support (not just 1-2)
- [ ] Has 2-3 examples per primitive type (agents, skills, commands, etc.)
- [ ] Includes both project-level AND global-level examples
- [ ] Shows nested directory examples (e.g., `frontend/.cursor/instructions.md`)
- [ ] Parity check: Compare line counts with other providers
  - Run: `wc -l site/src/data/fileTree.ts`
  - Compare demonstrated primitive types across providers
  - If your tree has <100 lines and others have 300+, investigate why
  - Sparse trees make providers look incomplete even with 11/11 support

### Data Consistency
- [ ] All 11 primitives have exactly matching IDs between primitives.ts and comparison.ts
- [ ] No typos in provider names (must be lowercase)
- [ ] Run `npm run typecheck` - Should have NO errors now

---

## Stream 3: UI Components Verification

### Comparison Table Headers
- [ ] `site/src/components/ProviderComparison/ComparisonTable.tsx` - Added `<th>` for new provider
- [ ] Header includes provider name
- [ ] Header includes emoji (if using emoji column headers)
- [ ] Header has proper Tailwind classes (text-center, text-sm, etc.)

### Table Rows
- [ ] Added `<td>` for new provider to table rows
- [ ] Cell contains `<SupportBadge level={row.{provider}.level} />`
- [ ] Cell has proper Tailwind classes (text-center)
- [ ] Badge styling is consistent with other providers

### Expanded Row Component
- [ ] `ExpandedRow` state typing updated: `const [copiedLocation, setCopiedLocation] = useState<'copilot' | 'claude' | '{provider}' | null>(null)`
- [ ] `handleCopy` function signature updated: `(provider: 'copilot' | 'claude' | '{provider}', location: string) => void`
- [ ] `colSpan` updated to include new provider column (e.g., 3 providers = colSpan={4})
- [ ] Grid layout updated: `md:grid-cols-X` where X = number of providers
- [ ] New provider details section added to expanded row:
  - [ ] Provider name in `<h4>`
  - [ ] Implementation description in `<p>`
  - [ ] Location in `<code>`
  - [ ] Copy button with proper click handler

### Styling & Responsiveness
- [ ] Mobile view: stacks providers vertically
- [ ] Medium+ view: displays all providers side-by-side
- [ ] Dark mode: text is readable (verify dark: classes)
- [ ] Copy button states work (clicked → "Copied" → reset)
- [ ] No overflow issues on any screen size

### Visual Verification
- [ ] `npm run dev` - Load comparison section
- [ ] All provider columns visible
- [ ] All 11 primitives listed
- [ ] Support badges show correct colors
- [ ] Click row to expand → shows all provider details
- [ ] Copy buttons work for each provider
- [ ] Expanded row dismisses when clicking other rows

---

## Stream 4: Testing Verification

### E2E Test Updates
- [ ] `site/tests/e2e/comparison.spec.ts` - Header test includes new provider
- [ ] Updated support badge count assertions
- [ ] Updated copy button count assertions (should be 3 for 3 providers)
- [ ] Updated implementation text assertions to match actual data
- [ ] Updated location assertions to match actual file paths

**Test file locations to verify:**
- [ ] All primitives referenced in tests exist in comparison.ts
- [ ] Test expectations match actual data:
  - [ ] Full Support badge count (e.g., 18 for cursor)
  - [ ] Partial badge count (e.g., 5 for cursor)
  - [ ] None badge count (if any)
  - [ ] Implementation text samples
  - [ ] File location samples

### Test Execution
- [ ] `npm run test` - All E2E tests pass
- [ ] No timeout failures
- [ ] No assertion failures
- [ ] No flaky tests (run multiple times)

### Badge Count Math
- [ ] Formula: (11 primitives) × (support levels count)
- [ ] Example for Cursor: (6 full + 5 partial) × 3 providers = ?
- [ ] Verify actual count matches test assertion
- [ ] If test fails: Update expectation to match actual count

---

## Stream 5: Documentation & Integration Verification

### App Integration
- [ ] `site/src/App.tsx` - Comparison section description includes new provider name
- [ ] `site/src/components/Hero/Hero.tsx` - Hero tagline mentions new provider
- [ ] Description text flows naturally with 3+ providers mentioned

### README Documentation
- [ ] `README.md` - Primitive count is accurate (should be 11)
- [ ] `README.md` - Provider comparison description mentions all providers
- [ ] `README.md` - Added new provider section with key paths table
- [ ] File paths in README match actual paths in fileTree.ts
- [ ] All tables format correctly (pipes aligned, no truncation)

### Documentation Consistency
- [ ] Provider name used consistently everywhere (e.g., "Cursor" not "cursor")
- [ ] File paths follow provider's official documentation
- [ ] Examples are valid and copy-pasteable
- [ ] No outdated references to "2 providers" or "2-provider layout"

### Build & Preview
- [ ] `npm run build` - No errors
- [ ] Build completes in reasonable time
- [ ] No warnings about unused code
- [ ] Preview shows correct styling

---

## Stream 6: LLMs Generation Verification

### Generation Script
- [ ] `.github/skills/generate-llms/scripts/generate-llms-full.ts` - Provider name mapping includes new provider
- [ ] Ternary operator or if-else chain handles all providers
- [ ] No defaulting to "Claude Code" for unknown providers

### Generated Files
- [ ] `site/public/llms-full.txt` - Regenerated successfully
- [ ] `site/public/llms.txt` - Regenerated successfully
- [ ] Check file modifications: `git status` shows updated llms files

**Verify llms-full.txt content:**
- [ ] All 11 primitives listed with provider data
- [ ] Provider name displays correctly (e.g., "Cursor" not "cursor")
- [ ] Implementation descriptions are readable
- [ ] File paths are accurate
- [ ] Support levels display correctly (full/partial/none/diy)
- [ ] Tables format correctly with pipe separators

### Generation Command
- [ ] `bun .github/skills/generate-llms/scripts/generate-llms-full.ts` - Completes without errors
- [ ] Files update with new provider data
- [ ] No console errors or warnings

---

## Final Integration Verification

### Type Safety
- [ ] `npm run typecheck` - NO errors
- [ ] `npm run typecheck` - NO warnings about unused types
- [ ] All Provider type references consistent

### Full Test Suite
- [ ] `npm run test` - All tests pass
- [ ] No flaky tests
- [ ] Badge count tests properly updated
- [ ] Header tests include new provider
- [ ] Expansion tests show all providers

### Production Build
- [ ] `npm run build` - Succeeds without errors
- [ ] `npm run build` - No TypeScript errors
- [ ] `npm run build` - No build warnings
- [ ] Output size is reasonable (no unexpected bloat)

### Manual Browser Testing
- [ ] Open http://localhost:5173 (after `npm run dev`)
- [ ] Scroll to Provider Comparison section
- [ ] Verify all 3+ provider columns visible
- [ ] Verify all 11 primitives listed
- [ ] Click each row to expand - shows all provider details
- [ ] Copy buttons work for each provider
- [ ] Mobile view (resize to mobile) - stacks correctly
- [ ] Dark mode toggle - styling correct
- [ ] All text readable (no dark text on dark background)

### Git Status
- [ ] All modified files tracked
- [ ] No uncommitted changes
- [ ] No untracked files (except node_modules, build artifacts)

---

## Common Pitfalls to Avoid

- [ ] **Case sensitivity**: Provider type must be lowercase ('cursor' not 'Cursor')
- [ ] **Missing primitives**: All 11 must be updated, not just a few
- [ ] **Type mismatches**: Provider field value must match the type exactly
- [ ] **colSpan errors**: Table colSpan must match number of columns (primitive + all providers)
- [ ] **Grid layout**: md:grid-cols-X where X = number of provider columns
- [ ] **Copy button count**: Should be 3 for 3 providers, update tests accordingly
- [ ] **Dark mode**: Use dark: prefix for visibility
- [ ] **Badge count tests**: Recalculate based on actual support levels

---

## Common Mistakes to Avoid

Based on real-world provider integrations, avoid these pitfalls:

### Documentation & Verification
- [ ] ❌ **Assumed support levels without checking official docs**
  - ✅ Always visit provider's official documentation (e.g., cursor.com/docs)
  - ✅ Verify file locations, not guessing them
  - ✅ Test support claims or mark as `partial`/`diy`
  - Real example: Cursor Hooks support was initially missed until official docs were checked

### UI Components
- [ ] ❌ **Forgot to add provider tab to File Tree component**
  - ✅ Must add provider to `FileTree.tsx` providers array
  - ✅ User won't see provider selection without this
  - ✅ This is in Stream 3.2, easy to skip

- [ ] ❌ **Used inconsistent emoji across comparison and file tree**
  - ✅ Comparison table and file tree can use different emojis
  - ✅ Use emoji that makes sense for each context
  - ✅ See PATTERNS.md emoji reference for guidance

- [ ] ❌ **File tree too sparse compared to other providers**
  - ✅ File tree is educational material—sparse trees make providers look incomplete
  - ✅ Include 2-3 examples per supported primitive (agents, skills, commands, hooks, etc.)
  - ✅ Add both project-level AND global-level examples
  - ✅ Show nested directory examples (frontend/.{provider}/instructions.md)
  - ✅ Check parity: `wc -l site/src/data/fileTree.ts` and compare line counts
  - Real example: Cursor tree was initially 64 lines vs Copilot 386 lines—made it look incomplete despite 11/11 full support
  - ✅ Use exact syntax from official docs (frontmatter fields, file naming, etc.)

### Data & Testing
- [ ] ❌ **Badge count assertions outdated after support changes**
  - ✅ Recalculate full/partial/none badges after changing support levels
  - ✅ Count: primitives × providers with each support level
  - ✅ Update E2E test assertions in comparison.spec.ts

- [ ] ❌ **Support levels inconsistent between primitives.ts and comparison.ts**
  - ✅ Both files must have matching support levels
  - ✅ Run typecheck after changes to catch mismatches
  - ✅ Verify in Stream 2 data consistency checks

### LLMs Generation
- [ ] ❌ **Forgot to regenerate llms-full.txt**
  - ✅ Must run generation script as final step (Stream 6)
  - ✅ llms files fall out of sync without this
  - ✅ AI agents will have outdated documentation

- [ ] ❌ **Provider name mapping missing in generation script**
  - ✅ Check `.github/skills/generate-llms/scripts/generate-llms-full.ts`
  - ✅ Add provider to ternary/mapping if needed
  - ✅ Verify output matches provider display name

### Commits & PR
- [ ] ❌ **PR description too verbose or unfocused**
  - ✅ Keep summary to one sentence
  - ✅ Organize changes by stream
  - ✅ Link to references instead of inlining details
  - ✅ Include concrete testing steps

- [ ] ❌ **Missed commits or bundled too many changes**
  - ✅ One semantic commit per stream
  - ✅ Easy to review and understand each change
  - ✅ Easier to debug issues later

---

## Sign-Off Checklist

Use this to confirm the provider integration is complete and ready for merge:

- [ ] All 6 streams completed
- [ ] All type errors resolved
- [ ] All E2E tests passing
- [ ] Production build succeeds
- [ ] Browser testing passed (light mode + dark mode + mobile)
- [ ] Documentation updated
- [ ] llms files regenerated
- [ ] Semantic commits created for each stream
- [ ] PR description updated with changes
- [ ] Ready for code review and merge

**Status**: ✅ Ready to Merge / ❌ Blockers Remain

**Blockers** (if any):
- [ ] TypeScript errors: ___________________
- [ ] Test failures: ___________________
- [ ] Build issues: ___________________
- [ ] Other: ___________________

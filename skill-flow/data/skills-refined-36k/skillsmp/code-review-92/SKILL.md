---
name: code-review
description: Code Review Protocol
---

Code review is risk mitigation, not gatekeeping.
The goal is catching issues the author couldn't see — and occasionally sharing a better pattern when it genuinely helps.

# Review Context

Before reviewing, establish context:
- **Intent:** For PRs, check ticket link or description. For pending changes, ask the author. If unclear, clarify before reviewing.
- **Timing:** Is now a good time to add this functionality? Half-baked features or premature additions warrant a `[question]`.
- **Approach:** For complex changes, was the high-level approach discussed before implementation? Complete rewrites are painful — catch architectural misalignment early.
- **Scope:** If diff >800 lines or >20 files, consider suggesting a split (PR) or incremental commits (pending). Large diffs hide bugs.
- **Large diffs:** If diff is truncated or >800 lines, verify critical findings against source before tagging `[blocker]` or `[concern]`.
- **Reviewer limits:** If reviewing outside your expertise, say so upfront. Make assumptions explicit.

# Review Modes

| Mode | Scope | When |
|------|-------|------|
| **Sanity** | Skim diff, check for obvious issues | Trivial changes, config, docs, low-risk path |
| **Standard** | Full diff, P0-P3 checklist, spot-check tests | Most changes — balanced cost/coverage |
| **Deep** | Full diff + context, all priorities, trace data flow | Security-sensitive, core architecture, unfamiliar domain |

Announce mode: `"Reviewing in [mode] because [reason]. Adjust?"`

Default to Standard. Escalate to Deep if review surfaces unexpected complexity.

**Start high level, work down:** In early rounds, focus on design and structure. Defer naming, comments, and style until high-level issues are resolved — low-level notes often become moot after refactoring.

# Review Hierarchy

Review in this order. Stop and flag blockers immediately.

| Priority | Category | Focus |
|----------|----------|-------|
| P0 | **Security** | Injection, auth bypass, secrets exposure, unsafe deserialization |
| P1 | **Correctness** | Does it do what it claims? Edge cases? Error paths? |
| P2 | **Data integrity** | Validation, transactions, idempotency, race conditions |
| P3 | **Architecture & Operability** | Coupling, contracts, backward compat, observability, rollback |
| P4 | **Performance** | Only if measurable impact — N+1, unbounded growth, hot paths |
| P5 | **Maintainability** | Readability, naming, complexity, test quality |
| P6 | **Style** | Only if egregious or violates established conventions |

**Attention budget:** P0-P2 (70%) catch most production incidents — prioritize these. P3-P4 (20%) catch architectural and performance issues. P5-P6 (10%) for maintainability and style only when egregious.

# Review Checklist

Not exhaustive — a mental sweep, not a checkbox exercise.

**Security (P0):**
- [ ] No hardcoded secrets
- [ ] Input validated at boundaries
- [ ] No injection vectors (SQL, command, XSS)
- [ ] Auth/authz not weakened
- [ ] Sensitive data not logged or exposed

**Correctness (P1):**
- [ ] Logic matches stated intent
- [ ] Edge cases handled (null, empty, boundary values)
- [ ] Error paths don't swallow failures silently
- [ ] Return values / exceptions match contract
- [ ] External calls/APIs verified to exist and behave as assumed
- [ ] Impact of code removal assessed (callers, dependencies)
- [ ] New behavior has corresponding tests
- [ ] Changed behavior has updated tests

**Data (P2):**
- [ ] Transactions wrap related mutations
- [ ] Concurrent access considered
- [ ] Migrations are reversible or safe; online-safe (no long-running locks on large tables)

**Architecture & Operability (P3):**
- [ ] Changes respect existing patterns
- [ ] No unnecessary coupling introduced
- [ ] Public API changes are intentional
- [ ] Backward compatibility considered (APIs, schemas, configs)
- [ ] Dependency additions justified; version changes assessed for breaking behavior
- [ ] Behavior not relying on implicit/undocumented configuration
- [ ] New environment variables documented and added to templates
- [ ] User-facing or operational behavior changes are documented
- [ ] README/CHANGELOG updated if user-facing changes
- [ ] Deployment procedure defined if relevant (db change, breaking change, etc.)
- [ ] Logs are actionable (not noisy, not silent)
- [ ] Errors include enough context to debug
- [ ] Metrics/tracing updated if behavior changes
- [ ] Feature flags/kill switches respected if applicable
- [ ] Rollback path exists (code + data)

**Performance (P4):**
- [ ] No N+1 queries or unbounded loops
- [ ] Hot paths not degraded
- [ ] No premature optimization — flag if complexity added for hypothetical gains

**Maintainability (P5):**
- [ ] Code is readable without author's context
- [ ] Names reveal intent
- [ ] Comments explain *why*, not *what* — if code needs explanation, simplify it
- [ ] TODOs have ticket references — naked TODOs pile up and become stale
- [ ] Complexity proportional to problem
- [ ] Tests validate intent, not implementation (see Test Protocol)
- [ ] Tests would fail if the behavior regressed
- [ ] Mock-heavy tests that verify implementation rather than behavior are flagged

# Feedback Format

**Severity tags:**

| Tag | Meaning | Blocking? |
|-----|---------|-----------|
| `[blocker]` | Must fix before merge — security, correctness, data integrity | Yes |
| `[concern]` | Should address — architecture, significant maintainability | Discuss |
| `[suggestion]` | Consider — minor improvements, alternatives | No |
| `[question]` | Clarify — reviewer may be missing context | No |
| `[nit]` | Take or leave — style, naming preference | No |
| `[appraisal]` | Acknowledge — good pattern, notable improvement, smart decision | No |

**Feedback structure:**
```
[tag] file:line — Brief issue

Why it matters: [impact if not addressed]
Suggestion: [concrete alternative, if any]
```
For `[nit]` and trivial `[suggestion]`: one-liner is fine — skip the template.

**Tone:** Avoid "you" — it shifts focus from code to coder. Use "we" or omit the subject entirely. "You forgot to close the handle" → "File handle left open" or "Can we close the handle here?"

**Example:**
```
[blocker] auth/login.py:47 — SQL injection via username parameter

Why it matters: Allows auth bypass and data exfiltration
Suggestion: Use parameterized query: cursor.execute("SELECT ... WHERE user = %s", (username,))
```

**Repeated patterns:** Don't flag every instance of the same issue. Call out 2-3 occurrences, then ask the author to fix the pattern throughout.

# Review Anti-Patterns

**Don't:**
- Invent requirements or failure modes not implied by the stated goal
- Nitpick style without a style guide (let linters handle it)
- Suggest rewrites when the code works and is readable
- Block on "I would have done it differently" without concrete risk
- Miss security issues while debating naming
- Demand perfection — good enough ships, perfect doesn't
- Accept style changes mixed with functional changes — ask to split
- Expand scope to untouched lines — if the changelist doesn't touch it, file a bug or fix it yourself

**Do:**
- Ask yourself: "How would I solve this?" If differently, why? Is yours shorter/cleaner/safer yet equivalent? Use the difference to guide feedback.
- Frame findings as questions when uncertain — you might be missing context
- Ask questions before demanding changes
- Distinguish preference from requirement
- Consider author's experience level — teach, don't gatekeep
- Offer alternatives when you see potential: simpler logic, existing library, codebase pattern. Frame as questions ("What about...?") — teaches without prescribing, contributes to the solution
- Treat your own confusion as signal — if you struggle to understand it, future maintainers will too
- Document in code, not PR — when a comment needs explanation, ask the author to add a code comment or rename; future readers won't see PR discussions
- Before posting feedback, ask: Is it true? (opinion ≠ truth) Is it necessary? (no nagging, no ego) Is it kind? (no shaming)
- Acknowledge good patterns, not just bad ones. Call out one good decision per substantial review when genuine (brief, no cheerleading)
- Surface low-probability edge cases as `[suggestion]` with explicit risk assessment (likelihood, impact, failure mode). Don't suppress legitimate findings just because they're unlikely — document the tradeoff and let the author decide.

# Approval Criteria

**Approve when:**
- No blockers remain
- Concerns are addressed or explicitly accepted as tech debt (record in `TECH_DEBT.md`)
- Code is better than before (not perfect, better)
- You would be comfortable debugging this at 2am
- You can approve with `[suggestion]`/`[nit]` comments — unblock progress while noting optional improvements
- "No notes" is a valid outcome — don't feel compelled to find something wrong

**Request changes when:**
- Blockers exist (P0-P2 issues)
- Significant concerns unaddressed without rationale
- Intent is unclear and author hasn't clarified

**Comment without blocking when:**
- Only suggestions/nits remain
- Concerns are acknowledged with reasonable deferral plan

# Failure Mode Sweep

Ask questions to surface risks — do not assume intent or invent scenarios.

Before finalizing review, ask:
- If this breaks, how would we notice?
- What's the blast radius?
- What's the worst realistic misuse?

If unsure, raise as `[question]` or `[concern]`, not `[blocker]`.

# Review Summary Format

After review, summarize:

**Compact (all true: Approve/Comment verdict, zero blockers/concerns, ≤3 inline suggestions, ≤3 files, high confidence):**
```
Review: [mode] — Approve
```

**Full (everything else):**
```
Review: [mode] — [verdict: Approve / Request Changes / Comment]

Blockers: [count or "None"]
Concerns: [count or "None"]
Suggestions: [count, optional to list]

Overall: [1-2 sentence assessment]
Blast Radius: [Low: internal refactor | Medium: logic change | High: migration/public API]
Confidence: [high: thorough review | medium: focused on key areas | low: quick pass]
Next step: [e.g., "Merge after addressing minor suggestions" | "Let me know when ready for another look"]
```

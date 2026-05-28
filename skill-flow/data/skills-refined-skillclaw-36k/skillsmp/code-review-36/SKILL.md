---
name: code-review
description: Conduct thorough, actionable code reviews that catch real problems without drowning in noise
invocation: /review
aliases:
  - cr
  - review-pr
---

# Code Review Skill

Conduct thorough, actionable code reviews that catch real problems without drowning in noise.

## When to Use

- Reviewing changes on a feature branch before merge
- Auditing a PR for a project you maintain
- Self-review before opening a PR
- Evaluating contributions to unfamiliar codebases

## Philosophy

Good code review serves three purposes:

1. **Catch defects** — bugs, security holes, performance traps
2. **Enforce consistency** — style, patterns, architectural boundaries
3. **Transfer knowledge** — reviewer learns the change, author learns alternatives

A review that only finds style nits has failed. A review that only finds bugs but ignores maintainability has also failed. Balance matters.

## Context Gathering

Never review blind. The diff alone lacks the information needed to judge whether code is correct, appropriate, or consistent.

### Required Context

| Source | Purpose |
|--------|---------|
| PR description / commit messages | Understand intent |
| `AGENTS.md` | Coding style rules |
| `.rules/*` | Additional project conventions |
| `docs/*-design.md` | Architectural intent |
| `docs/roadmap.md` | Current priorities |
| `docs/documentation-style-guide.md` | Doc conventions |
| Neighbouring files | Established patterns |
| `.github/workflows/*` | CI expectations |

### Detecting Project Type

```bash
# Determine primary language
if [ -f "Cargo.toml" ]; then
    echo "Rust"
elif [ -f "pyproject.toml" ]; then
    echo "Python"
elif [ -f "package.json" ]; then
    echo "TypeScript/JavaScript"
fi
```

### Useful Git Incantations

```bash
# Commits on this branch
git log --oneline $(git merge-base HEAD main)..HEAD

# Files changed with line counts
git diff $(git merge-base HEAD main)..HEAD --stat

# Full diff
git diff $(git merge-base HEAD main)..HEAD

# Show a specific commit
git show <sha> --stat

# Find the merge base
git merge-base HEAD main
```

### GitHub CLI Commands

```bash
# Check if a PR exists for the current branch
gh pr view --json number,title,state 2>/dev/null && echo "PR exists" || echo "No PR"

# Get PR description (body) and metadata
gh pr view --json title,body,baseRefName,headRefName,labels,milestone

# Get just the PR body (useful for piping)
gh pr view --json body --jq '.body'

# Get PR with comments (for context on ongoing discussion)
gh pr view --json body,comments --jq '{body, comments: [.comments[].body]}'

# Get linked issues from PR
gh pr view --json body --jq '.body' | grep -oE '#[0-9]+' | sort -u

# View a linked issue
gh issue view <number> --json title,body

# List PR checks and their status
gh pr checks

# Get PR diff directly (alternative to git diff)
gh pr diff

# Get PR files changed with stats
gh pr diff --stat
```

#### Putting It Together

```bash
# Full context dump for review
echo "=== PR Details ==="
gh pr view --json number,title,state,baseRefName,headRefName,labels

echo -e "\n=== PR Description ==="
gh pr view --json body --jq '.body'

echo -e "\n=== Linked Issues ==="
for issue in $(gh pr view --json body --jq '.body' | grep -oE '#[0-9]+' | tr -d '#' | sort -u); do
    echo "--- Issue #$issue ---"
    gh issue view "$issue" --json title,body --jq '"\(.title)\n\(.body)"' 2>/dev/null || echo "Could not fetch issue"
done

echo -e "\n=== CI Status ==="
gh pr checks

echo -e "\n=== Commits ==="
git log --oneline $(git merge-base HEAD main)..HEAD

echo -e "\n=== Files Changed ==="
gh pr diff --stat
```

## Review Dimensions

### 1. Correctness

The code should do what it claims to do.

- Does the implementation match the PR description?
- Are edge cases handled?
- Are error conditions recoverable or at least reported clearly?
- Do loops terminate? Are bounds checked?
- Is concurrent code free of races? Are invariants protected?

### 2. Style Compliance

The code should follow project conventions.

- Naming conventions (casing, prefixes, verb forms)
- Formatting (should be automated, but check if not)
- Import ordering and grouping
- Comment style and placement
- Error message formatting

**Check against:** `AGENTS.md`, `.rules/*`, language-specific linters

### 3. Architectural Fit

The code should respect established boundaries.

- Does it introduce new dependencies? Are they justified?
- Does it bypass abstraction layers?
- Does it duplicate functionality that exists elsewhere?
- Does it create circular dependencies?
- Does it respect module boundaries?

**Check against:** `docs/*-design.md`, existing module structure

### 4. Implementation Quality

The code should be maintainable.

**Code Smells to Flag:**

| Smell | Symptom |
|-------|---------|
| Repeated code | Copy-paste with minor variations |
| Complex conditionals | Nested if/else, boolean expressions with >3 terms |
| Bumpy road | Function alternates between high and low abstraction |
| High similarity | Two functions that differ only in one parameter |
| Magic literals | Unexplained numbers or strings |
| Long parameter lists | Functions taking >4 arguments |
| Feature envy | Method uses another object's data more than its own |
| Primitive obsession | Using strings/ints where a type would clarify intent |

**Positive Patterns to Encourage:**

- Early returns to reduce nesting
- Guard clauses at function entry
- Descriptive intermediate variables
- Type aliases for complex generics
- Exhaustive pattern matching

### 5. Documentation

The code should explain itself where it cannot show itself.

- Public APIs must have doc comments
- Complex algorithms need explanatory comments
- "Why" comments for non-obvious decisions
- No stale comments contradicting the code
- README updates for user-facing changes

**Check against:** `docs/documentation-style-guide.md`

### 6. Testing

The code should prove it works.

- Are new code paths covered by tests?
- Do tests verify behaviour, not implementation?
- Are edge cases tested?
- Are error paths tested?
- Do test names describe the scenario?

### 7. Security

The code should not introduce vulnerabilities.

- Input validation at trust boundaries
- No SQL/command/log/XSS injection vectors
- No hardcoded secrets
- Appropriate use of cryptographic primitives
- Safe deserialisation
- No TOCTOU race conditions

**See:** `guides/security-issues.md` for detailed patterns and examples.

### 8. Performance

The code should not introduce regressions.

- No O(n²) where O(n) suffices
- No repeated computation in loops
- No blocking calls on hot paths
- Appropriate data structure choices
- Memory allocation patterns (especially in Rust)
- Resources released promptly (connections, handles, memory)
- No bad neighbour patterns (unbounded memory, CPU monopolisation)

**See:** `guides/performance-concerns.md` for detailed patterns and examples.

## Review Output Format

Structure findings by severity:

```markdown
## Summary

<One paragraph overall assessment. Lead with the most important point.>

## Critical Issues

Issues that block merge. Security flaws, correctness bugs, data loss risks.

### [CRITICAL] <Short title>

**File:** `path/to/file.rs` (lines 42-56)

<Explanation of the problem>

```rust
// Problematic code
```

**Suggested fix:**

```rust
// Better approach
```

---

## Suggestions

Improvements that strengthen the code but are not blocking.

### [SUGGESTION] <Short title>

**File:** `path/to/file.rs` (line 78)

<Explanation and alternative>

---

## Observations

Questions, minor notes, patterns worth discussing.

- Observation one
- Observation two

---

## Checklist

- [ ] Passes CI
- [ ] Adheres to style guide
- [ ] Consistent with design documents
- [ ] Adequate documentation
- [ ] Test coverage appropriate
- [ ] No security concerns
- [ ] No performance regressions
```

## Best Practices

### Calibrate Severity

Not everything is critical. Reserve that label for:

- Security vulnerabilities
- Data corruption or loss
- Crashes or hangs
- Silent incorrect behaviour

Style violations and minor inefficiencies are suggestions, not blockers.

### Be Specific

Bad: "This function is too complex."

Good: "This function has a cyclomatic complexity of 15. The nested conditionals on lines 34-52 could be extracted into a `validate_input()` helper."

### Suggest, Don't Demand

Bad: "Change this to use `filter_map`."

Good: "Consider using `filter_map` here—it combines the filter and map into a single pass and makes the None-handling explicit."

### Acknowledge Good Work

If something is particularly well done, say so. Positive reinforcement shapes future contributions.

### Ask Questions

If you don't understand why something was done a certain way, ask. The author may have context you lack. Or they may realise their approach needs better documentation.

### Consider the Author

A junior contributor needs different feedback than a senior maintainer. Adjust your tone and the level of explanation accordingly.

### Timebox

Diminishing returns set in. If you've spent an hour on a 200-line PR, you're likely past the point of useful findings. Note your time limit and move on.

## Common Pitfalls

### Reviewing Without Context

Reading the diff without understanding the feature leads to superficial or incorrect feedback.

### Bikeshedding

Spending disproportionate time on trivial style matters while missing structural problems.

### Rubber Stamping

Approving without genuine review erodes the value of the process.

### Being Adversarial

Review is collaborative, not competitive. The goal is better code, not scoring points.

### Scope Creep

Requesting changes unrelated to the PR's purpose. File separate issues for pre-existing problems.

### Blocking on Preferences

Your preferred approach isn't necessarily better. If the code works, follows conventions, and is maintainable, accept it even if you'd have written it differently.

## Supplementary Guides

For detailed patterns and examples, see:

- `guides/security-issues.md` — Injection attacks (SQL, shell, log, XSS, prompt), TOCTOU race conditions, secret exposure, authentication/authorisation flaws, cryptographic issues, deserialisation, path traversal
- `guides/performance-concerns.md` — Algorithmic complexity (accidental quadratic), resource leaks, bad neighbour problems, database performance, network efficiency, memory management, concurrency issues
- `checklists/language-specific.md` — Rust, Python, TypeScript checklists
- `examples/code-smells.md` — Before/after examples of common smells

## Language-Specific Considerations

### Rust

- Ownership and borrowing: unnecessary clones, lifetime elision opportunities
- Error handling: appropriate use of `?`, `Result` vs `panic!`
- Unsafe code: is it necessary? Is the safety invariant documented?
- Clippy lints: are they addressed or explicitly allowed with justification?

### Python

- Type hints: present and accurate?
- Exception handling: bare `except:` is almost always wrong
- Resource management: `with` statements for files, connections
- Import hygiene: no wildcard imports, logical grouping

### TypeScript

- Type safety: avoiding `any`, proper null handling
- Async patterns: proper error handling in promises
- Module boundaries: avoiding circular imports
- Runtime checks: zod or similar for external data

## Prompt Template

See `templates/review-prompt.md` for a ready-to-use prompt incorporating these practices.

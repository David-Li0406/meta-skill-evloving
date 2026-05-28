# Code Review Prompt

You are conducting a thorough code review of the current branch against its base branch.

## Phase 1: Context Gathering

Before examining any code, gather the context needed to judge it. Read each file that exists:

### Branch State

```bash
# Identify the base branch (adjust if not 'main')
BASE_BRANCH="main"

# Commits under review
git log --oneline $(git merge-base HEAD $BASE_BRANCH)..HEAD

# Change summary
git diff $(git merge-base HEAD $BASE_BRANCH)..HEAD --stat
```

### PR Context (if PR exists)

```bash
# Check for PR and get metadata
gh pr view --json number,title,state,baseRefName,headRefName,labels

# Get the PR description
gh pr view --json body --jq '.body'

# Get PR with review comments for ongoing discussion context
gh pr view --json body,comments --jq '{body, comments: [.comments[].body]}'

# Extract and fetch linked issues from PR body
for issue in $(gh pr view --json body --jq '.body' | grep -oE '#[0-9]+' | tr -d '#' | sort -u); do
    gh issue view "$issue" --json title,body --jq '"#'"$issue"': \(.title)\n\(.body)"' 2>/dev/null
done

# Check CI status
gh pr checks
```

If no PR is open, read commit messages to understand intent.

### Project Standards

| File/Directory | Contains |
|----------------|----------|
| `AGENTS.md` | Coding style guide |
| `.rules/` | Additional rules (read all files) |
| `docs/documentation-style-guide.md` | Documentation conventions |

### Design Context

| File | Contains |
|------|----------|
| `docs/*-design.md` | Architectural decisions and rationale |
| `docs/roadmap.md` | Current priorities and planned work |

### Project Type

Detect from manifest files:

- `Cargo.toml` → Rust (check for `clippy.toml`, `.cargo/config.toml`)
- `pyproject.toml` → Python (check for `ruff.toml`, `mypy.ini`, `.python-version`)
- `package.json` → TypeScript (check for `tsconfig.json`, `.eslintrc.*`)

### CI Expectations

Read `.github/workflows/*.yml` to understand:

- Required checks
- Test commands
- Lint commands
- Build targets

### Established Patterns

Examine 2-3 files adjacent to the changed code:

- How are errors handled?
- What logging patterns are used?
- How is configuration accessed?
- What naming conventions are followed?
- Are there shared utilities that should be used?

## Phase 2: Review

With context gathered, review each changed file against these criteria:

### Correctness

- Does the implementation achieve what the PR claims?
- Are edge cases handled?
- Are error conditions recoverable or clearly reported?
- Is concurrent code free of data races?

### Style Compliance

- Does it follow `AGENTS.md`?
- Does it follow `.rules/*`?
- Is it consistent with neighbouring code?

### Architectural Fit

- Does it respect module boundaries from design docs?
- Does it introduce justified dependencies?
- Does it duplicate existing functionality?
- Does it bypass established abstractions?

### Implementation Quality

Flag these smells:

- **Repeated code** — copy-paste with minor variations
- **Complex conditionals** — deep nesting, long boolean expressions
- **Bumpy road** — mixed abstraction levels in one function
- **High similarity** — functions differing by one parameter
- **Magic literals** — unexplained numbers or strings
- **Long parameter lists** — more than 4 arguments
- **Feature envy** — using another object's data excessively

### Documentation

- Do public APIs have doc comments?
- Are complex algorithms explained?
- Are non-obvious decisions justified?
- Are there stale comments?

### Testing

- Are new code paths covered?
- Do tests verify behaviour, not implementation?
- Are edge cases and error paths tested?

### Security

- Is input validated at trust boundaries?
- Are there injection vectors (SQL, shell, log, XSS, prompt)?
- Are secrets handled appropriately?
- Is deserialisation safe?
- Are there TOCTOU race conditions?
- Is authentication and authorisation enforced?

**Reference:** `guides/security-issues.md`

### Performance

- Are there O(n²) algorithms where O(n) suffices?
- Is there repeated computation in loops?
- Are data structures appropriate?
- Are there blocking calls on hot paths?
- Are resources released promptly (connections, handles)?
- Are there bad neighbour patterns (unbounded memory/CPU)?

**Reference:** `guides/performance-concerns.md`

## Phase 3: Output

Structure your review as follows:

---

## Summary

<One paragraph: overall assessment, most significant finding first. State whether you recommend approval, changes requested, or needs discussion.>

## Critical Issues

<Security flaws, correctness bugs, data loss risks. These block merge.>

### [CRITICAL] <Title>

**File:** `path/to/file` (lines X-Y)

<Explanation of the problem and its consequences>

```
<Problematic code snippet>
```

**Recommendation:**

```
<Suggested fix or approach>
```

---

## Suggestions

<Improvements that strengthen the code but do not block merge.>

### [SUGGESTION] <Title>

**File:** `path/to/file` (line X)

<Explanation and alternative approach>

---

## Observations

<Questions, discussion points, patterns worth noting. Use a simple list.>

- <Observation>
- <Observation>

---

## Checklist

- [ ] Passes CI checks
- [ ] Adheres to `AGENTS.md` style guide
- [ ] Adheres to `.rules/*` conventions
- [ ] Consistent with design documents
- [ ] Documentation adequate
- [ ] Test coverage appropriate
- [ ] No security concerns identified
- [ ] No performance regressions expected

---

## Guidance

When writing your review:

1. **Be specific** — cite line numbers, quote code, name the violation
2. **Calibrate severity** — reserve "critical" for bugs, security, data loss
3. **Suggest, don't demand** — "Consider X" not "Change this to X"
4. **Stay in scope** — file separate issues for pre-existing problems
5. **Acknowledge good work** — if something is well done, say so
6. **Ask questions** — if intent is unclear, ask rather than assume

# Exploration Phase

Before implementing anything, complete these steps.

## Step 0: Set Task Status (if project uses task tracking)

- If project has a roadmap file (e.g., `FUTURE_ROADMAP.md`), set task status to **In Progress**
- If task has non-trivial design, check design docs (e.g., `docs/DESIGN_REMAINING_ISSUES.md`)

## Step 1: Read the Code First

> **Documents may be outdated. Code is the source of truth.**

1. **Read relevant source files** — Understand existing patterns, conventions, abstractions
2. **Check if feature/fix already exists** — Search codebase for similar implementations
3. **Identify exact insertion point** — Know which file(s) and line(s) to modify

### Exploration Order

| Step | What to Find | Examples |
|------|--------------|----------|
| 1. Entry points | Where app starts | `main.py`, `src/index.ts`, `main.go`, `src/main.rs` |
| 2. Routes / API | Request handlers | `routes/`, `api/`, `pages/`, CLI handlers |
| 3. Config | Project settings | `config.py`, `pyproject.toml`, `package.json`, `.env.example` |
| 4. Related modules | Code to modify | Follow imports from entry point |
| 5. Existing tests | Test patterns | `tests/`, `__tests__/`, `*_test.go`, `*.spec.ts` |

## Step 2: Verify Docs ↔ Code Sync

| Check | If Mismatch Found |
|-------|-------------------|
| `README.md` vs actual CLI flags | Sync README to match code |
| `CHANGELOG.md` vs recent commits | Backfill missing entries |
| Roadmap/task tracker vs code state | Update status (Pending → Done) |

**Rule:** If drift found → Sync docs to match code immediately, then proceed.

## Step 3: Confirm Scope

- Cross-reference task definition with code reading findings
- Follow defined scope; avoid speculative edits

## Step 4: Branch Strategy

- Main stays green; create feature branches: `feature/<name>` or `fix/<name>`
- Rebase regularly onto main to avoid conflicts

---

**→ Next:** Load `references/design.md` to define behavior via tests BEFORE coding.

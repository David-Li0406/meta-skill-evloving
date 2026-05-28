---
name: github-push
description: Project-specific workflow for building and pushing to GitHub. Use when the user asks to "build and push", "push to GitHub", or similar. Ensures build runs first, correct files are staged, and push completes to origin.
category: general
color: blue
displayName: GitHub Push
---

# GitHub Push Skill

This skill defines the **build-and-push-to-GitHub** workflow for this project. Use it whenever the user requests a build and push, or to push changes to GitHub.

## Golden Rules

1. **Always build before pushing.** Run `npm run build` and confirm it succeeds. Do not push if the build fails.
2. **Use project root.** Run all commands from the project root (`v0-4-11-2025-authors-info-2` or equivalent).
3. **Shell: PowerShell (Windows).** Use `;` to chain commands, not `&&`. Prefer separate commands when unsure.
4. **Never run database reset** or other destructive DB commands.
5. **Never commit** `.env`, `.env.local`, or other secrets.

## Standard Workflow

### 1. Build

```powershell
npm run build
```

- Fix any build errors before proceeding.
- If type/lint issues appear, address them or run `npm run lint` / `npm run types:check` as needed.

### 2. Check Status

```powershell
git status
```

- Review modified, added, and untracked files.
- Do **not** stage temporary scripts, `node_modules`, `*.log`, or env files.

### 3. Stage Changes

Stage only what belongs in the commit:

- **Typical includes:** `app/`, `components/`, `lib/`, `types/`, `utils/`, `hooks/`, `supabase/migrations/*.sql`, `.agent/skills/`, config/docs relevant to the change.
- **Exclude:** `node_modules/`, `.env*`, `*.log`, debug scripts (e.g. `scripts/debug-*.ts`, `scripts/check-*.ts` unless they are permanent tooling), `script-results.json`, `test-output.txt`, and other local/temporary artifacts.

Use explicit paths:

```powershell
git add <path1> <path2> ...
```

Or add by directory, e.g.:

```powershell
git add app/api/activities/route.ts components/entity-feed-card.tsx supabase/migrations/20260121000700_fix_validate_post_data_visibility.sql
```

### 4. Commit

```powershell
git commit -m "Short summary of changes

- Bullet point 1
- Bullet point 2 (if relevant)"
```

- Use clear, present-tense summaries (e.g. "Fix post visibility update" not "Fixed post visibility update").
- For larger changes, add 1–3 bullet points.

### 5. Push

```powershell
git push origin main
```

- Use `main` unless the user works on another branch; then use that branch name.
- If the push fails (e.g. remote has new commits), run `git pull --rebase origin main` (or the current branch), resolve any conflicts, then push again.

## Quick Reference (Copy-Paste)

```powershell
npm run build
git status
git add <paths>
git commit -m "Your message"
git push origin main
```

## When to Defer

- **Merge conflicts, history rewrite, complex Git issues** → Use **git-expert**.
- **CI/CD, GitHub Actions, workflow automation** → Use **github-actions-expert**.

## Project Details

- **Build:** `npm run build` (Next.js).
- **Migrations:** `npm run db:migrate supabase/migrations/<file>.sql` (see `docs/scripts/HOW_TO_RUN_MIGRATIONS.md`). Do not run migrations as part of push unless the user explicitly asks.
- **Remote:** `origin`; default branch `main`.

## Checklist Before Pushing

- [ ] `npm run build` succeeds.
- [ ] Only intentional files are staged (no secrets, logs, or temp scripts).
- [ ] Commit message clearly describes the change.
- [ ] `git push origin main` (or target branch) completes successfully.

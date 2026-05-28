---
name: final-release-review
description: Use this skill when validating the latest release candidate commit for release, ensuring that all changes are thoroughly reviewed for risks and improvements.
---

# Final Release Review

## Purpose

This skill guides you through performing a release-readiness review by locating the previous release tag from remote tags and auditing the diff (e.g., `v1.2.3...<commit>`) for breaking changes, regressions, improvement opportunities, and risks before releasing your project.

## Quick start

1. Ensure you are in the repository root:
   ```bash
   pwd  # should be path-to-workspace/<your-project>
   ```
2. Sync tags and pick the base tag (default `v*`):
   ```bash
   BASE_TAG="$(.codex/skills/final-release-review/scripts/find_latest_release_tag.sh origin 'v*')"
   ```
3. Choose the target commit (default tip of `origin/main`, ensure it's fresh):
   ```bash
   git fetch origin main --prune
   TARGET="$(git rev-parse origin/main)"
   ```
4. Snapshot the scope of changes:
   ```bash
   git diff --stat "${BASE_TAG}"..."${TARGET}"
   git diff --dirstat=files,0 "${BASE_TAG}"..."${TARGET}"
   git log --oneline --reverse "${BASE_TAG}".."${TARGET}"
   git diff --name-status "${BASE_TAG}"..."${TARGET}"
   ```
5. Conduct a deep review using a checklist to identify breaking changes, regressions, and improvement opportunities.
6. Document your findings and determine the release gate: decide to ship or block the release based on conditions; propose focused tests for any risky areas.

## Workflow

- **Prepare**
  - Run the quick-start tag command to ensure you are using the latest remote tag. If the tag pattern differs, override the pattern argument (e.g., `'*.*.*'`).
  - If a base tag is specified by the user, prefer it but still fetch remote tags first.
  - Keep the working tree clean to avoid diff noise.

- **Assumptions**
  - Assume the target commit (default `origin/main` tip) has already passed code change verification in CI unless stated otherwise.
  - Do not block a release solely due to untested local changes; focus on concrete behavioral or API risks.
  - Follow the release policy: routine releases use patch versions; use minor for breaking changes or major feature additions. Major versions are reserved until the 1.0 release.

- **Map the diff**
  - Use `--stat`, `--dirstat`, and `--name-status` outputs to identify critical directories and file types.
  - For suspicious files, prefer using `git diff --word-diff BASE...TARGET -- <path>` to inspect changes closely.
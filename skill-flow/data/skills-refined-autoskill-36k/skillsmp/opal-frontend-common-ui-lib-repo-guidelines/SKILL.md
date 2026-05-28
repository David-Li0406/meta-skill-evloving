---
name: opal-frontend-common-ui-lib-repo-guidelines
description: Repository structure, build/test commands, coding style, and contribution rules for opal-frontend-common-ui-lib. Use when navigating the repo, running or debugging builds/lint/tests, or following style conventions.
---

# Opal Frontend Common UI Lib Repo Guidelines

## Overview
Use these rules to keep work aligned with opal-frontend-common-ui-lib structure, tooling, and contribution expectations.

## Project Structure & Module Organization
- This repository hosts the Angular library `opal-frontend-common`. Source code lives under `projects/opal-frontend-common`, organized into feature folders such as `components`, `services`, `pipes`, and `stores`.
- Shared styles are stored in `projects/opal-frontend-common/styles`.
- `projects/opal-frontend-common/public-api.ts` governs which symbols are exported.
- Build artifacts land in `dist/opal-frontend-common`; clean it before publishing changes.

## Build, Test, and Development Commands
- Use Yarn for all tasks.
- `yarn start` serves the example harness via the Angular dev server for local smoke tests.
- `yarn watch` rebuilds the library in development watch mode.
- `yarn build` runs `yarn clean`, builds the production bundle, and copies `README.md` into `dist/`.
- `yarn test` executes the Karma/Jasmine suite once; prefer `yarn test:coverage` for a coverage report in `coverage/`.
- `yarn lint` runs Prettier checks followed by Angular ESLint; apply `yarn prettier:fix` to reformat automatically.

## Coding Style & Naming Conventions
- Respect `.editorconfig` (UTF-8, spaces, 2-space indent).
- Prettier enforces 120-character lines, single quotes, and semicolons.
- Angular ESLint rules require component selectors to use the `opal-lib-` prefix (kebab-case) and directives to use `opalLib` (camelCase).
- Keep the public surface curated through `public-api.ts`, and follow member ordering enforced by ESLint when adding class fields or methods.

## Testing Guidelines
- Author Jasmine specs beside their subjects using the `*.spec.ts` suffix.
- Karma is configured via `karma.conf.js`.
- Run `yarn test:coverage` before raising PRs and review generated reports to protect shared utilities, guards, and interceptors.
- For complex features, add harness components within `components/*/testing` folders to exercise interactions end-to-end.

## Design System References
- https://design.homeoffice.gov.uk/design-system
- https://design-patterns.service.justice.gov.uk/
- https://design-system.service.gov.uk/
- https://alphagov.github.io/accessible-autocomplete/examples/

## Commit & Pull Request Guidelines
- Use succinct, descriptive commit subjects (e.g., `chore(deps): update angular-cli monorepo to v20.3.5`, `PO-2278`).
- Mirror that structure and include ticket IDs where applicable.
- Keep commits focused and avoid bundling unrelated refactors.
- PRs should summarize intent, document testing performed, flag breaking API changes, and attach screenshots or GIFs for UI tweaks.
- Link Jira or GitHub issues and notify dependent teams if exports or selectors change.

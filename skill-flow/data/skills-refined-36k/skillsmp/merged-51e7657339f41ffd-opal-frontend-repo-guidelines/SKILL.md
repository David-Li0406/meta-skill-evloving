---
name: opal-frontend-repo-guidelines
description: Use this skill when navigating the opal-frontend and opal-frontend-common-ui-lib repositories, running or debugging builds/lint/tests, following style conventions, or setting up local tooling.
---

# Opal Frontend and Common UI Lib Repo Guidelines

## Overview
Use these rules to keep work aligned with the structure, tooling, and contribution expectations of both the opal-frontend and opal-frontend-common-ui-lib repositories.

## Project Structure
- For opal-frontend, keep Angular feature modules, shared services, and unit specs in `src/app`; colocate UI state with feature directories. Use `src/assets` and `src/styles.scss` for static assets and global styling.
- For opal-frontend-common-ui-lib, source code lives under `projects/opal-frontend-common`, organized into feature folders such as `components`, `services`, `pipes`, and `stores`. Shared styles are stored in `projects/opal-frontend-common/styles`.

## Build, Test, and Development Commands
- Use Yarn for all tasks.
- Run `yarn start` for local development; for opal-frontend, it serves at `http://localhost:4200/` with live reload. For opal-frontend-common-ui-lib, it serves the example harness.
- Run `yarn build` to create a production bundle; for opal-frontend, it outputs to `dist/`, and for opal-frontend-common-ui-lib, it cleans and builds the library.
- Run `yarn test` for Karma/Jasmine tests; use `yarn test:coverage` for coverage reports.

## Coding Style and Naming Conventions
- Follow `.editorconfig`: UTF-8, spaces, 2-space indent.
- Use Prettier for formatting: 120 character width, single quotes, and semicolons. Run `yarn prettier:fix` to reformat automatically.
- For opal-frontend, use Angular selectors with the `app` prefix; for opal-frontend-common-ui-lib, use the `opal-lib-` prefix (kebab-case) for components and `opalLib` (camelCase) for directives.

## Testing Guidelines
- Name Jasmine specs as `*.spec.ts` alongside sources.
- Prefer shallow `TestBed` setups and mock dependencies. Ensure major features have above 80% branch coverage before merging.
- For opal-frontend-common-ui-lib, add harness components within `components/*/testing` folders for complex features.

## Commit and Pull Request Guidelines
- Follow Conventional Commits, optionally prefixed with Jira keys; keep subjects at or below 72 characters.
- Include a concise summary, testing evidence, and updated checklists in PRs; attach relevant artifacts when debugging.
- Link Jira or GitHub issues and notify dependent teams if exports or selectors change.

## Design System References
- [Home Office Design System](https://design.homeoffice.gov.uk/design-system)
- [Justice Design Patterns](https://design-patterns.service.justice.gov.uk/)
- [GOV.UK Design System](https://design-system.service.gov.uk/)
- [Accessible Autocomplete Examples](https://alphagov.github.io/accessible-autocomplete/examples/)
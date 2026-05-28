---
name: opal-frontend-repo-guidelines
description: Use this skill when navigating the opal-frontend repository, running or debugging builds/lint/tests, following style conventions, or setting up local tooling.
---

# Opal Frontend Repo Guidelines

## Overview
Use these rules to keep work aligned with the opal-frontend structure, tooling, and contribution expectations.

## Project Structure
- Keep Angular feature modules, shared services, and unit specs in `src/app`; colocate UI state with feature directories.
- Use `src/assets` and `src/styles.scss` for static assets and global styling; add new bundled assets to `angular.json`.
- Keep deployment and infra logic under `infrastructure/` and `charts/`; keep SSR helpers in `server.ts` and `server-setup.ts`.
- For the common UI library, source code lives under `projects/opal-frontend-common`, organized into feature folders such as `components`, `services`, `pipes`, and `stores`. Shared styles are stored in `projects/opal-frontend-common/styles`.

## Build, Test, and Development Commands
- Run `yarn start` for `ng serve` at `http://localhost:4200/` with live reload or to serve the example harness via the Angular dev server for local smoke tests.
- Run `yarn ng lint` for Angular ESLint across `src/**/*.ts` and `src/**/*.html`, or `yarn lint` for Prettier checks followed by Angular ESLint.
- Run `yarn build` for a production bundle in `dist/` and to build the library, which includes cleaning before publishing changes.
- Run `yarn test` for Karma/Jasmine once; use `yarn test:coverage` for lcov in `coverage/` and to protect shared utilities, guards, and interceptors.

## Coding Style and Naming
- Follow `.editorconfig`: UTF-8, spaces, 2-space indent, trimmed trailing whitespace, single quotes in `.ts`.
- Follow `.prettierrc`: 120 character width, single quotes, and semicolons; run `npx prettier --write` on touched files if formatting drifts.
- Use Angular selectors with the `app` prefix (`app-example`) for components and `opal-lib-` prefix (kebab-case) for library components; keep directive selectors camelCase.
- Keep the public surface curated through `public-api.ts`, and follow member ordering enforced by ESLint when adding class fields or methods.

## Testing Basics
- Name Jasmine specs as `*.spec.ts` alongside sources.
- Prefer shallow `TestBed` setups and mock HTTP/Store dependencies.
- Keep major features above 80% branch coverage before merging.

## Commit and Pull Request Guidelines
- Follow Conventional Commits, optionally prefixed with Jira keys (e.g., `PO-716`); keep subjects at or below 72 characters.
- Reference the Jira ticket and linked PR (e.g., `(#1828)`) in subject or body.
- Include a concise summary, testing evidence, and updated checklists in PRs; attach Cypress artifacts when debugging flakes.

## Local Environment and Tooling
- Use Node `22.20.0` from `.nvmrc` and Yarn `4.10.3`; run `corepack enable` before `yarn install`.
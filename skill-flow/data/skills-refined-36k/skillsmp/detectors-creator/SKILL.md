---
name: detectors-creator
description: This skill should be used when a user requests creation of a new detector in this repo. It defines the mandatory workflow for analyzing provided outerHTML, aligning with existing detectors, creating detector files/tests/docs, and handing off usage.md completion to the user.
---

# Detectors Creator

## Overview

Create new detectors for this parser using a strict, repeatable workflow aligned with existing detector structure, validation style, tests, and documentation.

## When to Use

Use this skill when a user proposes, asks, or demands creation of a new detector for a UI component or section.

## Required Inputs

- Outer HTML of the target element (`outerHTML`) and optional brief description of what to look for as anchors.
- Any secondary HTML states (expanded/collapsed, selected/unselected) if they affect detection or meta.

## Workflow

### 1. Collect Input

- Require outerHTML and capture any user notes about anchors.
- Ask for missing HTML or states needed for strict validation.

### 2. Analyze the HTML

- Review semantics and MUI class patterns to identify the component type.
- Identify key points: root element, stable attributes, required child structure, unique identifiers, portal linkage, and state indicators.
- Avoid dynamic IDs; prefer data-testid, role-based selectors, stable classes, or label text patterns.

### 3. Calibrate Against Existing Detectors

- Review existing detectors for similar inputs/outputs and selector patterns.
- Align validation strictness, selector style, meta naming, and doc style with current detectors.
- Use references in `src/detectors/*/doc` and tests in `tests/detectors/*` as the style baseline.

### 4. Confirm Detector Name

- Propose the detector folder name `{kind}` in kebab-case.
- Ask the user to confirm the name before creating any new folder.

### 5. Implement Detector + Docs + Tests

- Create `src/detectors/{kind}/` with:
  - `detector.ts`, `validate.ts`, `types.ts`, `index.ts`
  - `doc/about.md`, `doc/html.md`, `doc/output.md`, `doc/usage.md`
- Populate docs with input/output and minimal narrative.
- Keep `doc/usage.md` as a template placeholder, not a complete playbook.
- Add tests in `tests/detectors/{kind}.test.ts` using `createContext`.
- Register the detector in `src/detectors/index.ts` and export types.
- Ensure detector docs live under `doc/` so CLI export (`src/cli.ts`) includes them.

### 6. Present Results and Hand Off

- Summarize created files and key selectors/meta fields.
- Ask the user to complete `doc/usage.md` with the correct Playwright actions.

## References

- Use templates from `references/templates.md` for detector files, docs, and tests.

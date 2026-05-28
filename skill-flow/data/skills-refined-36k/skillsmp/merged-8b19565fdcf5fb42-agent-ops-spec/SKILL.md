---
name: agent-ops-spec
description: Manage specification documents in `.agent/specs/` to track and validate requirements, acceptance criteria, or feature descriptions against implementation.
---

# Spec Management workflow

## Purpose

Capture, organize, and trace specifications/requirements so the agent can validate implementation against them.

## Location

All specs live in `.agent/specs/` with user-specified or auto-generated filenames.

## Procedure

### Creating a spec

1) Ask user for filename or generate one (e.g., `feature-<name>.spec.md`, `issue-<id>.spec.md`).
2) Use the spec template.
3) Fill in sections from user input.
4) Link spec to issue(s) in `.agent/issues/` via `spec_file:` field.

### Validating against spec

1) Read the linked spec file.
2) Create a traceability checklist:
   - Each requirement → implementation location → test(s).
3) Include in the critical review phase.

## Template

Start from [spec template](./templates/spec.template.md).
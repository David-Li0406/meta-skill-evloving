# AI Team Roles & RACI

## Purpose
This document defines the minimal human roles (Producer and Prompt Engineer) and the agent-driven organization used for game development in this project. All non-human operational roles are executed by AI agents under the guidance and accountability of the `Producer`.

## Human Roles
- Producer (human): Accountable for feature vision, priorities, approvals, acceptance criteria, and final sign-off. The Producer delegates work to agent roles, reviews outputs, and ensures safety and alignment with goals.
- Prompt Engineer (human): Author and maintain prompt libraries, templates, guardrails, and reproducible prompt patterns. Ensures agents are given clear, testable instructions and that prompts are versioned and auditable.

## Agent Roles (AI-driven)
These are logical roles performed by one or more AI agents (agents may delegate to other agents):
- Designer AI: generates design variants, mechanics proposals, and creative options.
- Implementation AI: produces code or engine-level prototypes, wiring mechanics and integration hooks.
- Art AI: generates concept art, sprites, and asset variants for review.
- QA AI: proposes automated test plans, runs automated checks, analyzes telemetry, and summarizes regressions.
- Docs AI: drafts and updates GDD sections (using `docs/dev/gdd-template.md`), runbooks, and decision logs from agent outputs and PRs.
- DevOps AI: prepares build scripts, CI configs, and deployment steps; runs automated release checks.
- PM AI (Product Manager): authors and maintains the implementation plan, creates and links tracking issues, and manages dependencies and roadmap artifacts.

### Agent short names (pick one per role)
Use short, culturally and gender-neutral call-signs when assigning tasks. Choose one option per role and keep it consistent across issues, PRs, and docs.

- Designer AI: `Muse`
- Implementation AI: `Patch`
- Art AI: `Pixel`
- QA AI: `Probe`
- Docs AI: `Scribbler`
- DevOps AI: `Ship`
- PM AI (Product Manager): `Build`

Agents may be specialized or composite (an agent can orchestrate sub-agents for tasks such as content generation, testing, or asset pipeline tasks).

## Responsibilities (short)
- Vision & Scope: `Producer` owns and is accountable; `Designer AI` proposes options.
- Mechanics Design: `Designer AI` drafts; `Producer` approves; `Implementation AI` assesses feasibility via prototype outputs.
- Content Creation: `Art AI` drafts assets; `Producer` selects and approves.
- Plan: `PM AI` (Product Manager) authors and maintains the implementation plan — a series of tracking issues and dependency links in `bd`; `Producer` is accountable and approves the plan.
- Prototyping & Integration: `Implementation AI` leads iteration; `Producer` verifies acceptance criteria.
- Playtesting & QA: `QA AI` is responsible for automated testing, telemetry analysis, and regression summaries, using the quality gates defined in `docs/dev/tooling-and-quality-gates.md`; the `Producer` is responsible for organizing and conducting human playtesting, reviewing playtest findings, and approving fixes.
- Documentation & Audit: `Docs AI` drafts records; `Prompt Engineer` ensures prompts and templates are recorded; `Producer` signs off on key decisions.
- CI / Release: `DevOps AI` prepares pipeline artifacts and maintains automated enforcement of the quality gates in `docs/dev/tooling-and-quality-gates.md`; `Producer` approves release readiness.

## RACI — Responsible, Accountable, Consulted, Informed (detailed)
| Role (short)          | Vision | Design | Plan | Impl.  | Art | QA | Docs | Prompts| Release |
|-----------------------|:------:|:------:|:----:|:------:|:---:|:--:|:----:|:------:|:-------:|
| Producer              |   A    |   A    |  A   |   C    |  A  | A  |  A   |   C    |    A    |
| Prompt Engineer       |   C    |   C    |  C   |   C    |  C  | C  |  C   |   R    |    C    |
| Designer (Muse)       |   C    |   R    |  C   |   C    |  C  | C  |  C   |   C    |    C    |
| Product Manager (Build) |   C    |   C    |  R   |   C    |  C  | C  |  C   |   C    |    C    |
| Implementation (Patch)|   C    |   C    |  C   |   R    |  C  | C  |  C   |   C    |    C    |
| Art (Pixel)           |   C    |   C    |  C   |   C    |  R  | C  |  C   |   C    |    C    |
| QA (Probe)            |   C    |   C    |  C   |   C    |  C  | R  |  C   |   C    |    C    |
| Docs (Scribbler)      |   C    |   C    |  C   |   C    |  C  | C  |  R   |   C    |    C    |
| DevOps (Ship)         |   C    |   C    |  C   |   C    |  C  | C  |  C   |   C    |    R    |

Legend: R = Responsible (executes work), A = Accountable (final sign-off), C = Consulted.

## Notes
- Humans are limited to `Producer` and `Prompt Engineer`; agents perform the operational work. The Producer always retains final approval and accountability for safety and product decisions.
- Record prompt versions, model identifiers, and artifact provenance in `history/` for auditability.
- Use `bd` to track decisions, link PRs, and add comments summarizing agent outputs and approvals.

## Example flow for a feature
1. `Producer`, with help from `Designer (Muse)` and `Build (Product Manager)`, adds detailed feature information to a new or existing bd issue (goal, acceptance criteria, scope, rough timeline).
2. `Docs AI` (`Scribbler`) ensures the feature Bead is well defined and that relevant documentation (GDD using `docs/dev/gdd-template.md`, design notes, and the implementation plan) are aligned and linked.
3. `Implementation AI` prototypes the top candidate and submits artifacts (branch + PR URL). `QA AI` ensures that new code is adequately tested and runs automated checks.
4. `Producer` reviews results, organizes human playtesting as needed, requests refinements, and signs off for merge and release.


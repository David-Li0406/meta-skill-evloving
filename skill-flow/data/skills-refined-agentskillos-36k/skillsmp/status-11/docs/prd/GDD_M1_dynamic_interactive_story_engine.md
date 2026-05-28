# Product Requirements Document

## Introduction

- One-liner
  - Build an InkJS runtime narrative engine for story-first games, starting with a text-only Ink-powered MVP that runs in browsers (desktop and mobile) and Node.
- Problem statement
  - We need a repeatable way to ship immersive interactive stories with a runtime-ready vertical slice (story runtime + player UX + save/load + runtime telemetry) that supports fast iteration.
- Goals
  - MVP (M1) delivers a complete playable text-only story with branching choices.
  - Provide VN-style player UX for reading + choice selection.
  - Support single-slot autosave + manual save/load (best-effort portability in M1; portable in later milestones).
  - Emit minimal runtime telemetry events for story start, choice selected, and story completion.
  - Meet cold start targets: ≤8s desktop; ≤12s mobile browsers.
- Non-goals
  - M1 does not require AI-generated branching at runtime.
  - M1 does not require backgrounds/characters/animation staging.
  - M1 does not require multi-slot saves or cloud saves.

## Users

- Primary users
  - Players who enjoy narrative-first experiences in 15–45 minute sessions on desktop and mobile browsers.
- Secondary users (optional)
  - Internal creator (Producer) iterating on Ink stories and demos.
- Key user journeys
  - Play story: launch app → story starts → read text → choose from options → reach completion.
  - Save/load: player triggers manual save, and the engine autosaves at defined points; player can load the single slot and continue.

## Requirements

- Functional requirements (MVP)
  - Story runtime
    - Load one Ink story and execute it end-to-end at runtime.
    - Present branching choices and apply the selected choice to advance the story.
    - Define a stable story identifier/version used for telemetry and saves (mechanism TBD).
  - VN-style UX (text-only)
    - Textbox-style presentation with readable typography.
    - Choice list UI supports mouse, touch, keyboard, and controller input.
    - No backlog/rewind required in M1.
  - Save/load (single slot)
    - Autosave: write save state automatically at explicit story checkpoints (Ink tags/markers). Configurable option: autosave after every choice.
    - Manual save: user can explicitly write to the same single slot.
    - Load: user can restore the single slot and continue.
    - Capture story state + UI state (e.g., history/scroll position), as feasible.
    - Portability: best-effort in M1; expected to become portable across platforms in later milestones.
  - Performance
    - Meet cold start targets for first story screen: ≤8s desktop; ≤12s mobile browsers.
  - Debug mode (no locked paths)
    - Provide a debug mode that automatically makes random choices during story execution to detect “locked paths” (paths that prevent the player from finishing).
    - M1 approach can be brute force (e.g., run many randomized playthroughs).
    - Later milestones should track which combinations/branches have been tested and bias exploration toward untested paths for more exhaustive coverage.
  - Observability
    - Emit runtime telemetry events (minimal schema for M1):
      - `story_start`
      - `choice_selected`
      - `story_complete`
- Non-functional requirements
  - Reliability: no fatal runtime errors during end-to-end story play.
  - Cross-platform: M1 must-pass quality gates for desktop, mobile, and browsers.
  - Maintainability: keep the story runtime, UI, save/load, and telemetry separated so later milestones can evolve independently.
- Integrations
  - Use the project's forked InkJS integration (fork reference pending).
- Security & privacy
  - Security note: treat save files and story content as untrusted inputs (especially for future external story loading); validate and fail safely.
  - Privacy note: telemetry should avoid collecting personal data by default; add identifiers only if explicitly required.

## Release & Operations

- Rollout plan
  - M0: UI scaffold runs in browsers.
  - M1: Ink runtime story + VN UI + single-slot save/load + minimal runtime telemetry.
  - Later milestones (from bead):
    - M1.5 content iteration loop
    - M2 AI-generated branches
    - M3 staging with backgrounds/characters
    - M4 reactive simulated world
- Quality gates / definition of done
  - Story plays end-to-end with branching choices on desktop and mobile browsers.
  - Single-slot autosave + manual save/load works (best effort portability).
  - Emits the three runtime telemetry events.
  - Cold start targets achieved or, if not met, a documented mitigation plan exists.
- Risks & mitigations
  - Ink runtime integration risk: runtime APIs may require glue code or adaptation.
    - Mitigation: validate early with a thin prototype, isolate adapter layer.
  - Telemetry gap: current telemetry may be design-time only.
    - Mitigation: define minimal runtime event emitter early; keep schema minimal for M1.
  - Browser constraints: performance/memory budgets may require tradeoffs.
    - Mitigation: profile early, keep assets minimal in M1.
  - Save compatibility: story changes can break saves.
    - Mitigation: version saves + define expected behavior for incompatible saves.

## Open Questions

- What is the canonical PRD/GDD path convention for this repo (we are using `docs/prd/GDD_M1_dynamic_interactive_story_engine.md` per current decision)?
- What Ink runtime integration package should be used, and where should story assets live?
- What constitutes a “safe point” for autosaves (after each choice? after each line? chapter boundaries)?
- Any accessibility requirements beyond supporting mouse/touch/keyboard/controller?
- What is the precise definition of “first story screen” for cold start timing (e.g., first text visible, first choice visible, first frame rendered)?
- How should portability work in later milestones (common serialization format, deterministic story version pinning, cloud saves, etc.)

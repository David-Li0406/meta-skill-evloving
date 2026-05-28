# Product Requirements Document

## Introduction

### One-liner
Add M2: AI-assisted branching support to enable runtime integration of AI-proposed story branches with an automated policy and sanitization guardrail.

### Problem statement
At runtime, players will be able to drive the story into unscripted flows. The priority is the player's experience: the AI Director guides unscripted branching so the story remains coherent and returns the narrative to the scripted path within a defined number of player choice points. An AI Writer will dynamically author story content using recorded LORE, character definitions, and the player's recent actions as inputs. The system must ensure the emergent branches remain playable, on-theme, and do not create dead-ends or permanent divergence from the intended story arc.

### Goals
- Enable players to experience emergent, AI-generated story branches that feel coherent and on-theme without author hand-crafting every branch.
- Ensure the AI Director reliably steers unscripted flows back to the authored narrative within a configurable 'return window' (player choice points).
- Design a safe, policy-driven validation pipeline that prevents unsafe, incoherent, or off-theme content from reaching players.
- Provide producers and designers with tooling to monitor, validate, and refine emergent branching in production.

### Non-goals
- This PRD does not mandate specific LLM providers or runtime hosting choices.
- This PRD does not require human-in-loop approval for every branch proposal (the chosen guardrail model is automated policy and sanitization).
- This PRD does not cover complex branching scenarios (e.g., multi-threading, permanent world state changes, or dynamic character resurrection).

## Terminology

This glossary defines key terms used throughout M2 documentation to ensure consistency:

| Term | Definition |
|------|------------|
| **AI Director** | Runtime governance component that evaluates branch proposals, enforces return window constraints, controls Writer creativity, and makes accept/reject decisions. Latency target: < 500ms. |
| **AI Writer** | Content generation component that produces branch proposals and runtime dialogue using LORE context and LLM calls. Latency target: 1–3s per generation. |
| **Branch Proposal** | A structured document containing metadata, story context, and content for an AI-generated story branch. Conforms to `branch-proposal.json` schema. |
| **Confidence Score** | AI Writer's self-assessed certainty (0.0–1.0) that a proposal is coherent and on-theme. Stored in `metadata.confidence_score`. |
| **Creativity Parameter** | Director-controlled value (0.0–1.0) that adjusts Writer's output variance. 0.0 = conservative/predictable; 1.0 = surprising/imaginative. Maps to LLM temperature. |
| **Hook Point** | A safe moment in the story runtime where a branch can be injected (scene boundary, choice point, quest completion, rest/load, combat victory). |
| **LORE** | Living Observed Runtime Experience — the contextual data (player state, game state, narrative context, player behavior) that feeds Writer generation. See `lore-model.md`. |
| **Return Path** | The scripted scene/knot that a branch returns to after completion. Specified in `content.return_path`. |
| **Return Path Confidence** | AI Writer's certainty (0.0–1.0) that the return path is narratively coherent. Stored in `content.return_path_confidence`. |
| **Return Window** | Maximum number of player choice points before a branch must return to scripted content. Configured value: 3–5 choices. |
| **Risk Score** | Director's weighted assessment (0.0–1.0) of proposal risk across 6 metrics: thematic consistency, LORE adherence, character voice, narrative pacing, player preference fit, and proposal confidence. |
| **Rollback** | Automatic recovery mechanism that reverts game state to last checkpoint when a branch fails during execution. |
| **Sanitization** | Deterministic content transforms applied to proposals (profanity redaction, HTML stripping, whitespace normalization) to ensure safety. |
| **Validation Pipeline** | Automated policy checks that evaluate proposals against rules (content safety, narrative consistency, structure, format, return path). Produces validation reports. |

## Users

### Primary users (end-players)
Players on desktop/mobile browsers who will experience emergent story branches during gameplay.

### Secondary users (post-M2 phases)
- Producers and tooling engineers who generate and validate AI-proposed branches during development (Phase 0–1).
- Writers and designers who may analyze branch performance and refine proposals between phases (post-Phase 3).
- Analytics teams who analyze telemetry to improve policy rules and Director heuristics.

### Key user journeys

#### Player journey: unscripted branching
- Player makes a story choice that triggers an unscripted condition.
- AI Writer generates a branch proposal based on LORE, character state, and player action.
- AI Director validates and evaluates the proposal against constraints and pacing.
- If approved, the branch is seamlessly integrated into the story; the player continues without interruption.
- The Director ensures the branch paces toward a return to the scripted path within the configured window.

#### Producer/designer journey: branch validation and refinement
- Authoring tool or batch process generates candidate branches for a given story context.
- Policy and sanitization pipeline automatically validates proposals (profanity, coherence, theme consistency).
- Producers review validation reports and can approve, reject, or request refinements.
- Approved branches are marked eligible for runtime integration; rejected branches are logged for analysis.

#### Post-launch analysis journey (between phases)
- Telemetry events are collected for branch proposals, Director decisions, and player outcomes.
- Logs and audit trails track all decisions to enable retrospective analysis and improvement of policy rules and Director heuristics for future phases.
- M2 is fully automated: no runtime monitoring or intervention. Learning happens between phases based on collected data.

## Requirements

### Functional requirements (MVP)

#### Player experience: unscripted branching at runtime
- At runtime, when a player choice triggers an unscripted condition, the system generates and integrates an AI-authored branch.
- The branch seamlessly continues the story without breaking immersion or narrative coherence.
- Players cannot distinguish between hand-authored and AI-generated branches (quality target).
- The system guarantees a return to the scripted narrative within the configured 'return window' (e.g., N player choice points).

#### AI Director (runtime governance)
- Evaluates incoming branch proposals from the AI Writer in real-time (latency target: < 500ms per decision).
- Applies risk metrics and coherence checks: thematic consistency, LORE adherence, character voice preservation, narrative pacing, and player preference fit.
- Predicts player enjoyment: assesses whether the branch aligns with demonstrated player preferences (branch types, themes, complexity, historical engagement).
- Enforces the 'return window' constraint: ensures the proposed branch includes a bridging pathway back to scripted content.
- Provides a fail-safe mechanism: if the Director cannot find a coherent return path, it auto-reverts to scripted content and logs the event.
- Emits decision telemetry: proposal timestamp, approval/rejection reason, detected risk score.

#### AI Writer (runtime content generation)
- Generates branch proposals using recorded LORE, character definitions, and recent player actions as context.
- Proposal schema includes: metadata (confidence score, provenance), story context (current scene, player inventory, character state), branch content (Ink fragment or delta).
- Accepts a **creativity parameter** (0.0–1.0) from the Director based on player state: lower values produce conservative, predictable branches; higher values produce more surprising, imaginative content.
- Outputs proposals that conform to the branch proposal schema and include provenance metadata (LLM model version, timestamp).

#### Branch proposal validation pipeline
- Automated policy checks: profanity, disallowed categories, length limits, prohibited narrative patterns.
- Sanitization transforms: strip unsafe HTML, normalize whitespace, enforce character encoding.
- Produces validation reports with pass/fail status and rule-level diagnostics (which rules triggered, which content was sanitized).
- Follows multi-stage proposal lifecycle: Outline (high-level concept review) → Detail (full Save-the-Cat definition + validation) → Placement (identify insertion points) → Runtime (dynamic content generation with sanitization) → Terminal (archived/reverted/deprecated).
- Allows queryable access to proposals and validation reports via API or database.

#### Runtime integration hooks
- Design hook points where validated branch content can be applied into the running story state with clear transaction boundaries.
- Define automatic rollback semantics: if a branch causes a runtime error, the system automatically reverts to the last checkpoint without corrupting save state.
- Persistence model: integrated branches are logged to ensure reproducibility and audit trails.

#### Telemetry and learning
- Emit telemetry events for each stage: proposal submission, validation result, Director decision, branch integration, player outcome.
- Minimal schema: event type, timestamp, branch ID, decision outcome, confidence/risk score.
- Player-facing telemetry: detect whether a player found a branch confusing or satisfying (via post-story survey or behavioral signals).
- Post-launch analysis: historical views of branch success rates, Director decision latency, and policy violation patterns for iterative improvement between phases.

### Non-functional requirements

#### Determinism and reproducibility
- Validation pipeline must be deterministic: same input + same ruleset version → same validation result.
- AI Writer proposals should be varied and creative: the same context may produce different proposals, controlled by the Director's creativity parameter (0.0–1.0).

#### Performance and responsiveness
- Branch proposal validation: complete within 2s (authoring time, not latency-critical).
- AI Director decision: complete within 500ms (player-facing, latency-critical; must feel real-time).
- Proposal generation (AI Writer): target 1–3s per branch (background process; can be async).

#### Configurability
- Policy rulesets, sanitizers, and the Director's 'return window' should be configurable without code changes (e.g., via config file or runtime flags).
- Director risk thresholds and coherence weights should be tunable.

#### Auditability and logging
- All proposals, validation reports, and Director decisions must be retained with versioning for audits.
- Audit logs include timestamps, actor (system component), action, and outcome.
- Support historical analysis: "why did a branch get rejected?" or "when did the Director last fail to find a return path?"

### Integrations
- The PRD is provider-agnostic: allow pluggable LLMs (OpenAI, Claude, local models) or authoring tools to submit proposals via a standard schema.
- Validation ruleset should be compatible with existing telemetry and logging systems (e.g., event streaming, analytics warehouses).
- Support integration with the existing Ink runtime and save/load systems (branch state must not corrupt existing save files).

### Security & privacy
- Security note: treat proposal content as untrusted input; run sanitizers and Writer/Director processing in isolated execution environments and validate encoding before applying to runtime.
- Privacy note: redact or avoid storing PII in proposals; if storing is required, ensure encryption-at-rest and limited access.
- Safety note: failed branches and policy violations must be logged (not silently dropped) to detect potential attacks or author errors.

### Proposal Lifecycle
- **Reference**: See [proposal-lifecycle.md](../dev/m2-design/proposal-lifecycle.md) for complete multi-stage proposal lifecycle
- High-level stages: Outline (concept review) → Detail (full development + validation) → Placement (identify insertion points) → Runtime (dynamic generation + sanitization) → Terminal (archived/reverted/deprecated)
- Key insight: Save-the-Cat structure and beats are written during Detail stage; actual interactive dialogue/content is generated dynamically at runtime based on player choices and director's creativity parameter

### Runtime Content Generation Architecture

**Critical architectural insight**: M2 uses a **two-phase content generation model**:

1. **Pre-validation phase (Detail stage)**: The AI Writer generates a **branch structure** — a Save-the-Cat outline with 4 beats (hook, rising action, climax, resolution), character voice guidelines, thematic constraints, and return path specification. This structure is validated by the policy pipeline and approved by the Director. The structure is stored and ready for runtime.

2. **Runtime phase (Execution)**: When a player triggers the branch, the AI Writer **dynamically generates the actual dialogue and narrative content** following the pre-approved structure. Each beat's content is generated on-demand, sanitized in real-time, and presented to the player. This enables:
   - Adaptive responses to player choices within the branch
   - Fresh, varied dialogue on each playthrough
   - Director-controlled creativity adjustment based on player engagement

**Latency implications**:
- The 500ms Director decision latency applies to **approving the branch structure** (pre-validated)
- Runtime content generation (1–3s per beat) happens **during branch execution**, not at the approval decision point
- Players experience natural dialogue pacing; generation latency is masked by reading time

**Fail-safe behavior**:
- If runtime generation fails, the system displays a pre-authored fallback line and logs the error
- If the branch cannot complete, automatic rollback restores the player to the last checkpoint
- Player notification: "The story encountered an issue. Returning to last save point."

## Release & Operations

### Rollout plan
#### Phase 0 — Design (this PRD)
- Final PRD approval and schema definitions.
- Spike validation pipeline prototypes in dev.
- Prototype AI Director and AI Writer interfaces.
- Define 'return window' semantics and test cases.

#### Phase 1 — Validation-only
- Implement branch proposal validation pipeline.
- Run validation on candidate branches; collect statistics (acceptance rate, top policy violations).
- No automatic runtime integration; branches are validated but not yet served to players.
- Gather feedback from producers on policy ruleset tuning.

#### Phase 2 — Limited integration (feature-flagged)
- Enable runtime hooks for branch integration in a controlled story or demo.
- Implement AI Director with initial coherence heuristics and 'return window' enforcement.
- Implement AI Writer with basic LORE-based generation.
- Pilot with internal playtesters and gather telemetry on Director success rate, player coherence perception.

#### Phase 3 — Soft launch and monitoring
- Roll out to live players with feature flags and kill-switches.
- Gather player feedback, Director decision latency, and policy violation patterns.
- Refine rulesets, Director heuristics, and Writer LORE context based on telemetry.
- Plan for human-in-loop review if safety concerns emerge.

#### Phase 4 — Scale and iterate (post-M2)
- Expand to additional stories and narrative scenarios.
- Add player-facing UX signals (e.g., "this choice was AI-generated"; trust/transparency features).
- Continuous tuning of Director heuristics and Writer prompts based on production telemetry.

### Quality gates / definition of done
- Proposal schema defined, documented, and validated with at least 10 example proposals.
- Policy ruleset implemented and tested against a corpus of ≥100 example branches; documented ruleset with rationale for each rule.
- Validation pipeline deterministic and passing an agreed test suite (≥20 test cases covering edge cases).
- AI Director design specifies 'return window' semantics, risk-scoring algorithm, and fail-safe fallback; includes test cases for both success and failure scenarios.
- AI Writer produces ≥5 example proposals that preserve LORE consistency, character voice, and narrative coherence.
- Branch integration hooks designed with rollback semantics tested (e.g., corrupted branch can be safely reverted).
- Telemetry schema defined and emitted correctly in test environment.
- Player experience validation: internal playtesters rate merged (hand-authored + AI-generated) stories; coherence score ≥4/5 (arbitrary scale).

### Risks & mitigations

#### Risk: AI Director fails to return to scripted path within the window
- Impact: player gets stuck in an infinite or dead-end unscripted loop; breaks immersion and breaks the story.
- Mitigation: implement a deterministic fail-safe that forces a return to scripted content after the window expires; log the event with high priority (alert operators).
- Mitigation: test the Director's return-path logic exhaustively during Phase 1–2; profile common failure modes.

#### Risk: AI Writer produces content that drifts off-theme or contradicts LORE
- Impact: player experiences an incoherent or jarring branch; reduces trust in emergent storytelling.
- Mitigation: enforce strong LORE and character constraints in the Writer's prompt; include embeddings or semantic similarity checks in the validation suite.
- Mitigation: add style/content tests that flag branches differing >N% from the original story's tone; collect examples from playtesters.

#### Risk: Policy pipeline is over-restrictive or under-restrictive
- Impact: either rejects too many valid branches (reduces emergent variety) or allows policy violations (safety breach).
- Mitigation: keep ruleset configurable and provide diagnostics for each rule (why was this branch rejected?); gather feedback from producers in Phase 1.
- Mitigation: start with a conservative policy and loosen it iteratively based on playtest feedback.

#### Risk: Performance bottleneck in Director decision latency
- Impact: branch integration is delayed; player sees a stall or "thinking" state; breaks immersion.
- Mitigation: profile Director decision-making during Phase 2; optimize hot paths (risk scoring, return-path search).
- Mitigation: consider pre-computing Director decisions for likely player choices (offline analysis).

#### Risk: Emergent branches undermine authored narrative intent
- Impact: players explore unscripted content that diminishes the story's themes or message.
- Mitigation: include thematic alignment as a Director risk metric; require branches to include explicit narrative intent statements.
- Mitigation (post-M2): future phases may add producer tools to review and disable problematic branches based on post-launch analysis.

## Resources

### M2 Design Documents

#### Core Design Specs
- **[Director Algorithm](../dev/m2-design/director-algorithm.md)** — Complete 5-step real-time governance algorithm with risk-scoring metrics, return-path feasibility validation, and fail-safe mechanisms.
- **[Policy Ruleset](../dev/m2-design/policy-ruleset.md)** — Validation rules across 5 categories (content safety, narrative consistency, structure, format, return path) with severity levels and tuning parameters.
- **[Sanitization Transforms](../dev/m2-design/sanitization-transforms.md)** — Deterministic content transformation algorithms (profanity redaction, HTML stripping, whitespace normalization) with test cases.
- **[Proposal Lifecycle](../dev/m2-design/proposal-lifecycle.md)** — Multi-stage process from Outline through Detail, Placement, Runtime, and Terminal states with key insights on late content generation.

#### AI Writer Design
- **[LORE Data Model](../dev/m2-design/lore-model.md)** — Complete specification of runtime context (player state, game state, narrative context, player behavior) that feeds Writer generation.
- **[Writer Prompts](../dev/m2-design/writer-prompts.md)** — 4 prompt templates (dialogue, exploration, combat, consequences) with constraint enforcement mechanisms and latency targets.
- **[Writer Examples](../dev/m2-design/writer-examples.md)** — 5 detailed proposal examples across branch types showing quality metrics and Writer capabilities.
- **[Determinism Specification](../dev/m2-design/determinism-spec.md)** — Reproducibility framework via input hashing and LLM seed management with fallback strategies.

#### Runtime & Integration
- **[Runtime Integration Hooks](../dev/m2-design/runtime-hooks.md)** — 5 safe hook point categories (scene boundaries, choice points, quests, rest/load, combat) with 12-state integration state machine and automatic rollback semantics.
- **[Telemetry Schema](../dev/m2-design/telemetry-schema.md)** — 6 event types spanning generation, validation, Director decision, presentation, choice, and outcome with 5 observability dashboards and post-launch analysis workflow.

#### Ink Language Integration
- **[Ink Validation Review](../dev/m2-design/ink-validation-review.md)** — Comprehensive validation of M2 design against Ink language capabilities, terminology consistency review, and implementation recommendations.

### M2 Schemas
- **[Branch Proposal Schema](../dev/m2-schemas/branch-proposal.json)** — JSON Schema definition with all required fields for proposal submissions.
- **[Validation Report Schema](../dev/m2-schemas/validation-report.json)** — Validation pipeline output structure with rule-level diagnostics.
- **[Example Proposals](../dev/m2-schemas/examples/)** — 10 detailed proposal examples across different narrative scenarios.

### Schema Documentation
- **[Schema Docs](../dev/m2-design/schema-docs.md)** — Field-by-field explanation of branch proposal schema with integration guidance.

---

## Design Decisions

The following decisions have been finalized for M2 implementation:

### Runtime Constraints

| Decision | Value | Rationale |
|----------|-------|-----------|
| **Return window** | 3–5 player choice points | Balances emergent exploration with narrative coherence; prevents infinite loops while allowing meaningful detours |
| **Director latency target** | < 500ms | Player-facing decision must feel instantaneous; validation happens on pre-approved structures |
| **Writer latency target** | 1–3s per beat | Acceptable for background/async generation; masked by player reading time during execution |

### AI Writer and LORE

| Decision | Value | Rationale |
|----------|-------|-----------|
| **LORE capture method** | Hybrid (auto-extracted + manual annotations) | Auto-extract player actions, inventory, relationships; manual annotations for narrative themes and character arcs |
| **Minimum LORE context** | 5–15 KB compressed | Sufficient for coherent generation; fits in LLM context windows; see lore-model.md for field specifications |
| **Creativity parameter mapping** | 0.0 = temperature 0.0 (deterministic); 1.0 = temperature 1.5 (high variance) | Linear mapping provides intuitive control; clamped to prevent incoherent outputs |
| **Proposal caching** | Yes, by context hash | Avoid redundant generation for identical contexts; cache invalidated when LORE changes |
| **Embedding model** | text-embedding-ada-002 (or equivalent) | Industry standard for semantic similarity; used in validation and Director risk scoring |

### Policy and Safety

| Decision | Value | Rationale |
|----------|-------|-----------|
| **Policy rule categories** | Content safety (profanity, explicit, hate speech), Narrative consistency (LORE, character voice, theme), Structural (length, format, Ink syntax), Return path validation | Comprehensive coverage; see policy-ruleset.md for full specification |
| **Policy scope** | Global defaults + story-specific overrides | Global rules ensure baseline safety; story-specific rules allow genre-appropriate content (e.g., darker themes in horror stories) |

### Storage & Access

| Decision | Value | Rationale |
|----------|-------|-----------|
| **Proposal retention** | 2 years for audit logs; 6 months for raw proposals with content | Compliance requirement; enables post-launch learning; older proposals archived |
| **Data handling** | Encrypt at rest; redact PII before storage; access limited to analytics roles | Privacy by design; GDPR-compatible |

### Player Experience

| Decision | Value | Rationale |
|----------|-------|-----------|
| **Coherence measurement** | Behavioral signals (reload frequency, skip rate, session continuation) + optional post-story survey | Non-intrusive primary measurement; explicit feedback for deep analysis |
| **AI transparency** | Seamless by default (no indication); opt-in transparency mode in settings | Prioritizes immersion; respects player choice for those who want to know |

### Validation UX

| Decision | Value | Rationale |
|----------|-------|-----------|
| **Authoring validation** | Asynchronous for proposals > 1000 tokens; synchronous for smaller proposals | Responsive UX for quick edits; background processing for large content |
| **Sanitization visibility** | Sanitized diffs logged but not auto-exposed; available on request | Reduces noise; diffs available for debugging when needed |

## Remaining Open Questions

The following questions require stakeholder input before Phase 1 implementation:

### Story-Specific Configuration
- What story-specific policy overrides are needed for the initial pilot story?
- Which characters have custom voice profiles that need explicit constraints?

### Operational Readiness
- What alerting channels should receive fail-safe notifications (Slack, PagerDuty, email)?
- Who is the on-call contact for Phase 2 pilot issues?

### Player Research
- Should we conduct A/B testing with AI-branches enabled vs. disabled?
- What is the target sample size for coherence perception surveys?

## Clarification: No Human-in-Loop in M2

**M2 is designed with fully automated validation and approval.** The PRD explicitly states (Non-goals, line 19) that "This PRD does not require human-in-loop approval for every branch proposal." All runtime acceptance decisions are made by the policy/sanitization pipeline and AI Director—no human approval or intervention is required.

**M2 has no operator disable/revert mechanism at runtime.** Operators observe telemetry to understand system behavior and detect issues, but cannot disable or revert branches once approved. All acceptance/rejection decisions are automated; there is no human gate at runtime.

**Human involvement is limited to between-phase improvements**:
- Producers analyzing telemetry and player feedback to refine policy rules and Director heuristics
- Future phases (Phase 3+) may introduce human-in-loop oversight if safety concerns emerge at scale


› now zoom out to the architecture of this system, we built a single source of truth system but we still have these issues. What about it architecturally
  allows for this to happen?


• What’s “architecturally allowing” this to happen is that the TableTask replay SSOT is not a single atomic state machine across the whole system. It’s a
  split-brain, cross-thread design:

  - UI thread owns the cursor (for responsiveness + Skia correctness)
  - JS thread owns the applied model/state (handState + side effects) and the phase machine
  - The bridge between them is eventual, not transactional (runOnJS + rAF coalescing)

  That architecture is intentional (performance contract), but it means you can still see transient inconsistencies like the logs you pasted.

  ## The three “truths” (and why SSOT doesn’t prevent the mismatch)

  ### 1) UI thread SSOT: the replay cursor

  The canonical “where the scrobbler is” is a Reanimated SharedValue written on the UI thread:

  - Scrub gesture writes scrubIndexSv directly (no JS ticks).
  - Snapback is started immediately on release on the UI thread (before JS is notified).

  Ground truth:

  - apps/mobile/src/features/puzzle/surface_skia/usePuzzleSkiaScrubber.ts:151 (onBegin writes epoch + cursor; stops snapback/autoplay immediately)
  - apps/mobile/src/features/puzzle/surface_skia/usePuzzleSkiaScrubber.ts:180 (onFinalize starts snapback on UI thread, then runOnJS onScrubEnd)

  This is why Skia visuals (like community cards visibility) can remain cursor-accurate even when JS is busy.

  ### 2) JS truth: “applied index” + applied handState

  JS owns handLogStepIndexRef.current / React handLogStepIndex and handState, updated when we “apply” an index.
  That apply is invoked from the UI thread via runOnJS, and then coalesced to rAF.

  Ground truth:

  - apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:1323 (worklet picks index from playbackMs or cursor SV, then
    runOnJS(applyReplayIndexFromWorklet)(...))
  - apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:1315 (uses useCoalescedIndexApplier)
  - apps/mobile/src/features/puzzle/utils/useCoalescedIndexApplier.ts:56 + :59 (defers apply to requestAnimationFrame)

  So: UI thread can “move” faster than JS can apply state, by design.

  ### 3) JS truth: replay “phase” is a mode signal (not the UI worklet status)

  The replay phase (replayCursorRef.current.phase) is a JS state machine updated by events like SCRUB_START, SCRUB_END, INDEX_APPLIED. It is not the same thing
  as snapBackActiveSv (UI-thread “worklet currently driving snapback”).

  Ground truth:

  - apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:547 (dispatchReplayEvent transitions the phase machine and emits trace logs)
  - apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:2019 comment explicitly says phase is a mode signal and not proof snapback is active
  - apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:2045 (“phase === 'snapback' is a mode signal, not proof…”)

  This is why your logs can legitimately show:

  - phase:"snapback" while
  - snapBackActive:0

  …and that’s not necessarily a UI-thread bug—just the expected separation of responsibilities.

  ## Why the specific error can happen (hand_scrobble_snapback_apply_backwards)

  That log is emitted here:

  - apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:1151

  It triggers when:

  - JS phase is snapback
  - and JS is about to apply an index < the last JS-applied index

  That’s exactly what your payload says:

  - phase:"snapback"
  - prevAppliedIndex:12
  - nextIndexClamped:2

  Architecturally, this can happen because we allow the following ordering:

  1. User scrubs backward (UI thread cursor drops to ~1–2).
  2. User releases → UI thread starts snapback immediately (cursor begins moving forward) before JS processes scrub end.
      - usePuzzleSkiaScrubber.ts:186-203
  3. JS receives SCRUB_END and transitions its phase machine to snapback.
      - TableTaskCore.tsx:2233 calls dispatchReplayEvent({type:'SCRUB_END'})
  4. JS still hasn’t “applied” the scrubbed-to index yet (or it’s queued behind rAF coalescing), so handLogStepIndexRef.current can still be 12.
  5. The next coalesced apply that lands is 2 (because the UI cursor is currently there) while phase is already snapback.
      - TableTaskCore.tsx:1315 + useCoalescedIndexApplier.ts:59

  Result: the diagnostic fires.

  This is the key architectural point:

  - We do not have a single atomic “commit” that updates {phase, cursor, appliedIndex} together across both threads.
  - We have eventually consistent signals that can be temporarily out of sync under rapid user interaction.

  ## Why “we built SSOT” doesn’t contradict this

  SSOT here is primarily about:

  - Rendering correctness under load (Skia stays tied to the cursor SV)
  - Eliminating competing writers to the cursor (gesture cancels snapback/autoplay synchronously)

  It does not mean:

  - JS and UI will observe the same value at the same time
  - phase changes and index applies are transactionally ordered across threads

  In fact, the system intentionally trades “perfect global synchronization” for:

  - UI responsiveness (no JS involvement per tick)
  - no scrub lag
  - no visual drift

  Your logs are showing the consequence of that trade.

  ## Bonus: why the other repeated logs show up (profile/daily streak)

  Those repeats are just React effects re-firing (not directly related to replay SSOT):

  - apps/mobile/src/services/puzzle/hooks.ts:149 and :197 re-run load() whenever the load callback identity changes (dependency changes), and dev StrictMode
    can amplify it.

  ———

  If you want, I can add a short “SSOT boundary contract” section to the new doc explaining this explicitly (UI cursor SSOT vs JS applied model SSOT vs phase
  mode), but I won’t change code unless you ask.


› put tha tanalysis into the doc


• Edited docs/PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md (+93 -0)
    346     - which is consistent with UI-thread-first snapback + rAF-coalesced JS applies.
    347 +
    348 +---
    349 +
    350 +## Architectural zoom-out: why SSOT still allows this to happen
    351 +
    352 +We built SSOT for TableTask replay, but it’s important to be precise about *what* is SSOT and *where*.
    353 +This system is intentionally **cross-thread** and therefore **eventually consistent**.
    354 +
    355 +There is no single atomic “transaction” that updates:
    356 +
    357 +- UI cursor index,
    358 +- JS-applied replay index + `handState`,
    359 +- and JS replay phase
    360 +
    361 +all at once, in the same turn, across both threads.
    362 +
    363 +Instead, the architecture has **separate sources of truth** for separate responsibilities:
    364 +
    365 +### 1) UI thread SSOT: the replay cursor (responsiveness + Skia correctness)
    366 +
    367 +The scrobbler gesture and snapback logic are designed so the UI thread can update the cursor immediately:
    368 +
    369 +- Scrubbing writes the cursor (`scrubIndexSv`) directly in the gesture worklet (no JS round-trip per tick).
    370 +- Snapback is configured and activated on the UI thread *before* notifying JS.
    371 +
    372 +Ground truth:
    373 +- `apps/mobile/src/features/puzzle/surface_skia/usePuzzleSkiaScrubber.ts:151` (scrub begin: epoch bump + cursor ownership + stop competing writers)
    374 +- `apps/mobile/src/features/puzzle/surface_skia/usePuzzleSkiaScrubber.ts:186` (scrub finalize: configure + start snapback on UI thread before JS callb
         ack)
    375 +
    376 +### 2) JS truth: the applied index + applied `handState` (data + side effects)
    377 +
    378 +JS “applies” indices by calling `applyHandReplayIndex(...)`, which sets the React `handState` snapshot and
    379 +updates `handLogStepIndex` / refs.
    380 +
    381 +But that apply is *not* synchronous with the UI thread cursor:
    382 +
    383 +- The UI thread worklet computes a desired next index and sends it to JS via `runOnJS`.
    384 +- JS applies indices through a **coalescer** that defers to `requestAnimationFrame`.
    385 +
    386 +Ground truth:
    387 +- `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:1323` (worklet selects nextIndex and calls `runOnJS(...)`)
    388 +- `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:1315` (uses `useCoalescedIndexApplier`)
    389 +- `apps/mobile/src/features/puzzle/utils/useCoalescedIndexApplier.ts:59` (rAF scheduling of the apply)
    390 +
    391 +This is a deliberate performance/UX trade:
    392 +
    393 +- UI thread stays responsive and “wins” for the cursor.
    394 +- JS applies state shortly after (next frame) and can lag under load.
    395 +
    396 +### 3) JS truth: the replay phase is a mode signal, not the UI worklet status
    397 +
    398 +The replay phase is a JS state machine (`replayCursorRef.current.phase`) driven by events like:
    399 +
    400 +- `SCRUB_START`
    401 +- `SCRUB_END`
    402 +- `INDEX_APPLIED`
    403 +
    404 +Those events are dispatched on JS via `dispatchReplayEvent(...)` and traced via `PuzzleTrace`.
    405 +
    406 +Ground truth:
    407 +- `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:547` (phase transition + event tracing)
    408 +
    409 +Critically, the code explicitly documents that phase does *not* necessarily equal “snapback is currently active”:
    410 +
    411 +> “`phase === 'snapback'` is a mode signal, not proof that snapback is currently active.”
    412 +
    413 +Ground truth:
    414 +- `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:2045`
    415 +
    416 +This explains log payloads where:
    417 +
    418 +- `phase: "snapback"` (JS mode), while
    419 +- `snapBackActive: 0` (UI-thread worklet already stopped/finished)
    420 +
    421 +### Putting it together (why the log pattern exists)
    422 +
    423 +During fast user interaction (grab/release/grab), the following ordering is possible and **architecturally allowed**:
    424 +
    425 +1) UI thread: user scrubs backward → cursor jumps to a low index (e.g. `1`).
    426 +2) UI thread: on release → snapback starts immediately and cursor begins moving forward.
    427 +3) JS: receives `SCRUB_END` and transitions its phase machine into `phase:'snapback'` (mode change).
    428 +4) JS: the latest “apply index” is still catching up via rAF coalescing, and may apply an older index (e.g. `2`)
    429 +   while JS is already in `phase:'snapback'`.
    430 +
    431 +That produces the exact diagnostic you saw:
    432 +
    433 +- `prevAppliedIndex: 12` (JS was previously applied further ahead)
    434 +- `nextIndexClamped: 2` (JS is now applying an earlier index, arriving late)
    435 +- `phase: "snapback"` (JS mode already flipped)
    436 +
    437 +This is why SSOT “for the cursor” does not automatically imply a globally atomic replay state machine: the SSOT is
    438 +intentionally split across thread boundaries, and the system tolerates short-lived mismatches in exchange for
    439 +responsive scrubbing and cursor-accurate Skia rendering.

─ Worked for 1m 04s ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• Updated the new audit doc with the architectural zoom-out analysis (SSOT boundaries + why the race is architecturally allowed):

  - docs/PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md

  Added section: “Architectural zoom-out: why SSOT still allows this to happen” with grounded references to:

  - UI-thread cursor ownership + snapback-start-before-JS: apps/mobile/src/features/puzzle/surface_skia/usePuzzleSkiaScrubber.ts:151 and :186
  - UI→JS apply path + rAF coalescing: apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:1323, :1315, and apps/mobile/src/features/puzzle/utils/
    useCoalescedIndexApplier.ts:59
  - Phase as mode signal, not snapback activity proof: apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:2045


› what is the elegant simplification that has performance in mind but prevents this inconsistency from arising?


• The inconsistency exists because the current “SSOT” is split across two control planes that are only eventually consistent:

  - UI thread owns the real cursor + snapback activity (scrubIndexSv, snapBackActiveSv, etc.).
  - JS owns a separate replay phase machine (replayCursorRef.current.phase) and a separate notion of “last applied index” (handLogStepIndexRef).
  - The bridge is runOnJS + requestAnimationFrame coalescing, so ordering is not transactional.

  So you can get “JS thinks we’re in snapback” while JS is still catching up applying an earlier cursor index.

  ———

  ## The elegant simplification (performance-first) that prevents this class of inconsistency

  ### Make the control plane SSOT only on the UI thread (one owner), and make JS a projection

  Right now, we maintain the same concept twice:

  - UI thread: “are we scrubbing / snapback active?”
  - JS: phase: 'scrubbing' | 'snapback' | ...

  That duplication is what allows “phase says snapback, but apply is behind” to exist.

  Simplification:

  - Define a single UI-thread enum like replayModeSv (number-based):
    0=autoplay, 1=scrubbing, 2=snapback, 3=hero_turn (or whatever your phase set is).
  - UI thread sets it synchronously inside the gesture worklets:
      - .onBegin → replayModeSv = scrubbing
      - .onFinalize → replayModeSv = snapback (or hero_turn if no snapback)
      - snapback completion worklet → replayModeSv = hero_turn
  - JS does not run its own phase machine for these modes. JS only mirrors replayModeSv for React UI needs and analytics.

  This keeps performance characteristics:

  - still no per-tick JS during scrubbing (cursor stays UI-thread)
  - still UI-thread snapback start (no “mode gap”)
  - still coalesced JS state application (optional)

  But it prevents the specific inconsistency because:

  - there is no longer a second independent JS “phase” that can be ahead/behind the UI reality.
  - “snapback” is only “true” if the UI-thread says so.

  Ground truth conflict today:

  - UI snapback is started/stopped in usePuzzleSkiaScrubber.ts on the UI thread
  - JS phase is transitioned in dispatchReplayEvent in TableTaskCore.tsx
    Those can reorder under fast user interaction.

  ———

  ## Second part of the simplification: stop treating “JS apply monotonicity” as a snapback invariant

  Even with the control plane unified, JS apply can still go backward when the user scrubs backward. That’s normal.

  So any “backwards apply” diagnostic should be based on the UI cursor monotonicity during snapback, not on the JS applied index relative to last time.

  You already have the right invariant in the codebase:

  - “cursor must be monotonic during snapback” (UI thread)
    TableTaskCore.tsx:2160-2184

  That’s the invariant that matters for user-visible stutter.

  The problematic diagnostic is:

  - “JS applied index went backward while phase says snapback”
    TableTaskCore.tsx:1151-1184

  That mixes control plane (JS phase) with data plane (JS apply lag), and will always be vulnerable to cross-thread ordering.

  So the simplification is:

  - Make cursor monotonicity the only snapback regression detector (UI-thread).
  - Treat JS apply ordering as “eventually consistent projection,” not a snapback correctness signal.

  ———

  ## If you want the smallest change that still “prevents it” (but less elegant)

  If you want to keep the JS phase machine for now, the minimal architectural patch is:

  - Introduce an explicit “epoch boundary” notion for JS applies:
      - SCRUB_START begins a new epoch.
      - The “backwards apply” diagnostic should only compare indices within the same epoch (or after JS has first applied the scrubbed-to baseline for that
        epoch).
  - And/or make the first apply of a new scrub epoch “immediate” (no rAF), so JS state can’t stay ahead at 12 while the cursor is already at 1–2.

  This reduces the symptom, but it keeps the dual-control-plane design that causes the issue in the first place.

  ———

  ## Why the UI-thread control plane is the “elegant” answer

  It’s one of those cases where SSOT only really works if you apply it to the mode/ownership signal as well, not just the cursor index.

  Right now we have:

  - UI: truth for cursor + snapback active
  - JS: truth for phase
    That’s two truths for the same “mode,” so you’ll keep seeing these “how did we end up in snapback while…” questions.

  A single UI-thread replay mode collapses that complexity and aligns with the performance contract (cursor-driven, UI-thread-first).

  If you want, I can sketch the exact minimal interface for a ReplayModeSv + the one low-frequency UI→JS signal you’d use to mirror it (no per-tick JS), but I
  won’t change code unless you tell me to implement it.


› put your proposed elegant architecture into the document, show the structure on disk, the contracts we'll enforce, the way we'll create clean abstractions
  that create a single source of truth and cannot drift, no code duplication, idiomatic and simple, show control flows, object hierarchy, call site changes,
  everything


• Context compacted

• Updated Plan
  └ □ Read QUICKSTART and existing docs
    □ Audit current scrub/snapback code paths
    □ Design SSOT control-plane simplification
    □ Update audit doc with proposal
    □ Self-review for consistency and simplicity

─ Worked for 1m 04s ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• Rephrasing goal: you want the scrub/snapback “apply backwards” audit doc updated to include the best, simple/elegant SSOT architecture that prevents this
  drift—showing proposed disk layout, contracts/invariants, control/data flow, object hierarchy, and the concrete call-site changes required.

  I’m going to: (1) read QUICKSTART.md + the existing audit doc, (2) re-audit the relevant code paths to confirm ground truth + line refs, then (3) write a
  detailed “Plan of Record” section into the doc with diagrams + contract definitions + file-level changes.

• Explored
  └ List ls
    Read QUICKSTART.md
    List docs
    Search PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS
    Read PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md
    List puzzle
    List surface_skia
    List components
    List tableTaskReplay
    List skiaTableTask
    Search hand_scrobble_snapback_apply_backwards in TableTaskCore.tsx
    Read TableTaskCore.tsx
    Search useCoalescedIndexApplier in TableTaskCore.tsx
    Read TableTaskCore.tsx, useCoalescedIndexApplier.ts, usePuzzleSkiaScrubber.ts, hooks.ts, SkiaInteractionBus.ts, puzzleTrace.ts, TableTaskReplayTrace.ts,
         TableTaskReplayTypes.ts, TableTaskReplayMachine.ts
    Search const snapBackActiveSv in TableTaskCore.tsx
    Read TableTaskCore.tsx
    Search replayCursorRef in TableTaskCore.tsx
    Read TableTaskCore.tsx
    Search usePuzzleSkiaScrubber in PuzzleSkiaSurface.tsx
    Read PuzzleSkiaSurface.tsx
    Search <PuzzleSkiaSurface in TableTaskCore.tsx
    Read TableTaskCore.tsx

• Updated Plan
  └ ✔ Read QUICKSTART and existing docs
    □ Audit current scrub/snapback code paths
    □ Design SSOT control-plane simplification
    □ Update audit doc with proposal
    □ Self-review for consistency and simplicity

• Explored
  └ Search snapBackActiveSv\.value in TableTaskCore.tsx
    Read TableTaskCore.tsx

• Updated Plan
  └ ✔ Read QUICKSTART and existing docs
    ✔ Audit current scrub/snapback code paths
    □ Design SSOT control-plane simplification
    □ Update audit doc with proposal
    □ Self-review for consistency and simplicity

• Explored
  └ List hooks
    Search useWorkletSignal
    Read useWorkletSignal.ts
    Read PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md, PuzzleSkiaSurface.tsx
    Search const showScrobbler in TableTaskCore.tsx

• Edited docs/PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md (+359 -1)
     12  This doc is a **ground-truth mapping** from those logs → emitting code paths.
     13 -It does **not** propose a fix; it documents what happened and why, based on the code.
     13 +It also includes a **Plan of Record** section proposing an **idiomatic SSOT control-plane simplification**
     14 +that prevents cross-thread “mode/index drift” from arising by construction.
     15
        ⋮
    440  responsive scrubbing and cursor-accurate Skia rendering.
    441 +
    442 +---
    443 +
    444 +## Plan of record: collapse the replay “control plane” into UI-thread SSOT (prevent drift by construction)
    445 +
    446 +### What we are fixing (precisely)
    447 +
    448 +The problem is not “the cursor went backwards”.
    449 +
    450 +The problem is that **we have two overlapping representations of the same replay mode**:
    451 +
    452 +- **UI thread truth** (what’s actually happening on the surface):
    453 +  - scrub gesture activity: `usePuzzleSkiaScrubber.ts` drives `isScrubbingSv` and the cursor
    454 +  - snapback activity: `TableTaskCore.tsx` worklet drives `snapBackActiveSv` + the cursor
    455 +- **JS truth** (what JS *believes* the current mode is):
    456 +  - the phase machine (`ReplayPhase`) includes `scrubbing` / `snapback`
    457 +  - and is advanced by JS callbacks (`handleScrubStart`, `handleScrubEnd`, `finishSnapBack`, etc.)
    458 +
    459 +Those two truths can temporarily diverge (by design) because:
    460 +
    461 +- the UI thread starts/ends snapback without waiting for JS (`usePuzzleSkiaScrubber.ts:186-204`,
    462 +  `TableTaskCore.tsx:2103-2127`)
    463 +- JS applies indices on rAF coalescing (`useCoalescedIndexApplier.ts:56-66`)
    464 +- JS phase is explicitly “a mode signal, not proof snapback is active” (`TableTaskCore.tsx:2045`)
    465 +
    466 +That overlap is what allows diagnostics like `hand_scrobble_snapback_apply_backwards` to exist at all:
    467 +they’re trying to reconcile two different “modes” across two threads.
    468 +
    469 +This plan removes that overlap.
    470 +
    471 +### Design goals (non-negotiable)
    472 +
    473 +1) **Single source of truth** for replay cursor ownership (writer/mode) on the UI thread.
    474 +2) **No competing sources of truth**: JS must not run a parallel scrubbing/snapback mode machine.
    475 +3) **Performance contract compliant**:
    476 +   - no per-tick `runOnJS`
    477 +   - keep hot loops in worklets (UI thread)
    478 +   - JS does data/state application and low-frequency side effects only
    479 +4) **One code path**: no “TableTask special casing” in shared components; no duplicated “mode flags”.
    480 +5) **Idiomatic in this repo**: use the existing patterns:
    481 +   - UI truth in `SharedValue`s
    482 +   - UI→JS boundary via `useWorkletSignal` / `useAnimationCompletionSignal` (events, not polling)
    483 +   - coalesced JS applies via `useCoalescedIndexApplier`
    484 +
    485 +### The simplification (the key idea)
    486 +
    487 +Split the replay system into **two orthogonal concepts**, each with exactly one owner:
    488 +
    489 +1) **Puzzle stage (JS-owned):** what the screen is doing conceptually.
    490 +   - `intro` → `autoplay_to_decision` → `hero_turn` → `hero_action_submitted` → `results`
    491 +   - This is already a JS concern: it gates actions, the intro modal, and results UI.
    492 +
    493 +2) **Cursor ownership (UI-owned):** who is currently driving the replay cursor *on the surface*.
    494 +   - `js` (idle / stable)
    495 +   - `autoplay_worklet`
    496 +   - `scrub_gesture_worklet`
    497 +   - `snapback_worklet`
    498 +
    499 +Crucially:
    500 +
    501 +- **Cursor ownership is derived from UI-thread flags** (`isScrubbingSv`, `snapBackActiveSv`, `handReplayIsPlaying`).
    502 +- Therefore it cannot drift, and it cannot disagree with reality (because it is computed from reality).
    503 +- JS receives ownership as a *fact* attached to cursor updates; it does not “infer” it.
    504 +
    505 +This makes “phase says snapback, but snapBackActive is 0” impossible as a conceptual state, because we stop using
    506 +JS phase as a proxy for snapback status. Snapback is “active” iff `snapBackActiveSv.value === 1`.
    507 +
    508 +### Proposed structure on disk (minimal + centralized)
    509 +
    510 +Keep this logic near the existing replay code, not scattered across `TableTaskCore.tsx`, `PuzzleSkiaSurface.tsx`, and
    511 +the replay machine. The goal is that there is one place to read when debugging replay control flow.
    512 +
    513 +Proposed additions/moves:
    514 +
    515 +```
    516 +apps/mobile/src/features/puzzle/components/tableTaskReplay/
    517 +  TableTaskReplayTypes.ts                 # stage types (JS-owned) + cursor owner types (UI-owned)
    518 +  TableTaskReplayMachine.ts               # JS stage machine only (NO scrubbing/snapback states)
    519 +  TableTaskReplayTrace.ts                 # existing logging helpers (keep)
    520 +  useTableTaskReplayControlPlane.ts       # NEW: creates the UI control plane + JS mirror
    521 +```
    522 +
    523 +And a small type-focused “API” surface exposed to the Skia surface:
    524 +
    525 +```
    526 +apps/mobile/src/features/puzzle/surface_skia/
    527 +  PuzzleSkiaSurface.tsx                   # accepts replayControlPlane instead of individual props
    528 +  usePuzzleSkiaScrubber.ts                # continues to be generic; writes only cursor + epoch + isScrubbing
    529 +```
    530 +
    531 +### Contracts we will enforce (the “cannot drift” guarantees)
    532 +
    533 +#### Contract A: UI owns cursor ownership
    534 +
    535 +Cursor ownership is derived on UI thread:
    536 +
    537 +```ts
    538 +// Conceptual (exact code may differ)
    539 +type ReplayCursorOwner = 0 | 1 | 2 | 3;
    540 +const ReplayCursorOwner = {
    541 +  JS: 0,
    542 +  AUTOPLAY: 1,
    543 +  SCRUB: 2,
    544 +  SNAPBACK: 3,
    545 +} as const;
    546 +
    547 +// UI-thread derived ownership (SSOT)
    548 +// Priority order matters: scrubbing > snapback > autoplay > idle
    549 +owner = isScrubbingSv.value === 1 ? SCRUB
    550 +      : snapBackActiveSv.value === 1 ? SNAPBACK
    551 +      : handReplayIsPlaying.value === 1 ? AUTOPLAY
    552 +      : JS;
    553 +```
    554 +
    555 +There is no JS “phase” that can contradict this, because JS no longer owns scrubbing/snapback mode.
    556 +
    557 +Ground truth of the flags we’re deriving from:
    558 +- `usePuzzleSkiaScrubber.ts:114` (`isScrubbingSv`)
    559 +- `usePuzzleSkiaScrubber.ts:151-204` (gesture begin/end)
    560 +- `TableTaskCore.tsx:743` (`snapBackActiveSv`)
    561 +- `TableTaskCore.tsx:2103-2127` (snapback worklet sets `snapBackActiveSv` and drives `handReplayScrubIndex`)
    562 +- `TableTaskCore.tsx:739` (`handReplayIsPlaying`)
    563 +
    564 +#### Contract B: A replay cursor update is a *snapshot*, not an event
    565 +
    566 +Every UI→JS apply carries enough information to be self-describing:
    567 +
    568 +```ts
    569 +type ReplayCursorUpdate = {
    570 +  epoch: number;          // scrubEpochSv
    571 +  index: number;          // desired replay index
    572 +  owner: ReplayCursorOwner;
    573 +};
    574 +```
    575 +
    576 +Why: if we send “index=2” without “owner=SCRUB, epoch=6”, JS has to guess what mode that index belongs to.
    577 +Snapshots prevent guessing, which prevents drift.
    578 +
    579 +Ground truth for the existing index bridge:
    580 +- `TableTaskCore.tsx:1323-1352` (`runOnJS(applyReplayIndexFromWorklet)(nextIndex, scrubEpochSv.value)`)
    581 +
    582 +#### Contract C: JS apply is epoch-aware and idempotent
    583 +
    584 +We keep `useCoalescedIndexApplier`, but we treat `(epoch, index)` as the replay cursor identity:
    585 +
    586 +- JS drops older epochs (`useCoalescedIndexApplier.ts:48-54`)
    587 +- JS applies only the latest `(epoch, index)` per frame (`useCoalescedIndexApplier.ts:56-66`)
    588 +
    589 +This stays exactly as-is conceptually; we just extend the payload to include `owner`.
    590 +
    591 +Ground truth:
    592 +- `apps/mobile/src/features/puzzle/utils/useCoalescedIndexApplier.ts:44-69`
    593 +
    594 +#### Contract D: “Backward applies” are not inherently errors
    595 +
    596 +Applying an earlier index is normal when the user scrubs backward.
    597 +
    598 +So:
    599 +
    600 +- We keep **UI-thread** monotonic cursor regression detection during snapback:
    601 +  - `hand_scrobble_snapback_cursor_regression` (`TableTaskCore.tsx:2159-2185`)
    602 +- We remove or redefine **JS-side** “apply backwards” diagnostics:
    603 +  - `hand_scrobble_snapback_apply_backwards` (`TableTaskCore.tsx:1151-1187`)
    604 +
    605 +If we still want a JS diagnostic, it must be based on a real invariant:
    606 +
    607 +- “Within the *same epoch* and while `owner === SNAPBACK`, JS applies should be non-decreasing.”
    608 +
    609 +That eliminates the false-positive where:
    610 +`prevAppliedIndex` is from epoch 5 but `nextIndex` is from epoch 6.
    611 +
    612 +### Control flow (by mode) — end-to-end
    613 +
    614 +Below, “control plane” refers to the UI-owned cursor + ownership + epoch.
    615 +
    616 +#### Autoplay (deal up to decision)
    617 +
    618 +```
    619 +JS stage machine: intro -> autoplay_to_decision
    620 +        |
    621 +        v
    622 +JS sets handReplayIsPlaying=1 (SharedValue write)
    623 +        |
    624 +        v
    625 +UI worklet computes nextIndex from playbackMs
    626 +UI sets cursor index (handReplayScrubIndex.value)
    627 +UI emits ReplayCursorUpdate {epoch, owner=AUTOPLAY, index}
    628 +        |
    629 +        v
    630 +JS coalesces + applies index -> handState snapshot updates
    631 +```
    632 +
    633 +Existing ground-truth pieces:
    634 +- cursor index updates + apply bridge: `TableTaskCore.tsx:1323-1344`
    635 +
    636 +#### Scrub begin (user grabs scrobbler)
    637 +
    638 +```
    639 +UI gesture .onBegin:
    640 +  epoch++
    641 +  stop snapback immediately (snapBack.activeSv=0)
    642 +  set isScrubbingSv=1
    643 +  update cursor index from finger
    644 +  signal JS (low-frequency) with epoch (optional)
    645 +```
    646 +
    647 +Ground truth:
    648 +- `usePuzzleSkiaScrubber.ts:151-174`
    649 +
    650 +#### Scrubbing (finger moves)
    651 +
    652 +```
    653 +UI gesture .onChange:
    654 +  update cursor index
    655 +
    656 +UI worklet emits ReplayCursorUpdate {epoch, owner=SCRUB, index}
    657 +JS applies on next frame (coalesced)
    658 +```
    659 +
    660 +Ground truth:
    661 +- `usePuzzleSkiaScrubber.ts:175-179`
    662 +- `TableTaskCore.tsx:1323-1344`
    663 +
    664 +#### Scrub end → snapback start (user releases)
    665 +
    666 +```
    667 +UI gesture .onFinalize:
    668 +  configure snapback
    669 +  set snapBack.activeSv = 1  (starts snapback immediately)
    670 +  set isScrubbingSv=0
    671 +  signal JS scrub_end (optional)
    672 +```
    673 +
    674 +Ground truth:
    675 +- `usePuzzleSkiaScrubber.ts:180-204`
    676 +
    677 +#### Snapback (cursor animates forward on UI thread)
    678 +
    679 +```
    680 +UI snapback worklet:
    681 +  while active:
    682 +    cursor index increases toward toIndex
    683 +  on completion:
    684 +    snapBack.activeSv = 0
    685 +    signal JS (useAnimationCompletionSignal)
    686 +
    687 +UI worklet emits ReplayCursorUpdate {epoch, owner=SNAPBACK, index}
    688 +JS applies on next frame (coalesced)
    689 +```
    690 +
    691 +Ground truth:
    692 +- snapback worklet: `TableTaskCore.tsx:2103-2127`
    693 +- snapback completion bridge: `TableTaskCore.tsx:2005-2012`
    694 +
    695 +#### Re-grab during snapback (the “thrash” case)
    696 +
    697 +This is the critical scenario from your logs.
    698 +
    699 +Under the proposed model:
    700 +
    701 +- UI `.onBegin` stops snapback immediately, sets `isScrubbingSv=1`, increments `epoch`.
    702 +- Ownership derived from flags flips from `SNAPBACK` → `SCRUB` immediately on UI thread.
    703 +- JS will only ever see cursor updates that include `(epoch, owner)` and therefore cannot
    704 +  interpret a scrub index as “a snapback apply”.
    705 +
    706 +### Object hierarchy (who owns what)
    707 +
    708 +```
    709 +TableTaskCore.tsx (JS)
    710 +  - owns puzzle stage machine (intro/autoplay/hero_turn/results)
    711 +  - owns applyHandReplayIndex(handState updates)
    712 +  - creates replayControlPlane (UI shared values + bridge)
    713 +  - passes replayControlPlane down to PuzzleSkiaSurface
    714 +
    715 +PuzzleSkiaSurface.tsx (JS)
    716 +  - owns Skia surface assembly + gestures
    717 +  - mounts scrubber gesture (usePuzzleSkiaScrubber) using replayControlPlane.cursor + replayControlPlane.snapBack
    718 +  - passes read-only cursor values to SkiaScene
    719 +
    720 +SkiaTableTaskScene.tsx (UI runtime + Skia)
    721 +  - reads cursor index to render cursor-driven visuals
    722 +  - should not infer replay mode from JS booleans
    723 +```
    724 +
    725 +### Call-site changes (systematic, no divergent paths)
    726 +
    727 +This is intentionally designed so we can migrate without introducing parallel systems:
    728 +
    729 +1) `apps/mobile/src/features/puzzle/components/tableTaskReplay/TableTaskReplayTypes.ts`
    730 +   - Split `ReplayPhase` into:
    731 +     - `ReplayStage` (JS-owned, no `scrubbing` / `snapback`)
    732 +     - `ReplayCursorOwner` (UI-owned)
    733 +   - Keep `scrubEpoch` concept, but treat it as UI-owned (already is via `scrubEpochSv`).
    734 +
    735 +2) `apps/mobile/src/features/puzzle/components/tableTaskReplay/TableTaskReplayMachine.ts`
    736 +   - Remove `SCRUB_START`, `SCRUB_END`, `SNAPBACK_FINISH` as “stage transitions”.
    737 +   - Stage machine remains for:
    738 +     - intro close
    739 +     - autoplay completion to hero turn
    740 +     - answer submitted → results shown
    741 +
    742 +3) `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx`
    743 +   - Replace `replayPhase` usage for scrubbing/snapback with UI-derived cursor ownership.
    744 +   - Replace writer gating:
    745 +     - today: `owner = scrubIndexWriterForPhase(replayCursorRef.current.phase)`
    746 +     - planned: `owner = derivedOwnerSv.value` (or owner passed into JS apply as a snapshot)
    747 +   - Remove/replace `hand_scrobble_snapback_apply_backwards`:
    748 +     - either delete it, or make it “same epoch + owner===SNAPBACK” only.
    749 +
    750 +4) `apps/mobile/src/features/puzzle/surface_skia/PuzzleSkiaSurface.tsx`
    751 +   - Replace the trio of props:
    752 +     - `handReplayScrubIndexSv`
    753 +     - `scrubEpochSv`
    754 +     - `snapBack`
    755 +     - `onScrubStart` / `onScrubEnd`
    756 +   - With a single prop:
    757 +     - `replayControlPlane` (containing cursor index sv, epoch sv, snapBack config, scrubber state, and signals)
    758 +
    759 +5) `apps/mobile/src/features/puzzle/surface_skia/usePuzzleSkiaScrubber.ts`
    760 +   - Keep generic; no TableTask knowledge.
    761 +   - Optionally: switch begin/end notifications to `useWorkletSignal` so we standardize on the repo’s
    762 +     UI→JS signaling primitive (`apps/mobile/src/hooks/useWorkletSignal.ts`).
    763 +
    764 +### Why this is the right solution (and why it’s simpler)
    765 +
    766 +This removes a whole class of bugs by eliminating the overlap:
    767 +
    768 +- Today: two “mode truths” exist:
    769 +  - UI: `isScrubbingSv` + `snapBackActiveSv`
    770 +  - JS: `ReplayPhase` includes `scrubbing` / `snapback`
    771 +- Plan: one truth per concept:
    772 +  - UI: cursor ownership (derived from active flags)
    773 +  - JS: stage machine (intro/autoplay/hero/results)
    774 +
    775 +It is simpler because:
    776 +
    777 +- There is no longer a need to “reason about JS phase lag” when debugging cursor behavior.
    778 +- A cursor update is self-describing (epoch + owner), so JS doesn’t guess.
    779 +- We reuse existing patterns and don’t add any new runtime dependencies.
    780 +
    781 +### Risks and mitigations
    782 +
    783 +- **Risk: migration complexity in `TableTaskCore.tsx`**
    784 +  - Mitigation: introduce `useTableTaskReplayControlPlane.ts` first, without changing behavior, then
    785 +    move call sites to it incrementally.
    786 +
    787 +- **Risk: too many `runOnJS` calls during scrubbing**
    788 +  - Mitigation: keep current coalescer (`useCoalescedIndexApplier`) and ensure we only emit updates
    789 +    when `nextIndex !== prevIndex` (already true in `TableTaskCore.tsx:1342-1344`).
    790 +
    791 +- **Risk: loss of “deterministic phase model”**
    792 +  - Mitigation: keep deterministic stage machine in JS; only remove the parts that duplicated UI truth.
    793 +    Snapback completion remains observable via `useAnimationCompletionSignal` (already present).
    794 +
    795 +- **Risk: new “owner” becomes yet another flag**
    796 +  - Mitigation: owner is *derived*, not set. It is computed from existing SSOT flags.
    797 +    It is not a new “source of truth”; it’s a projection of the truth we already have.

• Explored
  └ Read PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md

• Edited docs/PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md (+68 -0)
    611
    612 +### Public API shape (how we prevent drift via types + structure)
    613 +
    614 +The enforcement mechanism should be **primarily architectural** (API shape), with types to reduce “accidental writes”.
    615 +We already use this idea in `usePuzzleSkiaScrubber.ts` via `ReadableValue<T>` to avoid type variance + discourage
    616 +writing when only reading is intended (`usePuzzleSkiaScrubber.ts:32-34`).
    617 +
    618 +Proposed “control plane” API surface (conceptual):
    619 +
    620 +```ts
    621 +// UI-owned replay control plane (created in TableTaskCore; passed to PuzzleSkiaSurface)
    622 +export type TableTaskReplayControlPlane = {
    623 +  // Cursor (SSOT on UI thread)
    624 +  cursor: {
    625 +    indexSv: SharedValue<number>;     // writable only by worklets (gesture/autoplay/snapback)
    626 +    epochSv: SharedValue<number>;     // monotonic scrub epoch
    627 +    ownerSv: ReadableValue<number>;   // derived owner (SCRUB > SNAPBACK > AUTOPLAY > JS)
    628 +  };
    629 +
    630 +  // Snapback (UI SSOT)
    631 +  snapBack: {
    632 +    activeSv: SharedValue<number>;
    633 +    startClockMsSv: SharedValue<number>;
    634 +    fromIndexSv: SharedValue<number>;
    635 +    toIndexSv: SharedValue<number>;
    636 +    durationMsSv: SharedValue<number>;
    637 +    clockNowMsSv: SharedValue<number>;
    638 +    stepMs: number;
    639 +  };
    640 +
    641 +  // Low-frequency UI -> JS signals (optional; diagnostics/stage integration only)
    642 +  signals?: {
    643 +    scrubStart?: { token: number; epoch: number };
    644 +    scrubEnd?: { token: number; epoch: number };
    645 +    snapbackFinish?: { token: number; epoch: number };
    646 +  };
    647 +};
    648 +```
    649 +
    650 +Key points:
    651 +
    652 +- `PuzzleSkiaSurface` accepts **one prop** (`replayControlPlane`) instead of many.
    653 +- Only `PuzzleSkiaSurface` mounts the scrub gesture and therefore needs the writable `indexSv`.
    654 +- Other consumers (Skia scenes, renderers) should receive only `ReadableValue<number>` unless they truly must write.
    655 +
    656 +This makes it *hard* to create competing writers accidentally, because there is only one place where the writable
    657 +cursor is wired into gestures/worklets.
    658 +
    659 +### Data flow (explicit)
    660 +
    661 +Today, the system already separates “cursor truth” from “applied state truth”, but we blur the replay mode.
    662 +This plan makes the data flow explicit and one-directional:
    663 +
    664 +```
    665 +UI thread (Reanimated/Skia)                 JS thread (React/state)
    666 +-----------------------------------------  -----------------------------------------
    667 +cursor.indexSv (SSOT)                      handState (applied snapshot)
    668 +cursor.epochSv (SSOT)          ───────▶    applyHandReplayIndex(index)
    669 +cursor.ownerSv (derived)       ───────▶    (coalesced via rAF + epoch)
    670 +
    671 +snapBack.activeSv (SSOT)                   stage machine (intro/autoplay/hero/results)
    672 +isScrubbingSv (SSOT)             ────▶     actionsDisabled, showScrobbler, etc (JS UI)
    673 +```
    674 +
    675 +Importantly:
    676 +
    677 +- JS can lag applying `handState` under load, but it cannot “disagree” about what mode the UI is in, because
    678 +  mode is derived from UI SSOT flags and carried with updates.
    679 +
    680  ### Control flow (by mode) — end-to-end

• Updated Plan
  └ ✔ Read QUICKSTART and existing docs
    ✔ Audit current scrub/snapback code paths
    ✔ Design SSOT control-plane simplification
    □ Update audit doc with proposal
    □ Self-review for consistency and simplicity

• Explored
  └ Search Public API shape in PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md
    Read PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md
    Search Public API shape in PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md

• Updated Plan
  └ ✔ Read QUICKSTART and existing docs
    ✔ Audit current scrub/snapback code paths
    ✔ Design SSOT control-plane simplification
    ✔ Update audit doc with proposal
    □ Self-review for consistency and simplicity

• Updated Plan
  └ ✔ Read QUICKSTART and existing docs
    ✔ Audit current scrub/snapback code paths
    ✔ Design SSOT control-plane simplification
    ✔ Update audit doc with proposal
    ✔ Self-review for consistency and simplicity

• Explored
  └ Search Plan of record in PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md
    Search Public API shape in PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md
    Search Call-site changes in PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• Doc Updated

  - Added a full “Plan of Record” SSOT architecture proposal to docs/PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md:444.
  - Documented the core simplification: remove JS as a parallel source of truth for scrubbing/snapback and instead derive cursor “owner/mode” purely from UI-
    thread SSOT flags (isScrubbingSv, snapBackActiveSv, handReplayIsPlaying), so mode can’t drift.
  - Included proposed disk structure, contracts/invariants, a concrete control-plane API shape, and explicit data-flow + control-flow diagrams in docs/
    PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md:612.
  - Listed the full set of call-site changes needed to implement this without divergent code paths in docs/
    PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md:793.

  If you want, I can now implement this plan step-by-step (starting with a minimal useTableTaskReplayControlPlane.ts extraction so we don’t create parallel
  systems during the migration).


› put a depth first phased implementation plan at the top of the document each phase shoudl be fully specified showing exit criteria, all work to be done, it
  should be systematic building foundational pieces first, more phases are better than fewer.


• Explored
  └ Search <PuzzleSkiaSurface in mobile
    Read PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md
    Search typecheck in Makefile
    Read Makefile

• Edited docs/PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md (+233 -0)
      2
      3 +## Depth-first phased implementation plan (SSOT control plane; prevents drift by construction)
      4 +
      5 +This is the systematic, depth-first plan to implement the “control plane collapse” described later in this doc
      6 +(see: “Plan of record: collapse the replay control plane into UI-thread SSOT”).
      7 +
      8 +Execution principles:
      9 +
     10 +- **Foundations first**: types/contracts → control plane hook → wiring → then delete legacy overlap.
     11 +- **No divergent code paths**: when a signature changes, update the only call site in the same phase.
     12 +- **Performance contract**: no per-tick `runOnJS`; worklet→JS communication is event/snapshot driven and coalesced.
     13 +- **Diagnostics stay** until Amir confirms fixes work; do not delete instrumentation early.
     14 +
     15 +### Phase 0 — Baseline capture + guardrails (no behavior change)
     16 +
     17 +**Goal:** lock in a known-good baseline and a reproducible trace before restructuring anything.
     18 +
     19 +**Work to do:**
     20 +- Confirm puzzle trace is enabled so we get `PuzzleTrace` + `TableTask/Replay` logs.
     21 +  - `apps/mobile/src/features/puzzle/debug/puzzleTrace.ts:19-22`
     22 +- Capture a “thrash” session (rapid grab/release/grab on the scrobbler) that includes:
     23 +  - `SCRUB_START`, `SCRUB_END`, `table_task.snapback.cancel`, and `hand_scrobble_snapback_apply_backwards`.
     24 +  - Emission sites:
     25 +    - replay events: `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:547-563`
     26 +    - snapback cancel: `apps/mobile/src/features/puzzle/components/tableTaskReplay/TableTaskReplayTrace.ts:66-74`
     27 +    - apply-backwards diagnostic: `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:1151-1187`
     28 +- Add a short note (timestamp + puzzleId + sessionId) to this doc under this phase once captured.
     29 +
     30 +**Exit criteria:**
     31 +- We have a saved log excerpt proving the current “apply backwards while snapback mode” pattern exists.
     32 +- `make typecheck` passes on the baseline commit.
     33 +
     34 +---
     35 +
     36 +### Phase 1 — Introduce control-plane types + invariants (compile-only; no rewiring)
     37 +
     38 +**Goal:** make the desired architecture expressible and type-checkable before touching runtime behavior.
     39 +
     40 +**Work to do:**
     41 +- Update `apps/mobile/src/features/puzzle/components/tableTaskReplay/TableTaskReplayTypes.ts` to introduce:
     42 +  - `ReplayStage` (JS-owned screen stage: intro/autoplay/hero/results)
     43 +  - `ReplayCursorOwner` (UI-owned cursor ownership: JS/AUTOPLAY/SCRUB/SNAPBACK)
     44 +  - `ReplayCursorUpdate` = `{ epoch, index, owner }` (self-describing snapshot)
     45 +- Keep `ReplayPhase` temporarily (do not break call sites yet). The goal here is additive typing only.
     46 +
     47 +**Exit criteria:**
     48 +- Typecheck passes.
     49 +- No runtime behavior changes (purely additive).
     50 +
     51 +---
     52 +
     53 +### Phase 2 — Add `useTableTaskReplayControlPlane` (adapter hook; no call-site changes)
     54 +
     55 +**Goal:** centralize replay control-plane wiring in one file, initially as a thin adapter over existing SharedValues.
     56 +
     57 +**Work to do:**
     58 +- Add `apps/mobile/src/features/puzzle/components/tableTaskReplay/useTableTaskReplayControlPlane.ts`.
     59 +- Inputs (existing SVs owned in `TableTaskCore.tsx`):
     60 +  - cursor: `handReplayScrubIndex`, `scrubEpochSv`
     61 +  - autoplay: `handReplayIsPlaying`, `handReplayPlaybackMs` (or readable clock)
     62 +  - snapback: `snapBackActiveSv`, `snapBackStartClockMs`, `snapBackFromIndex`, `snapBackToIndex`, `snapBackDurationMs`
     63 +- Compute `ownerSv` as a **derived UI-thread value** with strict priority:
     64 +  - SCRUB (gesture active) > SNAPBACK (snapback active) > AUTOPLAY (playing) > JS (idle)
     65 +- Prefer the repo’s idiomatic UI→JS event primitive for low-frequency signals (optional but recommended):
     66 +  - `apps/mobile/src/hooks/useWorkletSignal.ts:1-44`
     67 +
     68 +**Exit criteria:**
     69 +- Hook compiles and is unused (or used only for derived reads).
     70 +- `make typecheck` passes.
     71 +
     72 +---
     73 +
     74 +### Phase 3 — Adopt control plane inside `TableTaskCore` (no external API change yet)
     75 +
     76 +**Goal:** make `TableTaskCore.tsx` read “cursor ownership” from the control plane (derived UI truth), while still
     77 +passing the old prop set down to `PuzzleSkiaSurface` for now.
     78 +
     79 +**Work to do:**
     80 +- In `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx`:
     81 +  - construct `replayControlPlane` via the new hook using the existing SVs (no rewiring yet).
     82 +  - add low-frequency trace/logging for `{ epoch, owner, isScrubbing, snapBackActive }` on ownership changes.
     83 +  - do not add logs in hot loops (no per-frame, no `onUpdate` spam).
     84 +
     85 +**Exit criteria:**
     86 +- In logs, `owner` transitions match reality during grab/release/snapback/autoplay.
     87 +- No change in user-visible behavior.
     88 +- `make typecheck` passes.
     89 +
     90 +---
     91 +
     92 +### Phase 4 — Make UI→JS index apply carry a self-describing snapshot (epoch + owner + index)
     93 +
     94 +**Goal:** eliminate the need for JS to infer mode from a laggy phase machine by attaching the “truth” to each apply.
     95 +
     96 +**Work to do:**
     97 +- Update the worklet→JS bridge in `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:1323-1352`:
     98 +  - today: `applyReplayIndexFromWorklet(nextIndex, scrubEpoch)`
     99 +  - planned: `applyReplayCursorUpdateFromWorklet({ index, epoch, owner })`
    100 +- Keep coalescing (performance contract) but coalesce **the snapshot**, not just the index:
    101 +  - `apps/mobile/src/features/puzzle/utils/useCoalescedIndexApplier.ts:44-69`
    102 +
    103 +**Exit criteria:**
    104 +- Replay still applies indices correctly (no freezes).
    105 +- Trace logs now include owner/epoch on index applies.
    106 +- `make typecheck` passes.
    107 +
    108 +---
    109 +
    110 +### Phase 5 — Redefine or remove `hand_scrobble_snapback_apply_backwards` (make diagnostics invariant-based)
    111 +
    112 +**Goal:** stop logging “errors” that can occur under normal scrubbing due to cross-thread scheduling.
    113 +
    114 +**Work to do:**
    115 +- Change `hand_scrobble_snapback_apply_backwards` (`apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:1151-1187`) to one of:
    116 +  - **Preferred:** remove it; rely on UI-thread monotonic cursor regression detection during snapback:
    117 +    - `hand_scrobble_snapback_cursor_regression` (`TableTaskCore.tsx:2159-2185`)
    118 +  - **Or:** redefine it as a *real* invariant:
    119 +    - only within the same epoch, and only while `owner === SNAPBACK` in the cursor update snapshot.
    120 +
    121 +**Exit criteria:**
    122 +- The original repro no longer produces spurious “apply backwards” errors.
    123 +- True snapback monotonicity violations are still caught by UI-thread regression diagnostics.
    124 +
    125 +---
    126 +
    127 +### Phase 6 — Move writer gating to UI-derived owner (delete “phase-as-owner” coupling)
    128 +
    129 +**Goal:** enforce “one writer” based on UI truth, not a JS phase that can lag (and is explicitly not “proof”).
    130 +
    131 +**Work to do:**
    132 +- Replace `scrubIndexWriterForPhase(replayCursorRef.current.phase)` logic in:
    133 +  - `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:775-819`
    134 +- Deprecate and then remove the phase→writer mapping in:
    135 +  - `apps/mobile/src/features/puzzle/components/tableTaskReplay/TableTaskReplayMachine.ts:83-104`
    136 +- The only valid cursor writers become structural:
    137 +  - autoplay worklet, scrub gesture worklet, snapback worklet; JS only when owner is JS.
    138 +
    139 +**Exit criteria:**
    140 +- No competing-writer violations in normal usage.
    141 +- Scrubbing remains smooth; no visible cursor stutter introduced.
    142 +- `make typecheck` passes.
    143 +
    144 +---
    145 +
    146 +### Phase 7 — Simplify JS replay machine to stage-only (remove scrubbing/snapback from JS phase)
    147 +
    148 +**Goal:** remove the overlapping source of truth: JS no longer owns scrubbing/snapback “mode” at all.
    149 +
    150 +**Work to do:**
    151 +- In `apps/mobile/src/features/puzzle/components/tableTaskReplay/TableTaskReplayTypes.ts`:
    152 +  - finish the split so “stage” is JS-owned and “owner” is UI-owned.
    153 +  - update helpers like `isHeroTurnEnabledPhase` to be stage/owner-based as needed.
    154 +    - current helper: `TableTaskReplayTypes.ts:53-55`
    155 +- In `apps/mobile/src/features/puzzle/components/tableTaskReplay/TableTaskReplayMachine.ts`:
    156 +  - remove `SCRUB_START`, `SCRUB_END`, `SNAPBACK_FINISH` as stage transitions.
    157 +  - keep stage transitions that are truly JS-owned (intro closed, decision index committed, results shown).
    158 +- In `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx`:
    159 +  - replace `replayPhase === 'scrubbing'|'snapback'` checks (`TableTaskCore.tsx:623-626`)
    160 +    with `ownerSv` checks.
    161 +
    162 +**Exit criteria:**
    163 +- Scrubbing/snapback behavior is fully described by UI SSOT flags and owner derivation.
    164 +- Stage gating (intro/actions/results) still works.
    165 +- `make typecheck` passes.
    166 +
    167 +---
    168 +
    169 +### Phase 8 — Collapse `PuzzleSkiaSurface` replay props into a single `replayControlPlane` (one-shot signature change)
    170 +
    171 +**Goal:** make incorrect wiring impossible by construction: the surface gets a single coherent control-plane object.
    172 +
    173 +**Work to do:**
    174 +- Change `apps/mobile/src/features/puzzle/surface_skia/PuzzleSkiaSurface.tsx` props to accept:
    175 +  - `replayControlPlane` (instead of individual cursor/epoch/snapback/scrub callbacks)
    176 +- Update the only call site in the same PR:
    177 +  - `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:2547-2576`
    178 +- Confirm there are no other call sites:
    179 +  - `rg "<PuzzleSkiaSurface"` should return only `TableTaskCore.tsx`.
    180 +
    181 +**Exit criteria:**
    182 +- Typecheck passes.
    183 +- Scrubbing and snapback still function.
    184 +- No duplicated API / no temporary dual-prop support introduced.
    185 +
    186 +---
    187 +
    188 +### Phase 9 — Standardize tracing vocabulary around `{ owner, epoch, index }` (observability hardening)
    189 +
    190 +**Goal:** future debugging should never require reading “phase is a mode signal, not proof” comments to interpret logs.
    191 +
    192 +**Work to do:**
    193 +- Update trace payloads in:
    194 +  - `apps/mobile/src/features/puzzle/components/tableTaskReplay/TableTaskReplayTrace.ts`
    195 +  - `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx` event tracing (`TableTaskCore.tsx:547-563`)
    196 +- Emit owner + epoch in relevant trace events (low-frequency only).
    197 +
    198 +**Exit criteria:**
    199 +- A scrub thrash session is unambiguous in logs: ownership transitions are explicit, not inferred.
    200 +
    201 +---
    202 +
    203 +### Phase 10 — Remove legacy overlap + dead code (cleanup; keep diagnostics until user verification)
    204 +
    205 +**Goal:** delete the scaffolding that allowed drift while preserving the diagnostics that prove correctness.
    206 +
    207 +**Work to do:**
    208 +- Remove unused replay events/types that only existed to model scrubbing/snapback on JS.
    209 +- Remove any leftover `ReplayPhase` coupling used purely for cursor ownership.
    210 +- Keep:
    211 +  - cursor regression diagnostic
    212 +  - writer violation diagnostics
    213 +  - any trace needed to prove behavior until Amir confirms correctness
    214 +
    215 +**Exit criteria:**
    216 +- `make typecheck` passes.
    217 +- No competing sources of truth remain for scrubbing/snapback mode.
    218 +
    219 +---
    220 +
    221 +### Phase 11 — QA validation + acceptance (user-confirmed)
    222 +
    223 +**Goal:** prove the original inconsistency class is eliminated, and verify no regressions were introduced.
    224 +
    225 +**Work to do:**
    226 +- Re-run the original repro (grab/release/grab thrash) and verify:
    227 +  - no spurious apply-backwards errors
    228 +  - no cursor regression during snapback
    229 +  - no competing-writer violations
    230 +- Verify normal playback behavior still matches expectations (including animation + audio where applicable).
    231 +
    232 +**Exit criteria:**
    233 +- Amir confirms behavior is correct in-app.
    234 +- Only after confirmation: optionally downgrade/remove extra diagnostics.
    235 +
    236  ## Why this doc exists

• Explored
  └ Read PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md
    Search ^## Why this doc exists in PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md
    Search ^### Phase 4 in PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md
    Read PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md
    Search ^### Phase 7 in PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md
    Search ^### Phase 8 in PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md
    Search ^### Phase 6 in PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md
    Search ^### Phase 9 in PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md

• Edited docs/PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md (+2 -0)
    95
    96 +Implementation note: execute this via Phases **4a–4c** so each change is small, observable in logs, and reversible.
    97 +
    98  **Work to do:**

• Edited docs/PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md (+60 -0)
    111
    112 +### Phase 4a — Add JS-side snapshot apply API (no worklet behavior change yet)
    113 +
    114 +**Goal:** introduce a single “apply cursor update” API on JS that will eventually be fed by the UI thread, without
    115 +changing runtime behavior yet.
    116 +
    117 +**Work to do:**
    118 +- Define/introduce the JS function that accepts a cursor update snapshot (even if owner is not yet fully wired):
    119 +  - `applyReplayCursorUpdateFromWorklet(update: ReplayCursorUpdate)`
    120 +- Keep the existing bridge callable for now:
    121 +  - `applyReplayIndexFromWorklet(nextIndex, scrubEpoch)` can continue to exist temporarily, and internally call the
    122 +    snapshot-based API with a placeholder `owner` (owner is not used for logic until Phase 6+).
    123 +- Ensure the coalescer can accept the update payload (either by adapting `useCoalescedIndexApplier` usage or by
    124 +  creating a small wrapper that coalesces `{ index, owner }` keyed by `epoch`).
    125 +
    126 +**Exit criteria:**
    127 +- No user-visible behavior changes.
    128 +- Typecheck passes.
    129 +- Logs/traces unchanged (this is just API scaffolding).
    130 +
    131 +---
    132 +
    133 +### Phase 4b — Lift `isScrubbingSv` into the control plane (owner becomes truly UI-derived)
    134 +
    135 +**Goal:** make `ReplayCursorOwner` derivation actually correct by construction: it must be derived from UI SSOT flags,
    136 +including the scrub gesture’s `isScrubbingSv`.
    137 +
    138 +**Work to do:**
    139 +- Refactor `usePuzzleSkiaScrubber` so `isScrubbingSv` is not “trapped” inside the hook.
    140 +  - Today, `usePuzzleSkiaScrubber` creates `isScrubbingSv` internally (`usePuzzleSkiaScrubber.ts:114`).
    141 +  - Planned: the control plane creates `isScrubbingSv` (UI SSOT), and the scrubber hook writes it.
    142 +- Wire the shared `isScrubbingSv` through:
    143 +  - `TableTaskCore.tsx` → `PuzzleSkiaSurface.tsx` → `usePuzzleSkiaScrubber(...)`
    144 +- Update the owner derivation in `useTableTaskReplayControlPlane` to use:
    145 +  - `isScrubbingSv`, `snapBackActiveSv`, `handReplayIsPlaying`
    146 +
    147 +**Exit criteria:**
    148 +- Ownership derivation no longer uses JS phase or JS refs at all.
    149 +- Logs show correct owner transitions during grab/release/snapback/autoplay.
    150 +- Typecheck passes.
    151 +
    152 +---
    153 +
    154 +### Phase 4c — Emit full `ReplayCursorUpdate` snapshots from UI thread (owner + epoch + index)
    155 +
    156 +**Goal:** stop sending “naked indices” to JS; every apply becomes self-describing, preventing interpretation drift.
    157 +
    158 +**Work to do:**
    159 +- Update the worklet reaction that currently sends `(index, epoch)`:
    160 +  - `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:1323-1352`
    161 +- Replace it with snapshot emission:
    162 +  - `runOnJS(applyReplayCursorUpdateFromWorklet)({ index, epoch, owner })`
    163 +- Ensure we still only emit when the index changes (`nextIndex !== prevIndex`) to keep `runOnJS` low-frequency.
    164 +
    165 +**Exit criteria:**
    166 +- Replay still applies indices correctly (no freezes).
    167 +- Trace logs now include owner/epoch on index applies (when trace enabled).
    168 +- Typecheck passes.
    169 +
    170 +---
    171 +
    172  ### Phase 5 — Redefine or remove `hand_scrobble_snapback_apply_backwards` (make diagnostics invariant-based)

• Edited docs/PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md (+34 -0)
    207
    208 +### Phase 6a — Switch cursor writer gating to `owner` snapshots (keep phase mapping only for parity logs)
    209 +
    210 +**Goal:** stop using JS phase as an input to cursor writer eligibility. Cursor writer eligibility should be a pure
    211 +function of UI-derived ownership.
    212 +
    213 +**Work to do:**
    214 +- In `apps/mobile/src/features/puzzle/components/TableTaskCore.tsx:775-819` (`setHandReplayScrubIndexFromJs`):
    215 +  - change the “who owns the cursor?” decision from `phase -> scrubIndexWriterForPhase(phase)` to `ownerSv`.
    216 +  - keep the old phase-based mapping temporarily **only** to emit a parity warning if it disagrees with `owner`.
    217 +    - (This is strictly transitional and should be removed in Phase 6b.)
    218 +- Ensure the write-blocked diagnostic still fires (it is valuable), but the fields now include `owner`.
    219 +
    220 +**Exit criteria:**
    221 +- Cursor writes are blocked exactly when `owner !== JS` (no false blocks).
    222 +- In logs, parity warnings (if any) are explainable and short-lived.
    223 +- `make typecheck` passes.
    224 +
    225 +---
    226 +
    227 +### Phase 6b — Delete phase→writer plumbing (owner is the only cursor ownership contract)
    228 +
    229 +**Goal:** remove the architectural footgun: phase-derived cursor ownership.
    230 +
    231 +**Work to do:**
    232 +- Remove `scrubIndexWriterForPhase` (or leave it only if used elsewhere, but do not use it for cursor gating).
    233 +  - Source: `apps/mobile/src/features/puzzle/components/tableTaskReplay/TableTaskReplayMachine.ts:83-104`
    234 +- Remove any remaining cursor-ownership checks that reference `replayPhase` instead of `owner`.
    235 +
    236 +**Exit criteria:**
    237 +- No call sites use phase to determine cursor ownership.
    238 +- `make typecheck` passes.
    239 +
    240 +---
    241 +
    242  ### Phase 7 — Simplify JS replay machine to stage-only (remove scrubbing/snapback from JS phase)

• Explored
  └ Search ^### Phase in PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md

• Edited docs/PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md (+2 -0)
    192
    193 +Implementation note: execute this via Phases **6a–6b** so we can first switch gating, then delete the legacy mapping.
    194 +
    195  **Work to do:**

• Explored
  └ Read PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md

─ Worked for 12m 11s ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• Added a depth-first, highly phased implementation plan at the top of docs/PUZZLES_TABLETASK_SCRUB_SNAPBACK_APPLY_BACKWARDS_LOG_AUDIT_2026-01-16.md:3.

  - Plan is foundations-first (types/contracts → control-plane hook → wiring → then delete legacy overlap).
  - Each phase includes Goal, Work to do (with concrete file callouts), and Exit criteria.




----------


How I typically get one built:

  □ Commit and push Phase 12

• Implementing systematically for Phase 12 (1h 37m 31s • esc to interrupt)
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
  ↳ Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
    encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
    push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).
    ⌥ + ↑ edit


› Now your job is to sytematically implement: docs/psmobile-puzzles-visual-animation-audit.md updating the documen tas you finish, noting any issues you
  encounter. Do not get blocked, especially on stupid shit like dirty files in git repo. Test as you can using the existing android sim (not ios). Commit and
  push after each phase, and when you finish get a code review from opus/gemini (give them wahtever files they ask for).

---

## Mocked arch_skill interaction (hypothetical planning exercise)

> Goal: show the **iterative, gated flow** the skill will enforce. This is a *mock* of the interaction pattern, not a real execution.

**User:**
We need to redesign the session replay pipeline to eliminate out-of-order state, keep UI thread responsive, and ship in phases.

**arch_skill:**
Got it. I’ll run Phase 1 (research) first. I’ll produce a short research brief + internal anchors, then pause for your sign‑off.

### Phase 1 — Research (internal + external)
**arch_skill:**
Internal scan plan:
- Find replay cursor ownership, phase machine, and apply logic.
- Inventory the current thread split and cross-thread messaging.
- Identify existing invariants and known failure logs.

External scan plan:
- Prior art on cross-thread state machines (Skia + JS bridge patterns).
- Known approaches for transactional apply vs eventual consistency.

Proceed? (yes/no)

**User:**
yes

**arch_skill (Phase 1 (Research) summary):**
Internal ground truth anchors:
- `apps/mobile/.../usePuzzleSkiaScrubber.ts` — UI cursor SSOT + snapback lifecycle
- `apps/mobile/.../TableTaskCore.tsx` — phase machine + apply orchestration
- `apps/mobile/.../useCoalescedIndexApplier.ts` — rAF coalescing

External anchors:
- “Cross-thread reconciliation” patterns (adopt: deterministic cursor ownership, reject: global locks)

Open questions:
- Can we introduce a single atomic “commit” boundary without UI thread regression?

Pause for Phase 1 (Research) sign‑off. Continue? (yes/no)

**User:**
yes

---

### Phase 2 — Architectural Planning (target design)
**arch_skill:**
I’ll draft Sections 0–6 in the architecture template:
- North Star (falsifiable)
- Current architecture (as-is)
- Target architecture (to-be)
- Call‑site audit

Proceed? (yes/no)

**User:**
yes

**arch_skill (Phase 2 (Architectural planning — target design) draft highlights):**
- North Star claim: “If we enforce atomic replay commits across UI/JS boundaries, then replay index will never regress under snapback within 1 frame, measured by replay-log invariant X.”
- Target architecture: introduce a single commit token and unify phase + apply boundary.
- Call‑site audit table started (12 entries).

Pause for Phase 2 (Architectural planning — target design) sign‑off. Continue? (yes/no)

**User:**
continue

---

### Phase 3 — Implementation Planning (execution design)
**arch_skill:**
I’ll produce Sections 7–9:
- Depth‑first phased plan (exit criteria + rollback)
- Test strategy (unit/integration/E2E)
- Rollout + telemetry changes

Proceed? (yes/no)

**User:**
yes

**arch_skill (Phase 3 (Implementation planning — execution design) plan snapshot):**
Phase 0: baseline invariant logging + tests
Phase 1: introduce commit token + no‑regression invariant
Phase 2: migrate apply pipeline to token gating
Phase 3: cleanup + remove old paths

Pause for Phase 3 (Implementation planning — execution design) sign‑off. Continue to execution? (yes/no)

**User:**
not yet — add a rollback for Phase 2 (migrate apply pipeline to token gating)

**arch_skill:**
Acknowledged. I’ll update Phase 2 (migrate apply pipeline to token gating) rollback and re‑present for sign‑off.

**arch_skill (Phase 3 updated):**
Phase 2 (migrate apply pipeline to token gating) rollback: restore previous apply gate and disable commit token enforcement via single flag.

Proceed to execution? (yes/no)

**User:**
yes

---

### Phase 4 — Execution (iterative delivery)
**arch_skill:**
Executing Phase 0 (baseline invariant logging + tests). I will:
- Add invariant logs
- Add baseline tests
- Update the architecture doc with completed work + decision log

(phase runs…)

**arch_skill (Phase 0 complete):**
- Added invariant logs and baseline tests
- Updated doc sections 4, 7, 10

Proceed to Phase 1 (introduce commit token + no‑regression invariant)? (yes/no)

**User:**
yes

…

**arch_skill (Final):**
All phases complete. Definition of done satisfied. Please verify in real usage; I’ll keep instrumentation until you confirm.

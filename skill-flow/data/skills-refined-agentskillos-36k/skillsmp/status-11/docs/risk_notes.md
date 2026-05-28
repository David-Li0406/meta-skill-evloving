# Risk notes (M0 InkJS demo)

## 1) Story/runtime version skew
- **Risk**: Ink stories compiled with a different ink/inkjs version may fail at runtime or diverge in branching/telemetry behaviour.
- **Impact**: Story load/runtime errors; subtle logic differences; broken telemetry assertions.
- **Mitigation**: Pin inkjs/ink compiler versions; keep compiled artifacts in-sync with source; add a simple compatibility check in build/test (fail fast if compile/runtime versions diverge); run Playwright smoke + telemetry tests after story updates.

## 2) Telemetry and smoke observability gaps
- **Risk**: Telemetry events (story_start, choice_selected, smoke_triggered, story_complete) or smoke_state events may not fire under certain paths or regress.
- **Impact**: Missing analytics/observability; CI flakes when telemetry assertions fail.
- **Mitigation**: Keep the telemetry facade default-enabled in demo; retain Playwright telemetry test coverage (tests/demo.telemetry.spec.ts) and smoke inputs (tests/demo.smoke.spec.ts); capture console logs in CI artifacts; add regression checks when new inputs/story branches are added.

## 3) Browser/platform performance constraints (smoke visual)
- **Risk**: Smoke effect or story load stutters/fails on low-end or mobile browsers (WebGL/canvas/JS perf, network latency for story assets).
- **Impact**: Poor UX or timeouts in CI (touch profile) and on devices; potential skips of smoke trigger.
- **Mitigation**: Keep smoke effect lightweight (CSS/Canvas) and configurable; test on touch profile in Playwright; keep demo assets small and served over HTTP (avoid file://); document fallback to disable smoke or reduce intensity/duration for constrained environments.

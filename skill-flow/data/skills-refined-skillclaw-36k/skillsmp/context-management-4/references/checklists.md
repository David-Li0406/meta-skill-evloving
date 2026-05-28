# Checklists

## KV-cache / prefix stability

- Remove timestamps or per-run IDs from the top of the prompt.
- Keep tool definitions stable across the whole episode.
- Make serialization deterministic (stable key ordering, stable whitespace).
- Prefer append-only logs; avoid editing historical entries.

## Append-only context

- Add corrections as new entries, not rewrites.
- When summarizing, keep summaries reversible by including pointers to source artifacts.

## Tool masking (instead of add/remove)

- Keep tool list fixed; gate usage via:
  - runtime-level masking/forcing (best), or
  - an `Allowed actions` block appended near the end (fallback).
- Use consistent tool-name prefixes to enable group gating.
- When tools are "disabled", still allow reading existing outputs that reference them.

## Filesystem as context

- Write large outputs to `.cache/context/run/` and reference them by path.
- Store only:
  - a short summary,
  - the pointer (path/URL),
  - and what to look for when reloading.
- Prefer recoverable compression: keep URLs/paths/IDs.

## Attention control via recitation

- Maintain `.cache/context/todo.md`; rewrite it frequently.
- Put "Goal / Next action" near the end of the context before decision time.
- If blocked, add a one-line "Blocked by" note in `.cache/context/todo.md`.

## Error preservation

- Keep the failure trace (or pointer to it).
- Use the 3-line template in `.cache/context/errors.md` (FAILED / WHY / NEXT).
- Do not hide failures by resetting state unless the reset itself is part of the context.

## Avoid few-shot lock-in

- If the context becomes repetitive, vary:
  - phrasing,
  - ordering of sections,
  - minor formatting changes,
  - while keeping the prefix stable.

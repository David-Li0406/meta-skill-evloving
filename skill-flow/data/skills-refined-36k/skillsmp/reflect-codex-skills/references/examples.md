# Example: ExampleProject

This example is illustrative. Treat reflection content as a heuristic signal,
not ground truth. Surface only non-niche, repeated patterns and confirm with the
user before acting on a pattern.

## Command

```bash
python3 reflect_sessions.py --project ExampleProject --limit 2 --output-style human --output -
```

## Sample output (human)

```
project: ExampleProject (2)
  title: Normalize markup milestones for documents
  last_updated: 2026-01-11T18:02:12Z
  reflected_at: 2026-01-11T18:05:02Z
  cache_status: fresh
  cache_status_reason: cache_up_to_date
  reflection:
    The session focused on normalizing milestone tags and inline markers across
    documents, with repeated attention to validation steps and edge cases in
    annotation handling. It also highlighted the need for a small helper to
    detect mismatched markers and to standardize how ranges are rendered across
    exports.

  title: Content export pipeline error triage
  last_updated: 2026-01-10T09:44:51Z
  reflected_at: 2026-01-10T09:47:03Z
  cache_status: fresh
  cache_status_reason: cache_up_to_date
  reflection:
    This session dealt with triaging export failures in the content pipeline,
    especially around missing metadata and inconsistent abbreviations. It
    repeated a theme of adding lightweight validation checks before export and
    consolidating mapping logic to avoid drift across tools.
```

## Example response (for the user)

Based on recent ExampleProject sessions, there are a couple of repeated, non-niche
themes of friction for me: (1) normalizing markers and annotations, and (2) adding lightweight
validation to catch export issues earlier. These are heuristic signals, so let
me know if you want to prioritize either, or if recent work has shifted.

## Related references

- `SKILL.md` for interpretation guardrails.
- `references/cli.md` for command recipes and flags.
- `references/README.md` for system behavior and output schema.

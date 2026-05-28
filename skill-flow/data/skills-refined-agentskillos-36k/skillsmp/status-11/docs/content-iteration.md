# Content Iteration: Replay Harness

Use the replay harness to drive an Ink story to completion with a scripted choice sequence. This is intended for golden-path regression of stable stories.

## Files
- `scripts/replay.js` — CLI entry point
- `web/stories/golden.demo.json` — example golden-path sequence for `web/stories/demo.ink`
- `tests/replay/replay.spec.js` — Jest test exercising the harness

## CLI usage
```bash
node scripts/replay.js --story web/stories/demo.ink --script web/stories/golden.demo.json
# options
#   --max-steps <n>   safety cap on total steps (default 2000)
```

Script format (golden path)
- JSON array; each entry is either:
  - a number: zero-based choice index, e.g., `[0,0,0,0]`
  - a string: substring matched (case-insensitive) against available choice text

Output
- JSON summary printed to stdout, e.g.:
```json
{
  "story": "/abs/path/web/stories/demo.ink",
  "pass": true,
  "steps": 21,
  "path": [0,0,0,0]
}
```
- Exit code 0 on success; non-zero on failure.

Tests
- Run the replay test: `npm run test:replay`
- Full suite: `npm test`

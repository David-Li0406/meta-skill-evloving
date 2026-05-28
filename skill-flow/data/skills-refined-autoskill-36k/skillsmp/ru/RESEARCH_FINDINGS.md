# RESEARCH FINDINGS: repo_updater (ru) — TOON Integration

Date: 2026-01-23

## Snapshot
- Language and entrypoint: Pure Bash; single executable script "ru" (Bash 4+).
- Primary outputs: Human-readable logs to stderr; structured JSON to stdout via --json; NDJSON and JSON state files under ~/.local/state/ru.
- Output discipline: stdout for structured data, stderr for human logs.

## Where JSON Output Is Produced
### Global switch
- --json sets JSON_OUTPUT=true in parse_args and is the global structured output switch.
- output_json() prints to stdout only when JSON_OUTPUT is true.

### Command level JSON
- ru sync --json calls generate_json_report and emits a summary object with summary and repos[].
- ru status --json emits an array of per-repo status entries (repo, path, status, branch, ahead, behind, dirty, mismatch).
- ru review --json builds discovery and summary JSON via build_review_discovery_json and related helpers.
- ru agent-sweep --json uses AGENT_SWEEP_JSON_OUTPUT and emits a JSON summary object; per-repo details are in NDJSON.

### Persistent NDJSON and JSON
- ~/.local/state/ru/logs/**/results.ndjson (run results)
- ~/.local/state/ru/review/** (state.json, checkpoint.json, gh_actions.jsonl, results.ndjson)
- ~/.local/state/ru/agent-sweep/** (state.json, results.ndjson)

## JSON Examples and Structure (from README)
- ru sync --json emits a single object containing version, timestamp, duration_seconds, config, summary, and repos[].
- README shows jq usage for filtering repos and summary counts.

## TOON Integration Opportunities
1. Single choke point: output_json() is the minimal wrapper for JSON to TOON conversion on stdout.
2. Top level JSON outputs: generate_json_report, status array, review discovery and completion JSON, agent-sweep summary.
3. NDJSON files: keep JSON for on-disk auditability unless a format flag explicitly requests TOON for stdout only.

## Suggested TOON Design
- Flag: --format=json|toon (default json), or env RU_OUTPUT_FORMAT.
- Envelope: {format:"toon", data:"<TOON>", meta:{...}} with fallback to JSON on encoder failure.
- Scope: stdout only; stderr remains human readable.
- Dependency: tr encoder path or TOON_TR_PATH env with graceful fallback.

## Gaps and Pending
- No live command capture: did not run ru sync --json or ru review --plan --json to avoid side effects. Use README sample JSON for now.
- Fixture capture: pending for ru once safe run parameters are agreed.

## Files Reviewed
- ru script (argument parsing, JSON helpers, sync and status JSON, review and agent-sweep helpers).
- README.md (JSON mode examples and output expectations).
- AGENTS.md (stdout and stderr separation, no delete rule).

## Token Savings Estimate (Proxy)
- mcp_agent_mail fixtures show TOON size ratios of ~0.69–0.79 vs JSON (character length).
- Applying that range to the README sync JSON example (371 chars compact) yields an estimated 256–293 chars in TOON.
- Real ru outputs may differ; capture live outputs for accurate measurement.

## Operational Constraints
- ru creates temp files via mktemp and removes them with rm -f; running ru implies deletions. Needs explicit approval.
- /tmp is currently full; set TMPDIR to a safe, existing directory if running ru (after approval).
- tr encoder binary is not currently present at /tmp/cargo-target/release/tr; rebuilding or setting TOON_TR_PATH will be needed for real encoding.


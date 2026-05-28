title: Ticket Queue — Command Reference

commands[22]:
  - name: list-ticket-ids
    command: "ls documents/work/tickets/TCK-*.yaml | rg -o \"TCK-[0-9]{5}\" | sort -u"
    purpose: "List all ticket IDs that MUST be merged."
  - name: list-completed-ticket-ids
    command: "timeout 30s gh pr list --state merged --limit 500 --json headRefName | rg -o \"TCK-[0-9]{5}\" | sort -u"
    purpose: "List completed ticket IDs (merged PRs)."
  - name: list-active-ticket-branch-ids
    command: "(git branch --list \"*ticket/*TCK-*\"; git branch -r --list \"*ticket/*TCK-*\") | rg -o \"TCK-[0-9]{5}\" | sort -u"
    purpose: "List ticket IDs that have local/remote branches (includes completed unless filtered)."
  - name: list-in-progress-ticket-ids
    command: "bash -lc 'set -euo pipefail; completed=$(timeout 30s gh pr list --state merged --limit 500 --json headRefName | rg -o \"TCK-[0-9]{5}\" | sort -u || true); branches=$( (git branch --list \"*ticket/*TCK-*\"; git branch -r --list \"*ticket/*TCK-*\") | rg -o \"TCK-[0-9]{5}\" | sort -u || true); comm -23 <(printf \"%s\\n\" \"$branches\") <(printf \"%s\\n\" \"$completed\")'"
    purpose: "List in-progress ticket IDs (branch exists, PR not merged)."
  - name: start-next-ticket
    command: "cargo xtask start-ticket $1"
    purpose: "Create a worktree + branch for the next unblocked ticket (or a specific RFC/ticket if $1 provided). SIDE EFFECTS: creates/updates worktrees and local branches."
  - name: check-status-on-ticket-branch
    command: "timeout 30s cargo xtask check"
    purpose: "Show status for the current ticket branch (CI + review + reviewer health)."
  - name: check-status-watch
    command: "timeout 200s cargo xtask check --watch"
    purpose: "Poll status for ~3 minutes (internal watch timeout is 180s)."
  - name: finish-after-merge
    command: "cargo xtask finish"
    purpose: "Cleanup worktree/branch after PR merges. SIDE EFFECTS: git worktree remove and local branch delete."
  - name: reviewer-state-path
    command: "printf \"%s\\n\" \"$HOME/.apm2/reviewer_state.json\""
    purpose: "Location of background reviewer health state."
  - name: reviewer-state-show
    command: "python3 - <<'PY'\nimport json\nfrom pathlib import Path\np = Path.home()/'.apm2'/'reviewer_state.json'\nprint(p)\nprint(json.dumps(json.loads(p.read_text()), indent=2, sort_keys=True))\nPY"
    purpose: "Print reviewer PIDs, started_at, log_file, pr_url, head_sha (out-of-band)."
  - name: reviewer-log-tail
    command: "tail -n 120 <LOG_FILE>"
    purpose: "Show the most recent reviewer output/tool calls/errors."
  - name: reviewer-log-mtime
    command: "stat -c \"%y %n\" <LOG_FILE>"
    purpose: "Show last modification time for a reviewer log (activity signal)."
  - name: pid-inspect
    command: "ps -p <PID> -o pid=,etime=,cmd="
    purpose: "Verify a process is alive and see its command line."
  - name: find-ai-pids
    command: "pgrep -fa \"(gemini|codex|claude)\" || true"
    purpose: "Find Gemini/Codex/Claude Code processes and PIDs (fallback when you don't have a PID file/state entry)."
  - name: log-tail-tool-ish-lines
    command: "tail -n 300 <LOG_FILE> | rg -n \"tool|Tool|Bash\\(|Read\\(|Edit\\(|Write\\(|exec|command\" || true"
    purpose: "Quickly extract the most recent tool-ish lines from a captured log."
  - name: implementer-log-mtime
    command: "stat -c \"%y %n\" <IMPLEMENTER_LOG_FILE>"
    purpose: "Show last modification time for implementer log (activity signal)."
  - name: implementer-log-tail
    command: "tail -n 200 <IMPLEMENTER_LOG_FILE>"
    purpose: "Out-of-band view of implementer progress and latest tool calls."
  - name: safe-kill-pid
    command: "bash -lc 'set -euo pipefail; ps -p <PID> -o pid=,cmd=; kill -TERM <PID>; sleep 5; kill -KILL <PID> 2>/dev/null || true'"
    purpose: "Terminate a stuck subagent/reviewer PID after verifying it is the expected process. SIDE EFFECTS: sends signals to a process."
  - name: codex-history-tail
    command: "tail -n 200 \"$HOME/.codex/history.jsonl\""
    purpose: "Out-of-band inspection of most recent Codex tool/event logs (fallback)."
  - name: claude-history-tail
    command: "tail -n 200 \"$HOME/.claude/history.jsonl\""
    purpose: "Out-of-band inspection of most recent Claude Code logs (fallback)."
  - name: start-claude-implementer-with-log
    command: "bash -lc 'set -euo pipefail; mkdir -p \"$HOME/.apm2/ticket-queue/logs\"; log=\"$HOME/.apm2/ticket-queue/logs/<TICKET_ID>.implementer.claude.log\"; script -q \"$log\" -c \"cd <WORKTREE_PATH> && claude --agent rust-developer --verbose \\\"<PASTE_IMPLEMENTER_TASK>\\\"\" & echo \"PID=$! LOG=$log\"'"
    purpose: "Spawn a Claude Code implementer session with a durable log file (run in a separate terminal/tab; you can background it and capture PID)."
  - name: start-codex-implementer-with-json-log
    command: "bash -lc 'set -euo pipefail; mkdir -p \"$HOME/.apm2/ticket-queue/logs\"; log=\"$HOME/.apm2/ticket-queue/logs/<TICKET_ID>.implementer.codex.jsonl\"; cd <WORKTREE_PATH>; codex exec --json --full-auto -p \"<PASTE_IMPLEMENTER_TASK>\" | tee \"$log\"'"
    purpose: "Run a Codex implementer subagent with JSONL event output captured to a log (out-of-band tool call visibility)."

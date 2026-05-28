#!/usr/bin/env bash
set -euo pipefail

N="${1:-3}"
SESSION="${2:-analysis_workers_$(date +%Y%m%d_%H%M%S)}"
ANALYSIS_DIR="${3:-analysis}"
MODEL="${MODEL:-}"
SANDBOX="${SANDBOX:-read-only}"
MODE="${MODE:-codex}"
PROMPT_TEMPLATE="${PROMPT_TEMPLATE:-}"
WORKER_ARGS="${WORKER_ARGS:-}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -d "$ANALYSIS_DIR/queue/pending" ]]; then
  echo "error: missing $ANALYSIS_DIR/queue/pending (did you run build_analysis_queue.py?)" >&2
  exit 1
fi

worker_cmd_base=(python "scripts/analysis_worker.py" --analysis-dir "$ANALYSIS_DIR" --sandbox "$SANDBOX" --mode "$MODE")
if [[ -n "$MODEL" ]]; then
  worker_cmd_base+=(--model "$MODEL")
fi
if [[ -n "$PROMPT_TEMPLATE" ]]; then
  worker_cmd_base+=(--prompt-template "$PROMPT_TEMPLATE")
fi
if [[ -n "$WORKER_ARGS" ]]; then
  # Space-separated extra args (keep simple; avoid quotes).
  read -r -a extra_args <<< "$WORKER_ARGS"
  worker_cmd_base+=("${extra_args[@]}")
fi

tmux new-session -d -s "$SESSION" -c "$ROOT_DIR" "${worker_cmd_base[*]} --worker-name w1"

if [[ "$N" -gt 1 ]]; then
  for i in $(seq 2 "$N"); do
    tmux new-window -t "$SESSION" -n "w$i" -c "$ROOT_DIR" "${worker_cmd_base[*]} --worker-name w$i"
  done
fi

tmux select-window -t "$SESSION:1"

echo "[ok] started tmux session: $SESSION"
echo "Attach: tmux attach -t $SESSION"
echo "Detach: Ctrl-b d"

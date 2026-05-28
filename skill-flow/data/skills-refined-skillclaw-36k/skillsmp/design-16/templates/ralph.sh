#!/bin/bash
# ralph.sh - Ralph Step Runner
# Generated for: {{PRP_ID}}
# PRP Hash: {{PRP_HASH}}

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_FILE="$SCRIPT_DIR/ralph-results.json"
export RALPH_FAILURE_CONTEXT="$SCRIPT_DIR/.failure-context.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Initialize results file if not exists
if [[ ! -f "$RESULTS_FILE" ]]; then
    echo '{"steps":{}, "gates":{}, "started":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' > "$RESULTS_FILE"
fi

usage() {
    echo "Ralph Step Runner"
    echo ""
    echo "Usage: ./ralph.sh <step-number|gate-number|command>"
    echo ""
    echo "Commands:"
    echo "  <N>        Run step N (e.g., ./ralph.sh 1)"
    echo "  gate <N>   Run gate N (e.g., ./ralph.sh gate 1)"
    echo "  status     Show progress"
    echo "  next       Run next incomplete step"
    echo "  retry      Retry last failed step with context"
    echo ""
    exit 1
}

run_step() {
    local step_num="$1"
    local step_file="$SCRIPT_DIR/step-$(printf "%02d" "$step_num").sh"
    local test_file="$SCRIPT_DIR/test-$(printf "%02d" "$step_num").sh"

    if [[ ! -f "$step_file" ]]; then
        echo -e "${RED}Step $step_num not found: $step_file${NC}"
        exit 1
    fi

    echo -e "${CYAN}Running step $step_num...${NC}"

    # Run step
    if bash "$step_file"; then
        echo -e "${GREEN}Step $step_num complete${NC}"
    else
        echo -e "${RED}Step $step_num failed${NC}"
        # Record failure
        python3 -c "
import json
with open('$RESULTS_FILE', 'r+') as f:
    data = json.load(f)
    data['steps']['$step_num'] = {'status': 'failed', 'attempts': data['steps'].get('$step_num', {}).get('attempts', 0) + 1}
    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()
"
        exit 1
    fi

    # Run test
    if [[ -f "$test_file" ]]; then
        echo -e "${CYAN}Running test $step_num...${NC}"
        if bash "$test_file"; then
            echo -e "${GREEN}Test $step_num passed${NC}"
            # Record success
            python3 -c "
import json
with open('$RESULTS_FILE', 'r+') as f:
    data = json.load(f)
    data['steps']['$step_num'] = {'status': 'passed', 'attempts': data['steps'].get('$step_num', {}).get('attempts', 0) + 1}
    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()
"
            # Clear failure context
            rm -f "$RALPH_FAILURE_CONTEXT"
        else
            echo -e "${RED}Test $step_num failed${NC}"
            exit 1
        fi
    fi
}

run_gate() {
    local gate_num="$1"
    local gate_file="$SCRIPT_DIR/gate-$gate_num.sh"

    if [[ ! -f "$gate_file" ]]; then
        echo -e "${RED}Gate $gate_num not found: $gate_file${NC}"
        exit 1
    fi

    echo -e "${CYAN}Running gate $gate_num...${NC}"
    if bash "$gate_file"; then
        # Record gate pass
        python3 -c "
import json
with open('$RESULTS_FILE', 'r+') as f:
    data = json.load(f)
    data['gates']['$gate_num'] = {'status': 'passed'}
    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()
"
    else
        # Record gate fail
        python3 -c "
import json
with open('$RESULTS_FILE', 'r+') as f:
    data = json.load(f)
    data['gates']['$gate_num'] = {'status': 'failed'}
    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()
"
        exit 1
    fi
}

show_status() {
    echo -e "${CYAN}Ralph Progress${NC}"
    echo ""
    python3 -c "
import json
import glob
import os

script_dir = '$SCRIPT_DIR'
with open('$RESULTS_FILE') as f:
    data = json.load(f)

steps = sorted(glob.glob(f'{script_dir}/step-*.sh'))
print(f'Steps: {len(steps)} total')
for step in steps:
    num = os.path.basename(step).replace('step-', '').replace('.sh', '').lstrip('0') or '0'
    status = data.get('steps', {}).get(num, {}).get('status', 'pending')
    icon = '[PASS]' if status == 'passed' else '[FAIL]' if status == 'failed' else '[    ]'
    print(f'  {icon} Step {num}: {status}')

gates = sorted(glob.glob(f'{script_dir}/gate-*.sh'))
print(f'\nGates: {len(gates)} total')
for gate in gates:
    num = os.path.basename(gate).replace('gate-', '').replace('.sh', '')
    status = data.get('gates', {}).get(num, {}).get('status', 'pending')
    icon = '[PASS]' if status == 'passed' else '[FAIL]' if status == 'failed' else '[    ]'
    print(f'  {icon} Gate {num}: {status}')
"
}

# Main
case "${1:-}" in
    "") usage ;;
    gate) run_gate "$2" ;;
    status) show_status ;;
    next)
        # Find next pending step
        next_step=$(python3 -c "
import json
import glob
import os

script_dir = '$SCRIPT_DIR'
with open('$RESULTS_FILE') as f:
    data = json.load(f)

for step in sorted(glob.glob(f'{script_dir}/step-*.sh')):
    num = os.path.basename(step).replace('step-', '').replace('.sh', '').lstrip('0') or '0'
    if data.get('steps', {}).get(num, {}).get('status') != 'passed':
        print(num)
        break
")
        if [[ -n "$next_step" ]]; then
            run_step "$next_step"
        else
            echo -e "${GREEN}All steps complete!${NC}"
        fi
        ;;
    retry)
        if [[ -f "$RALPH_FAILURE_CONTEXT" ]]; then
            last_step=$(python3 -c "import json; print(json.load(open('$RALPH_FAILURE_CONTEXT'))['step'])")
            run_step "$last_step"
        else
            echo "No failure context found"
        fi
        ;;
    [0-9]*)
        run_step "$1"
        ;;
    *)
        usage
        ;;
esac

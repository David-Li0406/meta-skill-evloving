#!/usr/bin/env bash
# ============================================================
# SSH Key Doctor - Fast SSH Health Check
# ============================================================

set -euo pipefail

VERBOSE=false
LOCAL_ONLY=false
REMOTE_ONLY=false
STRICT=false
SSH_TIMEOUT=5
CHECK_GITHUB=false
ACCEPT_NEW=false

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CANONICAL_TARGETS_SH="$REPO_ROOT/scripts/canonical-targets.sh"

# Canonical VMs (sourced if available)
CANONICAL_VMS=()
if [[ -f "$CANONICAL_TARGETS_SH" ]]; then
  # shellcheck disable=SC1090
  source "$CANONICAL_TARGETS_SH"
  if declare -p CANONICAL_VMS >/dev/null 2>&1; then
    for entry in "${CANONICAL_VMS[@]}"; do
      # entry format: user@host:os:desc
      CANONICAL_VMS+=( "${entry%%:*}" )
    done
  fi
fi
if [[ "${#CANONICAL_VMS[@]}" -eq 0 ]]; then
  CANONICAL_VMS=( "fengning@homedesktop-wsl" "fengning@macmini" )
fi

# ------------------------------------------------------------
# Output functions (safe, no escape issues)
# ------------------------------------------------------------

FAIL_COUNT=0
WARN_COUNT=0

fail() {
  echo "[FAIL] $*" >&2
  ((FAIL_COUNT++)) || true
}

warn() {
  echo "[WARN] $*" >&2
  ((WARN_COUNT++)) || true
}

pass() {
  echo "[PASS] $*"
}

info() {
  if [ "$VERBOSE" = true ]; then
    echo "[INFO] $*"
  fi
}

# ------------------------------------------------------------
# Parse arguments
# ------------------------------------------------------------

while [[ $# -gt 0 ]]; do
  case $1 in
    --verbose|-v)
      VERBOSE=true
      shift
      ;;
    --local-only)
      LOCAL_ONLY=true
      shift
      ;;
    --remote-only)
      REMOTE_ONLY=true
      shift
      ;;
    --strict)
      STRICT=true
      shift
      ;;
    --check-github)
      CHECK_GITHUB=true
      shift
      ;;
    --accept-new)
      ACCEPT_NEW=true
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 2
      ;;
  esac
done

# ------------------------------------------------------------
# Local Checks
# ------------------------------------------------------------

local_checks() {
  echo "=== Local SSH Checks ==="

  # Check SSH directory
  if [ -d "$HOME/.ssh" ]; then
    pass "SSH directory exists"
  else
    fail "SSH directory missing"
    return
  fi

  # Check known_hosts (presence only; do not print keys)
  if [ -f "$HOME/.ssh/known_hosts" ]; then
    pass "known_hosts exists"
  else
    warn "known_hosts missing (first SSH connect will prompt unless host key is already trusted)"
  fi

  # Check SSH key files
  local has_key=false
  for key_file in id_rsa id_ed25519 id_ecdsa; do
    local key_path="$HOME/.ssh/$key_file"
    if [ -f "$key_path" ]; then
      local perms
      perms=$(stat -c '%a' "$key_path" 2>/dev/null) || perms=$(stat -f '%A' "$key_path" 2>/dev/null)
      if [ "$perms" = "600" ]; then
        pass "SSH key has correct permissions: $key_file"
      else
        fail "SSH key has wrong permissions: $key_file ($perms)"
      fi
      has_key=true

      local pub_path="${key_path}.pub"
      if [ -f "$pub_path" ]; then
        pass "SSH public key exists: ${key_file}.pub"
      fi
    fi
  done

  if [ "$has_key" = false ]; then
    warn "No SSH keys found (id_rsa, id_ed25519, id_ecdsa)"
  fi

  # Check ssh-agent
  if pgrep -x ssh-agent > /dev/null 2>&1; then
    pass "ssh-agent is running"
  else
    warn "ssh-agent is not running"
  fi

  # GitHub SSH check (optional; must not hang)
  if [ "$CHECK_GITHUB" = true ]; then
    if command -v timeout >/dev/null 2>&1; then
      if timeout 5s ssh -o BatchMode=yes -o ConnectTimeout=$SSH_TIMEOUT -T git@github.com 2>/dev/null; then
        pass "GitHub SSH reachable"
      else
        warn "GitHub SSH check failed (may be expected if key not added to GitHub)"
      fi
    else
      warn "timeout not available; skipping GitHub SSH check (run manually: ssh -T git@github.com)"
    fi
  else
    info "GitHub SSH check skipped (enable with --check-github)"
  fi
}

# ------------------------------------------------------------
# Remote Checks
# ------------------------------------------------------------

remote_checks() {
  echo ""
  echo "=== Remote SSH Checks ==="

  local strict_opt="-o StrictHostKeyChecking=yes"
  if [ "$ACCEPT_NEW" = true ]; then
    strict_opt="-o StrictHostKeyChecking=accept-new"
  fi

  for vm in "${CANONICAL_VMS[@]}"; do
    info "Checking: $vm"
    # Known-hosts presence (non-fatal, but actionable)
    local host="${vm#*@}"
    if command -v ssh-keygen >/dev/null 2>&1; then
      if ssh-keygen -F "$host" >/dev/null 2>&1; then
        pass "known_hosts contains key for: $host"
      else
        warn "known_hosts missing host key for: $host"
      fi
    fi

    if ssh -o BatchMode=yes -o ConnectTimeout=$SSH_TIMEOUT $strict_opt "$vm" "echo OK" 2>/dev/null; then
      pass "SSH reachable: $vm"
    else
      fail "SSH not reachable: $vm"
    fi
  done
}

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

main() {
  echo "SSH Key Doctor - Non-hanging SSH health check"
  echo ""

  if [ "$REMOTE_ONLY" != true ]; then
    local_checks
  fi

  if [ "$LOCAL_ONLY" != true ]; then
    remote_checks
  fi

  # Summary
  echo ""
  echo "=== Summary ==="
  echo "Failures: $FAIL_COUNT"
  echo "Warnings: $WARN_COUNT"

  if [ $FAIL_COUNT -eq 0 ]; then
    echo "Result: PASS"
    if [ $WARN_COUNT -gt 0 ] && [ "$STRICT" = true ]; then
      exit 1
    fi
    exit 0
  else
    echo "Result: FAIL"
    exit 1
  fi
}

main "$@"

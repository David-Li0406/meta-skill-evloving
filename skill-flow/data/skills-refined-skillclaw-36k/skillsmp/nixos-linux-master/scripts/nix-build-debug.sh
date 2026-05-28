#!/usr/bin/env bash
# nix-build-debug.sh - Advanced Nix build troubleshooter

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

debug_log() {
    echo -e "${BLUE}[DEBUG]${NC} $*"
}

error_log() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

success_log() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
}

warn_log() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

# Check if flake.nix exists
check_flake() {
    if [[ -f "flake.nix" ]]; then
        success_log "flake.nix found"
        
        # Validate flake syntax
        debug_log "Validating flake syntax..."
        if nix flake check --no-build 2>&1 | tee /tmp/flake-check.log; then
            success_log "Flake syntax valid"
        else
            error_log "Flake syntax errors detected"
            cat /tmp/flake-check.log
            return 1
        fi
    else
        warn_log "No flake.nix found, checking for default.nix..."
        if [[ ! -f "default.nix" ]] && [[ ! -f "shell.nix" ]]; then
            error_log "No Nix expression files found"
            return 1
        fi
    fi
}

# Analyze build failures
analyze_build_failure() {
    local log_file="$1"
    
    debug_log "Analyzing build failure..."
    
    # Common error patterns
    if grep -q "error: hash mismatch" "$log_file"; then
        error_log "Hash mismatch detected"
        echo "Suggested fix: Update hash with:"
        echo "  nix-prefetch-url --unpack <url>"
        grep "got:" "$log_file" || true
    fi
    
    if grep -q "error: attribute.*missing" "$log_file"; then
        error_log "Missing attribute in expression"
        grep "attribute" "$log_file" | head -5
    fi
    
    if grep -q "infinite recursion" "$log_file"; then
        error_log "Infinite recursion detected"
        echo "Check for circular dependencies in your imports"
    fi
    
    if grep -q "building '.*' failed" "$log_file"; then
        error_log "Build phase failed"
        echo "Enable verbose logging with:"
        echo "  nix build --print-build-logs --verbose"
    fi
    
    if grep -q "cannot coerce" "$log_file"; then
        error_log "Type coercion error"
        grep "cannot coerce" "$log_file"
    fi
}

# Check Nix store integrity
check_store() {
    debug_log "Checking Nix store integrity..."
    
    if nix-store --verify --check-contents 2>&1 | grep -i error; then
        error_log "Store corruption detected"
        warn_log "Consider running: nix-store --verify --check-contents --repair"
    else
        success_log "Store integrity OK"
    fi
}

# Analyze closure size
analyze_closure() {
    local target="${1:-.#}"
    
    debug_log "Analyzing closure size for $target..."
    
    if nix path-info -rsSh "$target" 2>/dev/null | sort -hk2 | tail -20; then
        success_log "Top 20 largest dependencies shown"
        
        echo ""
        echo "Total closure size:"
        nix path-info -Sh "$target" 2>/dev/null || warn_log "Could not calculate total size"
    else
        warn_log "Could not analyze closure (target might not be built yet)"
    fi
}

# Check for common issues
check_common_issues() {
    debug_log "Checking for common issues..."
    
    # Check Nix version
    NIX_VERSION=$(nix --version | awk '{print $3}')
    debug_log "Nix version: $NIX_VERSION"
    
    # Check if flakes are enabled
    if nix eval --expr 'builtins.getFlake "nixpkgs"' &>/dev/null; then
        success_log "Flakes are enabled"
    else
        warn_log "Flakes might not be enabled. Add to ~/.config/nix/nix.conf:"
        echo "  experimental-features = nix-command flakes"
    fi
    
    # Check disk space
    AVAILABLE=$(df -h /nix/store | awk 'NR==2 {print $4}')
    debug_log "Available space in /nix/store: $AVAILABLE"
    
    # Check for stale locks
    if [[ -f "flake.lock" ]]; then
        LOCK_AGE=$(( ($(date +%s) - $(stat -c %Y flake.lock)) / 86400 ))
        if [[ $LOCK_AGE -gt 30 ]]; then
            warn_log "flake.lock is $LOCK_AGE days old. Consider updating:"
            echo "  nix flake update"
        fi
    fi
    
    # Check gc roots
    GC_ROOTS=$(nix-store --gc --print-roots | wc -l)
    debug_log "Number of GC roots: $GC_ROOTS"
    
    if [[ $GC_ROOTS -gt 1000 ]]; then
        warn_log "Many GC roots detected. Clean up old profiles:"
        echo "  nix-env --delete-generations old"
        echo "  nix-collect-garbage -d"
    fi
}

# Interactive build mode
interactive_build() {
    local target="${1:-.#}"
    
    debug_log "Entering interactive build mode for $target"
    
    # Try to build and capture output
    if nix build "$target" --show-trace --print-build-logs 2>&1 | tee /tmp/nix-build.log; then
        success_log "Build succeeded!"
        return 0
    else
        error_log "Build failed"
        analyze_build_failure /tmp/nix-build.log
        
        echo ""
        warn_log "Entering debug shell..."
        nix develop "$target" --command bash -c '
            echo "Debug environment loaded"
            echo "Build inputs available: $buildInputs"
            echo "Native build inputs: $nativeBuildInputs"
            echo ""
            echo "Try building manually:"
            echo "  cd $sourceRoot"
            echo "  genericBuild"
            exec bash
        '
    fi
}

# Generate build report
generate_report() {
    local target="${1:-.#}"
    local report_file="nix-debug-report-$(date +%Y%m%d-%H%M%S).txt"
    
    {
        echo "=== Nix Build Debug Report ==="
        echo "Generated: $(date)"
        echo "Target: $target"
        echo ""
        
        echo "=== System Info ==="
        nix --version
        uname -a
        echo ""
        
        echo "=== Flake Metadata ==="
        nix flake metadata 2>&1 || echo "Not a flake"
        echo ""
        
        echo "=== Build Evaluation ==="
        nix eval --show-trace "$target.meta" 2>&1 || echo "Could not evaluate meta"
        echo ""
        
        echo "=== Dependencies ==="
        nix-store --query --references "$target" 2>&1 | head -20 || echo "Not built yet"
        echo ""
        
        echo "=== Recent Build Logs ==="
        if [[ -f /tmp/nix-build.log ]]; then
            tail -100 /tmp/nix-build.log
        fi
        
    } > "$report_file"
    
    success_log "Report saved to: $report_file"
}

# Main function
main() {
    case "${1:-check}" in
        check)
            echo "=== Nix Build Debugger ==="
            check_flake
            check_common_issues
            check_store
            ;;
        build)
            interactive_build "${2:-.#}"
            ;;
        analyze)
            analyze_closure "${2:-.#}"
            ;;
        report)
            generate_report "${2:-.#}"
            ;;
        *)
            echo "Usage: $0 {check|build|analyze|report} [target]"
            echo ""
            echo "Commands:"
            echo "  check   - Run diagnostic checks"
            echo "  build   - Interactive build with debugging"
            echo "  analyze - Analyze closure size"
            echo "  report  - Generate detailed debug report"
            exit 1
            ;;
    esac
}

main "$@"

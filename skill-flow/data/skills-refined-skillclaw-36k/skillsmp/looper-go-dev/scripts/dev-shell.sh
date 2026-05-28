#!/usr/bin/env bash
# Looper-Go Development Helper
# Provides quick access to common dev commands

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
    cat <<'USAGE'
Looper-Go Development Helper

Usage: dev-shell.sh <command>

Commands:
  build           Build the looper binary
  install         Install looper to GOPATH/bin
  test            Run all tests
  test-v          Run tests with verbose output
  cover           Run tests with coverage
  lint            Run linter
  fmt             Format code
  clean           Clean build artifacts
  run             Run looper with default config
  doctor          Check dependencies
  validate        Validate task file
  logs            Tail log files
  shell           Start dev shell with LOOPER_REPO set

Examples:
  dev-shell.sh build
  dev-shell.sh test
  dev-shell.sh run

Environment:
  LOOPER_REPO     Auto-set to repo root
USAGE
}

# Find repo root
find_repo_root() {
    local dir="$PWD"
    while [ "$dir" != "/" ]; do
        if [ -f "$dir/go.mod" ] && grep -q "github.com/nibzard/looper-go" "$dir/go.mod" 2>/dev/null; then
            printf "%s" "$dir"
            return 0
        fi
        dir=$(dirname "$dir")
    done
    echo "Error: looper-go repo root not found" >&2
    return 1
}

REPO_ROOT=$(find_repo_root)
export LOOPER_REPO="$REPO_ROOT"

cd "$REPO_ROOT"

case "${1:-}" in
    build)
        echo -e "${GREEN}Building looper...${NC}"
        go build -o bin/looper ./cmd/looper
        echo -e "${GREEN}Built: bin/looper${NC}"
        ;;
    install)
        echo -e "${GREEN}Installing looper...${NC}"
        go install ./cmd/looper
        echo -e "${GREEN}Installed: $(go env GOPATH)/bin/looper${NC}"
        ;;
    test)
        echo -e "${GREEN}Running tests...${NC}"
        go test ./...
        ;;
    test-v)
        echo -e "${GREEN}Running tests (verbose)...${NC}"
        go test -v ./...
        ;;
    cover)
        echo -e "${GREEN}Running tests with coverage...${NC}"
        go test -cover ./...
        ;;
    lint)
        if command -v golangci-lint >/dev/null 2>&1; then
            echo -e "${GREEN}Running linter...${NC}"
            golangci-lint run ./...
        else
            echo -e "${YELLOW}golangci-lint not found. Install with:${NC}"
            echo "  go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest"
        fi
        ;;
    fmt)
        echo -e "${GREEN}Formatting code...${NC}"
        go fmt ./...
        gofmt -w .
        ;;
    clean)
        echo -e "${GREEN}Cleaning build artifacts...${NC}"
        go clean -cache
        rm -f bin/looper
        echo -e "${GREEN}Cleaned${NC}"
        ;;
    run)
        echo -e "${GREEN}Running looper...${NC}"
        if [ -x "./bin/looper" ]; then
            ./bin/looper run
        else
            echo -e "${YELLOW}Binary not found. Building first...${NC}"
            go build -o bin/looper ./cmd/looper
            ./bin/looper run
        fi
        ;;
    doctor)
        echo -e "${GREEN}Checking dependencies...${NC}"
        if [ -x "./bin/looper" ]; then
            ./bin/looper doctor
        else
            echo -e "${YELLOW}Binary not found. Building first...${NC}"
            go build -o bin/looper ./cmd/looper
            ./bin/looper doctor
        fi
        ;;
    validate)
        echo -e "${GREEN}Validating task file...${NC}"
        if [ -x "./bin/looper" ]; then
            ./bin/looper validate
        else
            echo -e "${YELLOW}Binary not found. Building first...${NC}"
            go build -o bin/looper ./cmd/looper
            ./bin/looper validate
        fi
        ;;
    logs)
        echo -e "${GREEN}Tailing logs...${NC}"
        if [ -x "./bin/looper" ]; then
            ./bin/looper tail
        else
            echo -e "${YELLOW}Binary not found. Building first...${NC}"
            go build -o bin/looper ./cmd/looper
            ./bin/looper tail
        fi
        ;;
    shell)
        echo -e "${GREEN}Entering dev shell...${NC}"
        echo -e "LOOPER_REPO=${LOOPER_REPO}"
        echo "Type 'exit' to leave"
        exec bash --norc
        ;;
    -h|--help|"")
        usage
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}" >&2
        usage
        exit 1
        ;;
esac

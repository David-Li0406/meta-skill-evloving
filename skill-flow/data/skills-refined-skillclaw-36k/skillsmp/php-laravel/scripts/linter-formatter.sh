#!/bin/bash

set -e

DIRTY_MODE=false
TEST_MODE=false
VERBOSE=false

show_help() {
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo ""
    echo "Run Laravel Pint code formatter"
    echo ""
    echo "Options:"
    echo "  -d, --dirty     Only format files with uncommitted Git changes"
    echo "  -t, --test      Dry run - check style without modifying files"
    echo "  -v, --verbose   Show verbose output"
    echo "  -h, --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $(basename "$0")              # Format all files"
    echo "  $(basename "$0") --dirty      # Format only modified files"
    echo "  $(basename "$0") --test       # Check style without changes"
}

while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--dirty)
            DIRTY_MODE=true
            shift
            ;;
        -t|--test)
            TEST_MODE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

build_pint_args() {
    local args=""

    if [[ "$DIRTY_MODE" == "true" ]]; then
        args="$args --dirty"
    fi

    if [[ "$TEST_MODE" == "true" ]]; then
        args="$args --test"
    fi

    if [[ "$VERBOSE" == "true" ]]; then
        args="$args -v"
    fi

    echo "$args"
}

run_pint() {
    local pint_args
    pint_args=$(build_pint_args)

    if [[ -f "vendor/bin/sail" ]]; then
        echo "Using Laravel Sail..."
        ./vendor/bin/sail pint $pint_args
    elif [[ -f "vendor/bin/pint" ]]; then
        echo "Using local Pint..."
        ./vendor/bin/pint $pint_args
    else
        echo "Error: Neither Sail nor Pint found in vendor/bin"
        echo "Install Pint with: composer require laravel/pint --dev"
        exit 1
    fi
}

run_pint

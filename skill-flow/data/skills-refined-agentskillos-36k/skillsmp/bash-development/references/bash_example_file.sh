#!/usr/bin/env bash
set -euo pipefail

# Script metadata
SCRIPT_NAME=$(basename "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
readonly SCRIPT_VERSION="1.0.0"
readonly SCRIPT_NAME SCRIPT_DIR

# Include utility functions
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/bash_example_includes.bash"

# Error handler
handle_error() {
    print_error "An error occurred on line \"$1\""
    exit 1
}

trap 'handle_error $LINENO' ERR

# Usage function
usage() {
    cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS] <argument>

Description:
    Brief description of what this script does

Options:
    -h, --help      Show this help message
    -v, --version   Show version information
    -d, --debug     Enable debug mode

Examples:
    ${SCRIPT_NAME} file.txt
    ${SCRIPT_NAME} --debug file.txt

EOF
}

# Main function
main() {
    local debug end_time duration start_time
    start_time=$(date +%s)
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h | --help)
                usage
                exit 0
                ;;
            -v | --version)
                printf '%s version %s\n' "${SCRIPT_NAME}" "${SCRIPT_VERSION}"
                exit 0
                ;;
            -d | --debug)
                debug=1
                set -x
                shift
                ;;
            -*)
                print_error "Unknown option: \"$1\""
                usage
                exit 1
                ;;
            *) break ;;
        esac
    done

    # Validate arguments
    if [[ $# -lt 1 ]]; then
        print_error "Missing required argument"
        usage
        exit 1
    fi

    # Main logic
    print_info "Starting ${SCRIPT_NAME}..."
    # TODO: Add your logic here

    print_success "Script completed successfully"
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    [[ -n "${debug:-}" ]] && print_info "Script completed in ${duration} seconds"
}

# Run main function
main "$@"

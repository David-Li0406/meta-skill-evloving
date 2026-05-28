#!/usr/bin/env nu
# Validate Nushell syntax without executing
# Usage: nu validate-syntax.nu <file.nu>

def main [file: path] {
    if not ($file | path exists) {
        print $"Error: File '($file)' not found"
        exit 1
    }

    # Parse the file to check for syntax errors
    let result = (do { nu --ide-check 100 $file } | complete)

    if $result.exit_code == 0 {
        if ($result.stdout | str trim | is-empty) {
            print $"✓ ($file): Syntax OK"
        } else {
            # IDE check outputs diagnostics
            print $"($file) diagnostics:"
            print $result.stdout
        }
    } else {
        print $"✗ ($file): Syntax errors found"
        print $result.stderr
        exit 1
    }
}

#!/usr/bin/env nu
# Run all tests for the nushell scripts

def main [] {
    print $"(ansi cyan)Running all nushell script tests...(ansi reset)"
    print ""

    let test_dir = $env.FILE_PWD
    let tests = [
        "test_lib.nu"
        "test_bundle_manager.nu"
        "test_skill_manager.nu"
    ]

    mut all_passed = true

    for test_file in $tests {
        print $"(ansi attr_bold)>>> ($test_file)(ansi reset)"
        let result = (nu ($test_dir | path join $test_file) | complete)
        if $result.exit_code != 0 {
            print $"(ansi red)FAILED:(ansi reset)"
            print $result.stderr
            $all_passed = false
        } else {
            print $result.stdout
        }
        print ""
    }

    if $all_passed {
        print $"(ansi green)(ansi attr_bold)All test suites passed!(ansi reset)"
    } else {
        print $"(ansi red)(ansi attr_bold)Some tests failed!(ansi reset)"
        exit 1
    }
}

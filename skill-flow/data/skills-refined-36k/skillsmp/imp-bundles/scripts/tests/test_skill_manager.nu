#!/usr/bin/env nu
# Tests for skill-manager.nu

use std/assert

def main [] {
    print "Running skill-manager.nu tests..."

    test_help_output
    test_available_returns_table
    test_status_returns_table
    test_list_local
    test_list_global

    print $"(ansi green)All tests passed!(ansi reset)"
}

def test_help_output [] {
    let script = ($env.FILE_PWD | path dirname | path join "skill-manager.nu")
    let result = (nu $script | complete)
    assert ($result.exit_code == 0) "Help should succeed"
    assert ($result.stdout | str contains "Usage:") "Should show usage"
    assert ($result.stdout | str contains "link") "Should show link command"
    assert ($result.stdout | str contains "unlink") "Should show unlink command"
    assert ($result.stdout | str contains "status") "Should show status command"
}

def test_available_returns_table [] {
    let script = ($env.FILE_PWD | path dirname | path join "skill-manager.nu")
    let result = (nu $script available | complete)
    assert ($result.exit_code == 0) "Available should succeed"
    # Table output contains column headers
    assert ($result.stdout | str contains "skill") "Should have skill column"
    assert ($result.stdout | str contains "bundle") "Should have bundle column"
    assert ($result.stdout | str contains "description") "Should have description column"
    # imp-bundles should always be available since we're in it
    assert ($result.stdout | str contains "imp-bundles") "Should list imp-bundles skill"
}

def test_status_returns_table [] {
    let script = ($env.FILE_PWD | path dirname | path join "skill-manager.nu")
    let result = (nu $script status | complete)
    assert ($result.exit_code == 0) "Status should succeed"
    # Table output contains column headers
    assert ($result.stdout | str contains "skill") "Should have skill column"
    assert ($result.stdout | str contains "status") "Should have status column"
    # Should show link status for imp-bundles
    assert ($result.stdout | str contains "imp-bundles") "Should list imp-bundles skill"
}

def test_list_local [] {
    let script = ($env.FILE_PWD | path dirname | path join "skill-manager.nu")
    let result = (nu $script list | complete)
    assert ($result.exit_code == 0) "List should succeed"
    # Returns table (may be empty) with skill and target columns
}

def test_list_global [] {
    let script = ($env.FILE_PWD | path dirname | path join "skill-manager.nu")
    let result = (nu $script list -g | complete)
    assert ($result.exit_code == 0) "List -g should succeed"
    # Returns table with skill and target columns
}

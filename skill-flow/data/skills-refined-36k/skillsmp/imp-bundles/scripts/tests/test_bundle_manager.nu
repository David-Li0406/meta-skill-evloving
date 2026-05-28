#!/usr/bin/env nu
# Tests for bundle-manager.nu

use std/assert

def main [] {
    print "Running bundle-manager.nu tests..."

    test_help_output
    test_list_returns_table
    test_available_returns_table

    print $"(ansi green)All tests passed!(ansi reset)"
}

def test_help_output [] {
    let script = ($env.FILE_PWD | path dirname | path join "bundle-manager.nu")
    let result = (nu $script | complete)
    assert ($result.exit_code == 0) "Help should succeed"
    assert ($result.stdout | str contains "Usage:") "Should show usage"
    assert ($result.stdout | str contains "add <name>") "Should show add command"
    assert ($result.stdout | str contains "list") "Should show list command"
}

def test_list_returns_table [] {
    let script = ($env.FILE_PWD | path dirname | path join "bundle-manager.nu")
    let result = (nu $script list | complete)
    assert ($result.exit_code == 0) "List should succeed"
    # Table output contains column headers
    assert ($result.stdout | str contains "name") "Should have name column"
    assert ($result.stdout | str contains "type") "Should have type column"
    # We know imp-bundles should exist since we're in it
    assert ($result.stdout | str contains "imp-bundles") "Should list imp-bundles"
}

def test_available_returns_table [] {
    let script = ($env.FILE_PWD | path dirname | path join "bundle-manager.nu")
    let result = (nu $script available | complete)
    # Should either succeed with gh available, or fail with "gh cli required"
    if $result.exit_code == 0 {
        assert ($result.stdout | str contains "name") "Should have name column"
        assert ($result.stdout | str contains "description") "Should have description column"
        assert ($result.stdout | str contains "rust") "Should list rust bundle"
    } else {
        assert ($result.stderr | str contains "gh cli required") "Should mention gh required"
    }
}

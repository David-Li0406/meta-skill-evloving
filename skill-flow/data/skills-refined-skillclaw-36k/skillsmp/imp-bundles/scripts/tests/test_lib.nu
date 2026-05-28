#!/usr/bin/env nu
# Tests for lib.nu

use std/assert

use ../lib.nu

def main [] {
    print "Running lib.nu tests..."

    test_find_project_root
    test_init_bundle_dir
    test_list_subdirs
    test_list_subdirs_nonexistent
    test_has_subdirs_true
    test_has_subdirs_false
    test_color_functions
    test_require_dir_exists
    test_require_dir_missing
    test_require_no_dir_missing
    test_require_no_dir_exists
    test_parse_frontmatter
    test_parse_frontmatter_missing

    print $"(ansi green)All tests passed!(ansi reset)"
}

def test_find_project_root [] {
    let result = (lib find-project-root)
    assert ($result | str contains "ocean-rs") $"Expected path containing ocean-rs, got: ($result)"
}

def test_init_bundle_dir [] {
    let result = (lib init-bundle-dir)
    assert ($result | str ends-with "nix/bundles") $"Expected path ending with nix/bundles, got: ($result)"
    assert ($result | path exists) $"Bundle dir should exist: ($result)"
}

def test_list_subdirs [] {
    let bundle_dir = (lib init-bundle-dir)
    let subdirs = (lib list-subdirs $bundle_dir)
    assert (($subdirs | length) > 0) "Should find at least one bundle"
}

def test_list_subdirs_nonexistent [] {
    let result = (lib list-subdirs "/nonexistent/path")
    assert (($result | length) == 0) "Should return empty list for nonexistent path"
}

def test_has_subdirs_true [] {
    let bundle_dir = (lib init-bundle-dir)
    let result = (lib has-subdirs $bundle_dir)
    assert $result "Bundle dir should have subdirs"
}

def test_has_subdirs_false [] {
    let result = (lib has-subdirs "/nonexistent")
    assert (not $result) "Nonexistent path should return false"
}

def test_color_functions [] {
    let red = (lib color-red "test")
    assert ($red | str contains "test") "Red output should contain test"

    let green = (lib color-green "test")
    assert ($green | str contains "test") "Green output should contain test"
}

def test_require_dir_exists [] {
    let bundle_dir = (lib init-bundle-dir)
    # Should not error
    lib require-dir $bundle_dir
}

def test_require_dir_missing [] {
    let result = (try { lib require-dir "/nonexistent"; "ok" } catch { "error" })
    assert ($result == "error") "require-dir should fail for missing dir"
}

def test_require_no_dir_missing [] {
    # Should not error
    lib require-no-dir "/nonexistent/path"
}

def test_require_no_dir_exists [] {
    let bundle_dir = (lib init-bundle-dir)
    let result = (try { lib require-no-dir $bundle_dir; "ok" } catch { "error" })
    assert ($result == "error") "require-no-dir should fail for existing dir"
}

def test_parse_frontmatter [] {
    let bundle_dir = (lib init-bundle-dir)
    let skill_md = $"($bundle_dir)/imp-bundles/skills/imp-bundles/SKILL.md"
    let fm = (lib parse-frontmatter $skill_md)
    assert ($fm.name? == "imp-bundles") "Should parse name from frontmatter"
    assert ($fm.description? | is-not-empty) "Should parse description from frontmatter"
}

def test_parse_frontmatter_missing [] {
    let fm = (lib parse-frontmatter "/nonexistent/file.md")
    assert (($fm | columns | length) == 0) "Should return empty record for missing file"
}

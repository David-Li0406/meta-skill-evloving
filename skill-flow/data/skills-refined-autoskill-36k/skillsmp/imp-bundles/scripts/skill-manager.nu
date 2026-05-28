#!/usr/bin/env nu
# Skill manager for Claude Code skills from imp bundles
#
# Symlinks nix/bundles/<bundle>/skills/<skill>/ to .claude/skills/
# or ~/.claude/skills/ when using --global flag.

use lib.nu

const LOCAL_SKILLS_DIR = ".claude/skills"
const GLOBAL_SKILLS_DIR = ".claude/skills"

# Get the skills directory path based on scope
def get-skills-dir [
    global: bool  # Use global ~/.claude/skills
]: nothing -> string {
    if $global {
        $"($env.HOME)/($GLOBAL_SKILLS_DIR)"
    } else {
        let root = lib find-project-root
        $"($root)/($LOCAL_SKILLS_DIR)"
    }
}

# Find all skills across all bundles
def find-all-skills []: nothing -> table<bundle: string, skill: string, path: string, description: string> {
    let bundle_dir = lib init-bundle-dir

    lib list-subdirs $bundle_dir
    | each {|bundle_name|
        let skills_dir = $"($bundle_dir)/($bundle_name)/skills"
        if ($skills_dir | path exists) {
            lib list-subdirs $skills_dir
            | each {|skill_name|
                let skill_path = $"($skills_dir)/($skill_name)"
                let skill_md = $"($skill_path)/SKILL.md"
                let frontmatter = lib parse-frontmatter $skill_md
                {
                    bundle: $bundle_name
                    skill: $skill_name
                    path: $skill_path
                    description: ($frontmatter.description? | default "")
                }
            }
        } else {
            []
        }
    }
    | flatten
}

# Find which bundle contains a given skill
def find-skill-bundle [
    skill_name: string  # Skill to find
]: nothing -> record<bundle: string, path: string> {
    let bundle_dir = lib init-bundle-dir

    for bundle_name in (lib list-subdirs $bundle_dir) {
        let skill_path = $"($bundle_dir)/($bundle_name)/skills/($skill_name)"
        if ($skill_path | path exists) {
            return { bundle: $bundle_name, path: $skill_path }
        }
    }

    lib die $"skill '($skill_name)' not found in any bundle"
}

# Build target symlink path
def skill-target [
    skills_dir: string  # Skills directory
    name: string        # Skill name
]: nothing -> string {
    $"($skills_dir)/($name)"
}

# Link skill(s) to skills directory
def "main link" [
    name?: string    # Skill name (all if not specified)
    --global (-g)    # Use ~/.claude/skills
] {
    let skills_dir = get-skills-dir $global
    mkdir $skills_dir

    if ($name | is-not-empty) {
        let skill_info = find-skill-bundle $name
        let target = skill-target $skills_dir $name

        if ($target | path type) == "symlink" {
            lib info $"skill '($name)' already linked"
        } else if ($target | path exists) {
            lib die $"(lib shorten-path $target) exists and is not a symlink"
        } else {
            let real_source = $skill_info.path | path expand
            ln -s $real_source $target
            lib ok $"linked: (lib shorten-path $target) -> (lib shorten-path $skill_info.path)"
        }
    } else {
        mut count = 0
        for skill in (find-all-skills) {
            let target = skill-target $skills_dir $skill.skill

            if ($target | path type) == "symlink" {
                # Already linked, skip silently
            } else if ($target | path exists) {
                lib warn $"(lib shorten-path $target) exists and is not a symlink, skipping"
            } else {
                let real_source = $skill.path | path expand
                ln -s $real_source $target
                lib ok $"linked: (lib shorten-path $target) -> (lib shorten-path $skill.path)"
                $count = $count + 1
            }
        }
        lib ok $"Done. Linked ($count) skill\(s\)."
    }
}

# Remove a skill symlink
def "main unlink" [
    name: string     # Skill name to unlink
    --global (-g)    # Use ~/.claude/skills
] {
    let skills_dir = get-skills-dir $global
    let target = skill-target $skills_dir $name

    let target_type = $target | path type
    if $target_type != "symlink" {
        if ($target | path exists) {
            lib die $"(lib shorten-path $target) exists but is not a symlink"
        } else {
            lib die $"skill '($name)' is not linked"
        }
    }

    rm $target
    lib ok $"unlinked: (lib shorten-path $target)"
}

# List linked skills
def "main list" [
    --global (-g)    # Use ~/.claude/skills
] {
    let skills_dir = get-skills-dir $global

    if not ($skills_dir | path exists) {
        return []
    }

    ls -la $skills_dir
    | where type == dir or type == symlink
    | each {|entry|
        {
            skill: ($entry.name | path basename)
            target: (if $entry.type == "symlink" { lib shorten-path $entry.target } else { null })
        }
    }
}

# List skills available from bundles
def "main available" [] {
    find-all-skills | select skill bundle description
}

# Show link status for all skills
def "main status" [
    --global (-g)    # Use ~/.claude/skills
] {
    let skills_dir = get-skills-dir $global

    find-all-skills
    | each {|skill|
        let target = skill-target $skills_dir $skill.skill
        let status = if ($target | path type) == "symlink" {
            "linked"
        } else if ($target | path exists) {
            "conflict"
        } else {
            "not linked"
        }
        {
            skill: $skill.skill
            status: $status
            bundle: $skill.bundle
        }
    }
}

# Show usage help
def main [] {
    print "Skill manager for Claude Code skills from imp bundles"
    print ""
    print "Usage: skill-manager.nu <command> [--global] [args]"
    print ""
    print "Commands:"
    print "  link [name]     Link skill\(s\), all if no name given"
    print "  unlink <name>   Remove skill symlink"
    print "  list            List linked skills"
    print "  available       List skills available from bundles"
    print "  status          Show link status for all skills"
    print ""
    print "Options:"
    print "  --global, -g    Use ~/.claude/skills instead of .claude/skills"
    print ""
    print "Examples:"
    print "  skill-manager.nu link"
    print "  skill-manager.nu link rust-code-quality"
    print "  skill-manager.nu list -g"
    print "  skill-manager.nu status --global"
}

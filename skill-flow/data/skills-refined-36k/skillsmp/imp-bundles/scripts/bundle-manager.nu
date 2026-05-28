#!/usr/bin/env nu
# Bundle manager for imp-nix bundles
#
# Manages git submodules sourced from github.com/imp-nix/bundle.<name>

use lib.nu

const BUNDLE_ORG = "imp-nix"
const BUNDLE_PREFIX = "bundle."

# Build GitHub URL for a bundle
def bundle-url [
    name: string  # Bundle name
]: nothing -> string {
    $"https://github.com/($BUNDLE_ORG)/($BUNDLE_PREFIX)($name)"
}

# Build local path for a bundle
def bundle-path [
    bundle_dir: string  # Base bundles directory
    name: string        # Bundle name
]: nothing -> string {
    $"($bundle_dir)/($name)"
}

# Add a bundle as a git submodule
def "main add" [
    name: string  # Bundle name to add
] {
    let bundle_dir = lib init-bundle-dir
    let url = bundle-url $name
    let path = bundle-path $bundle_dir $name

    lib require-no-dir $path

    lib info $"Adding bundle '($name)' from ($url)"
    git submodule add $url $path
    git submodule update --init $path
    lib ok $"Done. Bundle added at ($path)"
}

# Remove a bundle submodule
def "main remove" [
    name: string  # Bundle name to remove
] {
    let bundle_dir = lib init-bundle-dir
    let path = bundle-path $bundle_dir $name

    lib require-dir $path

    let git_dir = git -C $path rev-parse --absolute-git-dir | str trim

    lib info $"Removing bundle '($name)'"
    git submodule deinit -f $path
    git rm -f $path
    rm -rf $git_dir
    lib ok "Done. Remember to commit the changes."
}

# Update bundle(s) to latest remote version
def "main update" [
    name?: string  # Bundle name (all if not specified)
] {
    let bundle_dir = lib init-bundle-dir

    if ($name | is-not-empty) {
        let path = bundle-path $bundle_dir $name
        lib require-dir $path
        lib info $"Updating bundle '($name)'"
        git submodule update --remote $path
    } else {
        lib info "Updating all bundles"
        for bundle in (lib list-subdirs $bundle_dir) {
            let path = bundle-path $bundle_dir $bundle
            git submodule update --remote $path
        }
    }
    lib ok "Done. Review changes and commit if desired."
}

# List installed bundles
def "main list" [] {
    let bundle_dir = lib init-bundle-dir

    lib list-subdirs $bundle_dir
    | each {|name|
        let git_file = $"($bundle_dir)/($name)/.git"
        {
            name: $name
            type: (if ($git_file | path exists) { "submodule" } else { "directory" })
        }
    }
}

# List available bundles from GitHub (requires gh)
def "main available" [] {
    lib require-cmd "gh" "gh cli"

    gh repo list $BUNDLE_ORG --limit 100 --json name,description
    | from json
    | where name starts-with $BUNDLE_PREFIX
    | each {|r|
        {
            name: ($r.name | str replace $BUNDLE_PREFIX "")
            description: ($r.description | default "")
        }
    }
}

# Show bundle info from GitHub (requires gh)
def "main info" [
    name: string  # Bundle name
] {
    lib require-cmd "gh" "gh cli"

    let repo = $"($BUNDLE_ORG)/($BUNDLE_PREFIX)($name)"
    gh repo view $repo --json name,description,url,updatedAt
    | from json
    | select name url description updatedAt
}

# Show usage help
def main [] {
    print $"Bundle manager for ($BUNDLE_ORG) bundles"
    print ""
    print "Usage: bundle-manager.nu <command> [args]"
    print ""
    print "Commands:"
    print "  add <name>      Add bundle as git submodule"
    print "  remove <name>   Remove bundle submodule"
    print "  update [name]   Update bundle\(s\), all if no name given"
    print "  list            List installed bundles"
    print "  available       List available bundles \(requires gh\)"
    print "  info <name>     Show bundle info \(requires gh\)"
    print ""
    print "Examples:"
    print "  bundle-manager.nu add rust"
    print "  bundle-manager.nu update"
    print "  bundle-manager.nu available"
}

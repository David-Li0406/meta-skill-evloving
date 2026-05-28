#!/usr/bin/env nu
# Get information about a Nushell command
# Usage: nu command-info.nu <command>

def main [cmd: string] {
    # Get help output
    let help_result = (do { help $cmd } | complete)

    if $help_result.exit_code != 0 {
        print $"Command '($cmd)' not found"
        print ""
        print "Searching for similar commands..."
        help commands | where name =~ $cmd | select name description | first 10
    } else {
        print $help_result.stdout
    }
}

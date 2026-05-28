#!/usr/bin/env nu
# Common bash to nushell translations reference
# Usage: nu bash-to-nu.nu [pattern]

def main [pattern?: string] {
    let translations = [
        {bash: "$VAR", nu: "$env.VAR or $var", note: "env vs local variable"}
        {bash: "export VAR=value", nu: "$env.VAR = 'value'", note: "set environment variable"}
        {bash: "$(command)", nu: "(command)", note: "command substitution"}
        {bash: "command | grep pattern", nu: "command | where col =~ 'pattern'", note: "filter by pattern"}
        {bash: "command | grep -v pattern", nu: "command | where col !~ 'pattern'", note: "exclude pattern"}
        {bash: "command | awk '{print $1}'", nu: "command | get column", note: "extract column"}
        {bash: "command | cut -d: -f1", nu: "command | split column ':' | get column1", note: "split and extract"}
        {bash: "command | wc -l", nu: "command | length", note: "count lines/items"}
        {bash: "command | head -n 10", nu: "command | first 10", note: "first N items"}
        {bash: "command | tail -n 10", nu: "command | last 10", note: "last N items"}
        {bash: "command | sort", nu: "command | sort", note: "sort (structured)"}
        {bash: "command | sort -u", nu: "command | sort | uniq", note: "sort unique"}
        {bash: "command | uniq -c", nu: "command | uniq --count", note: "count occurrences"}
        {bash: "[ -f file ]", nu: "('file' | path exists)", note: "check file exists"}
        {bash: "[ -d dir ]", nu: "('dir' | path exists) and ('dir' | path type) == 'dir'", note: "check dir exists"}
        {bash: "[ -z \"$var\" ]", nu: "($var | is-empty)", note: "check empty"}
        {bash: "[ -n \"$var\" ]", nu: "not ($var | is-empty)", note: "check not empty"}
        {bash: "for i in list; do ... done", nu: "for i in $list { ... }", note: "for loop"}
        {bash: "while condition; do ... done", nu: "while $condition { ... }", note: "while loop"}
        {bash: "if condition; then ... fi", nu: "if $condition { ... }", note: "if statement"}
        {bash: "case $var in ...) ;; esac", nu: "match $var { pattern => { ... } }", note: "pattern matching"}
        {bash: "VAR=value command", nu: "with-env {VAR: 'value'} { command }", note: "temp env var"}
        {bash: "command > file", nu: "command | save file", note: "redirect stdout"}
        {bash: "command >> file", nu: "command | save --append file", note: "append to file"}
        {bash: "command 2>&1", nu: "command | complete", note: "capture all output"}
        {bash: "command &", nu: "# not directly supported, use par-each for parallelism", note: "background job"}
        {bash: "echo $((1 + 2))", nu: "1 + 2", note: "arithmetic"}
        {bash: "read -p 'prompt' var", nu: "let var = (input 'prompt')", note: "read input"}
        {bash: "cat file", nu: "open file", note: "read file"}
        {bash: "cat file1 file2", nu: "[file1 file2] | each { open $in } | flatten", note: "concatenate files"}
        {bash: "find . -name '*.txt'", nu: "glob **/*.txt", note: "find files"}
        {bash: "xargs", nu: "each { ... }", note: "process items"}
        {bash: "seq 1 10", nu: "1..10", note: "generate sequence"}
        {bash: "date +%Y-%m-%d", nu: "date now | format date '%Y-%m-%d'", note: "format date"}
    ]

    if $pattern != null {
        $translations | where {|row|
            ($row.bash | str contains -i $pattern) or
            ($row.nu | str contains -i $pattern) or
            ($row.note | str contains -i $pattern)
        }
    } else {
        $translations
    }
}

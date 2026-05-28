# Nushell Command Reference

## File System

| Command | Description        | Example                  |
| ------- | ------------------ | ------------------------ |
| `ls`    | List directory     | `ls **/*.rs`             |
| `cd`    | Change directory   | `cd ~/projects`          |
| `cp`    | Copy files         | `cp file.txt backup/`    |
| `mv`    | Move/rename        | `mv old.txt new.txt`     |
| `rm`    | Remove files       | `rm -r temp/`            |
| `mkdir` | Create directory   | `mkdir -p a/b/c`         |
| `touch` | Create empty file  | `touch file.txt`         |
| `open`  | Read & parse file  | `open data.json`         |
| `save`  | Write to file      | `$data \| save out.json` |
| `watch` | Watch file changes | `watch . {ls}`           |

## Text Processing

| Command         | Description        | Example                         |
| --------------- | ------------------ | ------------------------------- |
| `lines`         | Split into lines   | `open f.txt \| lines`           |
| `str trim`      | Remove whitespace  | `" hi " \| str trim`            |
| `str replace`   | Replace text       | `"ab" \| str replace "a" "x"`   |
| `str substring` | Extract substring  | `"hello" \| str substring 1..3` |
| `str upcase`    | Uppercase          | `"hi" \| str upcase`            |
| `str downcase`  | Lowercase          | `"HI" \| str downcase`          |
| `split row`     | Split by delimiter | `"a,b" \| split row ","`        |
| `str join`      | Join list          | `[a, b] \| str join ","`        |
| `parse`         | Parse with pattern | `"k=v" \| parse "{k}={v}"`      |
| `find`          | Search text        | `ls \| find ".rs"`              |

## Table Operations

| Command     | Description       | Example                  |
| ----------- | ----------------- | ------------------------ |
| `select`    | Choose columns    | `$t \| select col1 col2` |
| `reject`    | Remove columns    | `$t \| reject col3`      |
| `rename`    | Rename column     | `$t \| rename old new`   |
| `where`     | Filter rows       | `$t \| where age > 21`   |
| `sort-by`   | Sort table        | `$t \| sort-by name`     |
| `reverse`   | Reverse order     | `$t \| reverse`          |
| `uniq`      | Remove duplicates | `$t \| uniq`             |
| `uniq-by`   | Unique by column  | `$t \| uniq-by id`       |
| `first`     | First N rows      | `$t \| first 5`          |
| `last`      | Last N rows       | `$t \| last 5`           |
| `skip`      | Skip N rows       | `$t \| skip 10`          |
| `take`      | Take N rows       | `$t \| take 100`         |
| `group-by`  | Group rows        | `$t \| group-by type`    |
| `transpose` | Pivot table       | `$rec \| transpose k v`  |
| `flatten`   | Unnest columns    | `$t \| flatten nested`   |
| `join`      | Join tables       | `$t1 \| join $t2 id`     |
| `merge`     | Merge records     | `$r1 \| merge $r2`       |

## List Operations

| Command    | Description       | Example                                |
| ---------- | ----------------- | -------------------------------------- |
| `each`     | Transform items   | `$l \| each {\|x\| $x * 2}`            |
| `par-each` | Parallel each     | `$l \| par-each {slow-op}`             |
| `filter`   | Keep matching     | `$l \| filter {\|x\| $x > 0}`          |
| `reduce`   | Fold/accumulate   | `$l \| reduce {\|it,acc\| $acc + $it}` |
| `any`      | Any match?        | `$l \| any {\|x\| $x > 10}`            |
| `all`      | All match?        | `$l \| all {\|x\| $x > 0}`             |
| `zip`      | Pair lists        | `$l1 \| zip $l2`                       |
| `append`   | Add to end        | `$l \| append 99`                      |
| `prepend`  | Add to start      | `$l \| prepend 0`                      |
| `insert`   | Insert at index   | `$l \| insert 2 "x"`                   |
| `update`   | Update at index   | `$l \| update 0 "new"`                 |
| `length`   | Count items       | `$l \| length`                         |
| `is-empty` | Check empty       | `$l \| is-empty`                       |
| `compact`  | Remove nulls      | `$l \| compact`                        |
| `flatten`  | Flatten nested    | `[[1,2],[3]] \| flatten`               |
| `chunks`   | Split into chunks | `1..10 \| chunks 3`                    |
| `window`   | Sliding window    | `$l \| window 3`                       |

## Math

| Command      | Description    | Example               |
| ------------ | -------------- | --------------------- |
| `math sum`   | Sum values     | `[1,2,3] \| math sum` |
| `math avg`   | Average        | `[1,2,3] \| math avg` |
| `math max`   | Maximum        | `[1,2,3] \| math max` |
| `math min`   | Minimum        | `[1,2,3] \| math min` |
| `math abs`   | Absolute value | `-5 \| math abs`      |
| `math round` | Round number   | `3.7 \| math round`   |
| `math floor` | Round down     | `3.7 \| math floor`   |
| `math ceil`  | Round up       | `3.2 \| math ceil`    |

## Data Formats

| Command     | Description    | Example                  |
| ----------- | -------------- | ------------------------ |
| `from json` | Parse JSON     | `'{"a":1}' \| from json` |
| `to json`   | Generate JSON  | `{a: 1} \| to json`      |
| `from yaml` | Parse YAML     | `open f.yaml`            |
| `to yaml`   | Generate YAML  | `{a: 1} \| to yaml`      |
| `from csv`  | Parse CSV      | `open data.csv`          |
| `to csv`    | Generate CSV   | `$table \| to csv`       |
| `from toml` | Parse TOML     | `open config.toml`       |
| `to toml`   | Generate TOML  | `{a: 1} \| to toml`      |
| `to md`     | Markdown table | `$table \| to md`        |

## Network

| Command       | Description    | Example                            |
| ------------- | -------------- | ---------------------------------- |
| `http get`    | GET request    | `http get https://api.example.com` |
| `http post`   | POST request   | `http post url {data: 1}`          |
| `http put`    | PUT request    | `http put url {data: 1}`           |
| `http delete` | DELETE request | `http delete url`                  |

## System

| Command    | Description     | Example                |
| ---------- | --------------- | ---------------------- |
| `ps`       | List processes  | `ps \| where cpu > 10` |
| `sys`      | System info     | `sys \| get host`      |
| `which`    | Find command    | `which nu`             |
| `sleep`    | Pause execution | `sleep 1sec`           |
| `date now` | Current time    | `date now`             |

## Control Flow

| Command | Description      | Example                                 |
| ------- | ---------------- | --------------------------------------- |
| `if`    | Conditional      | `if $x > 0 { "pos" } else { "neg" }`    |
| `match` | Pattern match    | `match $x { 1 => "one", _ => "other" }` |
| `for`   | Loop over items  | `for x in $list { print $x }`           |
| `while` | Conditional loop | `while $x < 10 { $x += 1 }`             |
| `loop`  | Infinite loop    | `loop { if $done { break } }`           |
| `try`   | Error handling   | `try { risky } catch { fallback }`      |

## Shell Utilities

| Command    | Description     | Example                       |
| ---------- | --------------- | ----------------------------- |
| `print`    | Output text     | `print "message"`             |
| `input`    | Read user input | `let name = (input "Name: ")` |
| `clear`    | Clear screen    | `clear`                       |
| `history`  | Command history | `history \| last 10`          |
| `help`     | Get help        | `help str`                    |
| `complete` | Capture output  | `^cmd \| complete`            |
| `do`       | Execute closure | `do {ls}`                     |
| `with-env` | Run with env    | `with-env {A: 1} { $env.A }`  |

## Path Operations

| Command         | Description  | Example                         |
| --------------- | ------------ | ------------------------------- |
| `path exists`   | Check exists | `"f.txt" \| path exists`        |
| `path type`     | Get type     | `"f.txt" \| path type`          |
| `path dirname`  | Parent dir   | `"/a/b/c" \| path dirname`      |
| `path basename` | File name    | `"/a/b/c.txt" \| path basename` |
| `path expand`   | Resolve path | `"~/file" \| path expand`       |
| `path join`     | Join paths   | `"/a" \| path join "b"`         |
| `path parse`    | Parse path   | `"/a/b.txt" \| path parse`      |
| `path split`    | Split path   | `"/a/b/c" \| path split`        |

## Environment

| Command        | Description   | Example                                    |
| -------------- | ------------- | ------------------------------------------ |
| `$env.VAR`     | Get env var   | `$env.HOME`                                |
| `$env.VAR = x` | Set env var   | `$env.PATH = ($env.PATH \| append "/new")` |
| `load-env`     | Load env vars | `{A: 1, B: 2} \| load-env`                 |

## Getting Help

```nu
help                           # List all commands
help <command>                 # Command help
help str                       # Subcommand category
<command> --help               # Same as help <command>
```

## POSIX to Nushell Translation

| Task                    | POSIX                           | Nushell                                                   |
| ----------------------- | ------------------------------- | --------------------------------------------------------- |
| Find files recursively  | `find . -name "*.log"`          | `ls **/*.log`                                             |
| Filter text for pattern | `cmd \| grep "ERROR"`           | `cmd \| where col =~ "ERROR"` or `cmd \| find "ERROR"`    |
| Extract columns         | `cat f \| awk '{print $2, $5}'` | `open f \| select col2 col5`                              |
| Redirect to file        | `echo "hello" > file`           | `"hello" \| save file`                                    |
| Set environment var     | `export MY_VAR="value"`         | `$env.MY_VAR = "value"`                                   |
| Count lines             | `wc -l file`                    | `open file \| lines \| length`                            |
| Sort unique             | `sort -u file`                  | `open file \| lines \| sort \| uniq`                      |
| First N lines           | `head -n 5 file`                | `open file \| lines \| first 5`                           |
| Last N lines            | `tail -n 5 file`                | `open file \| lines \| last 5`                            |
| Check file exists       | `[ -f file ]`                   | `("file" \| path exists)`                                 |
| Check dir exists        | `[ -d dir ]`                    | `("dir" \| path type) == "dir"`                           |
| Command substitution    | `$(cmd)`                        | `(cmd)`                                                   |
| Temp environment        | `VAR=x cmd`                     | `with-env {VAR: x} { cmd }`                               |
| Process by PID          | `ps -p 1234`                    | `ps \| where pid == 1234`                                 |
| Kill by name            | `pkill -f pattern`              | `ps \| where name =~ pattern \| each { kill $in.pid }`    |
| Disk usage              | `du -sh *`                      | `ls \| select name size`                                  |
| Find large files        | `find . -size +100M`            | `ls **/* \| where size > 100mb`                           |
| Count occurrences       | `grep -c pattern file`          | `open file \| lines \| where {$in =~ pattern} \| length`  |
| Replace in file         | `sed -i 's/old/new/g' file`     | `open file \| str replace -a "old" "new" \| save -f file` |
| JSON query (jq)         | `cat f \| jq '.items[].name'`   | `open f \| get items.name`                                |
| Loop over files         | `for f in *.txt; do...`         | `ls *.txt \| each {\|f\| ... }`                           |
| Parallel execution      | `xargs -P 4`                    | `par-each`                                                |
| Background job          | `cmd &`                         | `job spawn { cmd }` (thread-based)                        |

## Advanced Glob Patterns

```nu
# Basic patterns
glob *.rs                         # All .rs files in current dir
glob **/*.rs                      # Recursive .rs files
glob **/*.{rs,toml}               # Multiple extensions

# Character classes
glob "[Cc]*"                      # Files starting with C or c
glob "[!cCbMs]*"                  # Files NOT starting with c, C, b, M, or s
glob "src/[a-m]*.rs"              # Files starting with a-m

# Exclusions
glob **/*.rs --exclude [**/target/** **/tests/**]
glob **/tsconfig.json --exclude [**/node_modules/**]

# Options
glob **/*.rs --depth 2            # Max 2 directories deep
glob "**/*.txt" --follow-symlinks # Follow symlinks
```

## Common Task Recipes

### File Operations

```nu
# List top 5 largest files
ls | sort-by size --reverse | first 5

# Find files modified in last 24 hours
ls **/* | where modified > ((date now) - 1day)

# Find duplicate files by name
ls **/* | group-by name | transpose name files | where {|r| ($r.files | length) > 1}

# Bulk rename: .jpeg to .jpg
ls *.jpeg | each {|f| mv $f.name ($f.name | str replace ".jpeg" ".jpg")}

# Total size of directory
ls | get size | math sum
```

### Process Management

```nu
# Top 5 processes by CPU
ps | sort-by cpu --reverse | first 5

# Find processes by name
ps | where name =~ "python"

# Memory usage by process name
ps | where name == "node" | get mem | math sum

# Kill all matching processes
ps | where name =~ "zombie" | each {|p| kill $p.pid}
```

### Data Analysis

```nu
# CSV: group and count
open data.csv | group-by category | transpose key items | insert count {|r| $r.items | length}

# JSON API: extract nested data
http get https://api.example.com/users | get data.users | select name email

# Log analysis: error frequency
open app.log | lines | where {$in =~ "ERROR"} | parse "[{level}] {msg}" | group-by msg | transpose msg entries | insert count {|r| $r.entries | length}

# Aggregate by field
open sales.json | group-by region | transpose region sales | insert total {|r| $r.sales.amount | math sum}
```

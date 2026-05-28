---
name: jj
description: Expert guidance for using JJ (Jujutsu) version control system. Use when user mentions jj, jujutsu, or needs version control in JJ-managed repositories. Covers commands, revsets, templates, evolog, operations log, and git interop.
---

<objective>
Provide expert guidance for JJ version control operations. Help users understand JJ's mental model (immutable change IDs, auto-snapshots, conflicts don't block) and execute commands correctly.
</objective>

<quick_start>

```bash
jj log -r <revset> [-p]               # View history (-p: diffs)
jj show -r <rev>                      # Revision details
jj new [-A] <base>                    # Create revision (-A: insert after)
jj edit <rev>                         # Switch to revision
jj desc -r <rev> -m "text"            # Set description
jj diff                               # Changes in @
jj restore <fileset>                  # Discard changes
jj rebase -s <src> -o <dest>          # Rebase onto dest
jj undo                               # Undo last operation
```
</quick_start>

<success_criteria>
- JJ operation completed without error
- Working copy (@) in expected state
- Revision graph reflects intended structure
- For rebases/splits: no unintended conflicts introduced
</success_criteria>

<core_principles>
- Change IDs (immutable) vs Commit IDs (content-hash, changes on edit)
- Operations log: every operation can be undone (progressive `jj undo`, `jj redo` reverses)
- No staging area: working copy auto-snapshots
- Conflicts don't block: resolve later
- Commits are lightweight: edit freely
- Colocated by default: Git repos have both `.jj` and `.git` (since v0.34)
- Three DSLs:
  - revsets: select revisions (a change ID is a valid singleton revset)
  - filesets: select files (a filepath is a valid singleton fileset)
  - templates: control output format
</core_principles>

<essential_commands>

```bash
jj log -r <revset> [-p]               # View history (--patch/-p: include diffs)
jj log -r <revset> -G                 # -G is short for --no-graph
jj show -r <rev>                      # Show revision details (description + diff)
jj evolog -r <rev> [-p]               # View a revision's evolution
jj new [-A] <base>                    # Create revision and edit it (-A: insert after base)
jj new --no-edit <base>               # Create without switching
jj edit <rev>                         # Switch to editing revision
jj desc -r <rev> -m "text"            # Set description
jj metaedit -r <rev> -m "text"        # Modify metadata (author, timestamps, description)

jj diff                               # Changes in @
jj diff -r <rev>                      # Changes in revision
jj file show -r <rev> <fileset>       # Show file contents at revision
jj restore <fileset>                  # Discard changes to files
jj restore --from <commit-id> <fileset> # Restore from another revision

jj split -r <rev> <paths> -m "text"   # Split into two revisions
jj absorb                             # Auto-squash changes into ancestor commits

jj rebase -s <src> -o <dest>          # Rebase with descendants onto dest
jj rebase -r <rev> -o <dest>          # Rebase single revision onto dest
jj rebase -s 'a | b | c' -o <dest>    # Batch: multiple roots via revset union

jj file annotate <path>               # Blame: who changed each line
jj bisect run -- <cmd>                # Binary search for bug-introducing commit
```
</essential_commands>

<additional_commands>

```bash
jj undo                               # Undo last operation (progressive)
jj redo                               # Redo undone operation
jj sign -r <rev>                      # Cryptographically sign commit
jj unsign -r <rev>                    # Remove signature
jj revert -r <rev>                    # Create commit that reverts changes
jj tag set <name> -r <rev>            # Create/update local tag
jj tag delete <name>                  # Delete local tag
jj git colocation enable              # Convert to colocated repo
jj git colocation disable             # Convert to non-colocated
```
</additional_commands>

<revset_reference>
```bash
@, @-, @--                            # Working copy, parent(s), grandparent(s)
::@                                   # Ancestors
@::                                   # Descendants
mine()                                # Your changes
conflicted()                          # Has conflicts
visible()                             # Visible revisions
hidden()                              # Hidden revisions
description(substring-i:"text")       # Match description (partial, case-insensitive)
subject(substring:"text")             # Match first line only
signed()                              # Cryptographically signed commits
A | B, A & B, A ~ B                   # Union, intersection, difference
change_id(prefix)                     # Explicit change ID prefix lookup
parents(x, 2)                         # Parents with depth
exactly(x, 3)                         # Assert exactly N revisions
```
</revset_reference>

<anti_patterns>
<pitfall name="use-short-flag">
Use `-r` not `--revisions`:
```bash
jj log -r xyz          # correct
jj log --revisions xyz # error
```
</pitfall>

<pitfall name="parallel-branches">
Use `--no-edit` for parallel branches:
```bash
jj new parent -m "A"; jj new -m "B"                             # B is child of A
jj new --no-edit parent -m "A"; jj new --no-edit parent -m "B"  # Both children of parent
```
</pitfall>

<pitfall name="quote-revsets">
Quote revsets in shell:
```bash
jj log -r 'description(substring:"[todo]")'
```
</pitfall>

<pitfall name="use-onto">
Use `-o`/`--onto` instead of deprecated `-d`/`--destination` (v0.36+):
```bash
jj rebase -s xyz -o main   # correct
jj rebase -s xyz -d main   # deprecated
```
</pitfall>

<pitfall name="symbol-expressions">
Symbol expressions are stricter (v0.32+). Revset symbols no longer resolve to multiple revisions:
```bash
jj log -r abc              # error if 'abc' matches multiple change IDs
jj log -r 'change_id(abc)' # explicit prefix query
jj log -r 'bookmarks(abc)' # for bookmark name patterns
```
</pitfall>

<pitfall name="glob-patterns">
Glob patterns are default in filesets (v0.36+):
```bash
jj diff 'src/*.rs'         # matches glob pattern by default
jj diff 'cwd:"src/*.rs"'   # use cwd: prefix for literal path
```
</pitfall>

<pitfall name="description-glob-brackets">
Don't use glob with `[` brackets in description() - they're character classes:
```bash
jj log -r 'description(glob:"*[task:*]*")'      # WRONG - [task:*] is char class
jj log -r 'description(substring:"[task:")'     # CORRECT
jj log -r 'tasks()'                             # BEST - use alias
```
</pitfall>
</anti_patterns>

<scripts>
Helper scripts:

| Script                        | Purpose                              |
| ----------------------------- | ------------------------------------ |
| `jjtask show-desc [REV]`         | Print full description only          |
| `jjtask desc-transform REV SED`  | Pipe description through command     |
| `jjtask batch-desc SED REVSET`   | Batch transform descriptions         |
| `jjtask checkpoint [NAME]`       | Record op ID before risky operations |
</scripts>

<recovery>

```bash
jj op log              # Find operation before problem
jj op restore <op-id>  # Restore WHOLE repository to that state
```
</recovery>

<reference_guides>
- Run `jj help -k bookmarks` - bookmarks, git branches, push/fetch
- Run `jj help -k revsets` - revset DSL syntax
- Run `jj help -k filesets` - filepath selection DSL
- Run `jj help -k templates` - template language
- All subcommands have detailed `--help`
- `references/command-syntax.md` - command flag details
- `references/batch-operations.md` - batch transformations
</reference_guides>

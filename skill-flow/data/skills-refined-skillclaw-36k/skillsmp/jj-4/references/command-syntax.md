# JJ Command Syntax Reference

## Flag Usage

JJ commands are inconsistent with flag naming. For most commands, use `-r` only:

```bash
jj log -r <revset>        # correct
jj desc -r <revset>       # correct
jj show -r <revset>       # correct
jj rebase -r <revset>     # correct
jj edit -r <revset>       # correct (no --revision)
```

Common mistake:
```bash
jj desc --revisions xyz   # error
jj log --revision xyz     # error
jj desc -r xyz            # correct
```

## Common Short Flags

```bash
-G                        # --no-graph (v0.35+)
-o                        # --onto (replaces -d in v0.36+)
-f / -t                   # --from / --to
```

## Reading Revision Info

```bash
jj log -r <rev> -n1 --no-graph -T description           # description only
jj log -r <rev> -n1 --no-graph -T builtin_log_detailed  # detailed info
jj log -r <rev> -T 'change_id.shortest(4) ++ " " ++ description.first_line()'
```

## Modifying Revisions

```bash
jj desc -r <rev> -m "New description"                    # from string
echo "New description" | jj desc -r <rev> --stdin        # from stdin
jj desc -r <rev> --stdin < /path/to/description.txt      # from file

jj log -r <rev> -n1 --no-graph -T description | \
  sed 's/old/new/' | \
  jj desc -r <rev> --stdin                               # pipeline pattern
```

## Creating Revisions

```bash
jj new <parent> -m "Description"                         # create and edit (moves @)
jj new --no-edit <parent> -m "Description"               # create without editing
jj new --no-edit <parent1> <parent2> -m "Merge point"    # merge with multiple parents
```

## Revset Syntax

Basic:
```bash
@                    # working copy
<change-id>          # specific revision
```

Operators:
```bash
<rev>::<rev>         # range (inclusive)
<rev>..              # all descendants
..<rev>              # all ancestors
::@                  # all ancestors of @
```

Functions:
```bash
description(glob:"pattern")
description(exact:"text")
description(substring:"text")
mine()
```

Combining:
```bash
rev1 | rev2          # union (OR)
rev1 & rev2          # intersection (AND)
```

## Shell Quoting

Revsets often need quoting:
```bash
jj log -r 'description(glob:"[todo]*")'            # single quotes (safest)
```

## Quick Reference

| Task             | Command                                         |
| ---------------- | ----------------------------------------------- |
| View description | `jj log -r <rev> -n1 --no-graph -T description` |
| Set description  | `jj desc -r <rev> -m "text"`                    |
| Set from stdin   | `jj desc -r <rev> --stdin`                      |
| Create (edit)    | `jj new <parent> -m "text"`                     |
| Create (no edit) | `jj new --no-edit <parent> -m "text"`           |
| Range query      | `jj log -r '<from>::<to>'`                      |
| Find pattern     | `jj log -r 'description(glob:"pat*")'`          |

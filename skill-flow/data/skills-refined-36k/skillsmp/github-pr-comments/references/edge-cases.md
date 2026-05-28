# Edge cases to handle

## Missing line numbers

Some threads may have `line: null` (e.g., file-level comments or diffs without stable line mapping). Display file path and link anyway.

## Outdated threads

Threads where `isOutdated === true` may no longer map cleanly to current code. Treat as “verify relevance” rather than “must fix”.

## Multiple comments per thread

A thread can contain several comments. For summaries, it’s usually best to show the **latest** comment body, but keep the thread metadata (`path`, `line`, `diffHunk`).

## Renames / deleted files

`path` may reference a file that no longer exists on the current branch. The summary should still include the link to the comment thread.

## Suggestions blocks

Comments can contain “suggestion” code blocks. Preserve the body as-is (don’t strip markdown).

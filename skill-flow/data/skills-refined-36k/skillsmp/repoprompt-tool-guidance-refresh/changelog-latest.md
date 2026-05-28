Version 1.6.4 (January 23, 2026)

New Features

Git Worktree Support - Compare diffs across worktrees and linked checkouts, with worktree info displayed in git operations (branch names, main checkout references). Use "main" or "trunk" aliases in compare specs for intuitive diff comparisons.
Improvements

Better file creation handling in multi-root workspaces - paths with folder aliases now resolve correctly
Git diff caching is more accurate, detecting file changes better and avoiding stale results
Codex CLI is now prioritized as the recommended chat backend for better cost efficiency
MCP tool connections are now more reliable - tools only become available once fully initialized
Improved tool documentation for better clarity and usability
Fixes

Fixed Codex CLI not being able to use the git tool in some cases
Fixed apply_edits line count reporting - changed line counts now accurately reported
Fixed lingering tools in Context Builder (Claude Code) - tools properly cleaned up after discovery runs
Fixed race condition where MCP clients could receive incomplete tool lists on fast connections

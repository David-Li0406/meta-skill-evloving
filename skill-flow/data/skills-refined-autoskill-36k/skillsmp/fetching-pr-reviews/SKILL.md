---
name: fetching-pr-reviews
description: Fetches GitHub pull request review comments for the current repository and formats them as markdown for LLM consumption. Use when the user asks to fetch or address PR review comments or feedback.
---

# Fetching PR reviews

Fetches PR review comments for the git project from GitHub and formats them as
LLM-friendly markdown.

## Primary usage

Get the last review in GitHub by the current user for an open Pull Request for the current branch in the git repository

```bash
repo-to-md review --author @me
```

The command can be executed anywhere in the repository. There is no need to
change the working directory.

## Prerequisites

If the command fails, please note potential failure cases:

- `gh` CLI must be installed and authenticated
- `repo-to-md` must be run from within a git repository with a configured
  remote

The tool auto-detects the repository from `git remote get-url origin` and the
current user from the authentication used for the `gh` command.

## Alternative usage

The command has many options

- `--author <USERNAME>` to filter the reviews by author
- `--pr-number <PR NUMBER>` to select a specific PR by number
- `--repo <REPOSTITORY>` to select the repository as `owner/repo`
- `--review <INDEX OR ID>` to select a specific review

Examples:

```bash
# select the review for the current branch in the repo chmp/repo-to-md
repo-to-md review --repo chmp/repo-to-md

# selecth the pull request number 6
repo-to-md review --pr 6
```

## Output format

Generates markdown with file sections containing code context and embedded
review comments:

````markdown
## `src/main.rs` - Lines 10-15

```rust
pub fn main() {
// <review user="reviewer">
// Consider using clap for argument parsing
// </review>
    println!("Hello");
}
```
````

Each comment is embedded as `<review user="...">...</review>` XML tags using the
language-specific comment syntax.

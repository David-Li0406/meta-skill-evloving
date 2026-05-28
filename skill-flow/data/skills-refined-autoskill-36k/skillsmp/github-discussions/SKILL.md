---
name: github-discussions
description: manage repository discussions, comments, and community engagement via GraphQL
metadata:
  category: github
---

# GitHub Discussions

## What is it?

This skill enables agents to manage **GitHub Discussions** within a repository. Since discussions are primarily accessible via GraphQL, this skill provides the necessary patterns and templates to create, list, and comment on discussions safely.

## Success Criteria

- Discussion categories are correctly identified by their names and IDs.
- New discussions are posted in the most relevant category.
- Comments and replies are linked to the correct parent discussion or comment ID.
- Search queries are used to find relevant existing discussions before creating new ones.

## Why use it?

- **Community engagement**: Facilitate open conversations outside of issues and PRs
- **GraphQL mastery**: Handles the complexity of GitHub's GraphQL API for discussions
- **Category organization**: Ensures discussions are properly categorized (Q&A, Ideas, Announcements)
- **Context awareness**: Searches existing discussions before creating duplicates
- **Threaded conversations**: Manages replies and comment hierarchies effectively

## When to use this skill

- "List the most recent discussions in this repository."
- "Start a new discussion about the proposed architectural changes."
- "Respond to the user's question in the 'Q&A' category."
- "What are the available discussion categories?"
- "Find discussions related to 'performance' and summarize them."

## What this skill can do

- **Exploration**: List discussions, categories, and comments.
- **Engagement**: Create new discussions, add comments, and reply to existing comments.
- **Organization**: Identify categories to ensure discussions are properly placed.

## What this skill will NOT do

- Manage repository-level settings (use `github-admin`).
- Manage issues or pull requests (use `github-issues` or `github-pr-flow`).
- Perform complex moderation tasks (locking/hiding) unless explicitly requested.

## How to use this skill

1. **Discovery**: Start by listing discussion categories to get the `categoryId` for new posts.
2. **Context**: Use the search or list operations to understand current community activity.
3. **Execution**: Use `gh api graphql` with the provided templates to perform mutations (create/comment).

## Tool usage rules

- **GraphQL Focused**: DISCUSSIONS MUST BE MANAGED VIA `gh api graphql`. There is no native `gh discussion` command.
- **ID Resolution**: Always fetch `repositoryId` and `categoryId` dynamically before creating a discussion.
- **Category Match**: Ensure the category allows new discussions (some may be read-only).
- **Search First**: Before creating new discussions, search for existing ones using the search query to prevent duplicates.
- **Search Syntax**: Format search queries as `repo:owner/name <keywords>` or add filters like `category:Ideas`.
- **Threaded Replies**: Use `replyToId` parameter when responding to specific comments for threaded conversations.
- **Q&A Answers**: Only the discussion author can mark comments as answers in Q&A category discussions.
- **Pagination**: Use `after` cursor with `pageInfo.endCursor` for fetching more than 20-100 results.

## Examples

See [references/examples.md](references/examples.md) for concrete GraphQL and CLI patterns.

## Query Templates

See [references/GRAPHQL_QUERIES.md](references/GRAPHQL_QUERIES.md) for ready-to-use GraphQL snippets.

## References

- [GitHub Discussions GraphQL API](https://docs.github.com/en/graphql/reference/objects#discussion)
- [Search Discussions Syntax](https://docs.github.com/en/search-github/searching-on-github/searching-discussions)
- [GitHub GraphQL API Explorer](https://docs.github.com/en/graphql/overview/explorer)
- [Discussions Mutations Reference](https://docs.github.com/en/graphql/reference/mutations#creatediscussion)

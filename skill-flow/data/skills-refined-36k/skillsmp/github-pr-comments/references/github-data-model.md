# GitHub review threads vs review comments

For this skill, we care about **review threads** (not just individual “review comments”), because threads contain:

- `isResolved`: whether the thread has been marked resolved in the PR UI
- `isOutdated`: whether the thread is attached to an outdated diff

The GitHub REST API endpoints for “review comments” don’t consistently provide the same **thread-level** resolution state.

## Data we fetch (GraphQL)

We query:

- `pullRequest.reviewThreads`
  - `isResolved`, `isOutdated`, `path`, `line`, `originalLine`, `diffHunk`
  - `comments.nodes[]` (author, body, url, createdAt)

See `assets/graphql/pull_request_review_threads.gql`.

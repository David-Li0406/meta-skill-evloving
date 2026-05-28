# Rate limits and pagination

## Pagination strategy

`reviewThreads(first: 100, after: $after)` is paginated using `pageInfo.endCursor`.

The script `scripts/fetch-review-threads.mjs` loops pages until:

- `hasNextPage` is false, or
- `endCursor` is missing, or
- `--max-pages` is reached (safety cap)

## Rate limits

If GitHub API rate limits are hit:

- The scripts should surface the `gh api` error output clearly.
- Re-run after waiting, or authenticate with a token that has higher limits.

# Examples: GitHub Review Cycle

The following example illustrates a common review workflow.

## Submitting a Review

```javascript
// 1. Add Code Comment to Pending Review
add_comment_to_pending_review({
  owner: "org",
  repo: "repo",
  pullNumber: 10,
  path: "src/main.ts",
  line: 25,
  body: "Potential null pointer here.",
});

// 2. Submit the Review
pull_request_review_write({
  owner: "org",
  repo: "repo",
  pullNumber: 10,
  event: "REQUEST_CHANGES",
  body: "Please fix the null pointer issue.",
});
```

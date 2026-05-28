# Examples: GitHub Discussions

The following examples demonstrate how to execute the GraphQL templates using the `gh api graphql` command.

## 1. Discovery

### Get Category IDs

```bash
gh api graphql -f query='
  query($owner: String!, $name: String!) {
    repository(owner: $owner, name: $name) {
      id
      discussionCategories(first: 10) {
        nodes { id name }
      }
    }
  }' -f owner="StaytunedLLP" -f name="dhoom"
```

---

## 2. Engagement

### Create a New Discussion

```bash
# repositoryId and categoryId found from the Discovery query
gh api graphql -f query='
  mutation($repoId: ID!, $catId: ID!, $title: String!, $body: String!) {
    createDiscussion(input: {repositoryId: $repoId, categoryId: $catId, title: $title, body: $body}) {
      discussion { id url }
    }
  }' -f repoId="R_..." -f catId="DIC_..." -f title="New Architecture" -f body="Proposed changes..."
```

### Post a Comment

```bash
gh api graphql -f query='
  mutation($discId: ID!, $body: String!) {
    addDiscussionComment(input: {discussionId: $discId, body: $body}) {
      comment { id url }
    }
  }' -f discId="D_..." -f body="I agree with this approach."
```

---

## 3. Search & Discovery

### Search Discussions by Keyword

```bash
# Search across all discussions in a repository
gh api graphql -f query='
  query($query: String!) {
    search(query: $query, type: DISCUSSION, first: 10) {
      discussionCount
      nodes {
        ... on Discussion {
          id
          number
          title
          url
          category { name }
        }
      }
    }
  }' -f query="repo:OWNER/REPO performance"
```

### Get Discussion with All Comments

```bash
gh api graphql -f query='
  query($owner: String!, $name: String!, $number: Int!) {
    repository(owner: $owner, name: $name) {
      discussion(number: $number) {
        id
        title
        body
        comments(first: 20) {
          totalCount
          nodes {
            id
            body
            author { login }
            replies(first: 10) {
              nodes {
                id
                body
                author { login }
              }
            }
          }
        }
      }
    }
  }' -f owner="OWNER" -f name="REPO" -F number=16
```

### Filter Discussions by Category

```bash
# List only Q&A discussions
gh api graphql -f query='
  query($owner: String!, $name: String!, $categoryId: ID!) {
    repository(owner: $owner, name: $name) {
      discussions(first: 20, categoryId: $categoryId, orderBy: {field: CREATED_AT, direction: DESC}) {
        nodes {
          id
          number
          title
          url
          category { name }
        }
      }
    }
  }' -f owner="OWNER" -f name="REPO" -f categoryId="DIC_..."
```

---

## 4. Advanced Operations

### Reply to a Specific Comment

```bash
# Create threaded reply
gh api graphql -f query='
  mutation($discussionId: ID!, $replyToId: ID!, $body: String!) {
    addDiscussionComment(input: {discussionId: $discussionId, replyToId: $replyToId, body: $body}) {
      comment { id url }
    }
  }' -f discussionId="D_..." -f replyToId="DC_..." -f body="Thanks for the suggestion!"
```

### Mark Answer in Q&A Discussion

```bash
# Only the discussion author can mark answers
gh api graphql -f query='
  mutation($id: ID!) {
    markDiscussionCommentAsAnswer(input: {id: $id}) {
      discussion { id answer { id } }
    }
  }' -f id="DC_..."
```

---

## Tips

- Always use the `-f` flag to pass variables to the query.
- Wrap the query in single quotes to avoid shell expansion issues.
- Use `-F` for numeric variables (e.g., issue/discussion numbers).
- Search query format: `repo:owner/name <keywords>` or add filters like `category:Ideas`.
- Get comment IDs from the discussion details query before marking answers or replying.

## References

- [GitHub Discussions GraphQL API Documentation](https://docs.github.com/en/graphql/reference/objects#discussion)
- [Searching Discussions](https://docs.github.com/en/search-github/searching-on-github/searching-discussions)
- [GitHub CLI GraphQL Reference](https://cli.github.com/manual/gh_api)

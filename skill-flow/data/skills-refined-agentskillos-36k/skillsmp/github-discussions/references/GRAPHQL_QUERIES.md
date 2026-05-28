# GraphQL Templates: GitHub Discussions

Use these templates with `gh api graphql` to manage discussions.

## 1. Discovery

### Fetch Repository and Category IDs

```graphql
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    id
    discussionCategories(first: 10) {
      nodes {
        id
        name
        description
      }
    }
  }
}
```

### List Recent Discussions

```graphql
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    discussions(first: 10, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        id
        number
        title
        body
        category {
          name
        }
      }
    }
  }
}
```

### Search Discussions

```graphql
query($query: String!) {
  search(query: $query, type: DISCUSSION, first: 10) {
    discussionCount
    nodes {
      ... on Discussion {
        id
        number
        title
        body
        url
        createdAt
        updatedAt
        author {
          login
        }
        category {
          name
        }
        upvoteCount
        comments {
          totalCount
        }
      }
    }
  }
}
```

### Get Discussion with Comments

```graphql
query($owner: String!, $name: String!, $number: Int!) {
  repository(owner: $owner, name: $name) {
    discussion(number: $number) {
      id
      number
      title
      body
      url
      createdAt
      updatedAt
      author {
        login
      }
      category {
        name
      }
      upvoteCount
      comments(first: 20) {
        totalCount
        nodes {
          id
          body
          createdAt
          author {
            login
          }
          url
          replies(first: 10) {
            totalCount
            nodes {
              id
              body
              author {
                login
              }
              createdAt
            }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
}
```

### Filter Discussions by Category

```graphql
query($owner: String!, $name: String!, $categoryId: ID!) {
  repository(owner: $owner, name: $name) {
    discussions(first: 20, categoryId: $categoryId, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        id
        number
        title
        body
        createdAt
        updatedAt
        url
        author {
          login
        }
        category {
          name
        }
        comments {
          totalCount
        }
        upvoteCount
      }
    }
  }
}
```

---

## 2. Mutations (Engagement)

### Create a Discussion

```graphql
mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
  createDiscussion(input: {repositoryId: $repositoryId, categoryId: $categoryId, title: $title, body: $body}) {
    discussion {
      id
      url
    }
  }
}
```

### Add a Comment to a Discussion

```graphql
mutation($discussionId: ID!, $body: String!) {
  addDiscussionComment(input: {discussionId: $discussionId, body: $body}) {
    comment {
      id
      url
    }
  }
}
```

### Reply to a Comment

```graphql
mutation($discussionId: ID!, $replyToId: ID!, $body: String!) {
  addDiscussionComment(input: {discussionId: $discussionId, replyToId: $replyToId, body: $body}) {
    comment {
      id
      url
    }
  }
}
```

### Mark Comment as Answer (Q&A)

```graphql
mutation($id: ID!) {
  markDiscussionCommentAsAnswer(input: {id: $id}) {
    discussion {
      id
      answer {
        id
        body
        author {
          login
        }
      }
    }
  }
}
```

### Upvote Discussion

```graphql
mutation($id: ID!) {
  addUpvote(input: {subjectId: $id}) {
    subject {
      id
    }
  }
}
```

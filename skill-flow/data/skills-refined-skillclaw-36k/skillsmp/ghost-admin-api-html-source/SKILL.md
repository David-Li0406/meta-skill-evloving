---
name: ghost-admin-api-html-source
description: |
  Fix for Ghost Admin API posts created with empty content when using HTML. Use when:
  (1) Ghost posts are created successfully but have no body content, (2) HTML field is
  sent in POST request but post appears empty, (3) title appears but html/body is blank,
  (4) implementing Ghost Admin API integration with HTML content. The fix is to use
  source=html as a QUERY PARAMETER, not in the JSON request body.
author: Claude Code
version: 1.0.0
date: 2026-01-21
---

# Ghost Admin API HTML Source Parameter

## Problem

When creating posts via the Ghost Admin API with HTML content, posts are created
successfully (201 response, post ID returned) but the HTML content is empty. Only
the title appears in the Ghost editor.

## Context / Trigger Conditions

- POST to `/ghost/api/admin/posts/` returns 201 success
- Post is created with correct title
- HTML content in response/editor is empty (0 chars)
- You're sending `html` field in the JSON body
- You may have tried adding `source: "html"` to the JSON body (this doesn't work)

## Root Cause

Ghost's Admin API requires `source=html` as a **query parameter**, not in the JSON
request body. The Ghost JavaScript SDK handles this automatically, but raw HTTP
implementations need to add it manually.

The JS SDK call:
```javascript
api.posts.add({ title, html }, { source: "html" })
```

Translates to the raw API as:
```
POST /ghost/api/admin/posts/?source=html
```

## Solution

### Correct Approach (Query Parameter)

```
POST /ghost/api/admin/posts/?source=html
Content-Type: application/json
Authorization: Ghost {jwt_token}

{
  "posts": [{
    "title": "My Post",
    "html": "<h2>Content here</h2><p>This will work!</p>",
    "status": "draft"
  }]
}
```

### Incorrect Approach (Body Parameter - Does NOT Work)

```
POST /ghost/api/admin/posts/
Content-Type: application/json

{
  "posts": [{ "title": "My Post", "html": "<p>Content</p>" }],
  "source": "html"  // <-- This is IGNORED!
}
```

### Implementation Examples

**Python (requests)**:
```python
url = f"{ghost_url}/ghost/api/admin/posts/?source=html"
response = requests.post(url, json={"posts": [post_data]}, headers=headers)
```

**Rust (reqwest)**:
```rust
let url = format!("{}/ghost/api/admin/posts/?source=html", base_url);
client.post(&url).json(&request_body).send().await?;
```

**For updates (PUT)**, also use the query parameter:
```
PUT /ghost/api/admin/posts/{id}/?source=html
```

## Verification

After creating a post, fetch it back and check the HTML length:

```python
get_url = f"{ghost_url}/ghost/api/admin/posts/{post_id}/?formats=html"
response = requests.get(get_url, headers=headers)
html = response.json()["posts"][0].get("html", "")
print(f"HTML length: {len(html)}")  # Should be > 0
```

## Example

Before fix:
```
Created post: 6970a142...
HTML length: 0  # Empty!
```

After fix:
```
Created post: 6970a3f0...
HTML length: 938  # Content preserved!
```

## Notes

- This applies to both POST (create) and PUT (update) operations
- The `formats=html` query parameter on GET requests is separate - that's for
  specifying the return format
- Ghost internally converts HTML to its mobiledoc/lexical format for storage
- The conversion is "lossy" - some HTML elements may not be preserved exactly
- For complex HTML, consider using mobiledoc format directly

## References

- [Ghost Admin API Overview](https://docs.ghost.org/admin-api)
- [TryGhost/api-demos - write-posts.js](https://github.com/TryGhost/api-demos)
- [Ghost Forum: Cannot post html](https://forum.ghost.org/t/cannot-post-html/56536)
- [Ghost Forum: How to Create a Post via API](https://forum.ghost.org/t/how-to-create-a-post-via-api-url-parameters-and-requirements/49501)

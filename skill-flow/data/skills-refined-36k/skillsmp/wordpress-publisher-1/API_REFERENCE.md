# WordPress REST API Reference

## Authentication

### Application Passwords (empfohlen)

```typescript
// 1. App Password in WP generieren:
// Users → Your Profile → Application Passwords

// 2. Basic Auth verwenden:
const credentials = `${username}:${appPassword}`;
const auth = Buffer.from(credentials).toString('base64');

const headers = {
  'Authorization': `Basic ${auth}`,
  'Content-Type': 'application/json'
};
```

### JWT Authentication (Alternative)

```typescript
// 1. JWT Plugin installieren
// 2. Token abrufen
const token = await fetch(`${WP_URL}/wp-json/jwt-auth/v1/token`, {
  method: 'POST',
  body: JSON.stringify({ username, password })
});

// 3. Token verwenden
const headers = {
  'Authorization': `Bearer ${token.token}`
};
```

---

## Posts API

### Create Post

```http
POST /wp-json/wp/v2/posts
```

```typescript
const createPost = async (postData: PostData) => {
  const response = await fetch(`${WP_URL}/wp-json/wp/v2/posts`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      title: postData.title,
      content: postData.content,
      excerpt: postData.excerpt,
      status: 'draft', // draft, publish, pending, future
      slug: postData.slug,
      categories: [1, 5],
      tags: [10, 15],
      featured_media: postData.featuredImageId,
      meta: postData.meta,
      acf: postData.acf
    })
  });

  return response.json();
};
```

### Update Post

```http
PUT /wp-json/wp/v2/posts/{id}
```

```typescript
const updatePost = async (postId: number, updates: Partial<PostData>) => {
  const response = await fetch(`${WP_URL}/wp-json/wp/v2/posts/${postId}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(updates)
  });

  return response.json();
};
```

### Get Post

```http
GET /wp-json/wp/v2/posts/{id}
```

```typescript
const getPost = async (postId: number) => {
  const response = await fetch(
    `${WP_URL}/wp-json/wp/v2/posts/${postId}?_embed`,
    { headers }
  );

  return response.json();
};
```

### List Posts

```http
GET /wp-json/wp/v2/posts
```

```typescript
const listPosts = async (params: ListParams) => {
  const queryString = new URLSearchParams({
    per_page: params.perPage?.toString() || '10',
    page: params.page?.toString() || '1',
    status: params.status || 'publish',
    categories: params.categories?.join(',') || '',
    search: params.search || '',
    orderby: params.orderby || 'date',
    order: params.order || 'desc'
  });

  const response = await fetch(
    `${WP_URL}/wp-json/wp/v2/posts?${queryString}`,
    { headers }
  );

  return {
    posts: await response.json(),
    total: parseInt(response.headers.get('X-WP-Total') || '0'),
    totalPages: parseInt(response.headers.get('X-WP-TotalPages') || '0')
  };
};
```

### Delete Post

```http
DELETE /wp-json/wp/v2/posts/{id}
```

```typescript
const deletePost = async (postId: number, force = false) => {
  const response = await fetch(
    `${WP_URL}/wp-json/wp/v2/posts/${postId}?force=${force}`,
    {
      method: 'DELETE',
      headers
    }
  );

  return response.json();
};
```

---

## Media API

### Upload Media

```http
POST /wp-json/wp/v2/media
```

```typescript
const uploadMedia = async (file: Buffer, filename: string, mimeType: string) => {
  const response = await fetch(`${WP_URL}/wp-json/wp/v2/media`, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${auth}`,
      'Content-Type': mimeType,
      'Content-Disposition': `attachment; filename="${filename}"`
    },
    body: file
  });

  return response.json();
  // Returns: { id: 123, source_url: "https://...", alt_text: "", ... }
};
```

### Upload from URL

```typescript
const uploadFromUrl = async (imageUrl: string, filename: string) => {
  // 1. Download image
  const imageResponse = await fetch(imageUrl);
  const imageBuffer = await imageResponse.buffer();
  const mimeType = imageResponse.headers.get('content-type') || 'image/jpeg';

  // 2. Upload to WordPress
  return uploadMedia(imageBuffer, filename, mimeType);
};
```

### Update Media (Alt Text, Caption)

```http
PUT /wp-json/wp/v2/media/{id}
```

```typescript
const updateMedia = async (mediaId: number, updates: MediaUpdate) => {
  const response = await fetch(`${WP_URL}/wp-json/wp/v2/media/${mediaId}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify({
      alt_text: updates.altText,
      caption: updates.caption,
      description: updates.description
    })
  });

  return response.json();
};
```

---

## Categories API

### Get Categories

```http
GET /wp-json/wp/v2/categories
```

```typescript
const getCategories = async () => {
  const response = await fetch(
    `${WP_URL}/wp-json/wp/v2/categories?per_page=100`,
    { headers }
  );

  return response.json();
};
```

### Create Category

```http
POST /wp-json/wp/v2/categories
```

```typescript
const createCategory = async (name: string, slug?: string, parent?: number) => {
  const response = await fetch(`${WP_URL}/wp-json/wp/v2/categories`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      name,
      slug: slug || name.toLowerCase().replace(/\s+/g, '-'),
      parent: parent || 0
    })
  });

  return response.json();
};
```

### Find or Create Category

```typescript
const findOrCreateCategory = async (name: string) => {
  // 1. Suchen
  const searchResponse = await fetch(
    `${WP_URL}/wp-json/wp/v2/categories?search=${encodeURIComponent(name)}`,
    { headers }
  );
  const existing = await searchResponse.json();

  if (existing.length > 0) {
    return existing[0];
  }

  // 2. Erstellen falls nicht vorhanden
  return createCategory(name);
};
```

---

## Tags API

### Get Tags

```http
GET /wp-json/wp/v2/tags
```

```typescript
const getTags = async (search?: string) => {
  const query = search ? `?search=${encodeURIComponent(search)}` : '';
  const response = await fetch(
    `${WP_URL}/wp-json/wp/v2/tags${query}`,
    { headers }
  );

  return response.json();
};
```

### Create Tag

```http
POST /wp-json/wp/v2/tags
```

```typescript
const createTag = async (name: string) => {
  const response = await fetch(`${WP_URL}/wp-json/wp/v2/tags`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      name,
      slug: name.toLowerCase().replace(/\s+/g, '-')
    })
  });

  return response.json();
};
```

---

## Users API

### Get Current User

```http
GET /wp-json/wp/v2/users/me
```

```typescript
const getCurrentUser = async () => {
  const response = await fetch(
    `${WP_URL}/wp-json/wp/v2/users/me`,
    { headers }
  );

  return response.json();
};
```

### Get User by ID

```http
GET /wp-json/wp/v2/users/{id}
```

```typescript
const getUser = async (userId: number) => {
  const response = await fetch(
    `${WP_URL}/wp-json/wp/v2/users/${userId}`,
    { headers }
  );

  return response.json();
};
```

---

## Custom Post Types

### Get Custom Post Type

```http
GET /wp-json/wp/v2/{post_type}
```

```typescript
// Beispiel: Custom Post Type "portfolio"
const getPortfolioItems = async () => {
  const response = await fetch(
    `${WP_URL}/wp-json/wp/v2/portfolio`,
    { headers }
  );

  return response.json();
};
```

### Create Custom Post

```typescript
const createCustomPost = async (postType: string, data: any) => {
  const response = await fetch(`${WP_URL}/wp-json/wp/v2/${postType}`, {
    method: 'POST',
    headers,
    body: JSON.stringify(data)
  });

  return response.json();
};
```

---

## ACF Fields

### Voraussetzung

ACF REST API muss aktiviert sein:
1. ACF → Settings → Tools
2. "Include ACF fields in REST API responses" aktivieren

### Fields in Post lesen

```typescript
const getPostWithAcf = async (postId: number) => {
  const response = await fetch(
    `${WP_URL}/wp-json/wp/v2/posts/${postId}?_fields=id,title,acf`,
    { headers }
  );

  const post = await response.json();
  return post.acf; // { custom_field_1: "value", ... }
};
```

### Fields in Post schreiben

```typescript
const updateAcfFields = async (postId: number, fields: Record<string, any>) => {
  const response = await fetch(`${WP_URL}/wp-json/wp/v2/posts/${postId}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify({
      acf: fields
    })
  });

  return response.json();
};
```

---

## Error Codes

| HTTP Code | WP Code | Bedeutung |
|-----------|---------|-----------|
| 400 | rest_invalid_param | Ungültiger Parameter |
| 401 | rest_not_logged_in | Nicht authentifiziert |
| 403 | rest_forbidden | Keine Berechtigung |
| 404 | rest_post_invalid_id | Post nicht gefunden |
| 409 | rest_cannot_create | Konflikt beim Erstellen |
| 500 | rest_error | Server-Fehler |

### Error Response Format

```json
{
  "code": "rest_invalid_param",
  "message": "Invalid parameter(s): status",
  "data": {
    "status": 400,
    "params": {
      "status": "status is not one of publish, draft, pending, private."
    }
  }
}
```

---

## Rate Limiting

### Best Practices

```typescript
// Rate Limiter implementieren
const rateLimiter = {
  requests: 0,
  resetTime: Date.now() + 60000,
  limit: 100, // 100 requests per minute

  async throttle() {
    if (Date.now() > this.resetTime) {
      this.requests = 0;
      this.resetTime = Date.now() + 60000;
    }

    if (this.requests >= this.limit) {
      const waitTime = this.resetTime - Date.now();
      await new Promise(resolve => setTimeout(resolve, waitTime));
      this.requests = 0;
    }

    this.requests++;
  }
};

// Verwendung
await rateLimiter.throttle();
await createPost(data);
```

### Batch Operations

```typescript
// Bulk-Updates mit Verzögerung
const bulkUpdate = async (posts: PostUpdate[]) => {
  const results = [];

  for (const post of posts) {
    await rateLimiter.throttle();
    const result = await updatePost(post.id, post.data);
    results.push(result);

    // Zusätzliche Verzögerung
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  return results;
};
```

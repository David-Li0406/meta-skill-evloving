# Ghost Admin API Reference

## Base Configuration

**Base URL:** `https://{admin_domain}/ghost/api/admin/`

**Required Headers:**
- `Accept-Version: v6.0` (or appropriate version)
- `Authorization: Ghost {jwt_token}`
- `Content-Type: application/json` (for POST/PUT requests)

## Authentication

### Integration Token Generation
Admin API key format: `{id}:{secret}`

**JWT Token Requirements:**
- Algorithm: HS256
- Header: `{"alg": "HS256", "typ": "JWT", "kid": "{id}"}`
- Payload: `{"iat": {timestamp}, "exp": {timestamp+300}, "aud": "/admin/"}`
- Sign with hex-decoded secret

**Curl Authentication Example:**
```bash
curl -H "Authorization: Ghost $TOKEN" \
     -H "Accept-Version: v6.0" \
     -H "Content-Type: application/json" \
     https://example.com/ghost/api/admin/posts/
```

## REST Endpoints

### Posts `/admin/posts/`

**Browse Posts**
```bash
GET /admin/posts/
GET /admin/posts/?include=tags,authors&limit=5&page=1
GET /admin/posts/?filter=status:published&order=published_at%20desc
```

**Read Post**
```bash
GET /admin/posts/{id}/
GET /admin/posts/slug/{slug}/
```

**Create Post**
```bash
POST /admin/posts/
Content-Type: application/json

{
    "posts": [{
        "title": "Post Title",
        "lexical": "{\"root\":{\"children\":[...]}}",
        "status": "draft|published|scheduled",
        "tags": ["tag1", "tag2"],
        "authors": ["author@example.com"],
        "featured": false,
        "visibility": "public|members|paid"
    }]
}
```

**Create from HTML**
```bash
POST /admin/posts/?source=html
{
    "posts": [{
        "title": "HTML Post",
        "html": "<p>Content here</p>",
        "status": "published"
    }]
}
```

**Update Post**
```bash
PUT /admin/posts/{id}/
{
    "posts": [{
        "title": "Updated Title",
        "updated_at": "2023-06-05T20:52:37.000Z"
    }]
}
```

**Publish Post**
```bash
PUT /admin/posts/{id}/
{
    "posts": [{
        "status": "published",
        "updated_at": "2023-06-05T20:52:37.000Z"
    }]
}
```

**Schedule Post**
```bash
PUT /admin/posts/{id}/
{
    "posts": [{
        "status": "scheduled",
        "published_at": "2024-12-25T09:00:00.000Z",
        "updated_at": "2023-06-05T20:52:37.000Z"
    }]
}
```

**Send Post via Email**
```bash
PUT /admin/posts/{id}/?newsletter={newsletter_slug}&email_segment=status:free
{
    "posts": [{
        "status": "published",
        "updated_at": "2023-06-05T20:52:37.000Z"
    }]
}
```

**Email-Only Post**
```bash
PUT /admin/posts/{id}/?newsletter={newsletter_slug}
{
    "posts": [{
        "status": "published",
        "email_only": true,
        "updated_at": "2023-06-05T20:52:37.000Z"
    }]
}
```

**Copy Post**
```bash
POST /admin/posts/{id}/copy/
```

**Delete Post**
```bash
DELETE /admin/posts/{id}/
```

### Pages `/admin/pages/`

**Browse Pages**
```bash
GET /admin/pages/
GET /admin/pages/?include=tags,authors&limit=15
```

**Read Page**
```bash
GET /admin/pages/{id}/
GET /admin/pages/slug/{slug}/
```

**Create Page**
```bash
POST /admin/pages/
{
    "pages": [{
        "title": "Page Title",
        "lexical": "{\"root\":{\"children\":[...]}}",
        "status": "published"
    }]
}
```

**Update Page**
```bash
PUT /admin/pages/{id}/
{
    "pages": [{
        "title": "Updated Page Title",
        "updated_at": "2023-06-05T20:52:37.000Z"
    }]
}
```

**Copy Page**
```bash
POST /admin/pages/{id}/copy/
```

**Delete Page**
```bash
DELETE /admin/pages/{id}/
```

### Members `/admin/members/`

**Browse Members**
```bash
GET /admin/members/
GET /admin/members/?include=newsletters,labels&limit=50
GET /admin/members/?filter=status:paid
```

**Read Member**
```bash
GET /admin/members/{id}/
```

**Create Member**
```bash
POST /admin/members/
{
    "members": [{
        "email": "member@example.com",
        "name": "Member Name",
        "note": "Member notes",
        "labels": [{"name": "VIP", "slug": "vip"}],
        "newsletters": [{"id": "newsletter_id"}]
    }]
}
```

**Update Member**
```bash
PUT /admin/members/{id}/
{
    "members": [{
        "name": "Updated Name",
        "note": "Updated notes"
    }]
}
```

### Tags `/admin/tags/`

**Browse Tags**
```bash
GET /admin/tags/
GET /admin/tags/?limit=all
```

**Read Tag**
```bash
GET /admin/tags/{id}/
GET /admin/tags/slug/{slug}/
```

**Create Tag**
```bash
POST /admin/tags/
{
    "tags": [{
        "name": "New Tag",
        "slug": "new-tag",
        "description": "Tag description"
    }]
}
```

**Update Tag**
```bash
PUT /admin/tags/{id}/
{
    "tags": [{
        "name": "Updated Tag Name",
        "description": "Updated description"
    }]
}
```

**Delete Tag**
```bash
DELETE /admin/tags/{id}/
```

### Tiers `/admin/tiers/`

**Browse Tiers**
```bash
GET /admin/tiers/
GET /admin/tiers/?include=monthly_price,yearly_price,benefits
```

**Read Tier**
```bash
GET /admin/tiers/{id}/
```

**Create Tier**
```bash
POST /admin/tiers/
{
    "tiers": [{
        "name": "Premium Tier",
        "description": "Access to premium content",
        "monthly_price": 1000,
        "yearly_price": 10000,
        "currency": "usd",
        "benefits": ["Benefit 1", "Benefit 2"],
        "visibility": "public"
    }]
}
```

**Update Tier**
```bash
PUT /admin/tiers/{id}/
{
    "tiers": [{
        "name": "Updated Tier Name",
        "description": "Updated description"
    }]
}
```

### Newsletters `/admin/newsletters/`

**Browse Newsletters**
```bash
GET /admin/newsletters/
```

**Read Newsletter**
```bash
GET /admin/newsletters/{id}/
```

**Create Newsletter**
```bash
POST /admin/newsletters/?opt_in_existing=true
{
    "newsletters": [{
        "name": "Weekly Newsletter",
        "description": "Weekly updates",
        "status": "active",
        "subscribe_on_signup": true,
        "sender_reply_to": "newsletter"
    }]
}
```

**Update Newsletter**
```bash
PUT /admin/newsletters/{id}/
{
    "newsletters": [{
        "name": "Updated Newsletter Name",
        "description": "Updated description"
    }]
}
```

### Offers `/admin/offers/`

**Browse Offers**
```bash
GET /admin/offers/
```

**Read Offer**
```bash
GET /admin/offers/{id}/
```

**Create Offer**
```bash
POST /admin/offers/
{
    "offers": [{
        "name": "Black Friday",
        "code": "blackfriday2024",
        "display_title": "Black Friday Sale",
        "display_description": "20% off yearly subscription",
        "type": "percent",
        "cadence": "year",
        "amount": 20,
        "duration": "once",
        "status": "active",
        "tier": {"id": "tier_id"}
    }]
}
```

**Update Offer**
```bash
PUT /admin/offers/{id}/
{
    "offers": [{
        "display_title": "Updated Sale Title",
        "display_description": "Updated description"
    }]
}
```

### Users `/admin/users/`

**Browse Users**
```bash
GET /admin/users/
GET /admin/users/?include=count.posts,permissions,roles
```

**Read User**
```bash
GET /admin/users/{id}/
```

**Update User**
```bash
PUT /admin/users/{id}/
{
    "users": [{
        "name": "Updated Name",
        "bio": "Updated bio"
    }]
}
```

**Delete User**
```bash
DELETE /admin/users/{id}/
```

### Roles `/admin/roles/`

**Browse Roles**
```bash
GET /admin/roles/
```

### Invites `/admin/invites/`

**Create Invite**
```bash
POST /admin/invites/
{
    "invites": [{
        "role_id": "role_id",
        "email": "newuser@example.com"
    }]
}
```

### Images `/admin/images/upload/`

**Upload Image**
```bash
POST /admin/images/upload/
Content-Type: multipart/form-data

curl -X POST \
  -F 'file=@/path/to/image.jpg' \
  -F 'purpose=image' \
  -F 'ref=original-filename.jpg' \
  -H "Authorization: Ghost $TOKEN" \
  -H "Accept-Version: v6.0" \
  https://example.com/ghost/api/admin/images/upload/
```

### Themes `/admin/themes/`

**Upload Theme**
```bash
POST /admin/themes/upload/
Content-Type: multipart/form-data

curl -X POST \
  -F 'file=@/path/to/theme.zip' \
  -H "Authorization: Ghost $TOKEN" \
  -H "Accept-Version: v6.0" \
  https://example.com/ghost/api/admin/themes/upload/
```

**Activate Theme**
```bash
PUT /admin/themes/{theme_name}/activate/
```

### Webhooks `/admin/webhooks/`

**Create Webhook**
```bash
POST /admin/webhooks/
{
    "webhooks": [{
        "event": "post.published",
        "target_url": "https://example.com/webhook",
        "name": "Post Published Hook",
        "secret": "webhook_secret"
    }]
}
```

**Update Webhook**
```bash
PUT /admin/webhooks/{id}/
{
    "webhooks": [{
        "event": "post.published.edited",
        "name": "Updated Webhook Name"
    }]
}
```

**Delete Webhook**
```bash
DELETE /admin/webhooks/{id}/
```

### Site `/admin/site/`

**Read Site Info**
```bash
GET /admin/site/
```

## Query Parameters

### Common Parameters
- `include`: Include related data (e.g., `tags,authors,tiers`)
- `fields`: Select specific fields (e.g., `title,slug,published_at`)
- `filter`: NQL filter (e.g., `status:published+featured:true`)
- `limit`: Number of results (default: 15, max: 50, use `all` for no limit)
- `page`: Page number (default: 1)
- `order`: Sort order (e.g., `published_at desc`, `title asc`)
- `formats`: Content formats to include (e.g., `html,lexical`)

### Filtering Examples
- `status:published` - Published posts only
- `status:draft` - Draft posts only
- `featured:true` - Featured posts only
- `tag:getting-started` - Posts with specific tag
- `author:john` - Posts by specific author
- `visibility:public` - Public posts only
- `published_at:>'2023-01-01'` - Posts published after date

## Response Format

All responses follow this structure:
```json
{
    "resource_type": [
        {
            "id": "resource_id",
            // ... resource fields
        }
    ],
    "meta": {
        "pagination": {
            "page": 1,
            "limit": 15,
            "pages": 10,
            "total": 150,
            "next": 2,
            "prev": null
        }
    }
}
```

## Error Handling

**HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `204` - No Content (successful delete)
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error

**Error Response Format:**
```json
{
    "errors": [{
        "type": "ValidationError",
        "message": "Error description",
        "property": "field_name"
    }]
}
```

## Content Formats

### Lexical JSON Structure
```json
{
    "root": {
        "children": [
            {
                "children": [
                    {
                        "detail": 0,
                        "format": 0,
                        "mode": "normal",
                        "style": "",
                        "text": "Hello world!",
                        "type": "extended-text",
                        "version": 1
                    }
                ],
                "direction": "ltr",
                "format": "",
                "indent": 0,
                "type": "paragraph",
                "version": 1
            }
        ],
        "direction": "ltr",
        "format": "",
        "indent": 0,
        "type": "root",
        "version": 1
    }
}
```

### HTML Card Wrapper (for lossless HTML)
```html
<!--kg-card-begin: html-->
<p>Your HTML content here</p>
<!--kg-card-end: html-->
```

## Important Notes

1. **Integration Token Security:** 
   - JWT tokens expire after 5 minutes maximum - generate fresh tokens for each request
   - Never expose integration keys in client-side code
   - Store API keys securely in environment variables

2. **Content Updates:** 
   - Always include `updated_at` field when updating resources
   - Get latest `updated_at` value before updates to prevent conflicts
   - Tags and authors are replaced, not merged in updates

3. **Content Format Priority:**
   - Use Lexical format for full Ghost editor feature support
   - HTML source is converted to Lexical (lossy conversion)
   - Use HTML card wrapper `<!--kg-card-begin: html-->` for exact HTML preservation

4. **Email Requirements:** 
   - Requires active newsletter for email sending
   - Use newsletter slug in query parameter: `?newsletter=newsletter-slug`
   - Email segments: `all`, `status:free`, `status:-free`, or custom NQL

5. **File Uploads:** 
   - Use `multipart/form-data` content type for images/themes
   - Supported image formats: WEBP, JPEG, GIF, PNG, SVG
   - Maximum file size limits apply (check your Ghost configuration)

6. **API Versioning:**
   - Always specify `Accept-Version` header
   - Current stable version: `v6.0`
   - API behavior may change between versions

7. **Error Handling:**
   - Check HTTP status codes: 200/201 success, 4xx client errors, 5xx server errors
   - Parse JSON error responses for detailed error information
   - Retry with fresh JWT token on 401 Unauthorized errors

8. **Rate Limiting:**
   - Respect any rate limits imposed by your Ghost installation
   - Implement exponential backoff for retries
   - Monitor response headers for rate limit information

9. **Testing:**
   - Test with draft posts first before publishing
   - Use a development Ghost instance for experimentation
   - Verify content formatting before bulk operations

10. **Common Gotchas:**
    - URL encode query parameters properly
    - Ensure JWT timestamps are in seconds, not milliseconds  
    - Check that your Ghost admin domain is correct (may differ from public domain)
    - Verify integration has necessary permissions for the operations you're attempting
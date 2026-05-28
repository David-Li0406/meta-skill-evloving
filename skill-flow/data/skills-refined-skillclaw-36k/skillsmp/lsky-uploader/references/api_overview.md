# Lsky Pro API overview (self-hosted instance)

Source: <https://v1.lskypro.com/page/api-docs.html>. Your deployment lives at `https://lsky.xueguo.us/api/v1`.

## Auth

- Create a personal token in the Lsky dashboard (user profile -> token management). The raw value looks like `1|1bJbwlqBfngg...`.
- Headers required for every call:
  - `Authorization: Bearer <token>`
  - `Accept: application/json`
- Without the header, uploads fall back to "guest" mode and cannot access private strategies/albums.

## Upload (`POST /upload`)

```
POST https://lsky.xueguo.us/api/v1/upload
Headers:
  Authorization: Bearer <token>
  Accept: application/json
Body (multipart/form-data):
  file          required binary blob
  name          optional display name
  album_id      optional album ID
  strategy_id   optional storage strategy ID (defaults to your profile setting)
  permission    optional, 0=public 1=private
```

Response sample:

```json
{
  "status": true,
  "message": "success",
  "data": {
    "links": {
      "url": "https://cdn.example.com/i/2024/01/01/abc.png",
      "markdown": "![img](https://...)",
      "delete_url": "https://lsky.../delete/xxx"
    },
    "origin_name": "demo.png",
    "size": 12345,
    "mime": "image/png"
  }
}
```

## Listing endpoints

| Endpoint | Purpose | Common params |
| --- | --- | --- |
| `GET /images` | Paginate current user images | `page`, `limit`, `album_id`, `order=latest,size,name` |
| `GET /albums` | List albums | none |
| `GET /strategies` | List storage strategies/drivers | none |

Each list returns `status`, `message`, and a `data` object containing `total` and `data[]`.

## Delete helpers

- Images: `DELETE /images/:id`
- Albums: `DELETE /albums/:id`

IDs come from the list endpoints or the upload response (`data.image.id`). Headers are identical to upload.

## Error codes

- `401` not logged in / invalid token
- `403` API disabled by the admin
- `429` rate limit exceeded
- `500` server error

The body includes `status=false` and a `message` string for details.

## Rate limiting

Every response includes:

- `X-RateLimit-Limit`: quota per minute
- `X-RateLimit-Remaining`: unused quota in the current minute

When Remaining reaches zero, stop calling for ~60 seconds; otherwise `/upload` will respond with HTTP 429.

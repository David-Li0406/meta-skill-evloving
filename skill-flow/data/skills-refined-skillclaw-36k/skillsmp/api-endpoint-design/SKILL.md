---
name: api-endpoint-design
description: REST API design standards for FanHub's Express backend. Use when creating or modifying API endpoints to ensure consistency.
---

# FanHub API Design Standards

## URL Conventions

- Use lowercase, hyphenated paths: `/api/tv-shows`, not `/api/tvShows`
- Use plural nouns for collections: `/api/characters`, not `/api/character`
- Use nested routes for relationships: `/api/shows/:showId/episodes`
- Version the API: `/api/v1/...`

## HTTP Methods

| Method | Use Case | Example |
|--------|----------|---------|
| GET | Retrieve resource(s) | GET /api/characters |
| POST | Create new resource | POST /api/characters |
| PUT | Replace entire resource | PUT /api/characters/:id |
| PATCH | Partial update | PATCH /api/characters/:id |
| DELETE | Remove resource | DELETE /api/characters/:id |

## Response Format

All responses follow this structure:

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20
  }
}
```

Error responses:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Character name is required",
    "details": [...]
  }
}
```

## Status Codes

- 200: Success (GET, PUT, PATCH)
- 201: Created (POST)
- 204: No Content (DELETE)
- 400: Bad Request (validation errors)
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

## Endpoint Template

```javascript
router.get('/characters', async (req, res, next) => {
  try {
    const { page = 1, limit = 20, show_id } = req.query;
    
    const characters = await CharacterService.list({
      page: parseInt(page),
      limit: parseInt(limit),
      showId: show_id ? parseInt(show_id) : undefined
    });
    
    res.json({
      success: true,
      data: characters.items,
      meta: {
        total: characters.total,
        page: characters.page,
        limit: characters.limit
      }
    });
  } catch (error) {
    next(error);
  }
});
```

---
name: local-places
description: Use this skill to search for nearby places (restaurants, cafes, etc.) via a local Google Places API proxy.
---

# 📍 Local Places

*Find places, Go fast*

Search for nearby places using a local Google Places API proxy. The workflow consists of resolving a location first, followed by searching for places.

## Setup

```bash
cd {baseDir}
echo "GOOGLE_PLACES_API_KEY=your-key" > .env
uv venv && uv pip install -e ".[dev]"
uv run --env-file .env uvicorn local_places.main:app --host 127.0.0.1 --port 8000
```

Requires `GOOGLE_PLACES_API_KEY` in `.env` or environment.

## Quick Start

1. **Check server:** `curl http://127.0.0.1:8000/ping`

2. **Resolve location:**
```bash
curl -X POST http://127.0.0.1:8000/locations/resolve \
  -H "Content-Type: application/json" \
  -d '{"location_text": "<location_text>", "limit": 5}'
```

3. **Search places:**
```bash
curl -X POST http://127.0.0.1:8000/places/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "<search_query>",
    "location_bias": {"lat": <latitude>, "lng": <longitude>, "radius_m": <radius>},
    "filters": {"open_now": <boolean>, "min_rating": <min_rating>},
    "limit": <limit>
  }'
```

4. **Get details:**
```bash
curl http://127.0.0.1:8000/places/{place_id}
```

## Conversation Flow

1. If the user says "near me" or provides a vague location, resolve it first.
2. If multiple results are found, show a numbered list and ask the user to pick.
3. Ask for preferences: type, open now, rating, price level.
4. Search using `location_bias` from the chosen location.
5. Present results with name, rating, address, and open status.
6. Offer to fetch details or refine the search.

## Filter Constraints

- `filters.types`: exactly ONE type (e.g., "restaurant", "cafe", "gym").
- `filters.price_levels`: integers 0-4 (0=free, 4=very expensive).
- `filters.min_rating`: 0-5 in 0.5 increments.
- `filters.open_now`: boolean.
- `limit`: 1-20 for search, 1-10 for resolve.
- `location_bias.radius_m`: must be > 0.

## Response Format

```json
{
  "results": [
    {
      "place_id": "ChIJ...",
      "name": "<place_name>",
      "address": "<place_address>",
      "location": {"lat": <latitude>, "lng": <longitude>},
      "rating": <rating>,
      "price_level": <price_level>,
      "types": ["<type1>", "<type2>"],
      "open_now": <boolean>
    }
  ],
  "next_page_token": "..."
}
```

Use `next_page_token` as `page_token` in the next request for more results.
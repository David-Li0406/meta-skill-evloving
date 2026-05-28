---
name: local-places
description: Use this skill when you want to search for nearby places like restaurants or cafes using a local Google Places API proxy.
---

# Skill body

## Setup

1. Navigate to your project directory:
   ```bash
   cd {baseDir}
   ```
2. Create a `.env` file with your Google Places API key:
   ```bash
   echo "GOOGLE_PLACES_API_KEY=your-key" > .env
   ```
3. Set up the virtual environment and install dependencies:
   ```bash
   uv venv && uv pip install -e ".[dev]"
   ```
4. Run the server:
   ```bash
   uv run --env-file .env uvicorn local_places.main:app --host 127.0.0.1 --port 8000
   ```

## Quick Start

1. **Check server status:**
   ```bash
   curl http://127.0.0.1:8000/ping
   ```

2. **Resolve a location:**
   ```bash
   curl -X POST http://127.0.0.1:8000/locations/resolve \
     -H "Content-Type: application/json" \
     -d '{"location_text": "Soho, London", "limit": 5}'
   ```

3. **Search for places:**
   ```bash
   curl -X POST http://127.0.0.1:8000/places/search \
     -H "Content-Type: application/json" \
     -d '{
       "query": "coffee shop",
       "location_bias": {"lat": 51.5137, "lng": -0.1366, "radius_m": 1000},
       "filters": {"open_now": true, "min_rating": 4.0},
       "limit": 10
     }'
   ```

4. **Get details of a specific place:**
   ```bash
   curl http://127.0.0.1:8000/places/{place_id}
   ```

## Conversation Flow

1. If the user says "near me" or provides a vague location, resolve it first.
2. If multiple results are found, show a numbered list and ask the user to pick one.
3. Ask for user preferences such as type, open status, rating, and price level.
4. Search using the `location_bias` from the chosen location.
5. Present results including name, rating, address, and open status.
6. Offer to fetch more details or refine the search.

## Filter Constraints

- `filters.types`: exactly ONE type (e.g., "restaurant", "cafe", "gym")
- `filters.price_levels`: integers 0-4 (0=free, 4=very expensive)
- `filters.min_rating`: 0-5 in 0.5 increments
- `filters.open_now`: boolean
- `limit`: 1-20 for search, 1-10 for resolve
- `location_bias.radius_m`: must be greater than 0

## Response Format

```json
{
  "results": [
    {
      "place_id": "ChIJ...",
      "name": "Coffee Shop",
      "address": "123 Main St",
      "location": {"lat": 51.5, "lng": -0.1},
      "rating": 4.6,
      "price_level": 2,
      "types": ["cafe", "food"],
      "open_now": true
    }
  ],
  "next_page_token": "..."
}
```

Use `next_page_token` as `page_token` in the next request for more results.
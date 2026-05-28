---
name: check-api
description: Check Teslamate API response format for a given endpoint. Use when you need to understand the JSON structure returned by the API.
allowed-tools: Read, WebFetch
---

# Check Teslamate API

Query the Teslamate API to inspect JSON response format for endpoints.

## Configuration

The API URL should be set in a `.env` file at the project root (gitignored):

```
TESLAMATE_API_URL=https://your-teslamate-api.example.com
```

If no `.env` file exists, ask the user for their Teslamate API URL.

## Common Endpoints

- `/api/v1/cars` - List all cars
- `/api/v1/cars/{id}` - Car details with current state (battery, location, climate, etc.)
- `/api/v1/cars/{id}/drives` - Drive history (supports `?start_date=` and `?end_date=`)
- `/api/v1/cars/{id}/charges` - Charge history (supports `?start_date=` and `?end_date=`)
- `/api/v1/cars/{id}/drives/{drive_id}` - Single drive details with positions
- `/api/v1/cars/{id}/charges/{charge_id}` - Single charge details with charging curve

## Instructions

1. Read the `.env` file to get `TESLAMATE_API_URL`
2. If not found, ask the user for the URL
3. Use WebFetch to query the requested endpoint
4. Present the JSON structure clearly, highlighting relevant fields

## Date Format

The API's parseDateParam function only accepts:
- RFC3339 format: `2024-12-07T00:00:00Z`
- DateTime format: `2024-12-07 00:00:00`

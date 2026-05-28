---
name: weather
description: Get weather information for any location using web search and fetch
homepage: https://github.com/haasonsaas/nexus
metadata:
  emoji: "🌤️"
  execution: core
  toolGroups:
    - group:web
---

# Weather Skill

Get current weather and forecasts for any location.

## When to Use

Use this skill when the user asks about:
- Current weather conditions
- Weather forecasts
- Temperature, humidity, wind
- Weather-related planning (outdoor events, travel)

## How to Use

1. First search for the location to confirm it exists
2. Fetch weather data from a reliable source (weather.gov, openweathermap, etc.)
3. Present the information clearly with:
   - Current conditions (temperature, description)
   - Key metrics (humidity, wind, visibility)
   - Forecast if requested

## Example Queries

- "What's the weather in Denver?"
- "Will it rain tomorrow in Seattle?"
- "What's the temperature in Tokyo right now?"

## Notes

- For US locations, prefer weather.gov for official forecasts
- Include both Fahrenheit and Celsius for temperature
- Mention the data source and time of last update
- If user doesn't specify location, ask for it

---
name: weather
description: Use this skill to get current weather and forecasts without requiring an API key.
---

# Weather

This skill utilizes two free services to provide weather information.

## wttr.in (primary)

### Quick one-liner:
```bash
curl -s "wttr.in/<location>?format=3"
# Output: <location>: ⛅️ +<temperature>°C
```

### Compact format:
```bash
curl -s "wttr.in/<location>?format=%l:+%c+%t+%h+%w"
# Output: <location>: ⛅️ +<temperature>°C <humidity>% ↙<wind_speed>km/h
```

### Full forecast:
```bash
curl -s "wttr.in/<location>?T"
```

### Format codes:
- `%c`: condition
- `%t`: temperature
- `%h`: humidity
- `%w`: wind
- `%l`: location
- `%m`: moon

### Tips:
- URL-encode spaces: `wttr.in/New+York`
- Use airport codes: `wttr.in/JFK`
- Units: `?m` (metric) or `?u` (USCS)
- For today only: `?1` or current only: `?0`
- To get a PNG: `curl -s "wttr.in/<location>.png" -o /tmp/weather.png`

## Open-Meteo (fallback, JSON)

This service is free and does not require a key, making it suitable for programmatic use:
```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=<latitude>&longitude=<longitude>&current_weather=true"
```

To use this service, find the coordinates for a city and query. It returns JSON with temperature, wind speed, and weather code.

### Documentation:
For more details, visit: [Open-Meteo Documentation](https://open-meteo.com/en/docs)
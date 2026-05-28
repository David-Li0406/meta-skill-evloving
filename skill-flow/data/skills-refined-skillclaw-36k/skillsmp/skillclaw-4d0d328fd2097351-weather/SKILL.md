---
name: weather
description: Use this skill when you need to get current weather and forecasts without requiring an API key.
---

# Weather

This skill utilizes two free services to provide current weather and forecasts without the need for an API key.

## wttr.in (primary)

### Quick one-liner:
```bash
curl -s "wttr.in/London?format=3"
# Output: London: ⛅️ +8°C
```

### Compact format:
```bash
curl -s "wttr.in/London?format=%l:+%c+%t+%h+%w"
# Output: London: ⛅️ +8°C 71% ↙5km/h
```

### Full forecast:
```bash
curl -s "wttr.in/London?T"
```

### Format codes:
- `%c`: condition
- `%t`: temperature
- `%h`: humidity
- `%w`: wind
- `%l`: location
- `%m`: moon phase

### Tips:
- URL-encode spaces: `wttr.in/New+York`
- Use airport codes: `wttr.in/JFK`
- Units: `?m` (metric) or `?u` (USCS)
- For today only: `?1` or current only: `?0`
- To get a PNG image: 
```bash
curl -s "wttr.in/Berlin.png" -o /tmp/weather.png
```

## Open-Meteo (fallback, JSON)

This service is also free and does not require an API key, making it suitable for programmatic use:
```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"
```
To use this, find the coordinates for a city and then query. It returns JSON with temperature, wind speed, and weather code.

### Documentation:
For more details, visit: [Open-Meteo Documentation](https://open-meteo.com/en/docs)
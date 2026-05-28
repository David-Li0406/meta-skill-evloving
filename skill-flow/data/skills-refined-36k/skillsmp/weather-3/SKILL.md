---
name: weather
description: Get the current weather for any city in the world
argument-hint: [city-name]
disable-model-invocation: false
allowed-tools: Bash(curl:*)
---

# Weather Skill

Get the current weather using wttr.in (a free weather API).

## Instructions

Run this command with the city name from $ARGUMENTS:

```bash
curl -s "wttr.in/$ARGUMENTS?format=3"
```

If the user wants more detail, use the full format:

```bash
curl -s "wttr.in/$ARGUMENTS?format=%l:+%c+%t+%h+%w"
```

Format codes:
- %l = location
- %c = condition icon
- %t = temperature
- %h = humidity
- %w = wind

Report the weather in a friendly, conversational way.

---
name: process-local-weather-mcp-response
description: Guide for mapping the weather JSON object properties. Use this after calling local-weather-server - GetWeatherForCity tool to map weather object properties to its respective full description.
---

# Process Local Weather MCP Server Weather response  to correct description

This skill helps you map the weather JSON object to its respective full description.

## When to use this skill

Use this skill when:
1. Requesting for city weather
2. Getting a city weather information using `local-weather-server` MCP Server - `GetWeatherForCity` tool

# Before calling MCP Server
Before calling `local-weather-server` MCP Server - `GetWeatherForCity` tool, make sure each property in the request is not null. If they are null, assigned the following default value:
- If Country is not specify, default to New Zealand
- If date is not specify, default to Tomorrow date

# Process Flow
1. After getting the response from MCP, the temperature fields can be mapped to the following description:
    - temperature1 = temperature_2m: Temperature at 2 meters above ground (°C)
    - temperature2 = temperature_80m: Temperature at 80 meters above ground (°C)
    - temperature3 = temperature_soil6cm: Soil temperature at 6 cm depth (°C)
    - temperature4 = temperatue_soil0cm: Soil temperature at 0 cm depth (°C)
    - temperature5 = apparent_temperature: Apparent temperature (°C)
2. Next to each celcius temperature information, append the Farenheit and Kelvin temperature
# Brand Context — Remote-First Architecture

> **This file is not used.** Brand context comes from your Robynn Brand Hub.

## How It Works

Rory uses a **thin-client architecture**. Your brand guidelines, voice, tone, product features, and all marketing context are stored in your Robynn Brand Hub — not in local files.

When you make a request:
1. Your request is sent to the Robynn API
2. The CMO v2 agent loads YOUR brand context from the database
3. Content is generated using YOUR voice and guidelines
4. Results come back already on-brand

## Why Remote-First?

- **Always up-to-date**: Changes in Brand Hub reflect immediately
- **No sync issues**: No stale local files to manage
- **Works anywhere**: Same brand context on any machine with your API key
- **Team consistency**: Everyone gets the same brand guidelines

## Setup Your Brand Hub

1. Go to https://robynn.ai
2. Navigate to **Settings → Brand Hub**
3. Add your:
   - Company name and description
   - Product features and differentiators
   - Brand voice and tone
   - Color palette and visual identity
   - Preferred/avoided terminology

## Verify Connection

Run `rory status` to confirm your Brand Hub is connected:

```
[RORY STATUS]
- API Key: ✅ Configured
- Brand Hub: ✅ Connected (Your Company)
- Tier: Free (18/20 tasks remaining this month)
```

## Need Help?

- Documentation: https://robynn.ai/docs/brand-hub
- Support: support@robynn.ai

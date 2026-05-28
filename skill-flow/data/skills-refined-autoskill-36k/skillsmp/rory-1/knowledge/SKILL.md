# Knowledge Layer — Remote-First

> **Local files are not used.** All brand context comes from your Robynn Brand Hub.

## How It Works

Rory uses a **thin-client architecture**:

1. You configure your brand in the **Robynn Brand Hub** (web app)
2. When you use Rory, your request goes to the Robynn API
3. The CMO v2 agent automatically loads YOUR brand context
4. Results come back already on-brand

**No local files. No syncing. No stale data.**

## What's Stored in Brand Hub

| Category | What It Includes |
|----------|------------------|
| **Company Profile** | Name, description, website, tagline |
| **Product Knowledge** | Features, differentiators, FAQs |
| **Brand Voice** | Tone, style, personality traits |
| **Terminology** | Preferred words, avoided words, branded terms |
| **Visual Identity** | Colors, logo, design style |
| **Personas** | Target audience segments |

## Setup

1. Go to https://robynn.ai
2. Navigate to **Settings → Brand Hub**
3. Fill in your brand details
4. Get your API key from **Settings → API Keys**
5. Configure Rory: `rory config <your_api_key>`

## Verify

Run `rory status` to confirm your Brand Hub is connected.

## Why Remote-First?

| Local Files | Remote Brand Hub |
|-------------|------------------|
| ❌ Can become stale | ✅ Always up-to-date |
| ❌ Manual syncing required | ✅ Automatic on each request |
| ❌ Different on each machine | ✅ Same everywhere |
| ❌ No version history | ✅ Full audit trail |

## About This Folder

The `knowledge/` folder exists for documentation purposes only. The files here explain how the remote-first architecture works — they are not read by Rory for brand context.

## Need Help?

- Brand Hub setup: https://robynn.ai/docs/brand-hub
- Support: support@robynn.ai

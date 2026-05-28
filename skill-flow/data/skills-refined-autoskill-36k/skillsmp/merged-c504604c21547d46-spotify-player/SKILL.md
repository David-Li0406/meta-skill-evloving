---
name: spotify-player
description: Use this skill for terminal-based Spotify playback and search using `spogo` (preferred) or `spotify_player`.
---

# spogo / spotify_player

Use `spogo` **(preferred)** for Spotify playback and search. Fall back to `spotify_player` if needed.

## Requirements
- Spotify Premium account.
- Either `spogo` or `spotify_player` installed.

## Setup
- For `spogo`, import cookies using: `spogo auth import --browser chromium`.

## Common CLI Commands
### spogo Commands
- Search: `spogo search track "query"`
- Playback: `spogo play|pause|next|prev`
- Devices: `spogo device list`, `spogo device set "<name|id>"`
- Status: `spogo status`

### spotify_player Commands (Fallback)
- Search: `spotify_player search "query"`
- Playback: `spotify_player playback play|pause|next|previous`
- Connect device: `spotify_player connect`
- Like track: `spotify_player like`

## Notes
- Config folder is located at `~/.config/spotify-player` (e.g., `app.toml`).
- For Spotify Connect integration, set a user `client_id` in the config.
- TUI shortcuts are available via `?` in the app.
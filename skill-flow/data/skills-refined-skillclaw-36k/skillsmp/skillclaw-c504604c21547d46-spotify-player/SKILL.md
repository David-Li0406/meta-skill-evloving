---
name: spotify-player
description: Use this skill when you want to control Spotify playback and search for tracks via the terminal using `spogo` or `spotify_player`.
---

# Skill body

## Requirements
- Spotify Premium account.
- Either `spogo` or `spotify_player` installed.

## Setup for spogo
- Import cookies: 
  ```bash
  spogo auth import --browser chromium
  ```

## Common CLI commands
### Using spogo (preferred)
- **Search for a track**: 
  ```bash
  spogo search track "query"
  ```
- **Playback controls**: 
  ```bash
  spogo play|pause|next|prev
  ```
- **Device management**: 
  ```bash
  spogo device list
  spogo device set "<name|id>"
  ```
- **Check status**: 
  ```bash
  spogo status
  ```

### Using spotify_player (fallback)
- **Search for a track**: 
  ```bash
  spotify_player search "query"
  ```
- **Playback controls**: 
  ```bash
  spotify_player playback play|pause|next|previous
  ```
- **Connect device**: 
  ```bash
  spotify_player connect
  ```
- **Like a track**: 
  ```bash
  spotify_player like
  ```

## Notes
- Configuration folder: `~/.config/spotify-player` (e.g., `app.toml`).
- For Spotify Connect integration, set a user `client_id` in the config.
- TUI shortcuts are available via `?` in the app.
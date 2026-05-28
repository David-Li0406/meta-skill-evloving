---
name: download
description: Download call recording for a specific session. Saves the audio file to the current directory.
allowed-tools: Bash
---

Download the audio recording for a specific call session.

First ensure CLI is installed:

```bash
pip install --upgrade vocal-bridge
```

## Download Recording

$ARGUMENTS should contain a session ID (UUID):

```bash
vb logs download $ARGUMENTS
```

This downloads the audio file to the current directory with filename `recording_<id>.<format>`.

## Custom Output Path

To save to a specific location, use the `-o` flag:

```bash
vb logs download <session_id> -o /path/to/call.ogg
```

## Notes

- Recordings are only available if the agent has call recording enabled
- Audio format depends on agent configuration (usually ogg or wav)
- Use `/vocal-bridge:logs <session_id>` first to check if a recording is available

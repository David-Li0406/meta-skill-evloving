---
name: transcribe
description: Speech-to-text with local NVIDIA Parakeet (NeMo) via the transcribe CLI.
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["transcribe"]}}}
---

# Transcribe

Local speech-to-text on NixOS (Parakeet / NeMo). GPU auto when CUDA available.

## Quick start

```bash
transcribe /path/to/audio.ogg
transcribe /path/to/audio.wav --output /tmp/out.txt
```

## Notes

- Default model: `nvidia/parakeet-tdt-0.6b-v3`
- Device auto: CUDA if available, else CPU
- Formats: any ffmpeg-supported input (ogg/wav/mp3/m4a)
- Former name: `parakeet-transcribe`

## Useful env / flags

```bash
PARAKEET_MODEL=nvidia/parakeet-tdt-0.6b-v3 transcribe file.ogg
PARAKEET_QUIET=0 transcribe file.ogg
PARAKEET_VENV=~/.local/share/parakeet-venv-py312 transcribe file.ogg
transcribe --device cuda file.ogg
```

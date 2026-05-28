---
name: openhue
description: Use this skill to control Philips Hue lights and scenes via the OpenHue CLI.
---

# OpenHue CLI

Use `openhue` to control Hue lights and scenes via a Hue Bridge.

## Setup
- Discover bridges: `openhue discover`
- Guided setup: `openhue setup`

## Read
- `openhue get light --json`
- `openhue get room --json`
- `openhue get scene --json`

## Write
- Turn on: `openhue set light <id-or-name> --on`
- Turn off: `openhue set light <id-or-name> --off`
- Brightness: `openhue set light <id> --on --brightness <value>`
- Color: `openhue set light <id> --on --rgb <color>`
- Scene: `openhue set scene <scene-id>`

## Notes
- You may need to press the Hue Bridge button during setup.
- Use `--room "<Room Name>"` when light names are ambiguous.

## Installation
- Install OpenHue CLI using Homebrew: `brew install openhue/cli/openhue-cli`
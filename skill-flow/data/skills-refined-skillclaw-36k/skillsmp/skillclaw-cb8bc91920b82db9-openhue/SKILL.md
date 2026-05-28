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
- Get light information: `openhue get light --json`
- Get room information: `openhue get room --json`
- Get scene information: `openhue get scene --json`

## Write
- Turn on a light: `openhue set light <id-or-name> --on`
- Turn off a light: `openhue set light <id-or-name> --off`
- Set brightness: `openhue set light <id> --on --brightness 50`
- Set color: `openhue set light <id> --on --rgb #3399FF`
- Activate a scene: `openhue set scene <scene-id>`

## Notes
- You may need to press the Hue Bridge button during setup.
- Use `--room "Room Name"` when light names are ambiguous.

## Installation
- Install OpenHue CLI using Homebrew: `brew install openhue/cli/openhue-cli`
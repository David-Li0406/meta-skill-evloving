---
name: device-camera
description: Take photos using the device camera on connected edge devices
homepage: https://github.com/haasonsaas/nexus
metadata:
  emoji: "📷"
  execution: edge
  os:
    - darwin
    - linux
  toolGroups: []
  requires:
    anyBins:
      - imagesnap
      - ffmpeg
      - fswebcam
---

# Device Camera Skill

Capture photos using the device camera on edge devices.

## When to Use

Use this skill when the user asks to:
- Take a photo or picture
- Capture something with the camera
- Scan or photograph a document
- Take a selfie

## Requirements

This skill requires:
1. A connected edge daemon (`nexus-edge`)
2. Camera access on the edge device
3. One of: `imagesnap` (macOS), `ffmpeg`, or `fswebcam` (Linux)

## Installation

### macOS
```bash
brew install imagesnap
```

### Linux
```bash
# Debian/Ubuntu
sudo apt install fswebcam

# Or use ffmpeg
sudo apt install ffmpeg
```

## How to Use

The skill uses the `nodes.camera_snap` tool which:
1. Requests approval from the user (high-risk action)
2. Captures a photo from the default camera
3. Returns the image as an artifact

## Privacy Notes

- Camera access always requires explicit user approval
- Photos are not stored persistently
- The user can see exactly what was captured
- No photos are sent externally without explicit action

## Example Queries

- "Take a photo"
- "Capture what's on my desk"
- "Can you see me through the camera?"

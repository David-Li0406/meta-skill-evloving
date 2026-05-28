---
name: pio-operator
description: Use for PlatformIO build/upload/monitor tasks in this repo. Must match repo README conventions.
---

Must follow repo commands:
- Build: pio run
- Flash: pio run -t upload [--upload-port <port>]
- Monitor: pio device monitor [--port <port>] --baud 115200

Never guess ports; request user to confirm actual device port string if unknown.

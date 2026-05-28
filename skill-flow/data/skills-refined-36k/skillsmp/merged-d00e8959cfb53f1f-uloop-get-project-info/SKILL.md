---
name: uloop-get-project-info
description: Use this skill when you need to retrieve detailed Unity project information, including Unity version, project settings, and platform details via the uloop CLI.
---

# uloop get-project-info

Get detailed Unity project information.

## Usage

```bash
uloop get-project-info
```

## Parameters

None.

## Output

Returns JSON with project information:
- `UnityVersion`: Unity Editor version
- `ProjectName`: Application product name
- `CompanyName`: Company name
- `Version`: Application version
- `Platform`: Current platform
- `DataPath`: Assets folder path
- `PersistentDataPath`: Persistent data path
- `TemporaryCachePath`: Temporary cache path
- `IsEditor`: Whether running in editor
- `IsPlaying`: Whether in play mode
- `DeviceType`: Device type
- `OperatingSystem`: OS information
- `ProcessorType`: CPU type
- `SystemMemorySize`: RAM size in MB
- `GraphicsDeviceName`: GPU name
- `Ver`: uLoopMCP package version

## Notes

This is a sample custom tool demonstrating how to create MCP tools.
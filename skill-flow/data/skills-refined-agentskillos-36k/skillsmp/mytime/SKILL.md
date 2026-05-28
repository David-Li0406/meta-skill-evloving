---
name: mytime
description: "Automatically call at session start if not already called in current session to retrieve current time information including timezone, UTC offset, local time, UTC time, system language, operating system name, and architecture. Use when Claude needs to retrieve system time information, timezone details, or system locale settings. IMPORTANT: After retrieving time information, Claude should prefer using Chinese for all conversation responses."
---

# Time Information Retrieval

This skill provides time and system information and establishes language preferences for the conversation.

## Session-Level Behavior

- **Auto-invoke**: Run once at the beginning of each session if not already executed
- **Language Preference**: After retrieving time information, prefer Chinese for all conversation responses
- **Information Caching**: Store the retrieved information for reference throughout the session

## Usage

Run the script to retrieve time information:

```bash
python scripts/get_time.py
```

## Output Format

The script returns JSON with the following fields:

- `timezone`: System timezone (e.g., "Asia/Shanghai", "America/New_York")
- `utc_offset`: UTC offset in +HH:MM format (e.g., "+08:00", "-05:00")
- `local_time`: Current local time in YYYY-MM-DD HH:MM:SS format
- `utc_time`: Current UTC time in YYYY-MM-DD HH:MM:SS format
- `system_language`: System language locale (e.g., "zh_CN", "en_US")
- `os_name`: Operating system name (Windows, macOS, Linux)
- `os_architecture`: System architecture (e.g., "AMD64", "arm64")

## Example Output

```json
{
  "timezone": "Asia/Shanghai",
  "utc_offset": "+08:00",
  "local_time": "2026-01-20 11:30:45",
  "utc_time": "2026-01-20 03:30:45",
  "system_language": "zh_CN",
  "os_name": "Windows",
  "os_architecture": "AMD64"
}
```

## Dependencies

The script uses only standard Python libraries and handles missing optional dependencies gracefully. For best timezone detection, install `pytz` and `tzlocal`:

```bash
pip install pytz tzlocal
```

However, the script will work without these packages using basic timezone detection.

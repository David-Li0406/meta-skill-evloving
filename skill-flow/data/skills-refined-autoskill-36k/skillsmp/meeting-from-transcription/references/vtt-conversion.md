# VTT File Handling

VTT (WebVTT) files are subtitle/caption files from video conferencing tools like Zoom, Teams, and Google Meet.

## Critical: Date Requirement

**VTT files REQUIRE the `--date` flag.**

Why:
- VTT format doesn't contain meeting date metadata
- File modification time is unreliable (changes on download, copy, or sync)
- The converted transcription note won't have a valid `recorded` field

**If `--date` is missing, stop immediately with:**
```
Error: VTT files require --date flag (file mtime is unreliable).
Example: --date 2026-01-15T14:30:00
```

## Conversion Command

```bash
cd ${CLAUDE_PLUGIN_ROOT} && bun src/cli.ts voice convert "<vtt-path>" --format json
```

## Output Format

```json
{
  "success": true,
  "notePath": "00 Inbox/🎤 YYYY-MM-DD h-mmam.md",
  "noteTitle": "🎤 YYYY-MM-DD h-mmam",
  "summary": "Brief summary of the transcription content"
}
```

## Error Output

```json
{
  "success": false,
  "error": "Description of what went wrong"
}
```

On failure, report: `Failed to convert VTT: <error message>`

## After Successful Conversion

1. Use `notePath` from the output as the transcription path for remaining steps
2. **Use the `--date` override as the meeting date** — ignore any `recorded` field from the converted note (it's based on unreliable file mtime)
3. Continue with Step 2 (Read & Validate) using the converted note path

## Example Usage

```bash
# User provides VTT file with required date
/meeting-from-transcription ~/Downloads/zoom-recording.vtt --date 2026-01-15T14:30:00

# With type override
/meeting-from-transcription ~/Downloads/teams-call.vtt --date 2026-01-10T09:00:00 --type standup
```

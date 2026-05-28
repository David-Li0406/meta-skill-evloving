# Voice Memos Reference

## Command: voice-memos

Transcribe Apple Voice Memos with speaker diarization.

```bash
voice-memos list                 # Show unprocessed memos
voice-memos list --all           # All memos (including processed)
voice-memos process              # Auto-process (prioritizes recent)
voice-memos process --dry-run    # Preview what would be processed
voice-memos transcribe <file>    # Transcribe specific memo
voice-memos stats                # Usage/cost statistics
```

## Features

- Reads from Apple's synced Voice Memos database (iCloud)
- Speaker diarization (identifies multiple speakers)
- Key phrase extraction
- Cost tracking (~$0.0025/min via AssemblyAI)

## Output

- Transcripts saved to `~/Vault/Voice-Transcripts/`
- Markdown format with speaker labels and timestamps

## Requirements

- `ASSEMBLYAI_API_KEY` environment variable
- Python package: `pip install assemblyai`

## Databases

- Apple source: `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/CloudRecordings.db`
- Tracking: `~/.voice-memos.db`

## Cost

~$0.15/hour of audio. Use `stats` to check balance.

## Examples

**"Transcribe my recent voice memos"**
```bash
voice-memos process
```

**"What memos need transcription?"**
```bash
voice-memos list
```

**"How much have I spent on transcription?"**
```bash
voice-memos stats
```

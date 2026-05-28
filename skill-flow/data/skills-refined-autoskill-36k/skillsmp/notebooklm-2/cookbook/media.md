# Media Cookbook

---

## Create an audio overview

**Problem**: Generate an audio summary for a notebook.

**Solution**:
```bash
nlm audio-create <notebook-id> "Summarize the key points in a professional tone."
```

**Tip**: Use `nlm audio-list <notebook-id>` to check status.

---

## Download an audio overview

**Problem**: Download the audio file locally.

**Solution**:
```bash
nlm audio-download <notebook-id> overview.mp3 --direct-rpc
```

**Tip**: Requires `--direct-rpc`.

---

## Create a video overview

**Problem**: Generate a video summary.

**Solution**:
```bash
nlm video-create <notebook-id> "Create a short overview video."
```

**Tip**: Use `nlm video-list <notebook-id>` to check status.

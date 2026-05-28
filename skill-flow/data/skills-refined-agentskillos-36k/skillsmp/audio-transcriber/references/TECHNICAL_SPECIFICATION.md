# Audio Transcription Pipeline - Technical Reference

**Document Version:** 2.0
**Last Updated:** 2025-10-26

---

## Quick Reference

### Key Design Decisions

1. **GPU-First Architecture**: Always prefer NVIDIA CUDA, gracefully fall back to CPU
2. **Never Average Sources**: Use hierarchical prioritization, never blend precision levels
3. **Segmentation Mutual Exclusion**: Fixed XOR VAD mode, never both
4. **Idempotent Operations**: Re-running is safe, skip existing unless `--force`
5. **Comprehensive Logging**: Every operation logged to `ops_log.ndjson`

---

## Processing Rules

### Rule A: Audio Extraction Retry Matrix

On FFmpeg failure, retry in sequence:

1. **Primary**: `pcm_s16le` codec, 16kHz, mono
2. **Retry 1**: Fallback to `flac` codec
3. **Retry 2**: Add demuxer args: `-fflags +genpts -rw_timeout 30000000`
4. **Retry 3**: Extended probe: `-analyzeduration 100M -probesize 100M`

If all retries fail → write `{video_stem}_FAILED.json` with error details.

### Rule B: Segmentation Mode Enforcement

```python
if mode == "fixed":
    # No VAD preprocessing
    # Split into 30s chunks (configurable)
    # Whisper handles timestamp alignment

elif mode == "vad":
    # Use Silero VAD to detect speech regions
    # Variable-length segments (2-60s)
    # NO fixed chunking
    # Segments are non-overlapping

else:
    raise ValueError("Invalid mode")
```

**NEVER run both modes simultaneously.**

### Rule C: GPU Metrics Collection

```python
# Sample GPU utilization at 1-2 Hz during transcription
# Record:
# - Device name, VRAM total/free
# - Average GPU % utilization
# - Average memory % utilization
# - CUDA version, driver version
# - torch version
```

### Rule D: Speaker Label Normalization

Different diarization backends produce different label formats:

- pyannote: `SPEAKER_00`, `SPEAKER_01`, ...
- speechbrain: `spk1`, `spk2`, ...

**Normalize to**: `spkA`, `spkB`, `spkC`, ... (consistent across all outputs)

### Rule E: INDEX.csv Composite Key

- **Key**: `(video_rel, seg_idx)`
- **Merge rule**: On duplicate, keep entry with latest `created_utc`
- **Text truncation**: 512 chars in CSV, full text in JSON

### Rule F: SRT/VTT Validation

```python
def validate_srt(srt_content):
    """
    1. Timestamps strictly monotonic
    2. No overlapping segments
    3. Clamp gaps <50ms
    4. Positive durations only
    5. Proper format: HH:MM:SS,mmm (comma for SRT)
    """
```

### Rule G: Failed File Logging

```json
{
  "video_path": "C:\\...\\video.mp4",
  "error_type": "ffmpeg_err | decode_err | OOM | corrupted | no_audio",
  "error_message": "Detailed error message",
  "ffprobe_metadata": { /* video metadata */ },
  "timestamp": "2025-09-03T14:30:00Z"
}
```

### Rule H: Diarization Graceful Fallback

```python
if diarization_enabled:
    try:
        # Check HF token
        # Run diarization
        # Normalize labels
    except (TokenError, OOMError) as e:
        log.warning(f"Diarization failed: {e}, continuing without speaker labels")
        # Continue transcription without diarization
```

### Rule I: Resume Safety

```python
def should_skip(video_path, output_dir, force=False):
    if force:
        return False

    expected_files = [
        f"{video_stem}.txt",
        f"{video_stem}.json"
    ]

    return all((output_dir / f).exists() for f in expected_files)
```

### Rule J: Language Detection

```python
if detect_language:
    # Per-file OR per-segment detection
    # Record lang (ISO 639-1) and conf (0-1) in INDEX.csv

if task == "translate":
    # Translate non-EN to English
    # Original lang preserved in metadata
```

---

## Implementation Checklist

### Phase 0: Validation
- [ ] Check `roots` provided and not empty
- [ ] Verify FFmpeg installed
- [ ] Check GPU available (if requested)
- [ ] Validate HF token (if diarization enabled)
- [ ] Confirm segmentation mode is "fixed" or "vad"
- [ ] Estimate disk space requirements
- [ ] Present configuration summary
- [ ] Wait for user confirmation

### Phase 1: Audio Extraction
- [ ] Run FFprobe preflight check
- [ ] Attempt primary extraction (PCM 16kHz mono)
- [ ] On failure, retry with codec fallback
- [ ] On failure, retry with demuxer args
- [ ] On all failures, log to `_FAILED.json`
- [ ] Clean up temp files if `keep_intermediate=false`

### Phase 2: Segmentation
- [ ] If mode="fixed": split into 30s chunks
- [ ] If mode="vad": detect speech regions with Silero
- [ ] Ensure no overlap between segments
- [ ] Validate segment durations within bounds

### Phase 3: Transcription
- [ ] Load Whisper model (reuse across files)
- [ ] Start GPU monitoring thread
- [ ] Transcribe each segment with word timestamps
- [ ] Adjust timestamps relative to video start
- [ ] Stop GPU monitoring, collect metrics

### Phase 4: Diarization (Optional)
- [ ] Check diarization enabled
- [ ] Load diarization model (pyannote or speechbrain)
- [ ] Run diarization on full audio
- [ ] Normalize speaker labels to spk{A..Z}
- [ ] Assign speakers to transcript segments
- [ ] On error, log warning and continue without speakers

### Phase 5: Output Generation
- [ ] Write TXT with timestamps
- [ ] Write JSON with full metadata
- [ ] Generate SRT, validate monotonic timestamps
- [ ] Generate VTT (optional)
- [ ] Write INDEX shard (per worker)

### Phase 6: Index Merge
- [ ] Collect all INDEX.<pid>.csv shards
- [ ] Merge with pandas
- [ ] Deduplicate by (video_rel, seg_idx)
- [ ] Keep latest created_utc on collision
- [ ] Sort by date, video_stem, seg_idx
- [ ] Write final INDEX.csv
- [ ] Delete shard files

### Phase 7: Results JSON
- [ ] Collect processing statistics
- [ ] Include GPU metrics (device, VRAM, utilization)
- [ ] List all artifacts with absolute paths
- [ ] Include CUDA/driver/torch versions
- [ ] List failed files with error types
- [ ] Write to `reports/{task_id}__results.json`

---

## Performance Tuning

### Model Selection Guide

| Use Case | Model | Device | Compute Type | Batch Size |
|----------|-------|--------|--------------|------------|
| Quick preview | tiny | GPU | float16 | 16 |
| Default (balanced) | base | GPU | float16 | 8 |
| Noisy audio | small | GPU | float16 | 8 |
| High accuracy | medium | GPU | float16 | 4 |
| Production quality | large-v3 | GPU | float16 | 2 |
| CPU fallback | base | CPU | int8 | 1 |

### Parallel Processing Recommendations

| Hardware | Workers | Notes |
|----------|---------|-------|
| RTX 4080 (16GB) | 3 | Default, balances GPU/disk I/O |
| RTX 3060 (12GB) | 2 | Reduce to avoid OOM |
| RTX 3090 (24GB) | 4-5 | Can handle more concurrent |
| CPU only (16-core) | 2 | Avoid thrashing |

### Segmentation Mode Selection

| Scenario | Mode | Chunk Size | Notes |
|----------|------|------------|-------|
| Continuous conversation | fixed | 30s | Predictable, robust |
| Parking mode (sparse) | vad | 2-60s | Skips long silences |
| Mixed (some silent periods) | fixed | 30s | Safer default |

---

## Troubleshooting Matrix

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| "GPU not detected" | CUDA not installed | Install CUDA toolkit OR use `--device cpu` |
| "FFmpeg command failed" | FFmpeg not in PATH | Install from ffmpeg.org |
| "Out of memory (OOM)" | GPU VRAM insufficient | Use smaller model OR reduce batch size |
| "Diarization failed" | HF token missing | Set `HF_TOKEN` OR disable diarization |
| "SRT validation errors" | Overlapping timestamps | Enable `--clamp-gaps` |
| "No audio stream" | Video has no audio track | Check with `ffprobe` OR skip file |
| "Slow transcription" | Running on CPU | Check GPU detection OR install CUDA |
| "Index merge duplicates" | Concurrent writes | Normal, deduplication handles this |

---

## API Reference

### Core Functions

```python
def validate_inputs(config: Dict) -> Tuple[bool, List[str]]:
    """Validate configuration before processing."""

def extract_audio_with_retry(video_path: Path, output_path: Path, config: Dict) -> Optional[Path]:
    """Extract audio with FFmpeg retry matrix."""

def segment_audio(audio_path: Path, config: Dict) -> List[Tuple[int, int]]:
    """Segment audio based on mode (fixed or VAD)."""

def transcribe_with_gpu_metrics(audio_path: Path, chunks: List, config: Dict) -> Tuple[List, Dict]:
    """Transcribe audio chunks with GPU metrics collection."""

def apply_diarization(audio_path: Path, segments: List, config: Dict) -> List:
    """Apply speaker diarization (optional, graceful fallback)."""

def write_all_formats(segments: List, metadata: Dict, output_dir: Path, config: Dict) -> List[Path]:
    """Generate all requested output formats."""

def merge_index_shards(shard_files: List[Path], output_file: Path):
    """Merge per-worker index shards into global INDEX.csv."""
```

---

## Testing

### Unit Test Coverage

1. **FFmpeg Command Builder**: Verify correct args for mono/16kHz, retry toggles
2. **Segment Combiner**: Ensure strictly monotonic timestamps with carryover
3. **SRT/VTT Serializer**: Validate timecode formatting (comma vs period), no overlaps
4. **Index Merger**: Test deduplication by (video_rel, seg_idx), keep latest
5. **Language Detection**: Stubbed non-EN clip picks correct path
6. **GPU Metrics**: Mock NVML to ensure fields populate

### Integration Smoke Test

```bash
# Input: 1 short MP4 (30 seconds)
# Expected outputs:
# - audio.wav (if keep_intermediate=true)
# - transcript.txt
# - transcript.json
# - transcript.srt
# - INDEX.csv with ≥1 row

# Validation:
# - Timestamps monotonic
# - SRT passes validator
# - Language matches expected
# - No missing segments
# - GPU metrics present in results JSON
```

---

## Version History

- **v2.0** (2025-10-26) - Production-ready specification with GPU-first architecture
- **v1.5** (2025-10-25) - Added diarization support and retry matrix
- **v1.0** (2025-10-20) - Initial technical specification

---

**Status:** Production Ready
**Maintained By:** Audio Transcription Pipeline Project

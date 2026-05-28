# Audio Transcription Pipeline - Complete Technical Specification v2.0

**Document Version:** 2.0
**Pipeline Version:** 2.0
**Last Updated:** 2025-10-26
**Status:** Production Ready

---

## Table of Contents

1. [Overview](#1-overview)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Input/Output Contracts](#3-inputoutput-contracts)
4. [Processing Pipeline](#4-processing-pipeline)
5. [Quality & Error Handling](#5-quality--error-handling)
6. [Performance & Optimization](#6-performance--optimization)
7. [Testing & Validation](#7-testing--validation)
8. [Configuration](#8-configuration)
9. [Implementation Requirements](#9-implementation-requirements)
10. [Acceptance Criteria](#10-acceptance-criteria)

---

## 1. Overview

### 1.1 Purpose

Extract audio from dashcam MP4 files and produce GPU-accelerated timestamped transcripts with optional speaker diarization, daily/aggregate summaries, and centralized indexing.

### 1.2 Key Features

- **GPU-First**: NVIDIA CUDA acceleration with automatic CPU fallback
- **Retry Matrix**: FFmpeg retry logic with codec fallback
- **Segmentation Modes**: Fixed-length OR VAD-based (mutually exclusive)
- **Speaker Diarization**: Optional pyannote/SpeechBrain integration
- **Multiple Formats**: TXT, JSON, SRT, VTT output
- **Global Index**: Searchable INDEX.csv with segment-level metadata
- **Resume Safety**: Skip existing transcripts, idempotent operations
- **Quality Metrics**: GPU utilization, confidence scores, coverage stats

### 1.3 Design Principles

1. **GPU-First, CPU-Fallback**: Always prefer GPU, gracefully degrade to CPU
2. **Never Average Sources**: Hierarchical source prioritization (no averaging)
3. **Explicit Gaps**: All time periods accounted for (data or gaps)
4. **Idempotent Operations**: Re-running is safe
5. **Fail-Fast Validation**: Check all prerequisites before processing
6. **Comprehensive Logging**: Every operation logged to ops_log.ndjson

---

## 2. High-Level Architecture

```
[Input: MP4 Files]
   │
   ▼
[FFprobe Preflight]
  ├─► Check audio stream exists
  ├─► Validate duration
  └─► Skip corrupted → _FAILED.json
   │
   ▼
[Audio Extraction (FFmpeg)]
  ├─► Primary: PCM 16kHz mono → WAV
  ├─► Retry: FLAC codec fallback
  └─► Retry: Extended probe + demuxer args
   │
   ▼
[Segmentation Branch]
  ├─► [Fixed Mode] 30s chunks, no VAD
  └─► [VAD Mode] Silero VAD → 2-60s speech regions
   │
   ▼
[GPU Transcription (faster-whisper)]
  ├─► CUDA FP16, batch=8
  ├─► Word-level timestamps
  └─► Language detection (optional)
   │
   ├─► [Optional Diarization]
   │   ├─► pyannote (HF token required)
   │   └─► speechbrain (no auth)
   │
   ├─► [Optional Redaction]
   │   └─► PII regex patterns
   │
   ▼
[Format Writers]
  ├─► TXT (timestamped plain text)
  ├─► JSON (complete metadata)
  ├─► SRT (SubRip subtitles)
  └─► VTT (WebVTT - optional)
   │
   ▼
[Index Writer]
  ├─► Write INDEX.<pid>.csv per worker
  └─► Merge → INDEX.csv (deduplicate by composite key)
   │
   ▼
[Results JSON]
  └─► GPU metrics, stats, artifacts list
```

---

## 3. Input/Output Contracts

### 3.1 Input JSON Schema

```json
{
  "mode": "transcribe_audio",
  "roots": ["G:\\...\\DASHCAM\\Movie_F\\20250903"],
  "output_dir": "G:\\...\\AudioTranscription\\out\\ALL_TRANSCRIPTS",

  "whisper": {
    "engine": "faster-whisper",
    "model_size": "base",
    "device": "cuda",
    "batch_size": 8,
    "compute_type": "float16",
    "language": "en",
    "detect_language": false,
    "task": "transcribe"
  },

  "audio": {
    "sample_rate": 16000,
    "channels": 1,
    "codec": "pcm_s16le",
    "format": "wav",
    "keep_intermediate": false,
    "ffmpeg_retry": {
      "enabled": true,
      "codec_fallback": "flac",
      "demuxer_args": ["-fflags", "+genpts", "-rw_timeout", "30000000"],
      "probe_args": ["-analyzeduration", "100M", "-probesize", "100M"]
    }
  },

  "segmentation": {
    "mode": "fixed",
    "chunk_length_sec": 30,
    "min_silence_gap_sec": 0.2,
    "vad_min_len_sec": 2,
    "vad_max_len_sec": 60
  },

  "diarization": {
    "enabled": false,
    "backend": "pyannote",
    "hf_token_env": "HF_TOKEN",
    "min_speakers": 1,
    "max_speakers": 10,
    "normalize_labels": true
  },

  "post": {
    "timestamps": true,
    "summarize": true,
    "categorize": true,
    "min_confidence": 0.5,
    "redact": {
      "enabled": false,
      "rules": ["phone", "email", "license_plate"]
    }
  },

  "formats": ["txt", "json", "srt"],

  "parallel": {
    "max_workers": 3
  },

  "limits": {
    "max_duration_per_run_sec": 7200,
    "skip_if_silent": true
  }
}
```

### 3.2 Output JSON Schema

```json
{
  "status": "ok",
  "summary": {
    "videos_processed": 15,
    "segments": 742,
    "hours_audio": 7.8,
    "gpu_detected": true,
    "device_count": 1,
    "devices": [
      {
        "index": 0,
        "name": "NVIDIA GeForce RTX 4080",
        "total_mem_mb": 16384,
        "free_mem_mb": 14200
      }
    ],
    "utilization": {
      "gpu_pct": 35,
      "mem_pct": 42,
      "sampling_hz": 2
    },
    "cuda_version": "12.1",
    "driver_version": "546.01",
    "torch_version": "2.2.0+cu121",
    "engine_commit": "v1.0.0",
    "errors": 0,
    "failed_files": []
  },
  "artifacts": {
    "index_csv": "G:\\...\\INDEX.csv",
    "output_dir": "G:\\...\\transcripts",
    "results_file": "G:\\...\\reports\\task_20250903_120000__results.json"
  },
  "notes": [
    "engine=faster-whisper(base, FP16, CUDA)",
    "formats=txt,json,srt",
    "segmentation=fixed(30s)"
  ]
}
```

### 3.3 INDEX.csv Schema

Composite Key: `(video_rel, seg_idx)`

| Column | Type | Description |
|--------|------|-------------|
| `dataset` | string | Movie_F / Movie_R / Park_F / Park_R |
| `date` | string | YYYYMMDD format |
| `video_rel` | string | Relative path from root |
| `video_stem` | string | Filename without extension |
| `seg_idx` | int | 0-based segment index |
| `ts_start_ms` | int | Segment start milliseconds |
| `ts_end_ms` | int | Segment end milliseconds |
| `text` | string | Transcript (truncated to 512 chars) |
| `text_len` | int | Full text length (chars) |
| `lang` | string | ISO 639-1 language code |
| `lang_conf` | float | Language detection confidence (0-1) |
| `conf_avg` | float | Average token confidence (0-1) |
| `speaker` | string | Normalized label (spkA, spkB, etc.) |
| `format_mask` | int | Bitmask: txt/json/srt/vtt |
| `transcript_file` | string | Basename (no path) |
| `audio_file` | string | Basename or empty |
| `engine` | string | e.g., faster-whisper:base:fp16 |
| `cuda_version` | string | CUDA version |
| `driver_version` | string | Driver version |
| `created_utc` | string | ISO 8601 timestamp |

---

## 4. Processing Pipeline

### 4.1 Phase 0: Input Validation

```python
def validate_inputs(config):
    """
    Validate all inputs before processing begins.
    Fail-fast on any critical issue.
    """
    # Check required inputs
    if not config.get('roots') or len(config['roots']) == 0:
        raise ValueError("Roots not provided or empty → hard fail")

    # Check FFmpeg available
    if not check_ffmpeg_installed():
        raise RuntimeError("FFmpeg not found in PATH")

    # Check GPU if requested
    if config['whisper']['device'] == 'cuda':
        if not torch.cuda.is_available():
            log.warning("CUDA requested but not available, falling back to CPU")
            config['whisper']['device'] = 'cpu'

    # Check HF token if diarization enabled
    if config['diarization']['enabled']:
        token_env = config['diarization']['hf_token_env']
        if not os.getenv(token_env):
            log.warning(f"HF token {token_env} not set, disabling diarization")
            config['diarization']['enabled'] = False

    # Check segmentation mode mutual exclusion
    if config['segmentation']['mode'] not in ['fixed', 'vad']:
        raise ValueError("Segmentation mode must be 'fixed' or 'vad'")

    # Estimate disk space required
    estimated_space_gb = estimate_disk_space(config)
    available_space_gb = get_available_disk_space(config['output_dir'])
    if estimated_space_gb > available_space_gb:
        raise RuntimeError(f"Insufficient disk space: need {estimated_space_gb}GB, have {available_space_gb}GB")
```

### 4.2 Phase 1: Audio Extraction

```python
def extract_audio_with_retry(video_path, output_path, config):
    """
    Extract audio with FFmpeg retry matrix.

    Retry sequence:
    1. Primary: PCM 16kHz mono
    2. Fallback: FLAC codec
    3. Extended probe + demuxer args
    """
    # FFprobe preflight check
    metadata = ffprobe(video_path)
    if not has_audio_stream(metadata):
        write_failed_json(video_path, "no_audio", metadata)
        return None

    # Primary extraction
    try:
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vn',  # No video
            '-acodec', config['audio']['codec'],
            '-ar', str(config['audio']['sample_rate']),
            '-ac', str(config['audio']['channels']),
            output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path

    except subprocess.CalledProcessError:
        log.warning(f"Primary extraction failed for {video_path}, trying fallback")

        # Retry 1: FLAC codec
        try:
            cmd_fallback = cmd.copy()
            cmd_fallback[cmd.index(config['audio']['codec'])] = config['audio']['ffmpeg_retry']['codec_fallback']
            subprocess.run(cmd_fallback, check=True, capture_output=True)
            return output_path

        except subprocess.CalledProcessError:
            log.warning(f"Fallback codec failed, trying extended probe")

            # Retry 2: Extended probe + demuxer args
            try:
                cmd_extended = (
                    config['audio']['ffmpeg_retry']['demuxer_args'] +
                    config['audio']['ffmpeg_retry']['probe_args'] +
                    cmd
                )
                subprocess.run(cmd_extended, check=True, capture_output=True)
                return output_path

            except subprocess.CalledProcessError as e:
                write_failed_json(video_path, "ffmpeg_err", metadata, str(e))
                return None
```

### 4.3 Phase 2: Segmentation

```python
def segment_audio(audio_path, config):
    """
    Segment audio based on mode (fixed OR VAD, never both).
    """
    mode = config['segmentation']['mode']

    if mode == 'fixed':
        # Fixed-length chunks
        chunk_size = config['segmentation']['chunk_length_sec']
        return segment_fixed(audio_path, chunk_size)

    elif mode == 'vad':
        # Voice Activity Detection
        vad_model = load_silero_vad()
        min_len = config['segmentation']['vad_min_len_sec']
        max_len = config['segmentation']['vad_max_len_sec']
        return segment_vad(audio_path, vad_model, min_len, max_len)

    else:
        raise ValueError(f"Invalid segmentation mode: {mode}")


def segment_fixed(audio_path, chunk_size_sec):
    """
    Split audio into fixed-length chunks.

    Returns: List of (start_ms, end_ms) tuples
    """
    duration = get_audio_duration(audio_path)
    chunks = []

    for start_sec in range(0, int(duration), chunk_size_sec):
        end_sec = min(start_sec + chunk_size_sec, duration)
        chunks.append((start_sec * 1000, end_sec * 1000))

    return chunks


def segment_vad(audio_path, vad_model, min_len_sec, max_len_sec):
    """
    Use Silero VAD to detect speech regions.

    Returns: List of (start_ms, end_ms) tuples for speech regions only
    """
    audio = load_audio(audio_path, sample_rate=16000)
    speech_timestamps = vad_model(audio, return_seconds=True)

    # Filter by length constraints
    chunks = []
    for segment in speech_timestamps:
        duration = segment['end'] - segment['start']
        if min_len_sec <= duration <= max_len_sec:
            chunks.append((
                int(segment['start'] * 1000),
                int(segment['end'] * 1000)
            ))

    return chunks
```

### 4.4 Phase 3: GPU Transcription

```python
def transcribe_with_gpu_metrics(audio_path, chunks, config):
    """
    Transcribe audio chunks with GPU metrics collection.
    """
    # Load model once (reuse across chunks)
    model = WhisperModel(
        config['whisper']['model_size'],
        device=config['whisper']['device'],
        compute_type=config['whisper']['compute_type']
    )

    # Start GPU monitoring
    gpu_monitor = GPUMonitor(sampling_hz=2)
    gpu_monitor.start()

    all_segments = []

    try:
        for chunk_start_ms, chunk_end_ms in chunks:
            # Extract chunk audio
            chunk_audio = extract_audio_segment(audio_path, chunk_start_ms, chunk_end_ms)

            # Transcribe chunk
            segments, info = model.transcribe(
                chunk_audio,
                beam_size=config['whisper'].get('beam_size', 5),
                word_timestamps=config['post']['timestamps'],
                language=config['whisper']['language'] if not config['whisper']['detect_language'] else None
            )

            # Adjust timestamps relative to video start
            for segment in segments:
                segment['start'] += chunk_start_ms / 1000.0
                segment['end'] += chunk_start_ms / 1000.0
                all_segments.append(segment)

    finally:
        # Stop GPU monitoring
        gpu_metrics = gpu_monitor.stop()

    return all_segments, gpu_metrics
```

### 4.5 Phase 4: Speaker Diarization (Optional)

```python
def apply_diarization(audio_path, segments, config):
    """
    Apply speaker diarization if enabled.
    Gracefully skip on errors (token missing, OOM).
    """
    if not config['diarization']['enabled']:
        return segments

    backend = config['diarization']['backend']

    try:
        if backend == 'pyannote':
            diarization_result = pyannote_diarize(audio_path, config)
        elif backend == 'speechbrain':
            diarization_result = speechbrain_diarize(audio_path, config)
        else:
            log.warning(f"Unknown diarization backend: {backend}, skipping")
            return segments

        # Normalize labels to spk{A..Z}
        if config['diarization']['normalize_labels']:
            diarization_result = normalize_speaker_labels(diarization_result)

        # Assign speaker labels to segments
        return assign_speakers_to_segments(segments, diarization_result)

    except Exception as e:
        log.warning(f"Diarization failed: {e}, continuing without speaker labels")
        return segments


def normalize_speaker_labels(diarization_result):
    """
    Convert backend-specific labels to unified spkA, spkB, etc.
    """
    label_map = {}
    normalized = []

    for segment in diarization_result:
        original_label = segment['speaker']

        if original_label not in label_map:
            # Assign next letter
            label_map[original_label] = f"spk{chr(65 + len(label_map))}"  # 65 = 'A'

        segment['speaker'] = label_map[original_label]
        normalized.append(segment)

    return normalized
```

### 4.6 Phase 5: Format Writers

```python
def write_all_formats(segments, metadata, output_dir, config):
    """
    Generate all requested output formats.
    """
    formats = config['formats']
    output_files = []

    base_name = metadata['video_stem']

    # TXT
    if 'txt' in formats:
        txt_path = os.path.join(output_dir, f"{base_name}.txt")
        write_txt(segments, txt_path, config['post']['timestamps'])
        output_files.append(txt_path)

    # JSON
    if 'json' in formats:
        json_path = os.path.join(output_dir, f"{base_name}.json")
        write_json(segments, metadata, json_path)
        output_files.append(json_path)

    # SRT
    if 'srt' in formats:
        srt_path = os.path.join(output_dir, f"{base_name}.srt")
        srt_content = generate_srt(segments)
        validate_srt_monotonic(srt_content)  # Raises if invalid
        write_file(srt_path, srt_content)
        output_files.append(srt_path)

    # VTT
    if 'vtt' in formats:
        vtt_path = os.path.join(output_dir, f"{base_name}.vtt")
        write_vtt(segments, vtt_path)
        output_files.append(vtt_path)

    return output_files


def generate_srt(segments):
    """
    Generate SRT content with validation.

    Rules:
    - Strictly monotonic timestamps
    - No overlapping segments
    - Clamp gaps <50ms
    - Format: HH:MM:SS,mmm
    """
    srt_lines = []

    for i, segment in enumerate(segments):
        # Cue number
        srt_lines.append(str(i + 1))

        # Timestamps (clamp tiny gaps)
        start_ms = int(segment['start'] * 1000)
        end_ms = int(segment['end'] * 1000)

        if i > 0:
            prev_end_ms = int(segments[i-1]['end'] * 1000)
            gap_ms = start_ms - prev_end_ms
            if 0 < gap_ms < 50:
                start_ms = prev_end_ms  # Clamp gap

        start_time = format_srt_timestamp(start_ms)
        end_time = format_srt_timestamp(end_ms)

        srt_lines.append(f"{start_time} --> {end_time}")

        # Text (with speaker label if available)
        text = segment['text'].strip()
        if 'speaker' in segment:
            text = f"[{segment['speaker']}] {text}"
        srt_lines.append(text)

        # Blank line separator
        srt_lines.append("")

    return "\n".join(srt_lines)


def format_srt_timestamp(ms):
    """
    Format milliseconds as SRT timestamp: HH:MM:SS,mmm
    """
    hours = ms // 3600000
    ms %= 3600000
    minutes = ms // 60000
    ms %= 60000
    seconds = ms // 1000
    milliseconds = ms % 1000

    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def validate_srt_monotonic(srt_content):
    """
    Validate SRT timestamps are strictly monotonic and non-overlapping.
    Raises ValueError if validation fails.
    """
    lines = srt_content.strip().split('\n')
    prev_end_ms = 0

    for i in range(0, len(lines), 4):
        if i + 1 >= len(lines):
            break

        timestamp_line = lines[i + 1]
        if '-->' not in timestamp_line:
            continue

        start_str, end_str = timestamp_line.split(' --> ')
        start_ms = parse_srt_timestamp(start_str)
        end_ms = parse_srt_timestamp(end_str)

        # Check monotonic
        if start_ms < prev_end_ms:
            raise ValueError(f"SRT validation failed: timestamp overlap at cue {i//4 + 1}")

        # Check duration positive
        if end_ms <= start_ms:
            raise ValueError(f"SRT validation failed: non-positive duration at cue {i//4 + 1}")

        prev_end_ms = end_ms
```

### 4.7 Phase 6: Index Writing

```python
def write_index_shard(segments, metadata, output_file, config):
    """
    Write per-worker index shard.

    Filename: INDEX.<pid>.csv
    """
    import csv

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=INDEX_CSV_SCHEMA)
        writer.writeheader()

        for seg_idx, segment in enumerate(segments):
            # Truncate text to 512 chars for CSV
            text = segment['text'][:512]
            text_len = len(segment['text'])

            row = {
                'dataset': metadata['dataset'],
                'date': metadata['date'],
                'video_rel': metadata['video_rel'],
                'video_stem': metadata['video_stem'],
                'seg_idx': seg_idx,
                'ts_start_ms': int(segment['start'] * 1000),
                'ts_end_ms': int(segment['end'] * 1000),
                'text': text,
                'text_len': text_len,
                'lang': metadata.get('language', 'en'),
                'lang_conf': metadata.get('language_confidence', 0.0),
                'conf_avg': segment.get('avg_confidence', 0.0),
                'speaker': segment.get('speaker', ''),
                'format_mask': calculate_format_mask(config['formats']),
                'transcript_file': f"{metadata['video_stem']}.txt",
                'audio_file': f"{metadata['video_stem']}.wav" if config['audio']['keep_intermediate'] else '',
                'engine': f"{config['whisper']['engine']}:{config['whisper']['model_size']}:{config['whisper']['compute_type']}",
                'cuda_version': metadata.get('cuda_version', ''),
                'driver_version': metadata.get('driver_version', ''),
                'created_utc': datetime.utcnow().isoformat() + 'Z'
            }

            writer.writerow(row)


def merge_index_shards(shard_files, output_file):
    """
    Merge per-worker index shards into global INDEX.csv.

    Deduplication rule:
    - Composite key: (video_rel, seg_idx)
    - Keep latest created_utc on collision
    """
    import pandas as pd

    # Load all shards
    dfs = [pd.read_csv(f) for f in shard_files]
    combined = pd.concat(dfs, ignore_index=True)

    # Deduplicate by composite key
    combined = combined.sort_values('created_utc', ascending=False)
    combined = combined.drop_duplicates(subset=['video_rel', 'seg_idx'], keep='first')

    # Sort by date, video_stem, seg_idx
    combined = combined.sort_values(['date', 'video_stem', 'seg_idx'])

    # Write to output
    combined.to_csv(output_file, index=False)

    # Clean up shards
    for shard_file in shard_files:
        os.remove(shard_file)
```

---

## 5. Quality & Error Handling

### 5.1 Error Types

```python
class TranscriptionError(Exception):
    """Base exception for transcription errors."""
    pass

class FFmpegError(TranscriptionError):
    """Audio extraction failed."""
    pass

class DecodeError(TranscriptionError):
    """Whisper decode failed."""
    pass

class OOMError(TranscriptionError):
    """Out of GPU memory."""
    pass

class CorruptedError(TranscriptionError):
    """Container/stream corrupted."""
    pass

class NoAudioError(TranscriptionError):
    """No audio stream detected."""
    pass
```

### 5.2 Failed File Logging

```python
def write_failed_json(video_path, error_type, metadata, error_message=""):
    """
    Write detailed failure log for video.

    Output: {video_stem}_FAILED.json
    """
    failed_info = {
        "video_path": str(video_path),
        "error_type": error_type,
        "error_message": error_message,
        "ffprobe_metadata": metadata,
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }

    video_stem = Path(video_path).stem
    output_path = Path(video_path).parent / f"{video_stem}_FAILED.json"

    with open(output_path, 'w') as f:
        json.dump(failed_info, f, indent=2)
```

### 5.3 Resume Safety

```python
def should_skip_video(video_path, output_dir, force=False):
    """
    Check if video should be skipped (already transcribed).

    Returns: True if should skip, False otherwise
    """
    if force:
        return False

    video_stem = Path(video_path).stem
    expected_files = [
        output_dir / f"{video_stem}.txt",
        output_dir / f"{video_stem}.json"
    ]

    # Skip if all expected files exist
    return all(f.exists() for f in expected_files)
```

---

## 6. Performance & Optimization

### 6.1 GPU Metrics Collection

```python
class GPUMonitor:
    """
    Monitor GPU utilization during transcription.

    Samples at 1-2 Hz, computes average.
    """
    def __init__(self, sampling_hz=2):
        import pynvml
        pynvml.nvmlInit()
        self.sampling_hz = sampling_hz
        self.samples = []
        self.running = False

    def start(self):
        """Start background monitoring thread."""
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop)
        self.thread.start()

    def _monitor_loop(self):
        """Sample GPU metrics periodically."""
        import pynvml
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)

        while self.running:
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)

            self.samples.append({
                'gpu_pct': util.gpu,
                'mem_pct': (mem.used / mem.total) * 100,
                'timestamp': time.time()
            })

            time.sleep(1.0 / self.sampling_hz)

    def stop(self):
        """Stop monitoring and return aggregated metrics."""
        self.running = False
        self.thread.join()

        if not self.samples:
            return {}

        avg_gpu_pct = sum(s['gpu_pct'] for s in self.samples) / len(self.samples)
        avg_mem_pct = sum(s['mem_pct'] for s in self.samples) / len(self.samples)

        return {
            'gpu_pct': round(avg_gpu_pct, 1),
            'mem_pct': round(avg_mem_pct, 1),
            'sampling_hz': self.sampling_hz,
            'sample_count': len(self.samples)
        }
```

### 6.2 Parallel Processing

```python
def process_videos_parallel(video_files, config):
    """
    Process multiple videos in parallel.

    Default: 3 workers (limits I/O contention)
    """
    from concurrent.futures import ProcessPoolExecutor, as_completed

    max_workers = config['parallel']['max_workers']
    results = []
    failed = []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_single_video, video, config): video
            for video in video_files
        }

        for future in as_completed(futures):
            video = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                log.error(f"Failed to process {video}: {e}")
                failed.append((video, str(e)))

    return results, failed
```

---

## 7. Testing & Validation

### 7.1 Unit Tests

```python
# Test 1: FFmpeg Command Builder
def test_ffmpeg_cmd_builder():
    config = {'audio': {'codec': 'pcm_s16le', 'sample_rate': 16000, 'channels': 1}}
    cmd = build_ffmpeg_cmd('input.mp4', 'output.wav', config)

    assert '-acodec' in cmd
    assert 'pcm_s16le' in cmd
    assert '-ar' in cmd
    assert '16000' in cmd

# Test 2: Segment Combiner
def test_segment_monotonic():
    segments = [
        {'start': 0.0, 'end': 5.0},
        {'start': 5.1, 'end': 10.0},
        {'start': 10.2, 'end': 15.0}
    ]
    assert is_monotonic(segments) == True

# Test 3: SRT Timecode Formatting
def test_srt_format():
    assert format_srt_timestamp(3661500) == "01:01:01,500"
    assert format_srt_timestamp(0) == "00:00:00,000"

# Test 4: Index Merger Deduplication
def test_index_merge_dedupe():
    shard1 = pd.DataFrame({
        'video_rel': ['a.mp4', 'b.mp4'],
        'seg_idx': [0, 0],
        'text': ['old', 'text'],
        'created_utc': ['2025-01-01T10:00:00Z', '2025-01-01T10:00:00Z']
    })
    shard2 = pd.DataFrame({
        'video_rel': ['a.mp4', 'c.mp4'],
        'seg_idx': [0, 0],
        'text': ['new', 'other'],
        'created_utc': ['2025-01-01T11:00:00Z', '2025-01-01T10:00:00Z']
    })

    merged = merge_shards([shard1, shard2])

    # Should keep 'new' for a.mp4 (latest timestamp)
    assert merged[merged['video_rel'] == 'a.mp4']['text'].iloc[0] == 'new'

# Test 5: Language Detection
def test_language_detection_stub():
    # Mock non-EN audio
    result = detect_language(mock_audio_spanish)
    assert result['lang'] == 'es'
    assert result['conf'] > 0.8

# Test 6: GPU Metrics
def test_gpu_metrics_mock():
    with mock.patch('pynvml.nvmlDeviceGetUtilizationRates') as mock_util:
        mock_util.return_value = MockUtilization(gpu=35, memory=42)

        monitor = GPUMonitor()
        monitor.start()
        time.sleep(2)
        metrics = monitor.stop()

        assert 'gpu_pct' in metrics
        assert metrics['gpu_pct'] > 0
```

### 7.2 Integration Smoke Test

```python
def test_smoke_integration():
    """
    1 short MP4 → WAV → transcript → INDEX.csv with ≥1 row
    """
    # Setup
    test_video = "test_data/sample_30sec.mp4"
    output_dir = "test_output/"
    config = load_default_config()

    # Execute pipeline
    result = process_single_video(test_video, config)

    # Validate outputs
    assert result['status'] == 'ok'
    assert Path(output_dir, "sample_30sec.txt").exists()
    assert Path(output_dir, "sample_30sec.json").exists()
    assert Path(output_dir, "sample_30sec.srt").exists()

    # Validate INDEX.csv
    index = pd.read_csv(Path(output_dir, "INDEX.csv"))
    assert len(index) >= 1

    # Validate timestamps monotonic
    assert (index['ts_start_ms'] < index['ts_end_ms']).all()

    # Validate GPU metrics present
    assert 'cuda_version' in result['summary']
    assert 'gpu_pct' in result['summary']['utilization']
```

### 7.3 Acceptance Checklist

✅ One short MP4 → TXT/JSON/SRT produced; INDEX.csv gains ≥1 row
✅ Timestamps strictly monotonic; SRT passes validator
✅ Results JSON includes GPU metrics, driver/CUDA, absolute paths
✅ Sharded index merge deduplicates by `(video_rel, seg_idx)`
✅ If `mode="vad"`, no fixed 30s slicing; segments variable-length, non-overlapping
✅ If `mode="fixed"`, no VAD preprocessing

---

## 8. Configuration

### 8.1 Default Parameters

```json
{
  "whisper": {
    "model_size": "base",
    "device": "auto",
    "compute_type": "auto",
    "batch_size": 8,
    "beam_size": 5,
    "language": "en",
    "detect_language": false,
    "task": "transcribe"
  },
  "audio": {
    "sample_rate": 16000,
    "channels": 1,
    "codec": "pcm_s16le",
    "format": "wav",
    "keep_intermediate": false
  },
  "segmentation": {
    "mode": "fixed",
    "chunk_length_sec": 30,
    "min_silence_gap_sec": 0.2,
    "vad_min_len_sec": 2,
    "vad_max_len_sec": 60
  },
  "diarization": {
    "enabled": false,
    "backend": "pyannote",
    "hf_token_env": "HF_TOKEN",
    "min_speakers": 1,
    "max_speakers": 10,
    "normalize_labels": true
  },
  "post": {
    "timestamps": true,
    "summarize": true,
    "categorize": true,
    "min_confidence": 0.5,
    "redact": {
      "enabled": false,
      "rules": ["phone", "email", "license_plate"]
    }
  },
  "output": {
    "formats": ["txt", "json", "srt"],
    "text_truncate_csv": 512
  },
  "parallel": {
    "max_workers": 3
  },
  "limits": {
    "max_duration_per_run_sec": 7200,
    "skip_if_silent": true
  }
}
```

---

## 9. Implementation Requirements

### 9.1 Dependencies

```
torch>=2.0
torchaudio>=2.0
faster-whisper>=1.0
pyannote.audio>=3.1
speechbrain>=0.5.15
psutil>=5.9
py-cpuinfo>=9.0
pynvml>=11.5
librosa>=0.10
soundfile>=0.12
pydub>=0.25
silero-vad>=4.0
numpy>=1.24
pandas>=2.0
scipy>=1.10
pysrt>=1.1.2
webvtt-py>=0.4.6
pyyaml>=6.0
python-dotenv>=1.0
click>=8.1
rich>=13
tqdm>=4.65
pytest>=7.4
pytest-asyncio>=0.21
```

### 9.2 Hard Guards

- **Roots validation**: If `roots` not provided or empty → hard fail with actionable message
- **Path discipline**: Do not touch `PROJECTS\\` root; require user subfolder before any write
- **Output scope**: Keep outputs inside user-specified CWD only
- **Op logging**: Log every op to `ops_log.ndjson`; register every artifact in results JSON
- **Test enforcement**: Enforce pytest JSON reporting for all Python deliverables
- **GPU preference**: Prefer GPU; record GPU metrics; CPU only if no GPU
- **Output format**: Always emit the 5 blocks in order and return absolute results file path
- **Segmentation mutual exclusion**: Enforce `mode="fixed"` XOR `mode="vad"`, never both
- **Path formatting**: No line-wrapped Windows paths; use `\\` everywhere in JSON/examples

---

## 10. Acceptance Criteria

A production-ready implementation must satisfy ALL of the following:

### 10.1 Functional Requirements

✅ Extract audio from MP4 files with FFmpeg retry matrix
✅ Support both fixed and VAD segmentation modes (mutually exclusive)
✅ Transcribe with faster-whisper using GPU acceleration (FP16, CUDA)
✅ Optionally perform speaker diarization (pyannote/speechbrain)
✅ Generate all requested formats (TXT, JSON, SRT, VTT)
✅ Create global INDEX.csv with segment-level metadata
✅ Write comprehensive results JSON with GPU metrics
✅ Handle errors gracefully (FFmpeg failures, OOM, corrupted files)
✅ Support resume (skip existing transcripts unless --force)

### 10.2 Quality Requirements

✅ SRT/VTT timestamps strictly monotonic, no overlaps
✅ Text truncated to 512 chars in INDEX.csv, full text in JSON
✅ GPU metrics captured: device, VRAM, utilization, CUDA/driver versions
✅ Failed files logged with detailed error information
✅ Index merge deduplicates by `(video_rel, seg_idx)`, keeps latest
✅ Speaker labels normalized to `spk{A..Z}` format

### 10.3 Performance Requirements

✅ GPU utilization 30-50% during transcription (base model)
✅ Processing speed ~1.5x realtime on RTX 4080 (base, FP16)
✅ Parallel processing: 3 workers default (configurable)
✅ Memory-efficient: audio segments cleaned after transcription

### 10.4 Testing Requirements

✅ 6 unit tests pass (FFmpeg cmd, segment combiner, SRT format, index merge, lang detect, GPU metrics)
✅ Integration smoke test passes (1 MP4 → all outputs + INDEX.csv)
✅ SRT validation passes (monotonic, no overlaps, proper formatting)
✅ pytest JSON report included in results

---

**END OF SPECIFICATION v2.0**

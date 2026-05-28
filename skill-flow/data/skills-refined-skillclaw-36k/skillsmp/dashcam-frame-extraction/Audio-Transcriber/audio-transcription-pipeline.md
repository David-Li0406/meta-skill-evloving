# **SKILL: Audio Transcription Pipeline v2 (DASHCAM_AUDIO_TRANSCRIBE)**

## **Purpose**
Extract audio from dashcam MP4s and produce GPU-accelerated timestamped transcripts with optional speaker diarization, daily/aggregate summaries, and centralized indexing. Optimized for NVIDIA GPU processing with automatic CPU fallback.

---

## **1. High-Level Behavior**

**Input**: One or more MP4 folders from dashcam structure
**Core Tasks**:
1. Audio extraction (FFmpeg with retry matrix) → WAV/FLAC @ 16kHz mono
2. Segmentation (fixed-length OR VAD-based, mutually exclusive)
3. GPU transcription (faster-whisper with CUDA, FP16)
4. Optional speaker diarization (pyannote.audio / SpeechBrain)
5. Normalization, punctuation, timestamp alignment
6. Centralized writing (TXT/JSON/SRT/VTT) + global INDEX.csv with deduplication

**Output Root**: `G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS\\`
- Per-video files: `.txt`, `.json`, `.srt`, `.vtt`
- Optional: extracted audio cache (`.wav` or `.flac`)
- Global `INDEX.csv` with segment-level metadata for search/cross-referencing
- Results JSON with GPU metrics, driver/CUDA versions, absolute paths

---

## **2. Skill Contract (Claude-Facing)**

### **2.1 Input JSON**
```json
{
  "mode": "transcribe_audio",
  "roots": [
    "G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Movie_F\\20250903"
  ],
  "output_dir": "G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS",
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

### **2.2 Output JSON**
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
    "index_csv": "G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS\\INDEX.csv",
    "output_dir": "G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS",
    "results_file": "G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS\\reports\\task_20250903_120000__results.json"
  },
  "notes": [
    "engine=faster-whisper(base, FP16, CUDA)",
    "formats=txt,json,srt",
    "segmentation=fixed(30s)"
  ]
}
```

### **2.3 CLI Parity**
```powershell
python -m transcribe.batch ^
  --roots "G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Movie_F\\20250903" ^
  --out "G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS" ^
  --engine faster-whisper --model base --device cuda --batch 8 --fp16 ^
  --segmentation fixed --chunk 30 --formats txt json srt ^
  --force --dry-run
```

---

## **3. File/Index Conventions**

### **3.1 Single Output Folder**
All transcripts → `…\\out\\ALL_TRANSCRIPTS\\`
Optional per-date subindexes allowed, but `INDEX.csv` is the source of truth.

### **3.2 Filename Pattern**
```
<date>__<video_stem>__t<start_ms>__d<dur_ms>__v<ver>
```

**Example**:
`20250903__20250903133516_059495B__t0__d3600000__v1.txt`

**Generated Files**:
- `….txt` – Plain text transcript with timestamps
- `….json` – Full segments with confidence scores, speaker labels
- `….srt` – SubRip subtitle format (HH:MM:SS,mmm)
- `….vtt` – WebVTT format (HH:MM:SS.mmm) (optional)
- `….wav` – Extracted audio (if `keep_intermediate=true`)

### **3.3 INDEX.csv (Global)**
One row per segment (default) for granular search. Composite key: `(video_rel, seg_idx)`.

| Column | Description |
|--------|-------------|
| `dataset` | Movie_F / Movie_R / Park_F / Park_R |
| `date` | YYYYMMDD (source folder) |
| `video_rel` | e.g., `20250903/20250903133516_059495B.MP4` |
| `video_stem` | `20250903133516_059495B` |
| `seg_idx` | 0-based segment index |
| `ts_start_ms` | Segment start milliseconds |
| `ts_end_ms` | Segment end milliseconds |
| `text` | Normalized transcript (**truncated to 512 chars**) |
| `text_len` | Full text length (chars) |
| `lang` | ISO code (e.g., `en`) |
| `lang_conf` | Language detection confidence (0-1) |
| `conf_avg` | Average token confidence (0-1) |
| `speaker` | Normalized speaker label (e.g., `spkA`) |
| `format_mask` | Bitmask: txt/json/srt/vtt |
| `transcript_file` | Basename (no path) |
| `audio_file` | Basename or empty if discarded |
| `engine` | e.g., `faster-whisper:base:fp16` |
| `cuda_version` | e.g., `12.1` |
| `driver_version` | e.g., `546.01` |
| `created_utc` | ISO 8601 timestamp |

**Concurrency**: Each worker writes `INDEX.<pid>.csv`, then merges → `INDEX.csv`.
**Merge Rule**: Deduplicate by `(video_rel, seg_idx)`; keep latest `created_utc`.

---

## **4. Architecture (GPU-First, Disk-Light)**

```
[Disk MP4s]
   │
   ▼
[FFprobe Preflight]
  Check duration, audio streams; skip corrupted → _FAILED.json
   │
   ▼
[Audio Extract with Retry Matrix]
  FFmpeg (PCM 16k mono → WAV)
  Fallback: FLAC codec, genpts, extended probe
   │
   ▼
[Segmentation Branch]
  ├─► [Fixed Mode] 30s chunks, no VAD
  └─► [VAD Mode] Silero VAD → 2-60s speech regions
   │
   ▼
[Transcription Engine]
  faster-whisper / whisper (CUDA, FP16, batch=8)
  Language detection (if enabled)
  Word-level timestamps
   │
   ├─► [Segments JSON] (timestamps, text, conf)
   │
   ├─► [Optional Diarization]
   │   pyannote/SpeechBrain → normalized spk{A..Z} labels
   │
   ├─► [Optional Redaction] regex-based PII removal
   │
   ├─► [TXT/SRT/VTT] serializers
   │   • SRT validator: monotonic, no overlaps, clamp <50ms gaps
   │   • VTT: correct decimal separator (.)
   │
   └─► [Shard Index Writer] INDEX.<pid>.csv
                            (segment rows, text truncated to 512 chars)
   │
   ▼
[Global Merge] → INDEX.csv
  Deduplicate by (video_rel, seg_idx), keep latest created_utc
```

**Notes**:
- If `keep_intermediate=false`, temp audio is memory-mapped or deleted after use
- Target ~1.5× realtime on base model (CUDA, FP16)
- GPU metrics sampled at 1-2 Hz during run; averaged to `utilization.gpu_pct`, `mem_pct`
- If `skip_if_silent=true` and VAD detects no speech → short-circuit with "no_speech" result row

---

## **5. Default Config & Rationale**

| Setting | Default | Rationale |
|---------|---------|-----------|
| **Engine** | `faster-whisper` | GPU-efficient, robust, faster than OpenAI Whisper |
| **Model** | `base` | Good accuracy/latency balance. Use `small`/`medium` for higher accuracy |
| **Audio** | mono 16 kHz PCM | Stable decoding; WAV primary, FLAC fallback |
| **Segmentation** | `fixed` (30s) | Simpler, robust; avoids double-slicing with VAD |
| **Formats** | txt, json, srt | VTT optional |
| **Parallel** | 3 workers | Limits I/O contention; CPU rarely bottleneck |
| **Diarization** | Off by default | Opt-in (requires pyannote HF token + VRAM) |
| **Language Detection** | Off by default | Enable for multilingual clips |

---

## **6. Segmentation Modes (Mutually Exclusive)**

### **6.1 Fixed Mode (Recommended)**
- Split audio into fixed 30s chunks (configurable)
- Whisper handles timestamp alignment internally
- No external VAD required
- **Use when**: Most clips have continuous speech or you want predictable processing time

### **6.2 VAD Mode (Advanced)**
- Use Silero VAD to create variable-length speech regions (2-60s)
- No fixed chunking applied
- Segments are non-overlapping
- **Use when**: Audio is very sparse (long silences) and you want to skip non-speech

**Enforcement**: If `segmentation.mode="vad"`, disable fixed `chunk_length_sec`. If `mode="fixed"`, skip VAD preprocessing.

---

## **7. Performance Targets (RTX 4080)**

| Metric | Target |
|--------|--------|
| **Speed** | ~1.5× realtime (base, FP16, batch=8) |
| **GPU Util** | 30–50% (transcription lighter than vision) |
| **Disk Growth** | Mostly text; audio temp deleted unless `keep_intermediate=true` |
| **Stability** | Handle long files (auto chunking, max 2h per run with resume) |
| **Resume Safety** | Skip existing transcripts unless `--force` |

---

## **8. GPU-First Execution**

- Auto-detect CUDA/NVIDIA; prefer GPU paths; CPU fallback only if GPU unavailable
- **Record in results JSON**:
  ```json
  {
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
    "torch_version": "2.2.0+cu121"
  }
  ```

**GPU Metrics Capture**:
- Use `pynvml` to sample GPU utilization at ~1-2 Hz during run
- Average `gpu_pct` and `mem_pct` over entire run
- Record driver version, CUDA version, torch version

**Min Dependencies** (compact list):
```
torch>=2.0
torchaudio>=2.0
faster-whisper>=1.0
openai-whisper==20231117
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

---

## **9. Error Handling & Resume Safety**

### **9.1 Resume Logic**
- If transcript exists (matching filename stem), **skip** unless `--force`
- Idempotent: re-running same command is safe

### **9.2 Per-Video Failures**
Write `{video_stem}_FAILED.json` with:
```json
{
  "video_path": "G:\\…\\video.mp4",
  "error_type": "ffmpeg_err",
  "error_message": "Failed to decode audio stream",
  "ffprobe_metadata": { "duration": null, "codec": "h264" },
  "timestamp": "2025-09-03T14:30:00Z"
}
```

**Error Types**:
- `ffmpeg_err`: Audio extraction failed
- `decode_err`: Whisper decode failed
- `OOM`: Out of memory (GPU)
- `corrupted`: Container/stream corrupted
- `no_audio`: No audio stream detected

### **9.3 FFmpeg Retry Matrix**
On failure, retry with:
1. **Codec fallback**: `pcm_s16le` → `flac`
2. **Demuxer args**: `-fflags +genpts -rw_timeout 30000000`
3. **Shorter probe**: `-analyzeduration 100M -probesize 100M`

### **9.4 Index Merge Deduplication**
- Composite key: `(video_rel, seg_idx)`
- On merge: deduplicate, keep latest `created_utc`
- Ensures idempotent shard merging

### **9.5 Edge Cases**
- **Very long videos (>2h)**: Enforce `max_duration_per_run_sec=7200`; resume from last checkpoint
- **Silent audio**: If `skip_if_silent=true` and VAD detects no speech → create "no_speech" result row, skip transcription
- **Corrupted containers**: FFprobe preflight; if duration missing → skip with `_FAILED.json`

---

## **10. Language Detection & Multilingual Support**

### **10.1 Language Detection**
- Set `whisper.detect_language=true` to enable per-file or per-segment language detection
- Records `lang` (ISO 639-1 code) and `lang_conf` (0-1) in INDEX.csv

### **10.2 Translation**
- If non-EN detected and `whisper.task="translate"` → translate to English
- Configurable: transcribe as-is or translate

**Example**:
```json
{
  "whisper": {
    "detect_language": true,
    "task": "transcribe"
  }
}
```

---

## **11. Speaker Diarization**

### **11.1 Backend Options**
- **pyannote**: State-of-the-art, requires HF auth token + VRAM
- **speechbrain**: Good performance, no authentication required

### **11.2 Token Handling**
- `diarization.hf_token_env="HF_TOKEN"` → read from environment variable
- If token missing or OOM → **skip diarization**, log soft warning, continue

### **11.3 Label Normalization**
- Different backends output different formats
- Normalize to `spk{A..Z}` per video
- Ensure `INDEX.csv.speaker` and `.json` use same labels

**Example**:
```json
{
  "diarization": {
    "enabled": true,
    "backend": "pyannote",
    "hf_token_env": "HF_TOKEN",
    "normalize_labels": true
  }
}
```

---

## **12. SRT/VTT Correctness**

### **12.1 SRT Format**
- Timecode: `HH:MM:SS,mmm` (comma separator)
- Cues must be strictly monotonic
- No overlapping segments
- Clamp tiny gaps (<50 ms) to prevent validation errors

### **12.2 VTT Format**
- Timecode: `HH:MM:SS.mmm` (period separator)
- Same monotonic/non-overlapping requirements

### **12.3 Unit Tests**
- Validate cue ordering
- Check for boundary overlaps
- Verify timecode formatting

---

## **13. Privacy & Redaction**

### **13.1 Optional PII Redaction**
- Regex-based stub for phone, email, license plate patterns
- Disabled by default
- Can be extended with custom rules

**Example**:
```json
{
  "post": {
    "redact": {
      "enabled": true,
      "rules": ["phone", "email", "license_plate"]
    }
  }
}
```

### **13.2 Data Privacy**
- No telemetry or external calls
- All processing local
- Speaker profiles stored locally

---

## **14. Guardrails (Claude Skill)**

✅ **DO**:
- Normalize punctuation and spacing
- Include timestamps in all textual outputs if `timestamps=true`
- Truncate text to 512 chars in INDEX.csv; store full text in `.json`
- Record GPU metrics, driver/CUDA versions in results JSON
- Use pytest for all Python deliverables
- Validate SRT/VTT cue ordering and formatting
- Normalize speaker labels to `spk{A..Z}`

❌ **DO NOT**:
- Delete or overwrite source MP4s
- Attempt diarization without HF token (skip with warning)
- Modify the `PROJECTS/` base folder
- Run without user-specified subfolder
- Mix segmentation modes (fixed + VAD)

---

## **15. Testing & Verification**

### **15.1 Unit Tests** (High-Signal, Fast)

1. **FFmpeg Command Builder**
   - Test: Exact args for mono/16 kHz
   - Test: Retry toggles (codec fallback, demuxer args)

2. **Segment Combiner**
   - Test: Strictly monotonic timestamps
   - Test: Carryover across chunks

3. **SRT/VTT Serializer**
   - Test: Timecode formatting (comma vs period)
   - Test: No overlaps, clamp <50ms gaps

4. **Index Merger**
   - Test: Deduplicate by `(video_rel, seg_idx)`
   - Test: Shard → global with latest `created_utc`

5. **Language Detection**
   - Test: Stubbed non-EN clip picks correct path

6. **GPU Metrics**
   - Test: Mock NVML to ensure fields populate

### **15.2 Integration Smoke Test**
1 short MP4 → WAV → transcript → INDEX.csv with ≥1 row

**Checklist**:
- Timestamps strictly monotonic
- SRT passes validator (no overlaps)
- Language matches expected
- No missing segments
- GPU metrics present in results JSON

### **15.3 Acceptance Criteria (Tight)**

✅ One short MP4 → TXT/JSON/SRT produced; INDEX.csv gains ≥1 row
✅ Timestamps strictly monotonic; SRT passes validator
✅ Results JSON includes GPU metrics, driver/CUDA, absolute paths
✅ Sharded index merge deduplicates by `(video_rel, seg_idx)`
✅ If `mode="vad"`, no fixed 30s slicing; segments variable-length, non-overlapping
✅ If `mode="fixed"`, no VAD preprocessing

---

## **16. Example Invocations**

### **16.1 Single Day (Fixed Mode)**
```powershell
python -m transcribe.batch ^
  --roots "G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Movie_R\\20250903" ^
  --out "G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS" ^
  --engine faster-whisper --model base --device cuda --batch 8 --fp16 ^
  --segmentation fixed --chunk 30 --formats txt json srt
```

### **16.2 Two Days in Parallel (PowerShell)**
```powershell
$roots = @(
  "G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Movie_F\\20250903",
  "G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Movie_R\\20250903"
)
$OUT = "G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS"

foreach ($r in $roots) {
  Start-Process -NoNewWindow python -ArgumentList @(
    "-m", "transcribe.batch",
    "--roots", $r, "--out", $OUT,
    "--engine", "faster-whisper", "--model", "base", "--device", "cuda",
    "--batch", "8", "--fp16", "--segmentation", "fixed", "--chunk", "30",
    "--formats", "txt", "json", "srt"
  )
}
```

### **16.3 VAD Mode (Sparse Audio)**
```powershell
python -m transcribe.batch ^
  --roots "G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Park_F\\20250903" ^
  --out "G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS" ^
  --engine faster-whisper --model base --device cuda --batch 8 --fp16 ^
  --segmentation vad --vad-min 2 --vad-max 60 --formats txt json srt
```

### **16.4 With Diarization**
```powershell
$env:HF_TOKEN = "hf_..."
python -m transcribe.batch ^
  --roots "G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Movie_F\\20250903" ^
  --out "G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS" ^
  --engine faster-whisper --model base --device cuda --batch 8 --fp16 ^
  --segmentation fixed --chunk 30 --formats txt json srt ^
  --diarize --diarize-backend pyannote
```

---

## **17. Results File (Single Source of Truth)**

Write one consolidated file **per task**: `reports\\{task_id}__results.json` (under CWD)

**Must Contain**:
- Task metadata (ID, timestamp, objective)
- All ops executed (from `ops_log.ndjson`)
- Artifacts with `{path, absolute_path, bytes, sha256, created_ts}`
- GPU metrics (device name, VRAM, utilization, driver/CUDA versions)
- pytest summary (if Python code generated)
- Planned checks and outcomes
- `failed_files` list with reasons

**Example Absolute Path**:
`G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS\\reports\\task_20250903_120000__results.json`

**COMPLETION_REPORT must include the absolute Windows path** to this file.

---

## **18. Example Claude Invoke (Natural Language → JSON)**

**User**: "Transcribe all front dashcam videos from Sep 3 with diarization, keep timestamps, output txt/json/srt into the single transcripts folder, and give me a summary."

**Claude produces**:
```json
{
  "mode": "transcribe_audio",
  "roots": ["G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Movie_F\\20250903"],
  "output_dir": "G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS",
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
    "min_silence_gap_sec": 0.2
  },
  "diarization": {
    "enabled": true,
    "backend": "pyannote",
    "hf_token_env": "HF_TOKEN",
    "normalize_labels": true
  },
  "post": {
    "timestamps": true,
    "summarize": true,
    "categorize": true,
    "min_confidence": 0.5
  },
  "formats": ["txt", "json", "srt"],
  "parallel": { "max_workers": 3 },
  "limits": {
    "max_duration_per_run_sec": 7200,
    "skip_if_silent": true
  }
}
```

---

## **19. COMPLETION_REPORT (Example)**

```json
{
  "envelope_type": "completion_report",
  "timestamp": "2025-09-03T14:30:00Z",
  "manager_id": "worker_executor",
  "content": {
    "objective_achieved": true,
    "tasks_completed": 1,
    "results_file": "G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS\\reports\\task_20250903_120000__results.json",
    "evidence_collected": [
      "G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS\\INDEX.csv",
      "G:\\My Drive\\PROJECTS\\AudioTranscription\\out\\ALL_TRANSCRIPTS\\20250903__20250903133516_059495B__t0__d3600000__v1.txt"
    ],
    "notes": "Executed 15 videos; GPU metrics recorded (RTX 4080, CUDA 12.1, driver 546.01); tests passed; formats=txt,json,srt; segmentation=fixed(30s); diarization=pyannote(spkA,spkB)."
  }
}
```

---

## **20. HARD GUARDS (One-Liners)**

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

**END OF SKILL SPECIFICATION v2**

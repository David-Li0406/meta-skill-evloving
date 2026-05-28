# Audio Transcription Scripts

This folder contains complete Python implementation scripts for the audio transcription pipeline, copied from the working AudioTranscription project.

## 🔧 Core Processing Scripts

### batch_orchestrator.py (28 KB)
**Purpose**: Main batch processing orchestrator - coordinates entire transcription pipeline.

**Key Functions**:
- Multi-file batch processing with parallel workers
- Progress tracking and resumption
- Error handling and retry logic
- Results aggregation and reporting

**Usage**:
```python
from batch_orchestrator import BatchOrchestrator

orchestrator = BatchOrchestrator(config)
results = orchestrator.process_batch(video_files)
```

---

### audio_extractor.py (11 KB)
**Purpose**: FFmpeg wrapper with retry matrix for robust audio extraction.

**Key Functions**:
- `extract_audio(video_path, output_path)` - Extract audio with retry logic
- Codec fallback (PCM → FLAC)
- Demuxer args for corrupted files
- Extended probe for edge cases

**Usage**:
```python
from audio_extractor import AudioExtractor

extractor = AudioExtractor()
audio_path = extractor.extract(video_path, sample_rate=16000, channels=1)
```

---

### transcriber.py (15 KB)
**Purpose**: Whisper transcription engine with GPU optimization.

**Key Functions**:
- `transcribe(audio_path, model_size, device)` - Main transcription
- Word-level timestamp generation
- Language detection
- Confidence scoring per segment

**Usage**:
```python
from transcriber import Transcriber

transcriber = Transcriber(model="base", device="cuda")
segments = transcriber.transcribe(audio_path)
```

---

### gpu_pipeline.py (23 KB)
**Purpose**: GPU-optimized transcription pipeline with CUDA acceleration.

**Key Functions**:
- Batch processing with optimal GPU utilization
- Memory management (FP16, batch sizing)
- GPU metrics collection (pynvml)
- Automatic CPU fallback

**Usage**:
```python
from gpu_pipeline import GPUPipeline

pipeline = GPUPipeline(config)
results = pipeline.process_audio(audio_files)
```

---

### hardware_optimizer.py (20 KB)
**Purpose**: Hardware detection and optimization for GPU/CPU.

**Key Functions**:
- `detect_gpu()` - CUDA device detection
- `optimize_batch_size()` - Dynamic batch size based on VRAM
- `get_gpu_metrics()` - Utilization, memory, temperature
- CPU core count and optimization

**Usage**:
```python
from hardware_optimizer import HardwareOptimizer

optimizer = HardwareOptimizer()
optimal_config = optimizer.optimize(base_config)
```

---

## 🎤 Audio Processing Scripts

### vad.py (14 KB)
**Purpose**: Voice Activity Detection using Silero VAD.

**Key Functions**:
- `detect_speech_regions(audio_path)` - Detect speech timestamps
- Silence removal
- Variable-length speech segmentation (2-60s)

**Usage**:
```python
from vad import VADProcessor

vad = VADProcessor()
speech_regions = vad.detect(audio_path)
```

---

### diarizer.py (17 KB)
**Purpose**: Speaker diarization with pyannote/SpeechBrain backends.

**Key Functions**:
- `diarize(audio_path, backend)` - Identify speakers
- Label normalization (spkA, spkB, etc.)
- Graceful fallback on errors (token missing, OOM)

**Usage**:
```python
from diarizer import Diarizer

diarizer = Diarizer(backend="pyannote")
speaker_labels = diarizer.diarize(audio_path)
```

---

### speaker_manager.py (19 KB)
**Purpose**: Speaker profile management and identification.

**Key Functions**:
- Speaker enrollment from audio samples
- Vector embeddings and similarity matching
- Profile persistence and loading

**Usage**:
```python
from speaker_manager import SpeakerManager

manager = SpeakerManager()
manager.enroll_speaker("Alice", audio_samples)
speaker_id = manager.identify(unknown_audio)
```

---

## 📝 Output & Export Scripts

### exporters.py (15 KB)
**Purpose**: Multi-format transcript writers (TXT, JSON, SRT, VTT).

**Key Functions**:
- `write_txt(segments, output_path)` - Plain text with timestamps
- `write_json(segments, metadata, output_path)` - Complete metadata
- `write_srt(segments, output_path)` - SubRip subtitles
- `write_vtt(segments, output_path)` - WebVTT format
- SRT/VTT validation (monotonic timestamps, no overlaps)

**Usage**:
```python
from exporters import ExportManager

exporter = ExportManager()
exporter.write_all_formats(segments, output_dir, formats=["txt", "json", "srt"])
```

---

## ⚙️ Configuration & Utilities

### config.py (6 KB)
**Purpose**: Configuration management and validation.

**Key Functions**:
- Load/save YAML/JSON configs
- Preset application (speed, balanced, accuracy)
- Parameter validation

**Usage**:
```python
from config import Config

config = Config.load("config.yaml")
config.apply_preset("balanced")
```

---

### pipeline.py (17 KB)
**Purpose**: High-level transcription pipeline abstraction.

**Key Functions**:
- End-to-end processing (extract → transcribe → export)
- Automatic mode selection (GPU/CPU)
- Progress callbacks

**Usage**:
```python
from pipeline import TranscriptionPipeline

pipeline = TranscriptionPipeline(config)
results = pipeline.process(video_files)
```

---

### validation.py (11 KB)
**Purpose**: Input validation and prerequisite checks.

**Key Functions**:
- `validate_inputs(config)` - Pre-flight validation
- `check_ffmpeg_installed()` - FFmpeg availability
- `check_gpu_available()` - CUDA detection
- `auto_discover_videos()` - Video folder discovery

**Usage**:
```python
from validation import validate_inputs, get_gpu_info

is_valid, errors = validate_inputs(config)
gpu_info = get_gpu_info()
```

---

## 🚀 Ready-to-Run Scripts

### optimized_transcribe_gpu.py (16 KB)
**Purpose**: Standalone GPU-optimized transcription script.

**Usage**:
```bash
python optimized_transcribe_gpu.py \
  --input video.mp4 \
  --output ./transcripts \
  --model base \
  --device cuda
```

---

### fast_transcribe.py (17 KB)
**Purpose**: Fast transcription with minimal dependencies.

**Usage**:
```bash
python fast_transcribe.py \
  --folder C:\CARDV\Movie_F\20250903 \
  --formats txt json srt
```

---

## 📦 Dependencies

Install all requirements:
```bash
# GPU-accelerated (recommended)
pip install -r ../requirements_gpu.txt

# CPU-only fallback
pip install -r ../requirements.txt
```

**Key Packages**:
- `torch>=2.0`, `torchaudio>=2.0` - PyTorch with CUDA support
- `faster-whisper>=1.0` - Optimized Whisper inference
- `pyannote.audio>=3.1` - Speaker diarization (requires HF token)
- `speechbrain>=0.5.15` - Alternative diarization backend
- `pynvml>=11.5` - GPU metrics collection
- `silero-vad>=4.0` - Voice activity detection
- `librosa>=0.10`, `soundfile>=0.12` - Audio processing

---

## 🧪 Testing

Run validation check:
```bash
python validation.py
```

Test GPU detection:
```bash
python hardware_optimizer.py
```

Smoke test transcription:
```bash
python fast_transcribe.py --input test_video.mp4 --output ./test_output
```

---

## 📚 Complete Script Inventory

| Script | Size | Purpose |
|--------|------|---------|
| `batch_orchestrator.py` | 28 KB | Main batch processor |
| `gpu_pipeline.py` | 23 KB | GPU-optimized pipeline |
| `hardware_optimizer.py` | 20 KB | Hardware detection & optimization |
| `speaker_manager.py` | 19 KB | Speaker profiles & identification |
| `pipeline.py` | 17 KB | High-level pipeline abstraction |
| `diarizer.py` | 17 KB | Speaker diarization |
| `optimized_transcribe_gpu.py` | 16 KB | Standalone GPU script |
| `fast_transcribe.py` | 17 KB | Fast standalone script |
| `transcriber.py` | 15 KB | Whisper transcription engine |
| `exporters.py` | 15 KB | Multi-format writers |
| `vad.py` | 14 KB | Voice activity detection |
| `audio_extractor.py` | 11 KB | FFmpeg wrapper |
| `validation.py` | 11 KB | Input validation |
| `config.py` | 6 KB | Configuration management |

**Total: 14 production-ready scripts, ~213 KB of implementation code**

---

## 🎯 Quick Start Examples

### Example 1: Process Single Day
```python
from batch_orchestrator import BatchOrchestrator
from config import Config

config = Config.load("../assets/config.yaml")
config.roots = ["C:\\CARDV\\Movie_F\\20250903"]

orchestrator = BatchOrchestrator(config)
results = orchestrator.process_batch()

print(f"✅ Processed {results['videos_processed']} videos")
print(f"   Transcripts: {results['output_dir']}")
```

### Example 2: GPU-Optimized Batch
```python
from gpu_pipeline import GPUPipeline
from hardware_optimizer import HardwareOptimizer

optimizer = HardwareOptimizer()
config = optimizer.optimize(base_config)

pipeline = GPUPipeline(config)
results = pipeline.process_folder("C:\\CARDV\\Movie_F\\20250903")
```

### Example 3: With Speaker Diarization
```python
from pipeline import TranscriptionPipeline
from config import Config

config = Config.load("../assets/config.yaml")
config.diarization.enabled = True
config.diarization.backend = "pyannote"

pipeline = TranscriptionPipeline(config)
results = pipeline.process(video_files)
```

---

## 🔍 Architecture Overview

```
User Request
   │
   ▼
validation.py (check prerequisites)
   │
   ▼
batch_orchestrator.py (coordinate processing)
   │
   ├──► audio_extractor.py (FFmpeg → WAV)
   │
   ├──► vad.py (optional speech detection)
   │
   ├──► gpu_pipeline.py / transcriber.py
   │    (Whisper transcription)
   │
   ├──► diarizer.py (optional speaker labels)
   │
   └──► exporters.py (TXT/JSON/SRT/VTT)
        │
        └──► INDEX.csv + results JSON
```

---

**Status**: Complete production implementation from working AudioTranscription project
**Last Updated**: 2025-10-26
**Total Scripts**: 14 core modules + 2 standalone runners

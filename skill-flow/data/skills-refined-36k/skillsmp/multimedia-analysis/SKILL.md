---
name: multimedia_analysis
description: 動画・音声ファイルの内容、メタデータ、およびストリーム情報の分析を行う
---

# Multimedia Analysis

Analyze video and audio files by combining programming approaches with tools such as `ffmpeg`.

## 1. Retrieval of Metadata and Stream Information
*   Execute `ffmpeg` or `ffprobe` via `run_command` to check codecs, bitrates, frame rates, sampling frequencies, duration, etc.
*   `ffprobe -v error -show_format -show_streams -of json <filename>`

## 2. Audio Signal Analysis
*   Use libraries like `librosa`, `scipy.io.wavfile`, or `pydub` to extract waveforms, spectrograms, RMS levels, fundamental frequencies, etc.
*   **Note**: Propose and execute `pip install` as needed.

## 3. Video Frame Analysis
*   Use `OpenCV (cv2)` or `MoviePy` to extract frames at specific timestamps or perform image processing (e.g., brightness changes, motion detection).
*   Save extracted frames as images and consider having the AI visually inspect them (if the model supports image input) to read metadata or other information.

## 4. Transcription and Summarization (APIs / Libraries)
*   If text needs to be extracted from audio data, consider using libraries (e.g., `SpeechRecognition`) or external APIs.

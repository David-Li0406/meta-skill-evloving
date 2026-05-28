"""Voice Activity Detection and audio chunking module."""

import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import torch
import torchaudio
from dataclasses import dataclass
import soundfile as sf

logger = logging.getLogger(__name__)


@dataclass
class SpeechSegment:
    """Represents a speech segment detected by VAD."""
    start: float
    end: float
    confidence: float
    
    @property
    def duration(self) -> float:
        return self.end - self.start


class VADProcessor:
    """Voice Activity Detection processor with Silero VAD."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize VAD processor."""
        self.config = config
        self.backend = config.get('vad.backend', 'silero')
        self.threshold = config.get('vad.threshold', 0.5)
        self.min_speech_duration_ms = config.get('vad.min_speech_duration_ms', 250)
        self.min_silence_duration_ms = config.get('vad.min_silence_duration_ms', 1000)
        self.speech_pad_ms = config.get('vad.speech_pad_ms', 30)
        self.window_size_samples = config.get('vad.window_size_samples', 512)
        self.max_chunk_duration_s = config.get('vad.max_chunk_duration_s', 600)
        
        self.model = None
        self.utils = None
        
        # Load VAD model
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the VAD model."""
        if self.backend == 'silero':
            self._load_silero_vad()
        else:
            raise ValueError(f"Unsupported VAD backend: {self.backend}")
    
    def _load_silero_vad(self) -> None:
        """Load Silero VAD model."""
        try:
            # Load Silero VAD
            model, utils = torch.hub.load(
                repo_or_dir='snakers4/silero-vad',
                model='silero_vad',
                force_reload=False,
                onnx=False
            )
            
            self.model = model
            self.utils = utils
            
            # Get utility functions
            (self.get_speech_timestamps,
             self.save_audio,
             self.read_audio,
             self.VADIterator,
             self.collect_chunks) = utils
            
            logger.info("Silero VAD model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading Silero VAD: {str(e)}")
            raise
    
    def detect_speech(
        self,
        audio_path: Path,
        return_seconds: bool = True
    ) -> List[SpeechSegment]:
        """
        Detect speech segments in audio file.
        
        Args:
            audio_path: Path to audio file
            return_seconds: Return timestamps in seconds (vs samples)
            
        Returns:
            List of speech segments
        """
        try:
            # Read audio
            wav = self.read_audio(str(audio_path), sampling_rate=16000)
            
            # Get speech timestamps
            speech_timestamps = self.get_speech_timestamps(
                wav,
                self.model,
                threshold=self.threshold,
                min_speech_duration_ms=self.min_speech_duration_ms,
                min_silence_duration_ms=self.min_silence_duration_ms,
                speech_pad_ms=self.speech_pad_ms,
                return_seconds=return_seconds
            )
            
            # Convert to SpeechSegment objects
            segments = []
            for ts in speech_timestamps:
                segment = SpeechSegment(
                    start=ts['start'],
                    end=ts['end'],
                    confidence=ts.get('confidence', 1.0)
                )
                segments.append(segment)
            
            logger.info(f"Detected {len(segments)} speech segments in {audio_path}")
            return segments
            
        except Exception as e:
            logger.error(f"Error detecting speech in {audio_path}: {str(e)}")
            return []
    
    def chunk_audio(
        self,
        audio_path: Path,
        output_dir: Path,
        max_duration: Optional[float] = None,
        use_vad: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Chunk audio file into smaller segments.
        
        Args:
            audio_path: Path to input audio file
            output_dir: Directory for output chunks
            max_duration: Maximum chunk duration in seconds
            use_vad: Use VAD to find natural breaks
            
        Returns:
            List of chunk information dictionaries
        """
        max_duration = max_duration or self.max_chunk_duration_s
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Read audio info
        audio_info = sf.info(str(audio_path))
        total_duration = audio_info.duration
        sample_rate = audio_info.samplerate
        
        chunks = []
        
        if total_duration <= max_duration:
            # No chunking needed
            return [{
                'path': audio_path,
                'start': 0.0,
                'end': total_duration,
                'duration': total_duration,
                'index': 0
            }]
        
        if use_vad:
            # Use VAD to find natural breaks
            segments = self.detect_speech(audio_path, return_seconds=True)
            chunks = self._chunk_by_vad(
                audio_path,
                segments,
                output_dir,
                max_duration
            )
        else:
            # Simple time-based chunking
            chunks = self._chunk_by_time(
                audio_path,
                output_dir,
                max_duration,
                total_duration
            )
        
        return chunks
    
    def _chunk_by_vad(
        self,
        audio_path: Path,
        segments: List[SpeechSegment],
        output_dir: Path,
        max_duration: float
    ) -> List[Dict[str, Any]]:
        """Chunk audio using VAD segments."""
        chunks = []
        current_chunk_segments = []
        current_duration = 0
        chunk_index = 0
        
        for segment in segments:
            segment_duration = segment.duration
            
            # Check if adding this segment exceeds max duration
            if current_duration + segment_duration > max_duration and current_chunk_segments:
                # Save current chunk
                chunk_info = self._save_chunk(
                    audio_path,
                    output_dir,
                    chunk_index,
                    current_chunk_segments
                )
                chunks.append(chunk_info)
                
                # Start new chunk
                current_chunk_segments = [segment]
                current_duration = segment_duration
                chunk_index += 1
            else:
                # Add to current chunk
                current_chunk_segments.append(segment)
                current_duration += segment_duration
        
        # Save final chunk
        if current_chunk_segments:
            chunk_info = self._save_chunk(
                audio_path,
                output_dir,
                chunk_index,
                current_chunk_segments
            )
            chunks.append(chunk_info)
        
        return chunks
    
    def _chunk_by_time(
        self,
        audio_path: Path,
        output_dir: Path,
        max_duration: float,
        total_duration: float
    ) -> List[Dict[str, Any]]:
        """Simple time-based chunking."""
        chunks = []
        chunk_index = 0
        current_time = 0
        
        while current_time < total_duration:
            chunk_start = current_time
            chunk_end = min(current_time + max_duration, total_duration)
            
            # Extract chunk
            chunk_path = output_dir / f"chunk_{chunk_index:04d}.wav"
            
            # Read and save chunk
            audio_data, sr = sf.read(
                str(audio_path),
                start=int(chunk_start * 16000),
                stop=int(chunk_end * 16000)
            )
            sf.write(str(chunk_path), audio_data, sr)
            
            chunks.append({
                'path': chunk_path,
                'start': chunk_start,
                'end': chunk_end,
                'duration': chunk_end - chunk_start,
                'index': chunk_index
            })
            
            current_time = chunk_end
            chunk_index += 1
        
        return chunks
    
    def _save_chunk(
        self,
        audio_path: Path,
        output_dir: Path,
        chunk_index: int,
        segments: List[SpeechSegment]
    ) -> Dict[str, Any]:
        """Save audio chunk from segments."""
        if not segments:
            return None
        
        # Get chunk boundaries
        chunk_start = segments[0].start
        chunk_end = segments[-1].end
        
        # Add padding
        pad_seconds = self.speech_pad_ms / 1000.0
        chunk_start = max(0, chunk_start - pad_seconds)
        
        # Read audio chunk
        audio_data, sr = sf.read(
            str(audio_path),
            start=int(chunk_start * 16000),
            stop=int(chunk_end * 16000)
        )
        
        # Save chunk
        chunk_path = output_dir / f"chunk_{chunk_index:04d}.wav"
        sf.write(str(chunk_path), audio_data, sr)
        
        return {
            'path': chunk_path,
            'start': chunk_start,
            'end': chunk_end,
            'duration': chunk_end - chunk_start,
            'index': chunk_index,
            'segments': len(segments)
        }
    
    def merge_chunks(
        self,
        chunk_results: List[Dict[str, Any]],
        gap_threshold: float = 0.5
    ) -> Dict[str, Any]:
        """
        Merge chunk results back into single transcript.
        
        Args:
            chunk_results: List of transcription results from chunks
            gap_threshold: Maximum gap between segments to merge
            
        Returns:
            Merged transcription result
        """
        all_segments = []
        all_text = []
        
        for chunk in chunk_results:
            chunk_start = chunk.get('chunk_start', 0)
            segments = chunk.get('segments', [])
            
            for segment in segments:
                # Adjust segment timing
                adjusted_segment = segment.copy()
                adjusted_segment['start'] += chunk_start
                adjusted_segment['end'] += chunk_start
                
                # Adjust word timings if present
                if 'words' in adjusted_segment:
                    for word in adjusted_segment['words']:
                        word['start'] += chunk_start
                        word['end'] += chunk_start
                
                all_segments.append(adjusted_segment)
                all_text.append(segment['text'])
        
        # Sort segments by start time
        all_segments.sort(key=lambda x: x['start'])
        
        # Merge consecutive segments if gap is small
        merged_segments = []
        current_segment = None
        
        for segment in all_segments:
            if current_segment is None:
                current_segment = segment
            elif segment['start'] - current_segment['end'] <= gap_threshold:
                # Merge segments
                current_segment['end'] = segment['end']
                current_segment['text'] += ' ' + segment['text']
                if 'words' in current_segment and 'words' in segment:
                    current_segment['words'].extend(segment['words'])
            else:
                # Save current and start new
                merged_segments.append(current_segment)
                current_segment = segment
        
        if current_segment:
            merged_segments.append(current_segment)
        
        # Create merged result
        merged_result = {
            'text': ' '.join(all_text),
            'segments': merged_segments,
            'chunks_processed': len(chunk_results)
        }
        
        return merged_result
    
    def remove_silence(
        self,
        audio_path: Path,
        output_path: Path,
        min_silence_len: float = 0.5
    ) -> Tuple[Path, List[Tuple[float, float]]]:
        """
        Remove silence from audio file.
        
        Args:
            audio_path: Input audio file
            output_path: Output audio file
            min_silence_len: Minimum silence length to remove
            
        Returns:
            Tuple of (output_path, list of removed silence regions)
        """
        # Detect speech segments
        segments = self.detect_speech(audio_path, return_seconds=False)
        
        if not segments:
            logger.warning(f"No speech detected in {audio_path}")
            return audio_path, []
        
        # Read audio
        wav = self.read_audio(str(audio_path), sampling_rate=16000)
        
        # Collect speech chunks
        speech_chunks = self.collect_chunks(
            [{'start': s.start, 'end': s.end} for s in segments],
            wav
        )
        
        # Concatenate chunks
        concatenated = torch.cat(speech_chunks)
        
        # Save
        torchaudio.save(str(output_path), concatenated.unsqueeze(0), 16000)
        
        # Calculate removed regions
        removed_regions = []
        prev_end = 0
        
        for segment in segments:
            if segment.start - prev_end >= min_silence_len:
                removed_regions.append((prev_end, segment.start))
            prev_end = segment.end
        
        # Add final silence region if exists
        total_samples = len(wav)
        if total_samples - prev_end >= min_silence_len * 16000:
            removed_regions.append((prev_end / 16000, total_samples / 16000))
        
        logger.info(f"Removed {len(removed_regions)} silence regions from {audio_path}")
        return output_path, removed_regions
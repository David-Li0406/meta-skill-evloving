"""Audio extraction module using ffmpeg."""

import os
import json
import logging
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import ffmpeg
import numpy as np
import soundfile as sf
from tqdm import tqdm

logger = logging.getLogger(__name__)


class AudioExtractor:
    """Extract and process audio from video files using ffmpeg."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize audio extractor with configuration."""
        self.config = config
        self.sample_rate = config.get('audio.sample_rate', 16000)
        self.channels = config.get('audio.channels', 1)
        self.normalize = config.get('audio.normalize', True)
        self.denoise = config.get('audio.denoise', False)
        self.high_pass = config.get('audio.high_pass_filter', False)
        self.high_pass_freq = config.get('audio.high_pass_freq', 80)
        
    def probe_file(self, file_path: Path) -> Dict[str, Any]:
        """Probe video file for metadata using ffprobe."""
        try:
            probe = ffmpeg.probe(str(file_path))
            return probe
        except ffmpeg.Error as e:
            logger.error(f"Error probing file {file_path}: {e.stderr.decode()}")
            return {}
    
    def has_audio(self, file_path: Path) -> bool:
        """Check if video file contains audio stream."""
        probe_data = self.probe_file(file_path)
        if not probe_data:
            return False
        
        streams = probe_data.get('streams', [])
        for stream in streams:
            if stream.get('codec_type') == 'audio':
                return True
        return False
    
    def get_audio_info(self, file_path: Path) -> Dict[str, Any]:
        """Get detailed audio stream information."""
        probe_data = self.probe_file(file_path)
        if not probe_data:
            return {}
        
        audio_info = {
            'has_audio': False,
            'streams': [],
            'duration': None,
            'format': None
        }
        
        # Get format info
        format_info = probe_data.get('format', {})
        audio_info['duration'] = float(format_info.get('duration', 0))
        audio_info['format'] = format_info.get('format_name')
        
        # Get audio streams
        streams = probe_data.get('streams', [])
        for stream in streams:
            if stream.get('codec_type') == 'audio':
                audio_info['has_audio'] = True
                stream_info = {
                    'index': stream.get('index'),
                    'codec': stream.get('codec_name'),
                    'sample_rate': int(stream.get('sample_rate', 0)),
                    'channels': stream.get('channels'),
                    'bit_rate': stream.get('bit_rate'),
                    'duration': float(stream.get('duration', audio_info['duration']))
                }
                audio_info['streams'].append(stream_info)
        
        return audio_info
    
    def extract_audio(
        self,
        input_path: Path,
        output_path: Path,
        stream_index: Optional[int] = None,
        start_time: Optional[float] = None,
        duration: Optional[float] = None
    ) -> Tuple[bool, Optional[Path]]:
        """
        Extract audio from video file.
        
        Args:
            input_path: Path to input video file
            output_path: Path for output audio file
            stream_index: Specific audio stream index to extract
            start_time: Start time in seconds
            duration: Duration in seconds to extract
            
        Returns:
            Tuple of (success, output_path)
        """
        try:
            # Check if input has audio
            if not self.has_audio(input_path):
                logger.warning(f"No audio stream found in {input_path}")
                return False, None
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Build ffmpeg command
            stream = ffmpeg.input(str(input_path))
            
            # Apply time selection if specified
            if start_time is not None:
                stream = stream.filter('atrim', start=start_time, duration=duration)
            
            # Select specific audio stream if specified
            if stream_index is not None:
                stream = stream['a:' + str(stream_index)]
            else:
                stream = stream.audio
            
            # Apply audio filters
            filters = []
            
            # Resample to target sample rate
            if self.sample_rate:
                filters.append(f'aresample={self.sample_rate}')
            
            # Convert to mono if specified
            if self.channels == 1:
                filters.append('pan=mono|c0=0.5*c0+0.5*c1')
            
            # Apply high-pass filter if enabled
            if self.high_pass:
                filters.append(f'highpass=f={self.high_pass_freq}')
            
            # Apply denoising if enabled
            if self.denoise:
                filters.append('afftdn=nf=-25')
            
            # Apply loudness normalization if enabled
            if self.normalize:
                filters.append('loudnorm=I=-16:TP=-1.5:LRA=11')
            
            # Apply all filters
            if filters:
                stream = stream.filter('aformat', sample_fmts='s16', sample_rates=str(self.sample_rate))
                for filter_str in filters:
                    if '=' in filter_str:
                        parts = filter_str.split('=', 1)
                        stream = stream.filter(parts[0], parts[1])
                    else:
                        stream = stream.filter(filter_str)
            
            # Output to file
            stream = ffmpeg.output(
                stream,
                str(output_path),
                acodec='pcm_s16le',
                ar=self.sample_rate,
                ac=self.channels
            )
            
            # Run ffmpeg command
            ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
            
            logger.info(f"Successfully extracted audio from {input_path} to {output_path}")
            return True, output_path
            
        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error extracting audio from {input_path}: {e.stderr.decode()}")
            return False, None
        except Exception as e:
            logger.error(f"Unexpected error extracting audio from {input_path}: {str(e)}")
            return False, None
    
    def extract_batch(
        self,
        input_files: List[Path],
        output_dir: Path,
        skip_existing: bool = True
    ) -> Dict[Path, Path]:
        """
        Extract audio from multiple video files.
        
        Args:
            input_files: List of input video files
            output_dir: Directory for output audio files
            skip_existing: Skip if output file already exists
            
        Returns:
            Dictionary mapping input paths to output paths
        """
        results = {}
        
        for input_path in tqdm(input_files, desc="Extracting audio"):
            # Generate output filename
            output_name = input_path.stem + '.wav'
            output_path = output_dir / output_name
            
            # Skip if exists and skip_existing is True
            if skip_existing and output_path.exists():
                logger.info(f"Skipping existing file: {output_path}")
                results[input_path] = output_path
                continue
            
            # Extract audio
            success, extracted_path = self.extract_audio(input_path, output_path)
            if success:
                results[input_path] = extracted_path
            else:
                results[input_path] = None
        
        return results
    
    def split_long_audio(
        self,
        audio_path: Path,
        max_duration: float = 600.0,
        overlap: float = 1.0
    ) -> List[Tuple[Path, float, float]]:
        """
        Split long audio files into chunks.
        
        Args:
            audio_path: Path to audio file
            max_duration: Maximum chunk duration in seconds
            overlap: Overlap between chunks in seconds
            
        Returns:
            List of (chunk_path, start_time, end_time) tuples
        """
        # Get audio duration
        probe_data = self.probe_file(audio_path)
        if not probe_data:
            return []
        
        duration = float(probe_data['format'].get('duration', 0))
        if duration <= max_duration:
            return [(audio_path, 0, duration)]
        
        # Calculate chunks
        chunks = []
        chunk_dir = audio_path.parent / f"{audio_path.stem}_chunks"
        chunk_dir.mkdir(exist_ok=True)
        
        start_time = 0
        chunk_idx = 0
        
        while start_time < duration:
            end_time = min(start_time + max_duration, duration)
            chunk_path = chunk_dir / f"chunk_{chunk_idx:04d}.wav"
            
            # Extract chunk
            success, _ = self.extract_audio(
                audio_path,
                chunk_path,
                start_time=start_time,
                duration=end_time - start_time
            )
            
            if success:
                chunks.append((chunk_path, start_time, end_time))
            
            start_time = end_time - overlap if end_time < duration else duration
            chunk_idx += 1
        
        return chunks
    
    def normalize_audio_file(self, audio_path: Path, target_db: float = -20.0) -> bool:
        """
        Normalize audio file to target loudness.
        
        Args:
            audio_path: Path to audio file
            target_db: Target loudness in dB
            
        Returns:
            Success status
        """
        try:
            # Read audio
            audio_data, sr = sf.read(str(audio_path))
            
            # Calculate current RMS
            rms = np.sqrt(np.mean(audio_data**2))
            current_db = 20 * np.log10(rms) if rms > 0 else -np.inf
            
            # Calculate scaling factor
            target_rms = 10**(target_db / 20)
            scale_factor = target_rms / rms if rms > 0 else 1.0
            
            # Apply scaling
            normalized_audio = audio_data * scale_factor
            
            # Clip to prevent overflow
            normalized_audio = np.clip(normalized_audio, -1.0, 1.0)
            
            # Write back
            sf.write(str(audio_path), normalized_audio, sr)
            
            logger.info(f"Normalized {audio_path} from {current_db:.1f} dB to {target_db:.1f} dB")
            return True
            
        except Exception as e:
            logger.error(f"Error normalizing audio {audio_path}: {str(e)}")
            return False
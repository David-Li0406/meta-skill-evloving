"""ASR transcription module using faster-whisper."""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Iterator
from dataclasses import dataclass, asdict
import numpy as np
from faster_whisper import WhisperModel
from faster_whisper.vad import VadOptions
import torch

logger = logging.getLogger(__name__)


@dataclass
class Word:
    """Represents a transcribed word with timing."""
    text: str
    start: float
    end: float
    probability: float
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Segment:
    """Represents a transcribed segment."""
    id: int
    text: str
    start: float
    end: float
    words: List[Word]
    avg_logprob: float
    compression_ratio: float
    no_speech_prob: float
    temperature: float
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['words'] = [w.to_dict() if isinstance(w, Word) else w for w in self.words]
        return data


class Transcriber:
    """Transcribe audio using faster-whisper with GPU acceleration."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize transcriber with configuration."""
        self.config = config
        self.model = None
        self.model_size = config.get('asr.model', 'large-v3')
        self.device = config.get('asr.device', 'cuda')
        self.compute_type = config.get('asr.compute_type', 'float16')
        self.language = config.get('asr.language', 'en')
        self.task = config.get('asr.task', 'transcribe')
        
        # Load model
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the Whisper model with appropriate settings."""
        # Determine device and compute type
        if self.device == 'cuda' and not torch.cuda.is_available():
            logger.warning("CUDA requested but not available, falling back to CPU")
            self.device = 'cpu'
            self.compute_type = 'int8'
        
        # Adjust compute type for device
        if self.device == 'cpu' and self.compute_type in ['float16', 'int8_float16']:
            self.compute_type = 'int8'
        
        logger.info(f"Loading Whisper model: {self.model_size} on {self.device} with {self.compute_type}")
        
        try:
            # Get model path from config or use default
            model_path = self.config.get('paths.models_dir', './models')
            model_full_path = Path(model_path) / f"whisper-{self.model_size}"
            
            # Load model (will download if not present)
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
                download_root=model_path,
                local_files_only=False
            )
            
            logger.info(f"Successfully loaded Whisper model: {self.model_size}")
            
        except Exception as e:
            logger.error(f"Error loading Whisper model: {str(e)}")
            # Try fallback to smaller model
            if self.model_size != 'base':
                logger.info("Attempting to load base model as fallback")
                self.model_size = 'base'
                self.model = WhisperModel(
                    'base',
                    device=self.device,
                    compute_type=self.compute_type
                )
    
    def transcribe(
        self,
        audio_path: Path,
        language: Optional[str] = None,
        initial_prompt: Optional[str] = None,
        word_timestamps: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Transcribe audio file.
        
        Args:
            audio_path: Path to audio file
            language: Language code or None for auto-detection
            initial_prompt: Initial prompt to guide transcription
            word_timestamps: Whether to include word-level timestamps
            **kwargs: Additional arguments for transcribe method
            
        Returns:
            Dictionary containing transcription results
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Prepare VAD options
        vad_options = None
        if self.config.get('asr.vad_filter', True):
            vad_params = self.config.get('asr.vad_parameters', {})
            vad_options = VadOptions(
                threshold=vad_params.get('threshold', 0.5),
                min_speech_duration_ms=vad_params.get('min_speech_duration_ms', 250),
                max_speech_duration_s=vad_params.get('max_speech_duration_s', 0),
                min_silence_duration_ms=vad_params.get('min_silence_duration_ms', 2000),
                speech_pad_ms=vad_params.get('speech_pad_ms', 400)
            )
        
        # Transcription parameters
        params = {
            'language': language or self.language,
            'task': self.task,
            'beam_size': self.config.get('asr.beam_size', 5),
            'best_of': self.config.get('asr.best_of', 5),
            'patience': self.config.get('asr.patience', 1.0),
            'temperature': self.config.get('asr.temperature', [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]),
            'compression_ratio_threshold': 2.4,
            'log_prob_threshold': -1.0,
            'no_speech_threshold': 0.6,
            'word_timestamps': word_timestamps,
            'vad_filter': self.config.get('asr.vad_filter', True),
            'vad_parameters': vad_options,
            'initial_prompt': initial_prompt,
        }
        
        # Update with any additional kwargs
        params.update(kwargs)
        
        try:
            logger.info(f"Transcribing {audio_path}")
            
            # Perform transcription
            segments_gen, info = self.model.transcribe(str(audio_path), **params)
            
            # Process segments
            segments = []
            all_text = []
            
            for segment in segments_gen:
                # Extract words if available
                words = []
                if word_timestamps and hasattr(segment, 'words'):
                    for word in segment.words:
                        words.append(Word(
                            text=word.word,
                            start=word.start,
                            end=word.end,
                            probability=word.probability
                        ))
                
                # Create segment object
                seg = Segment(
                    id=segment.id,
                    text=segment.text.strip(),
                    start=segment.start,
                    end=segment.end,
                    words=words,
                    avg_logprob=segment.avg_logprob,
                    compression_ratio=segment.compression_ratio,
                    no_speech_prob=segment.no_speech_prob,
                    temperature=segment.temperature if hasattr(segment, 'temperature') else 1.0
                )
                
                segments.append(seg)
                all_text.append(seg.text)
            
            # Compile results
            result = {
                'text': ' '.join(all_text),
                'segments': [s.to_dict() for s in segments],
                'language': info.language if info else self.language,
                'language_probability': info.language_probability if info else 1.0,
                'duration': info.duration if info else None,
                'audio_file': str(audio_path),
                'model': self.model_size,
                'device': self.device,
                'word_timestamps': word_timestamps
            }
            
            logger.info(f"Transcription complete: {len(segments)} segments, {len(all_text)} words")
            return result
            
        except Exception as e:
            logger.error(f"Error transcribing {audio_path}: {str(e)}")
            raise
    
    def transcribe_with_progress(
        self,
        audio_path: Path,
        callback: Optional[callable] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Transcribe with progress callback.
        
        Args:
            audio_path: Path to audio file
            callback: Progress callback function(current, total, segment)
            **kwargs: Additional transcription arguments
            
        Returns:
            Transcription results
        """
        # Get audio duration for progress estimation
        import soundfile as sf
        audio_info = sf.info(str(audio_path))
        total_duration = audio_info.duration
        
        # Transcribe with generator
        params = kwargs.copy()
        params['language'] = params.get('language', self.language)
        params['task'] = self.task
        params['word_timestamps'] = params.get('word_timestamps', True)
        
        segments_gen, info = self.model.transcribe(str(audio_path), **params)
        
        segments = []
        all_text = []
        current_time = 0
        
        for segment in segments_gen:
            # Process segment
            words = []
            if params.get('word_timestamps') and hasattr(segment, 'words'):
                for word in segment.words:
                    words.append(Word(
                        text=word.word,
                        start=word.start,
                        end=word.end,
                        probability=word.probability
                    ))
            
            seg = Segment(
                id=segment.id,
                text=segment.text.strip(),
                start=segment.start,
                end=segment.end,
                words=words,
                avg_logprob=segment.avg_logprob,
                compression_ratio=segment.compression_ratio,
                no_speech_prob=segment.no_speech_prob,
                temperature=getattr(segment, 'temperature', 1.0)
            )
            
            segments.append(seg)
            all_text.append(seg.text)
            current_time = seg.end
            
            # Call progress callback
            if callback:
                callback(current_time, total_duration, seg)
        
        # Compile final results
        result = {
            'text': ' '.join(all_text),
            'segments': [s.to_dict() for s in segments],
            'language': info.language if info else self.language,
            'language_probability': info.language_probability if info else 1.0,
            'duration': info.duration if info else total_duration,
            'audio_file': str(audio_path),
            'model': self.model_size,
            'device': self.device,
            'word_timestamps': params.get('word_timestamps')
        }
        
        return result
    
    def batch_transcribe(
        self,
        audio_files: List[Path],
        batch_size: Optional[int] = None,
        **kwargs
    ) -> Dict[Path, Dict[str, Any]]:
        """
        Transcribe multiple audio files.
        
        Args:
            audio_files: List of audio file paths
            batch_size: Batch size for processing
            **kwargs: Additional transcription arguments
            
        Returns:
            Dictionary mapping file paths to transcription results
        """
        results = {}
        batch_size = batch_size or self.config.get('performance.batch_size', 1)
        
        # Process in batches (though faster-whisper processes one at a time)
        for i in range(0, len(audio_files), batch_size):
            batch = audio_files[i:i + batch_size]
            
            for audio_path in batch:
                try:
                    result = self.transcribe(audio_path, **kwargs)
                    results[audio_path] = result
                except Exception as e:
                    logger.error(f"Error transcribing {audio_path}: {str(e)}")
                    results[audio_path] = {'error': str(e)}
        
        return results
    
    def align_with_diarization(
        self,
        transcription: Dict[str, Any],
        diarization: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Align transcription segments with speaker diarization.
        
        Args:
            transcription: Transcription results
            diarization: List of diarization segments
            
        Returns:
            Merged transcription with speaker labels
        """
        segments = transcription.get('segments', [])
        
        # Create speaker timeline
        speaker_timeline = []
        for diar_seg in diarization:
            speaker_timeline.append({
                'start': diar_seg['start'],
                'end': diar_seg['end'],
                'speaker': diar_seg['speaker']
            })
        
        # Sort timeline by start time
        speaker_timeline.sort(key=lambda x: x['start'])
        
        # Align each transcription segment with speakers
        aligned_segments = []
        
        for segment in segments:
            seg_start = segment['start']
            seg_end = segment['end']
            seg_mid = (seg_start + seg_end) / 2
            
            # Find overlapping speaker segments
            speakers = []
            for speaker_seg in speaker_timeline:
                # Check for overlap
                if speaker_seg['end'] > seg_start and speaker_seg['start'] < seg_end:
                    overlap_start = max(seg_start, speaker_seg['start'])
                    overlap_end = min(seg_end, speaker_seg['end'])
                    overlap_duration = overlap_end - overlap_start
                    
                    speakers.append({
                        'speaker': speaker_seg['speaker'],
                        'overlap': overlap_duration
                    })
            
            # Assign speaker with maximum overlap
            if speakers:
                speakers.sort(key=lambda x: x['overlap'], reverse=True)
                segment['speaker'] = speakers[0]['speaker']
            else:
                segment['speaker'] = 'UNKNOWN'
            
            # Also align words if present
            if 'words' in segment and segment['words']:
                for word in segment['words']:
                    word_mid = (word['start'] + word['end']) / 2
                    word_speaker = 'UNKNOWN'
                    
                    for speaker_seg in speaker_timeline:
                        if speaker_seg['start'] <= word_mid <= speaker_seg['end']:
                            word_speaker = speaker_seg['speaker']
                            break
                    
                    word['speaker'] = word_speaker
            
            aligned_segments.append(segment)
        
        # Update transcription with aligned segments
        transcription['segments'] = aligned_segments
        transcription['speakers'] = list(set(
            seg.get('speaker', 'UNKNOWN') for seg in aligned_segments
        ))
        
        return transcription
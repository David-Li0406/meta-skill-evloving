"""Main transcription pipeline that orchestrates all components."""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Callable
from datetime import datetime
import time
import traceback
from tqdm import tqdm

from .config import Config
from .audio_extractor import AudioExtractor
from .transcriber import Transcriber
from .vad import VADProcessor
from .diarizer import Diarizer
from .speaker_manager import SpeakerManager
from .voice_sex_classifier import VoiceSexClassifier

logger = logging.getLogger(__name__)


class TranscriptionPipeline:
    """Main pipeline for audio/video transcription with speaker diarization."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the transcription pipeline."""
        self.config = config or Config()
        
        # Initialize components
        self.audio_extractor = AudioExtractor(self.config.config_dict)
        self.transcriber = Transcriber(self.config.config_dict)
        self.vad_processor = VADProcessor(self.config.config_dict)
        self.diarizer = Diarizer(self.config.config_dict)
        self.speaker_manager = SpeakerManager(self.config.config_dict)
        self.voice_sex_classifier = VoiceSexClassifier(self.config.config_dict)
        
        # Processing state
        self.current_job = None
        self.progress_callback = None
        
        logger.info("Transcription pipeline initialized")
    
    def process_file(
        self,
        input_path: Path,
        output_dir: Optional[Path] = None,
        preset: Optional[str] = None,
        skip_existing: bool = True,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Process a single video/audio file through the complete pipeline.
        
        Args:
            input_path: Path to input video/audio file
            output_dir: Output directory (auto-generated if None)
            preset: Performance preset (speed/balanced/accuracy)
            skip_existing: Skip if output already exists
            progress_callback: Progress callback function
            
        Returns:
            Processing results dictionary
        """
        self.progress_callback = progress_callback
        start_time = time.time()
        
        # Apply preset if specified
        if preset:
            self.config.apply_preset(preset)
        
        # Generate output directory
        if output_dir is None:
            output_root = Path(self.config.get('paths.output_root'))
            # Extract metadata for path generation
            camera_folder = self._detect_camera_folder(input_path)
            date_str = datetime.now().strftime('%Y%m%d')
            basename = input_path.stem
            
            output_dir = output_root / camera_folder / date_str / basename
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if already processed
        result_file = output_dir / 'transcript.json'
        if skip_existing and result_file.exists():
            logger.info(f"Skipping existing result: {result_file}")
            with open(result_file, 'r') as f:
                return json.load(f)
        
        try:
            self._update_progress(0, f"Starting processing of {input_path.name}")
            
            # Step 1: Extract audio
            self._update_progress(10, "Extracting audio...")
            audio_result = self._extract_audio(input_path, output_dir)
            
            if not audio_result['success']:
                return {
                    'success': False,
                    'error': audio_result['error'],
                    'input_file': str(input_path),
                    'has_audio': False
                }
            
            audio_path = audio_result['audio_path']
            
            # Step 2: Check if chunking needed
            self._update_progress(20, "Checking audio duration...")
            audio_info = self.audio_extractor.get_audio_info(audio_path)
            duration = audio_info.get('duration', 0)
            
            max_chunk_duration = self.config.get('vad.max_chunk_duration_s', 600)
            
            if duration > max_chunk_duration:
                # Process in chunks
                result = self._process_long_audio(audio_path, output_dir, duration)
            else:
                # Process as single file
                result = self._process_single_audio(audio_path, output_dir)
            
            # Add metadata
            result.update({
                'input_file': str(input_path),
                'output_dir': str(output_dir),
                'audio_file': str(audio_path),
                'processing_time': time.time() - start_time,
                'config_preset': self.config.get('performance.preset'),
                'has_audio': True,
                'success': True
            })
            
            # Save results
            self._save_results(result, output_dir)
            
            self._update_progress(100, "Processing complete")
            return result
            
        except Exception as e:
            logger.error(f"Error processing {input_path}: {str(e)}")
            logger.debug(traceback.format_exc())
            
            error_result = {
                'success': False,
                'error': str(e),
                'input_file': str(input_path),
                'output_dir': str(output_dir) if output_dir else None,
                'processing_time': time.time() - start_time
            }
            
            # Save error result
            if output_dir:
                error_file = output_dir / 'error.json'
                with open(error_file, 'w') as f:
                    json.dump(error_result, f, indent=2)
            
            return error_result
    
    def _extract_audio(self, input_path: Path, output_dir: Path) -> Dict[str, Any]:
        """Extract audio from input file."""
        audio_path = output_dir / 'audio.wav'
        
        # Check if audio already extracted
        if audio_path.exists():
            return {'success': True, 'audio_path': audio_path}
        
        # Extract audio
        success, extracted_path = self.audio_extractor.extract_audio(
            input_path, audio_path
        )
        
        if success:
            return {'success': True, 'audio_path': extracted_path}
        else:
            return {
                'success': False,
                'error': 'No audio stream found or extraction failed'
            }
    
    def _process_single_audio(self, audio_path: Path, output_dir: Path) -> Dict[str, Any]:
        """Process audio file as single unit."""
        # Step 3: Transcribe
        self._update_progress(30, "Transcribing audio...")
        transcription = self.transcriber.transcribe(
            audio_path,
            word_timestamps=True
        )
        
        # Step 4: Diarize
        self._update_progress(60, "Performing speaker diarization...")
        diarization_segments = self.diarizer.diarize(audio_path)
        
        # Step 5: Merge transcription with diarization
        self._update_progress(70, "Merging transcription with diarization...")
        merged_result = self._merge_transcription_diarization(
            transcription, diarization_segments
        )
        
        # Step 6: Speaker identification
        self._update_progress(80, "Identifying speakers...")
        identified_result = self._identify_speakers(
            merged_result, audio_path, diarization_segments
        )
        
        # Step 7: Voice sex classification (if enabled)
        self._update_progress(90, "Analyzing voice characteristics...")
        final_result = self._add_voice_characteristics(
            identified_result, audio_path
        )
        
        return final_result
    
    def _process_long_audio(
        self, 
        audio_path: Path, 
        output_dir: Path, 
        duration: float
    ) -> Dict[str, Any]:
        """Process long audio file in chunks."""
        self._update_progress(25, "Chunking long audio...")
        
        # Create chunks directory
        chunks_dir = output_dir / 'chunks'
        chunks_dir.mkdir(exist_ok=True)
        
        # Chunk audio
        chunks = self.vad_processor.chunk_audio(
            audio_path, chunks_dir, use_vad=True
        )
        
        if not chunks:
            # Fallback to single processing
            return self._process_single_audio(audio_path, output_dir)
        
        # Process each chunk
        chunk_results = []
        progress_per_chunk = 40 / len(chunks)  # 40% for transcription phase
        
        for i, chunk_info in enumerate(chunks):
            chunk_path = chunk_info['path']
            chunk_start = chunk_info['start']
            
            self._update_progress(
                30 + (i * progress_per_chunk),
                f"Processing chunk {i+1}/{len(chunks)}"
            )
            
            # Transcribe chunk
            chunk_transcription = self.transcriber.transcribe(
                chunk_path, word_timestamps=True
            )
            
            # Adjust timestamps
            for segment in chunk_transcription['segments']:
                segment['start'] += chunk_start
                segment['end'] += chunk_start
                
                if 'words' in segment:
                    for word in segment['words']:
                        word['start'] += chunk_start
                        word['end'] += chunk_start
            
            chunk_results.append({
                'transcription': chunk_transcription,
                'chunk_start': chunk_start,
                'chunk_index': i
            })
        
        # Merge chunk results
        self._update_progress(70, "Merging chunks...")
        merged_transcription = self._merge_chunk_results(chunk_results)
        
        # Global diarization on full audio
        self._update_progress(75, "Performing global speaker diarization...")
        diarization_segments = self.diarizer.diarize(audio_path)
        
        # Merge with diarization
        self._update_progress(80, "Merging with diarization...")
        merged_result = self._merge_transcription_diarization(
            merged_transcription, diarization_segments
        )
        
        # Speaker identification
        self._update_progress(85, "Identifying speakers...")
        identified_result = self._identify_speakers(
            merged_result, audio_path, diarization_segments
        )
        
        # Voice characteristics
        self._update_progress(90, "Analyzing voice characteristics...")
        final_result = self._add_voice_characteristics(
            identified_result, audio_path
        )
        
        return final_result
    
    def _merge_chunk_results(self, chunk_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge transcription results from multiple chunks."""
        all_segments = []
        all_text = []
        
        for chunk in chunk_results:
            transcription = chunk['transcription']
            segments = transcription.get('segments', [])
            
            all_segments.extend(segments)
            all_text.append(transcription.get('text', ''))
        
        # Sort segments by start time
        all_segments.sort(key=lambda x: x['start'])
        
        # Create merged result
        merged = {
            'text': ' '.join(all_text),
            'segments': all_segments,
            'language': chunk_results[0]['transcription'].get('language', 'en'),
            'chunks_processed': len(chunk_results)
        }
        
        return merged
    
    def _merge_transcription_diarization(
        self,
        transcription: Dict[str, Any],
        diarization_segments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Merge transcription with diarization results."""
        return self.transcriber.align_with_diarization(
            transcription, diarization_segments
        )
    
    def _identify_speakers(
        self,
        transcription: Dict[str, Any],
        audio_path: Path,
        diarization_segments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Identify speakers using enrolled profiles."""
        # Get speaker embeddings from diarization
        speaker_embeddings = self.diarizer.get_speaker_embeddings(
            audio_path, diarization_segments
        )
        
        # Map to enrolled speakers
        speaker_mapping = self.speaker_manager.map_diarization_to_enrolled(
            speaker_embeddings
        )
        
        # Apply mapping to transcription segments
        for segment in transcription.get('segments', []):
            original_speaker = segment.get('speaker', 'UNKNOWN')
            if original_speaker in speaker_mapping:
                segment['speaker_name'] = speaker_mapping[original_speaker]
                segment['speaker_id'] = original_speaker
            else:
                segment['speaker_name'] = original_speaker
                segment['speaker_id'] = original_speaker
        
        # Add speaker embeddings to result
        transcription['speaker_embeddings'] = {
            k: v.tolist() for k, v in speaker_embeddings.items()
        }
        transcription['speaker_mapping'] = speaker_mapping
        
        return transcription
    
    def _add_voice_characteristics(
        self,
        transcription: Dict[str, Any],
        audio_path: Path
    ) -> Dict[str, Any]:
        """Add voice sex classification if enabled."""
        if not self.voice_sex_classifier.enabled:
            return transcription
        
        # Get speaker embeddings
        speaker_embeddings = {}
        for k, v in transcription.get('speaker_embeddings', {}).items():
            speaker_embeddings[k] = np.array(v)
        
        # Add voice characteristics to segments
        segments = transcription.get('segments', [])
        enhanced_segments = self.voice_sex_classifier.add_voice_sex_to_segments(
            segments, audio_path, speaker_embeddings
        )
        
        transcription['segments'] = enhanced_segments
        
        # Add disclaimer
        transcription['voice_sex_disclaimer'] = self.voice_sex_classifier.get_disclaimer()
        
        return transcription
    
    def _save_results(self, result: Dict[str, Any], output_dir: Path) -> None:
        """Save processing results to files."""
        # Save main JSON result
        json_path = output_dir / 'transcript.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved transcription results to {output_dir}")
    
    def _detect_camera_folder(self, file_path: Path) -> str:
        """Detect camera folder from file path."""
        video_folders = self.config.get('video_folders', ['Movie', 'Park', 'F', 'R'])
        
        # Check parent directories
        for part in file_path.parts:
            if part in video_folders:
                return part
        
        # Default fallback
        return 'Unknown'
    
    def _update_progress(self, percent: float, message: str) -> None:
        """Update progress if callback is provided."""
        if self.progress_callback:
            self.progress_callback(percent, message)
        else:
            logger.info(f"Progress {percent:.1f}%: {message}")
    
    def process_batch(
        self,
        input_files: List[Path],
        output_root: Optional[Path] = None,
        preset: Optional[str] = None,
        skip_existing: bool = True,
        max_workers: int = 1
    ) -> Dict[Path, Dict[str, Any]]:
        """
        Process multiple files in batch.
        
        Args:
            input_files: List of input files
            output_root: Root output directory
            preset: Performance preset
            skip_existing: Skip existing results
            max_workers: Number of parallel workers (currently 1)
            
        Returns:
            Dictionary mapping input files to results
        """
        results = {}
        
        # Process files sequentially for now
        # TODO: Add parallel processing support
        for i, input_path in enumerate(tqdm(input_files, desc="Processing files")):
            logger.info(f"Processing file {i+1}/{len(input_files)}: {input_path}")
            
            try:
                result = self.process_file(
                    input_path,
                    output_dir=output_root,
                    preset=preset,
                    skip_existing=skip_existing
                )
                results[input_path] = result
                
            except Exception as e:
                logger.error(f"Error processing {input_path}: {str(e)}")
                results[input_path] = {
                    'success': False,
                    'error': str(e),
                    'input_file': str(input_path)
                }
        
        return results
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported input formats."""
        return self.config.get('file_patterns', [
            '*.mp4', '*.mov', '*.mkv', '*.avi', '*.webm', '*.wav', '*.mp3'
        ])
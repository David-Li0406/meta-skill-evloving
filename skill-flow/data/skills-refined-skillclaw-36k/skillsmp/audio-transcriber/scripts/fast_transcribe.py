#!/usr/bin/env python3
"""
Fast standalone transcription script with hardware optimization.
No complex dependencies - just processes videos and combines transcripts.
"""

import os
import json
import logging
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
import argparse
from datetime import datetime
import time
from tqdm import tqdm
import torch

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transcription.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FastTranscriber:
    """Fast transcriber using faster-whisper with automatic hardware optimization."""
    
    def __init__(self):
        """Initialize with hardware-optimized settings."""
        try:
            from faster_whisper import WhisperModel
            self.WhisperModel = WhisperModel
        except ImportError:
            logger.error("faster-whisper not installed. Please install it with: pip install faster-whisper")
            raise
        
        # Auto-detect hardware
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.compute_type = 'float16' if self.device == 'cuda' else 'int8'
        
        # Select model based on hardware
        self.model_size = self._select_optimal_model()
        
        logger.info(f"Hardware: {self.device}, Model: {self.model_size}, Compute: {self.compute_type}")
        
        # Load model
        self.model = self.WhisperModel(
            self.model_size,
            device=self.device,
            compute_type=self.compute_type
        )
        
        logger.info("Model loaded successfully!")
    
    def _select_optimal_model(self) -> str:
        """Select optimal model based on available hardware."""
        if self.device == 'cuda':
            # Get VRAM
            gpu_memory_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            logger.info(f"GPU VRAM: {gpu_memory_gb:.1f} GB")
            
            if gpu_memory_gb >= 10:
                return 'large-v3'
            elif gpu_memory_gb >= 6:
                return 'large-v2'
            elif gpu_memory_gb >= 4:
                return 'medium'
            elif gpu_memory_gb >= 2:
                return 'small'
            else:
                return 'base'
        else:
            # CPU - use smaller models
            import psutil
            ram_gb = psutil.virtual_memory().total / (1024**3)
            logger.info(f"System RAM: {ram_gb:.1f} GB")
            
            if ram_gb >= 16:
                return 'medium'
            elif ram_gb >= 8:
                return 'small'
            else:
                return 'base'
    
    def extract_audio(self, video_path: Path, audio_path: Path) -> bool:
        """Extract audio from video using ffmpeg."""
        try:
            cmd = [
                'ffmpeg', '-i', str(video_path),
                '-vn',  # No video
                '-acodec', 'pcm_s16le',  # PCM 16-bit
                '-ar', '16000',  # 16kHz sample rate
                '-ac', '1',  # Mono
                '-y',  # Overwrite
                str(audio_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return True
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
                
        except FileNotFoundError:
            logger.error("ffmpeg not found. Please install ffmpeg and add it to PATH.")
            return False
        except Exception as e:
            logger.error(f"Audio extraction error: {str(e)}")
            return False
    
    def transcribe_file(self, audio_path: Path) -> Dict[str, Any]:
        """Transcribe audio file."""
        try:
            # Transcribe (not translate) with auto-detected language
            segments, info = self.model.transcribe(
                str(audio_path),
                task='transcribe',  # Important: transcribe, not translate
                language=None,  # Auto-detect language
                word_timestamps=True,
                beam_size=5,
                best_of=5
            )
            
            # Convert to our format
            result_segments = []
            full_text = []
            
            for i, segment in enumerate(segments):
                words = []
                if hasattr(segment, 'words') and segment.words:
                    words = [
                        {
                            'text': word.word,
                            'start': word.start,
                            'end': word.end,
                            'probability': word.probability
                        }
                        for word in segment.words
                    ]
                
                segment_dict = {
                    'id': i,
                    'text': segment.text.strip(),
                    'start': segment.start,
                    'end': segment.end,
                    'words': words
                }
                
                result_segments.append(segment_dict)
                full_text.append(segment.text.strip())
            
            return {
                'text': ' '.join(full_text),
                'segments': result_segments,
                'language': info.language,
                'language_probability': info.language_probability
            }
            
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            raise
    
    def process_video(self, video_path: Path, output_path: Path) -> Dict[str, Any]:
        """Process single video file."""
        start_time = time.time()
        
        try:
            # Extract audio to temp file
            temp_audio = output_path.with_suffix('.wav')
            
            logger.info(f"Extracting audio from {video_path.name}...")
            if not self.extract_audio(video_path, temp_audio):
                return {
                    'success': False,
                    'error': 'Audio extraction failed',
                    'input_file': str(video_path)
                }
            
            # Transcribe
            logger.info(f"Transcribing {video_path.name}...")
            transcription = self.transcribe_file(temp_audio)
            
            # Create result
            result = {
                'success': True,
                'input_file': str(video_path),
                'source_file': video_path.name,
                'camera': self._detect_camera_from_path(video_path),
                'processing_time': time.time() - start_time,
                'hardware_optimized': True,
                'model_used': self.model_size,
                'device_used': self.device,
                'timestamp': datetime.now().isoformat(),
                **transcription
            }
            
            # Save result
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            # Clean up temp file
            if temp_audio.exists():
                temp_audio.unlink()
            
            logger.info(f"Completed {video_path.name} in {time.time() - start_time:.1f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error processing {video_path}: {str(e)}")
            
            # Clean up temp file
            temp_audio = output_path.with_suffix('.wav')
            if temp_audio.exists():
                temp_audio.unlink()
            
            return {
                'success': False,
                'error': str(e),
                'input_file': str(video_path),
                'processing_time': time.time() - start_time
            }
    
    def _detect_camera_from_path(self, file_path: Path) -> str:
        """Simple camera detection from path."""
        path_str = str(file_path).lower()
        
        if 'movie_f' in path_str or '/f/' in path_str:
            return 'Movie_F'
        elif 'movie_r' in path_str or '/r/' in path_str:
            return 'Movie_R'
        elif 'front' in path_str:
            return 'Front'
        elif 'rear' in path_str:
            return 'Rear'
        elif 'park' in path_str:
            return 'Park'
        elif 'movie' in path_str:
            return 'Movie'
        else:
            return 'Unknown'

def process_folder(input_folder: Path, output_folder: Path, skip_existing: bool = True) -> Dict[str, Any]:
    """Process all videos in a folder."""
    start_time = time.time()
    
    # Find all video files
    video_extensions = {'.mp4', '.mov', '.mkv', '.avi', '.webm', '.m4v'}
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(input_folder.glob(f'**/*{ext}'))
    
    logger.info(f"Found {len(video_files)} video files in {input_folder}")
    
    if not video_files:
        return {'success': False, 'error': 'No video files found'}
    
    # Create output directory
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # Initialize transcriber
    transcriber = FastTranscriber()
    
    # Process files
    results = []
    successful = 0
    failed = 0
    
    for i, video_file in enumerate(tqdm(video_files, desc="Processing videos")):
        # Generate output path
        relative_path = video_file.relative_to(input_folder)
        output_file = output_folder / relative_path.with_suffix('.json')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Skip existing
        if skip_existing and output_file.exists():
            logger.info(f"Skipping existing: {output_file}")
            successful += 1
            continue
        
        # Process
        result = transcriber.process_video(video_file, output_file)
        results.append(result)
        
        if result.get('success', False):
            successful += 1
        else:
            failed += 1
    
    # Summary
    total_time = time.time() - start_time
    summary = {
        'success': True,
        'total_files': len(video_files),
        'successful_files': successful,
        'failed_files': failed,
        'processing_time_seconds': total_time,
        'processing_time_formatted': f"{total_time/60:.1f} minutes",
        'output_folder': str(output_folder),
        'model_used': transcriber.model_size,
        'device_used': transcriber.device,
        'timestamp': datetime.now().isoformat()
    }
    
    # Save summary
    with open(output_folder / 'processing_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"Processing complete: {successful} successful, {failed} failed")
    logger.info(f"Total time: {total_time/60:.1f} minutes")
    
    return summary

def combine_transcripts(transcripts_folder: Path, output_file: Path) -> Dict[str, Any]:
    """Combine all transcript JSON files into one readable document."""
    logger.info(f"Combining transcripts from {transcripts_folder}")
    
    # Find all JSON files
    json_files = list(transcripts_folder.glob('**/*.json'))
    transcript_files = [f for f in json_files if f.name != 'processing_summary.json']
    
    logger.info(f"Found {len(transcript_files)} transcript files")
    
    if not transcript_files:
        return {'success': False, 'error': 'No transcript files found'}
    
    # Combine transcripts
    combined_text = []
    total_segments = 0
    
    for transcript_file in sorted(transcript_files):
        try:
            with open(transcript_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data.get('success', False):
                continue
            
            source_file = data.get('source_file', transcript_file.name)
            camera = data.get('camera', 'Unknown')
            language = data.get('language', 'unknown')
            
            # File header
            combined_text.append(f"\n{'='*80}")
            combined_text.append(f"FILE: {source_file}")
            combined_text.append(f"CAMERA: {camera}")
            combined_text.append(f"LANGUAGE: {language}")
            combined_text.append(f"{'='*80}\n")
            
            # Add segments
            segments = data.get('segments', [])
            total_segments += len(segments)
            
            for segment in segments:
                text = segment.get('text', '').strip()
                if text:
                    start = segment.get('start', 0)
                    end = segment.get('end', 0)
                    
                    # Format timestamp
                    start_time = format_timestamp(start)
                    end_time = format_timestamp(end)
                    
                    combined_text.append(f"[{start_time} - {end_time}] {text}")
            
        except Exception as e:
            logger.error(f"Error processing {transcript_file}: {str(e)}")
            continue
    
    # Write combined file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    final_text = '\n'.join(combined_text)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_text)
    
    summary = {
        'success': True,
        'transcript_files_processed': len([f for f in transcript_files if f.suffix == '.json']),
        'total_segments': total_segments,
        'output_file': str(output_file),
        'timestamp': datetime.now().isoformat()
    }
    
    logger.info(f"Combined {len(transcript_files)} files with {total_segments} segments")
    return summary

def format_timestamp(seconds: float) -> str:
    """Format seconds as HH:MM:SS."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Fast video transcription with hardware optimization")
    parser.add_argument("input_folder", type=str, help="Folder containing video files")
    parser.add_argument("--output-folder", type=str, help="Output folder for transcripts")
    parser.add_argument("--combine-only", action="store_true", help="Only combine existing transcripts")
    parser.add_argument("--skip-existing", action="store_true", default=True, help="Skip existing transcripts")
    
    args = parser.parse_args()
    
    input_folder = Path(args.input_folder)
    if not input_folder.exists():
        logger.error(f"Input folder does not exist: {input_folder}")
        return
    
    # Default output folder
    if args.output_folder:
        output_folder = Path(args.output_folder)
    else:
        output_folder = input_folder / "transcripts"
    
    if args.combine_only:
        # Just combine existing transcripts
        combined_file = output_folder / "all_transcripts_combined.txt"
        summary = combine_transcripts(output_folder, combined_file)
        print(f"Combined transcripts: {combined_file}")
    else:
        # Process videos and combine
        logger.info("Starting video transcription...")
        processing_summary = process_folder(
            input_folder,
            output_folder,
            skip_existing=args.skip_existing
        )
        
        if processing_summary.get('success', False):
            # Combine transcripts
            combined_file = output_folder / "all_transcripts_combined.txt"
            combination_summary = combine_transcripts(output_folder, combined_file)
            
            print(f"\n{'='*60}")
            print("TRANSCRIPTION COMPLETE")
            print(f"{'='*60}")
            print(f"Total files: {processing_summary['total_files']}")
            print(f"Successful: {processing_summary['successful_files']}")
            print(f"Failed: {processing_summary['failed_files']}")
            print(f"Processing time: {processing_summary['processing_time_formatted']}")
            print(f"Model used: {processing_summary['model_used']}")
            print(f"Device: {processing_summary['device_used']}")
            print(f"Transcripts folder: {output_folder}")
            print(f"Combined transcript: {combined_file}")
            print(f"{'='*60}")
        else:
            logger.error("Processing failed!")

if __name__ == "__main__":
    main()
"""
GPU-accelerated transcription pipeline with multi-GPU support.
Implements high-performance batch processing with automatic load balancing.
"""

import os
import json
import torch
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
import logging
import asyncio
import concurrent.futures
from queue import Queue, Empty
import threading
import time
from contextlib import contextmanager

import whisper
from faster_whisper import WhisperModel
from pyannote.audio import Pipeline as DiarizationPipeline
from pyannote.audio import Audio
from pyannote.core import Segment, Annotation

from .hardware_optimizer import HardwareOptimizer

logger = logging.getLogger(__name__)


@dataclass
class TranscriptionJob:
    """Represents a single transcription job"""
    job_id: str
    input_path: Path
    output_path: Path
    options: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    gpu_id: Optional[int] = None
    status: str = 'pending'
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    result: Optional[Dict] = None
    error: Optional[str] = None


@dataclass 
class GPUWorkerStats:
    """Statistics for a GPU worker"""
    gpu_id: int
    jobs_completed: int = 0
    jobs_failed: int = 0
    total_processing_time: float = 0.0
    current_job: Optional[str] = None
    memory_used_gb: float = 0.0
    utilization_percent: float = 0.0


class GPUMemoryManager:
    """Manages GPU memory allocation and optimization"""
    
    def __init__(self, gpu_id: int, memory_fraction: float = 0.8):
        self.gpu_id = gpu_id
        self.memory_fraction = memory_fraction
        self.allocated_models = {}
        
    @contextmanager
    def allocate(self, model_name: str, model_size_gb: float):
        """Context manager for GPU memory allocation"""
        torch.cuda.set_device(self.gpu_id)
        
        # Check available memory
        free_memory_gb = torch.cuda.mem_get_info(self.gpu_id)[0] / (1024**3)
        
        if free_memory_gb < model_size_gb:
            # Try to free cache
            torch.cuda.empty_cache()
            free_memory_gb = torch.cuda.mem_get_info(self.gpu_id)[0] / (1024**3)
            
            if free_memory_gb < model_size_gb:
                raise RuntimeError(f"Insufficient GPU memory on device {self.gpu_id}: {free_memory_gb:.1f}GB available, {model_size_gb:.1f}GB required")
        
        self.allocated_models[model_name] = model_size_gb
        
        try:
            yield
        finally:
            # Clean up
            if model_name in self.allocated_models:
                del self.allocated_models[model_name]
            torch.cuda.empty_cache()
    
    def get_memory_stats(self) -> Dict:
        """Get current memory statistics"""
        torch.cuda.set_device(self.gpu_id)
        
        total_memory = torch.cuda.get_device_properties(self.gpu_id).total_memory / (1024**3)
        free_memory = torch.cuda.mem_get_info(self.gpu_id)[0] / (1024**3)
        used_memory = total_memory - free_memory
        
        return {
            'gpu_id': self.gpu_id,
            'total_gb': total_memory,
            'used_gb': used_memory,
            'free_gb': free_memory,
            'utilization_percent': (used_memory / total_memory) * 100,
            'allocated_models': self.allocated_models.copy()
        }


class GPUTranscriptionWorker:
    """Worker for processing transcription jobs on a specific GPU"""
    
    def __init__(self, gpu_id: int, model_config: Dict, memory_fraction: float = 0.8):
        self.gpu_id = gpu_id
        self.model_config = model_config
        self.memory_manager = GPUMemoryManager(gpu_id, memory_fraction)
        self.stats = GPUWorkerStats(gpu_id=gpu_id)
        self.model = None
        self.diarization_pipeline = None
        self._lock = threading.Lock()
        
    def initialize_models(self):
        """Initialize ASR and diarization models on the GPU"""
        torch.cuda.set_device(self.gpu_id)
        
        # Initialize Whisper model
        model_name = self.model_config.get('model', 'large-v3')
        compute_type = self.model_config.get('compute_type', 'float16')
        
        logger.info(f"GPU {self.gpu_id}: Loading Whisper model {model_name}")
        
        # Use FasterWhisper for better performance
        self.model = WhisperModel(
            model_name,
            device='cuda',
            device_index=self.gpu_id,
            compute_type=compute_type,
            num_workers=self.model_config.get('num_workers', 4),
            download_root=self.model_config.get('model_dir', './models')
        )
        
        # Initialize diarization if enabled
        if self.model_config.get('diarization_enabled', True):
            logger.info(f"GPU {self.gpu_id}: Loading diarization pipeline")
            self.diarization_pipeline = DiarizationPipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=self.model_config.get('hf_token')
            )
            self.diarization_pipeline.to(torch.device(f'cuda:{self.gpu_id}'))
        
        logger.info(f"GPU {self.gpu_id}: Models initialized successfully")
    
    def process_job(self, job: TranscriptionJob) -> TranscriptionJob:
        """Process a single transcription job"""
        
        with self._lock:
            self.stats.current_job = job.job_id
            job.status = 'processing'
            job.start_time = time.time()
            job.gpu_id = self.gpu_id
        
        try:
            # Set GPU
            torch.cuda.set_device(self.gpu_id)
            
            # Process audio
            result = self._transcribe_audio(job)
            
            # Add diarization if enabled
            if self.diarization_pipeline and job.options.get('diarization', True):
                result = self._add_diarization(job, result)
            
            # Add confidence scores
            result = self._add_confidence_scores(result)
            
            # Save results
            self._save_results(job, result)
            
            job.result = result
            job.status = 'completed'
            
            with self._lock:
                self.stats.jobs_completed += 1
            
        except Exception as e:
            logger.error(f"GPU {self.gpu_id}: Error processing job {job.job_id}: {e}")
            job.error = str(e)
            job.status = 'failed'
            
            with self._lock:
                self.stats.jobs_failed += 1
        
        finally:
            job.end_time = time.time()
            
            with self._lock:
                self.stats.current_job = None
                if job.start_time and job.end_time:
                    self.stats.total_processing_time += (job.end_time - job.start_time)
            
            # Clear GPU cache periodically
            if (self.stats.jobs_completed + self.stats.jobs_failed) % 10 == 0:
                torch.cuda.empty_cache()
        
        return job
    
    def _transcribe_audio(self, job: TranscriptionJob) -> Dict:
        """Transcribe audio using Whisper"""
        
        # Transcription options
        options = {
            'language': job.options.get('language', 'en'),
            'task': job.options.get('task', 'transcribe'),
            'beam_size': job.options.get('beam_size', 5),
            'best_of': job.options.get('best_of', 5),
            'patience': job.options.get('patience', 1.0),
            'temperature': job.options.get('temperature', [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]),
            'word_timestamps': True,
            'vad_filter': True,
            'vad_parameters': job.options.get('vad_parameters', {
                'threshold': 0.5,
                'min_speech_duration_ms': 250,
                'max_speech_duration_s': 0,
                'min_silence_duration_ms': 2000,
                'speech_pad_ms': 400
            })
        }
        
        # Process with batch support
        segments, info = self.model.transcribe(
            str(job.input_path),
            **options
        )
        
        # Convert to list and add metadata
        segment_list = []
        for segment in segments:
            seg_dict = {
                'id': len(segment_list),
                'start': segment.start,
                'end': segment.end,
                'text': segment.text.strip(),
                'words': []
            }
            
            # Add word-level timestamps if available
            if hasattr(segment, 'words') and segment.words:
                seg_dict['words'] = [
                    {
                        'word': w.word,
                        'start': w.start,
                        'end': w.end,
                        'probability': w.probability
                    }
                    for w in segment.words
                ]
            
            segment_list.append(seg_dict)
        
        return {
            'segments': segment_list,
            'language': info.language,
            'duration': info.duration,
            'transcription_options': options
        }
    
    def _add_diarization(self, job: TranscriptionJob, result: Dict) -> Dict:
        """Add speaker diarization to transcription"""
        
        try:
            # Run diarization
            diarization = self.diarization_pipeline(str(job.input_path))
            
            # Map segments to speakers
            for segment in result['segments']:
                segment_time = Segment(segment['start'], segment['end'])
                
                # Find overlapping speakers
                speakers = []
                for turn, _, speaker in diarization.itertracks(yield_label=True):
                    if turn.overlaps(segment_time):
                        overlap_duration = turn.intersection(segment_time).duration
                        speakers.append((speaker, overlap_duration))
                
                # Assign speaker with maximum overlap
                if speakers:
                    speakers.sort(key=lambda x: x[1], reverse=True)
                    segment['speaker'] = speakers[0][0]
                else:
                    segment['speaker'] = 'Unknown'
            
            # Add diarization metadata
            result['diarization'] = {
                'enabled': True,
                'num_speakers': len(diarization.labels()),
                'speakers': list(diarization.labels())
            }
            
        except Exception as e:
            logger.warning(f"Diarization failed for job {job.job_id}: {e}")
            result['diarization'] = {
                'enabled': True,
                'error': str(e)
            }
        
        return result
    
    def _add_confidence_scores(self, result: Dict) -> Dict:
        """Calculate and add confidence scores"""
        
        for segment in result['segments']:
            # Calculate segment confidence from word probabilities
            if segment.get('words'):
                probs = [w.get('probability', 1.0) for w in segment['words']]
                segment['confidence'] = np.mean(probs) if probs else 0.5
            else:
                # Default confidence if no word-level data
                segment['confidence'] = 0.7
            
            # Add voice characteristics placeholder
            segment['voice_sex'] = 'unknown'  # Will be implemented with voice classifier
        
        return result
    
    def _save_results(self, job: TranscriptionJob, result: Dict):
        """Save transcription results"""
        
        output_path = job.output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save JSON
        json_path = output_path.with_suffix('.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Save other formats as configured
        if job.options.get('export_formats'):
            self._export_formats(job, result)
    
    def _export_formats(self, job: TranscriptionJob, result: Dict):
        """Export to various formats"""
        
        formats = job.options.get('export_formats', ['srt', 'vtt'])
        
        for fmt in formats:
            if fmt == 'srt':
                self._export_srt(job.output_path.with_suffix('.srt'), result)
            elif fmt == 'vtt':
                self._export_vtt(job.output_path.with_suffix('.vtt'), result)
            elif fmt == 'csv':
                self._export_csv(job.output_path.with_suffix('.csv'), result)
    
    def _export_srt(self, path: Path, result: Dict):
        """Export to SRT format"""
        with open(path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(result['segments'], 1):
                start_time = self._format_timestamp(segment['start'], 'srt')
                end_time = self._format_timestamp(segment['end'], 'srt')
                speaker = f"[{segment.get('speaker', 'Unknown')}] " if segment.get('speaker') else ''
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{speaker}{segment['text']}\n\n")
    
    def _export_vtt(self, path: Path, result: Dict):
        """Export to WebVTT format"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")
            
            for segment in result['segments']:
                start_time = self._format_timestamp(segment['start'], 'vtt')
                end_time = self._format_timestamp(segment['end'], 'vtt')
                speaker = f"<v {segment.get('speaker', 'Unknown')}>" if segment.get('speaker') else ''
                
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{speaker}{segment['text']}\n\n")
    
    def _export_csv(self, path: Path, result: Dict):
        """Export to CSV format"""
        import csv
        
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Start', 'End', 'Speaker', 'Text', 'Confidence'])
            
            for segment in result['segments']:
                writer.writerow([
                    segment['start'],
                    segment['end'],
                    segment.get('speaker', 'Unknown'),
                    segment['text'],
                    segment.get('confidence', 0.0)
                ])
    
    @staticmethod
    def _format_timestamp(seconds: float, format_type: str) -> str:
        """Format timestamp for SRT/VTT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        
        if format_type == 'srt':
            return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace('.', ',')
        else:  # vtt
            return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
    
    def get_stats(self) -> GPUWorkerStats:
        """Get worker statistics"""
        with self._lock:
            # Update memory stats
            mem_stats = self.memory_manager.get_memory_stats()
            self.stats.memory_used_gb = mem_stats['used_gb']
            self.stats.utilization_percent = mem_stats['utilization_percent']
            
            return self.stats


class ParallelGPUPipeline:
    """Manages parallel transcription across multiple GPUs"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.hardware_optimizer = HardwareOptimizer(config_path)
        self.config = self.hardware_optimizer.generate_config_override()
        
        self.gpu_count = self.hardware_optimizer.specs.gpu_count
        self.workers = []
        self.job_queue = Queue()
        self.result_queue = Queue()
        self.executor = None
        self._shutdown = False
        
        logger.info(f"Initializing parallel pipeline with {self.gpu_count} GPU(s)")
    
    def initialize(self):
        """Initialize all GPU workers"""
        
        if self.gpu_count == 0:
            raise RuntimeError("No GPUs available for parallel processing")
        
        # Create workers for each GPU
        for gpu_id in range(self.gpu_count):
            worker = GPUTranscriptionWorker(
                gpu_id=gpu_id,
                model_config=self.config['asr'],
                memory_fraction=self.config['performance'].get('torch_memory_fraction', 0.8)
            )
            worker.initialize_models()
            self.workers.append(worker)
        
        # Create thread pool for parallel execution
        max_workers = self.config['performance'].get('max_concurrent_gpus', self.gpu_count)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        
        logger.info(f"Initialized {len(self.workers)} GPU workers")
    
    def process_batch(self, input_files: List[Path], output_dir: Path, options: Dict = None) -> List[TranscriptionJob]:
        """Process a batch of files in parallel"""
        
        if not self.executor:
            self.initialize()
        
        jobs = []
        futures = []
        
        # Create jobs
        for i, input_file in enumerate(input_files):
            job = TranscriptionJob(
                job_id=f"job_{i:04d}_{input_file.stem}",
                input_path=input_file,
                output_path=output_dir / input_file.stem / 'transcript',
                options=options or {},
                priority=i
            )
            jobs.append(job)
        
        # Submit jobs to workers (round-robin distribution)
        for i, job in enumerate(jobs):
            worker = self.workers[i % len(self.workers)]
            future = self.executor.submit(worker.process_job, job)
            futures.append((future, job))
        
        # Collect results
        completed_jobs = []
        for future, job in futures:
            try:
                result = future.result(timeout=None)
                completed_jobs.append(result)
                logger.info(f"Completed job {job.job_id} on GPU {job.gpu_id}")
            except Exception as e:
                logger.error(f"Job {job.job_id} failed: {e}")
                job.status = 'failed'
                job.error = str(e)
                completed_jobs.append(job)
        
        return completed_jobs
    
    def process_stream(self, input_generator, output_dir: Path, options: Dict = None):
        """Process a stream of files with dynamic load balancing"""
        
        if not self.executor:
            self.initialize()
        
        # Start worker threads
        worker_threads = []
        for worker in self.workers:
            thread = threading.Thread(
                target=self._worker_loop,
                args=(worker,)
            )
            thread.start()
            worker_threads.append(thread)
        
        # Submit jobs
        job_count = 0
        for input_file in input_generator:
            if self._shutdown:
                break
            
            job = TranscriptionJob(
                job_id=f"stream_job_{job_count:06d}",
                input_path=input_file,
                output_path=output_dir / input_file.stem / 'transcript',
                options=options or {}
            )
            
            self.job_queue.put(job)
            job_count += 1
        
        # Signal completion
        for _ in self.workers:
            self.job_queue.put(None)
        
        # Wait for workers
        for thread in worker_threads:
            thread.join()
        
        # Collect results
        results = []
        while not self.result_queue.empty():
            try:
                results.append(self.result_queue.get_nowait())
            except Empty:
                break
        
        return results
    
    def _worker_loop(self, worker: GPUTranscriptionWorker):
        """Worker loop for processing jobs"""
        
        while not self._shutdown:
            try:
                job = self.job_queue.get(timeout=1)
                
                if job is None:  # Shutdown signal
                    break
                
                result = worker.process_job(job)
                self.result_queue.put(result)
                
            except Empty:
                continue
            except Exception as e:
                logger.error(f"Worker error: {e}")
    
    def get_statistics(self) -> Dict:
        """Get pipeline statistics"""
        
        stats = {
            'pipeline': {
                'gpu_count': self.gpu_count,
                'active_workers': len(self.workers),
                'jobs_in_queue': self.job_queue.qsize(),
                'results_ready': self.result_queue.qsize()
            },
            'workers': []
        }
        
        for worker in self.workers:
            worker_stats = worker.get_stats()
            stats['workers'].append({
                'gpu_id': worker_stats.gpu_id,
                'jobs_completed': worker_stats.jobs_completed,
                'jobs_failed': worker_stats.jobs_failed,
                'total_processing_time': worker_stats.total_processing_time,
                'current_job': worker_stats.current_job,
                'memory_used_gb': worker_stats.memory_used_gb,
                'utilization_percent': worker_stats.utilization_percent
            })
        
        # Calculate aggregates
        stats['aggregate'] = {
            'total_jobs_completed': sum(w['jobs_completed'] for w in stats['workers']),
            'total_jobs_failed': sum(w['jobs_failed'] for w in stats['workers']),
            'average_memory_usage_gb': np.mean([w['memory_used_gb'] for w in stats['workers']]),
            'average_utilization_percent': np.mean([w['utilization_percent'] for w in stats['workers']])
        }
        
        return stats
    
    def shutdown(self):
        """Shutdown the pipeline"""
        
        self._shutdown = True
        
        if self.executor:
            self.executor.shutdown(wait=True)
        
        # Clear GPU memory
        for worker in self.workers:
            torch.cuda.set_device(worker.gpu_id)
            torch.cuda.empty_cache()
        
        logger.info("Pipeline shutdown complete")


def create_optimized_pipeline(config_path: Optional[Path] = None) -> ParallelGPUPipeline:
    """Factory function to create an optimized pipeline"""
    
    pipeline = ParallelGPUPipeline(config_path)
    pipeline.initialize()
    
    return pipeline


if __name__ == "__main__":
    # Test the pipeline
    logging.basicConfig(level=logging.INFO)
    
    # Create pipeline
    pipeline = create_optimized_pipeline()
    
    # Get statistics
    stats = pipeline.get_statistics()
    print(json.dumps(stats, indent=2))
    
    # Shutdown
    pipeline.shutdown()
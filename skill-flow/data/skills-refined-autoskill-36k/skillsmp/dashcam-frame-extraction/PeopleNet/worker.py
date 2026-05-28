#!/usr/bin/env python3
"""
Continuous GPU Worker - Processes videos from staging directory continuously
Supports multiple parallel workers with file-based locking
"""

import os
import sys
import time
import subprocess
import cv2
import numpy as np
import onnxruntime as ort
from pathlib import Path
import fcntl

# Configuration (can be overridden via environment variables)
BATCH_NAME = os.environ.get('BATCH_NAME', 'Park_F_Batch1')
STAGING_DIR = f"/workspace/Staging/{BATCH_NAME}"
OUTPUT_DIR = f"/workspace/Outputs/{BATCH_NAME}"
MODEL_PATH = "/workspace/model/resnet34_peoplenet_int8.onnx"
PROCESSED_LIST = f"/workspace/Outputs/{BATCH_NAME}/processed_videos.txt"
LOCK_DIR = f"/workspace/Outputs/{BATCH_NAME}/locks"
WORKER_ID = int(sys.argv[1]) if len(sys.argv) > 1 else 1
LOG_FILE = f"/workspace/Outputs/{BATCH_NAME}/worker_{WORKER_ID}_log.txt"

class ContinuousGPUWorker:
    def __init__(self, worker_id, confidence_threshold=0.8, buffer_seconds=1):
        self.worker_id = worker_id
        self.confidence_threshold = confidence_threshold
        self.buffer_seconds = buffer_seconds

        # Create lock directory
        os.makedirs(LOCK_DIR, exist_ok=True)

        self.log(f"Worker {worker_id} initializing...", verbose=True)

        # Initialize ONNX session with GPU
        available = ort.get_available_providers()
        preferred_providers = []

        if 'CUDAExecutionProvider' in available:
            preferred_providers.append(('CUDAExecutionProvider', {
                'device_id': 0,
                'arena_extend_strategy': 'kSameAsRequested',
                'gpu_mem_limit': 2 * 1024 * 1024 * 1024,  # 2GB per worker
                'cudnn_conv_algo_search': 'EXHAUSTIVE',
                'do_copy_in_default_stream': True,
            }))

        preferred_providers.append('CPUExecutionProvider')

        self.session = ort.InferenceSession(MODEL_PATH, providers=[p[0] if isinstance(p, tuple) else p for p in preferred_providers])
        self.log(f"Worker {worker_id} ready! Using: {self.session.get_providers()}", verbose=True)

    def log(self, message, verbose=False):
        """Log to file only. Use verbose=True to also print to stdout."""
        timestamp = time.strftime('%H:%M:%S')
        log_msg = f"[{timestamp}] W{self.worker_id}: {message}"

        # Only print to stdout for critical messages
        if verbose:
            print(log_msg)

        # Always write to log file
        with open(LOG_FILE, 'a') as f:
            f.write(log_msg + '\n')

    def try_claim_video(self, video_path):
        """Try to claim a video for processing using file lock"""
        video_name = os.path.basename(video_path)
        lock_file = os.path.join(LOCK_DIR, f"{video_name}.lock")

        try:
            # Try to create lock file exclusively
            lock_fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(lock_fd, f"Worker {self.worker_id}\n".encode())
            os.close(lock_fd)
            return True
        except FileExistsError:
            # Another worker claimed it
            return False

    def release_video(self, video_path):
        """Release video lock and mark as processed"""
        video_name = os.path.basename(video_path)
        lock_file = os.path.join(LOCK_DIR, f"{video_name}.lock")

        try:
            os.remove(lock_file)
        except:
            pass

        # Mark as processed
        with open(PROCESSED_LIST, 'a') as f:
            f.write(video_name + '\n')

        # Delete video from staging to free up space
        try:
            os.remove(video_path)
        except:
            pass

    def get_next_video(self):
        """Get next unprocessed video from staging"""
        try:
            # Get list of processed videos
            processed = set()
            if os.path.exists(PROCESSED_LIST):
                with open(PROCESSED_LIST, 'r') as f:
                    processed = set(line.strip() for line in f)

            # Get all videos, sorted
            videos = sorted([f for f in os.listdir(STAGING_DIR) if f.endswith('.MP4')])

            for video in videos:
                # Skip if already processed
                if video in processed:
                    continue

                # Try to claim this video
                video_path = os.path.join(STAGING_DIR, video)
                if self.try_claim_video(video_path):
                    return video_path

            return None
        except Exception as e:
            self.log(f"Error getting next video: {e}")
            return None

    def detect_in_frame(self, frame):
        """Run detection on a single frame"""
        try:
            img = cv2.resize(frame, (960, 544))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
            img = np.transpose(img, (2, 0, 1))[np.newaxis, ...]

            outputs = self.session.run(None, {'input_1:0': img})
            max_conf = outputs[0][0, 0, :, :].max()

            return max_conf >= self.confidence_threshold, max_conf
        except Exception as e:
            self.log(f"Detection error: {e}")
            return False, 0.0

    def process_video(self, video_path):
        """Process single video and extract people clips"""
        video_name = os.path.basename(video_path)
        base_name = os.path.splitext(video_name)[0]

        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                self.log(f"Failed to open: {video_name}")
                return []

            fps = cap.get(cv2.CAP_PROP_FPS)
            if fps == 0:
                fps = 30

            detections = []
            frame_num = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_num += 1

                # Sample every 0.5 seconds (twice per second)
                if frame_num % int(fps / 2) != 0:
                    continue

                has_people, conf = self.detect_in_frame(frame)
                if has_people:
                    timestamp = frame_num / fps
                    detections.append(timestamp)

            cap.release()

            if not detections:
                return []

            # Merge nearby detections into segments
            segments = []
            for ts in detections:
                start = max(0, ts - self.buffer_seconds)
                end = ts + self.buffer_seconds

                if segments and start <= segments[-1]['end']:
                    segments[-1]['end'] = max(segments[-1]['end'], end)
                else:
                    segments.append({'start': start, 'end': end})

            # Extract segments with ffmpeg
            clips = []
            for i, seg in enumerate(segments):
                output = f"{OUTPUT_DIR}/{base_name}_people_{int(seg['start'])}-{int(seg['end'])}s.mp4"
                duration = seg['end'] - seg['start']
                cmd = ['ffmpeg', '-i', video_path, '-ss', str(seg['start']),
                       '-t', str(duration), '-c', 'copy', output, '-y']
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if os.path.exists(output):
                    clips.append(output)

            return clips

        except Exception as e:
            self.log(f"Error processing {video_name}: {e}")
            return []

    def run(self):
        """Main loop - continuously process videos from staging"""
        self.log("Starting continuous processing...", verbose=True)
        videos_processed = 0
        idle_count = 0

        while True:
            video_path = self.get_next_video()

            if video_path is None:
                # No more videos, check again in 5 seconds
                idle_count += 1
                if idle_count == 1:
                    self.log(f"Queue empty. Processed {videos_processed} videos. Waiting...", verbose=True)
                time.sleep(5)
                continue

            idle_count = 0
            video_name = os.path.basename(video_path)
            start_time = time.time()

            clips = self.process_video(video_path)

            elapsed = time.time() - start_time
            videos_processed += 1

            # Log to file always, but only print to stdout every 50 videos
            verbose = (videos_processed % 50 == 0)
            if clips:
                self.log(f"[{videos_processed}] {video_name}: {len(clips)} clips ({elapsed:.1f}s)", verbose=verbose)
            else:
                self.log(f"[{videos_processed}] {video_name}: No people ({elapsed:.1f}s)", verbose=verbose)

            # Release and mark as processed
            self.release_video(video_path)

if __name__ == "__main__":
    worker = ContinuousGPUWorker(WORKER_ID)
    worker.run()

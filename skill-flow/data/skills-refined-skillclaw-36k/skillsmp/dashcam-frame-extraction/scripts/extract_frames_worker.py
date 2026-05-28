#!/usr/bin/env python3
"""
GPU-Accelerated Frame Extraction Worker
Extracts 3 frames per video: BEGIN, MIDDLE, END
CRITICAL: Works with HEVC videos - does NOT use -hwaccel_output_format
"""
import subprocess
import sys
from pathlib import Path
import json
import shutil

class FrameExtractor:
    def __init__(self, video_list_file, category, worker_id):
        self.video_list = Path(video_list_file)
        self.category = category
        self.worker_id = worker_id
        self.desktop_source = Path(f"/mnt/sdcard/CARDV/{category}")
        self.output_dir = Path("/home/yousuf/GoogleDrive/PROJECTS/INVESTIGATION/DASHCAM/FRAMES_CLIPS/Movie_F&R_MotionSamples")
        self.staging_dir = Path(f"/home/yousuf/PROJECTS/PeopleNet/Staging/{category}_Worker{worker_id}")
        self.staging_dir.mkdir(parents=True, exist_ok=True)

    def get_duration(self, video_path):
        """Get video duration in seconds"""
        try:
            result = subprocess.run([
                'ffprobe', '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                str(video_path)
            ], capture_output=True, text=True, timeout=10)
            return float(result.stdout.strip())
        except:
            return None

    def extract_frame(self, video_path, timestamp, output_path, use_gpu=True):
        """
        Extract single frame at timestamp using GPU acceleration
        CRITICAL: Does NOT use -hwaccel_output_format cuda (breaks HEVC->JPEG)
        """
        try:
            cmd = ['ffmpeg', '-y']

            # GPU hardware acceleration for decoding only
            if use_gpu:
                cmd.extend(['-hwaccel', 'cuda'])
                # CRITICAL: DO NOT add '-hwaccel_output_format', 'cuda'
                # This breaks HEVC to JPEG conversion

            cmd.extend([
                '-ss', str(timestamp),
                '-i', str(video_path),
                '-frames:v', '1',
                '-q:v', '2',
                str(output_path)
            ])

            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=30,
                text=True
            )

            return result.returncode == 0 and Path(output_path).exists()
        except subprocess.TimeoutExpired:
            return False
        except Exception:
            return False

    def process_video(self, video_filename):
        """Extract 3 frames from a single video"""
        source_path = self.desktop_source / video_filename

        if not source_path.exists():
            return {'status': 'not_found', 'frames': 0}

        # Copy to staging for faster I/O
        staged_path = self.staging_dir / video_filename
        try:
            shutil.copy2(source_path, staged_path)
        except Exception:
            return {'status': 'copy_failed', 'frames': 0}

        # Get duration
        duration = self.get_duration(staged_path)
        if not duration or duration < 3:
            staged_path.unlink(missing_ok=True)
            return {'status': 'invalid_duration', 'frames': 0}

        # Calculate timestamps
        begin_ts = 1.0
        middle_ts = duration / 2.0
        end_ts = max(1.0, duration - 1.0)

        video_base = video_filename.replace('.MP4', '')
        frames_extracted = 0

        # Extract 3 frames
        positions = [
            ('BEGIN', begin_ts, int(begin_ts * 1000)),
            ('MIDDLE', middle_ts, int(middle_ts * 1000)),
            ('END', end_ts, int(end_ts * 1000))
        ]

        for pos_name, timestamp, timestamp_ms in positions:
            output_path = self.output_dir / f"{video_base}_{pos_name}_{timestamp_ms:06d}ms.jpg"

            if self.extract_frame(staged_path, timestamp, output_path):
                frames_extracted += 1

        # Cleanup staging
        staged_path.unlink(missing_ok=True)

        return {
            'status': 'success' if frames_extracted == 3 else 'partial',
            'frames': frames_extracted
        }

    def process_batch(self):
        """Process all videos in the batch"""
        videos = self.video_list.read_text().strip().split('\n')
        videos = [v.strip() for v in videos if v.strip()]

        stats = {
            'total': len(videos),
            'success': 0,
            'partial': 0,
            'failed': 0,
            'frames': 0
        }

        for i, video in enumerate(videos, 1):
            result = self.process_video(video)
            stats['frames'] += result['frames']

            if result['status'] == 'success':
                stats['success'] += 1
            elif result['frames'] > 0:
                stats['partial'] += 1
            else:
                stats['failed'] += 1

        return stats

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: script.py <video_list> <category> <worker_id>")
        sys.exit(1)

    extractor = FrameExtractor(sys.argv[1], sys.argv[2], sys.argv[3])
    stats = extractor.process_batch()

    print(json.dumps(stats))

    # Exit with error if any videos failed
    if stats['failed'] > 0:
        sys.exit(1)
    sys.exit(0)

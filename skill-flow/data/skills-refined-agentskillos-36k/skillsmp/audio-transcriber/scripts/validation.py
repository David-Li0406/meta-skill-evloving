"""
Input validation and prerequisite checks for audio transcription pipeline.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import torch
except ImportError:
    torch = None


def validate_inputs(config: Dict) -> Tuple[bool, List[str]]:
    """
    Validate all inputs before processing begins.
    Fail-fast on any critical issue.

    Args:
        config: Configuration dictionary

    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []

    # Check required inputs
    if not config.get('roots') or len(config['roots']) == 0:
        errors.append("ERROR: Roots not provided or empty. Please specify video folder path.")

    # Check FFmpeg available
    if not check_ffmpeg_installed():
        errors.append("ERROR: FFmpeg not found in PATH. Please install FFmpeg from https://ffmpeg.org/download.html")

    # Check GPU if requested
    if config.get('whisper', {}).get('device') == 'cuda':
        if not check_gpu_available():
            errors.append("WARNING: CUDA requested but not available. Will fall back to CPU.")
            config['whisper']['device'] = 'cpu'

    # Check HF token if diarization enabled
    if config.get('diarization', {}).get('enabled'):
        token_env = config['diarization'].get('hf_token_env', 'HF_TOKEN')
        if not os.getenv(token_env):
            errors.append(f"WARNING: HF token {token_env} not set. Diarization will be disabled.")
            config['diarization']['enabled'] = False

    # Check segmentation mode mutual exclusion
    mode = config.get('segmentation', {}).get('mode', 'fixed')
    if mode not in ['fixed', 'vad']:
        errors.append(f"ERROR: Segmentation mode must be 'fixed' or 'vad', got: {mode}")

    # Check output directory writable
    output_dir = config.get('output_dir')
    if output_dir:
        output_path = Path(output_dir)
        if output_path.exists() and not os.access(output_path, os.W_OK):
            errors.append(f"ERROR: Output directory not writable: {output_dir}")

    # Estimate disk space required
    if output_dir and config.get('roots'):
        try:
            estimated_gb = estimate_disk_space(config)
            available_gb = get_available_disk_space(output_dir)
            if estimated_gb > available_gb:
                errors.append(f"ERROR: Insufficient disk space. Need ~{estimated_gb}GB, have {available_gb}GB")
        except Exception as e:
            errors.append(f"WARNING: Could not estimate disk space: {e}")

    # Check video files exist
    if config.get('roots'):
        for root in config['roots']:
            root_path = Path(root)
            if not root_path.exists():
                errors.append(f"ERROR: Video folder does not exist: {root}")
            elif not any(root_path.glob('*.mp4')) and not any(root_path.glob('*.MP4')):
                errors.append(f"WARNING: No MP4 files found in: {root}")

    is_valid = not any(err.startswith("ERROR:") for err in errors)
    return is_valid, errors


def check_ffmpeg_installed() -> bool:
    """Check if FFmpeg is installed and accessible."""
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def check_gpu_available() -> bool:
    """Check if CUDA GPU is available."""
    if torch is None:
        return False

    try:
        return torch.cuda.is_available()
    except Exception:
        return False


def get_gpu_info() -> Optional[Dict]:
    """
    Get detailed GPU information.

    Returns:
        Dictionary with GPU details or None if no GPU
    """
    if not check_gpu_available():
        return None

    try:
        import pynvml
        pynvml.nvmlInit()

        device_count = torch.cuda.device_count()
        devices = []

        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle)
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)

            devices.append({
                'index': i,
                'name': name.decode('utf-8') if isinstance(name, bytes) else name,
                'total_mem_mb': mem_info.total // (1024 ** 2),
                'free_mem_mb': mem_info.free // (1024 ** 2)
            })

        cuda_version = torch.version.cuda
        driver_version = pynvml.nvmlSystemGetDriverVersion()

        pynvml.nvmlShutdown()

        return {
            'gpu_detected': True,
            'device_count': device_count,
            'devices': devices,
            'cuda_version': cuda_version,
            'driver_version': driver_version.decode('utf-8') if isinstance(driver_version, bytes) else driver_version
        }

    except Exception as e:
        return {
            'gpu_detected': True,
            'device_count': torch.cuda.device_count(),
            'error': str(e)
        }


def estimate_disk_space(config: Dict) -> float:
    """
    Estimate required disk space in GB.

    Args:
        config: Configuration dictionary

    Returns:
        Estimated disk space in GB
    """
    roots = config.get('roots', [])
    if not roots:
        return 0.0

    total_video_size_gb = 0.0

    for root in roots:
        root_path = Path(root)
        if root_path.exists():
            for video in root_path.glob('*.mp4'):
                total_video_size_gb += video.stat().st_size / (1024 ** 3)
            for video in root_path.glob('*.MP4'):
                total_video_size_gb += video.stat().st_size / (1024 ** 3)

    # Estimate:
    # - Audio: ~10% of video size (compressed)
    # - Transcripts: ~1% of video size (text)
    # - Overhead: 20% buffer
    keep_audio = config.get('audio', {}).get('keep_intermediate', False)

    if keep_audio:
        estimated_gb = total_video_size_gb * 0.11 * 1.2
    else:
        estimated_gb = total_video_size_gb * 0.01 * 1.2

    return round(estimated_gb, 2)


def get_available_disk_space(path: str) -> float:
    """
    Get available disk space in GB.

    Args:
        path: Directory path to check

    Returns:
        Available space in GB
    """
    import shutil
    stat = shutil.disk_usage(path)
    return stat.free / (1024 ** 3)


def auto_discover_videos(search_paths: Optional[List[str]] = None) -> List[str]:
    """
    Auto-discover video folders in expected locations.

    Args:
        search_paths: Optional list of paths to search

    Returns:
        List of discovered folder paths containing MP4 files
    """
    if search_paths is None:
        search_paths = [
            Path(os.path.expanduser("~")) / "Desktop" / "CARDV" / "Movie_F",
            Path(os.path.expanduser("~")) / "Desktop" / "CARDV" / "Movie_R",
            Path("G:/My Drive/PROJECTS/INVESTIGATION/DASHCAM/Movie_F"),
            Path("G:/My Drive/PROJECTS/INVESTIGATION/DASHCAM/Movie_R"),
            Path.cwd()
        ]

    discovered = []

    for base_path in search_paths:
        if not base_path.exists():
            continue

        # Check if base path has MP4s
        if any(base_path.glob('*.mp4')) or any(base_path.glob('*.MP4')):
            discovered.append(str(base_path))
            continue

        # Check for date-organized subfolders (YYYYMMDD pattern)
        for subfolder in base_path.iterdir():
            if subfolder.is_dir() and len(subfolder.name) == 8 and subfolder.name.isdigit():
                if any(subfolder.glob('*.mp4')) or any(subfolder.glob('*.MP4')):
                    discovered.append(str(subfolder))

    return discovered


def validate_video_folder(folder_path: str) -> Tuple[bool, Dict]:
    """
    Validate video folder and collect metadata.

    Args:
        folder_path: Path to video folder

    Returns:
        Tuple of (is_valid, metadata_dict)
    """
    folder = Path(folder_path)

    if not folder.exists():
        return False, {'error': 'Folder does not exist'}

    if not folder.is_dir():
        return False, {'error': 'Path is not a directory'}

    # Count MP4 files
    mp4_files = list(folder.glob('*.mp4')) + list(folder.glob('*.MP4'))

    if len(mp4_files) == 0:
        return False, {'error': 'No MP4 files found'}

    # Estimate total duration (requires ffprobe)
    total_duration_sec = 0
    total_size_gb = 0

    for video in mp4_files[:10]:  # Sample first 10 for speed
        try:
            duration = get_video_duration(video)
            if duration:
                total_duration_sec += duration
        except Exception:
            pass

        total_size_gb += video.stat().st_size / (1024 ** 3)

    # Extrapolate if more than 10 videos
    if len(mp4_files) > 10:
        total_duration_sec = (total_duration_sec / 10) * len(mp4_files)
        total_size_gb = (total_size_gb / 10) * len(mp4_files)

    metadata = {
        'folder': str(folder),
        'video_count': len(mp4_files),
        'estimated_duration_hours': round(total_duration_sec / 3600, 2),
        'total_size_gb': round(total_size_gb, 2)
    }

    return True, metadata


def get_video_duration(video_path: Path) -> Optional[float]:
    """
    Get video duration in seconds using ffprobe.

    Args:
        video_path: Path to video file

    Returns:
        Duration in seconds or None if failed
    """
    try:
        result = subprocess.run(
            [
                'ffprobe', '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                str(video_path)
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0 and result.stdout.strip():
            return float(result.stdout.strip())

    except (subprocess.SubprocessError, ValueError):
        pass

    return None


if __name__ == "__main__":
    # Quick validation test
    print("=== Audio Transcription Pipeline - Validation Check ===\n")

    print("1. Checking FFmpeg...")
    if check_ffmpeg_installed():
        print("   ✅ FFmpeg installed\n")
    else:
        print("   ❌ FFmpeg not found\n")

    print("2. Checking GPU...")
    gpu_info = get_gpu_info()
    if gpu_info and gpu_info.get('gpu_detected'):
        print(f"   ✅ GPU detected: {gpu_info['device_count']} device(s)")
        for dev in gpu_info.get('devices', []):
            print(f"      - {dev['name']} ({dev['free_mem_mb']} MB free)")
        print(f"   CUDA: {gpu_info.get('cuda_version')}")
        print(f"   Driver: {gpu_info.get('driver_version')}\n")
    else:
        print("   ❌ No GPU detected (CPU fallback will be used)\n")

    print("3. Auto-discovering video folders...")
    discovered = auto_discover_videos()
    if discovered:
        print(f"   ✅ Found {len(discovered)} folder(s):")
        for folder in discovered:
            print(f"      - {folder}")
    else:
        print("   ❌ No video folders found")

    print("\n=== Validation Complete ===")

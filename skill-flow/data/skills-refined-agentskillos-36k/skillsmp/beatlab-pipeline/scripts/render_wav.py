#!/usr/bin/env python3
"""
BeatLab WAV Renderer

Usage:
    python3 render_wav.py <beat.json> <output.wav>

Renders beat data to a WAV audio file using simple synthesis.
"""

import json
import math
import struct
import sys
import random

# Audio settings
SAMPLE_RATE = 44100
CHANNELS = 2
BITS_PER_SAMPLE = 16

# MIDI note frequencies
NOTE_FREQS = {
    "C5": 523.25, "B4": 493.88, "A4": 440.00, "G4": 392.00, "F4": 349.23,
    "E4": 329.63, "D4": 293.66, "C4": 261.63, "B3": 246.94, "A3": 220.00, "G3": 196.00
}


def generate_sine(freq: float, duration: float, volume: float = 0.3) -> list[float]:
    """Generate a sine wave with decay envelope."""
    samples = int(SAMPLE_RATE * duration)
    result = []
    for i in range(samples):
        t = i / SAMPLE_RATE
        envelope = math.exp(-t * 5)  # Decay envelope
        sample = math.sin(2 * math.pi * freq * t) * envelope * volume
        result.append(sample)
    return result


def generate_kick(duration: float = 0.2, volume: float = 0.8) -> list[float]:
    """Generate a kick drum sound (pitch-dropping sine)."""
    samples = int(SAMPLE_RATE * duration)
    result = []
    for i in range(samples):
        t = i / SAMPLE_RATE
        freq = 150 * math.exp(-t * 30) + 40  # Pitch drops from ~150Hz to ~40Hz
        envelope = math.exp(-t * 10)
        sample = math.sin(2 * math.pi * freq * t) * envelope * volume
        result.append(sample)
    return result


def generate_snare(duration: float = 0.15, volume: float = 0.6) -> list[float]:
    """Generate a snare drum sound (noise + tone)."""
    samples = int(SAMPLE_RATE * duration)
    result = []
    for i in range(samples):
        t = i / SAMPLE_RATE
        envelope = math.exp(-t * 20)
        noise = (random.random() * 2 - 1) * 0.7
        tone = math.sin(2 * math.pi * 200 * t) * 0.3
        sample = (noise + tone) * envelope * volume
        result.append(sample)
    return result


def generate_hihat(duration: float = 0.05, volume: float = 0.3) -> list[float]:
    """Generate a hi-hat sound (filtered noise)."""
    samples = int(SAMPLE_RATE * duration)
    result = []
    for i in range(samples):
        t = i / SAMPLE_RATE
        envelope = math.exp(-t * 50)
        noise = (random.random() * 2 - 1)
        sample = noise * envelope * volume
        result.append(sample)
    return result


def generate_clap(duration: float = 0.12, volume: float = 0.5) -> list[float]:
    """Generate a clap sound (multiple noise bursts)."""
    samples = int(SAMPLE_RATE * duration)
    result = []
    for i in range(samples):
        t = i / SAMPLE_RATE
        envelope = math.exp(-t * 25)
        # Multiple hits effect
        if t < 0.02:
            burst = 1.0 if random.random() > 0.3 else 0.5
        else:
            burst = 1.0
        noise = (random.random() * 2 - 1)
        sample = noise * envelope * volume * burst
        result.append(sample)
    return result


def generate_openhat(duration: float = 0.2, volume: float = 0.35) -> list[float]:
    """Generate an open hi-hat sound."""
    samples = int(SAMPLE_RATE * duration)
    result = []
    for i in range(samples):
        t = i / SAMPLE_RATE
        envelope = math.exp(-t * 8)
        noise = (random.random() * 2 - 1)
        sample = noise * envelope * volume
        result.append(sample)
    return result


def generate_tom(duration: float = 0.2, volume: float = 0.5) -> list[float]:
    """Generate a tom drum sound."""
    samples = int(SAMPLE_RATE * duration)
    result = []
    for i in range(samples):
        t = i / SAMPLE_RATE
        freq = 100 * math.exp(-t * 10) + 80
        envelope = math.exp(-t * 8)
        sample = math.sin(2 * math.pi * freq * t) * envelope * volume
        result.append(sample)
    return result


def generate_crash(duration: float = 0.5, volume: float = 0.4) -> list[float]:
    """Generate a crash cymbal sound."""
    samples = int(SAMPLE_RATE * duration)
    result = []
    for i in range(samples):
        t = i / SAMPLE_RATE
        envelope = math.exp(-t * 3)
        noise = (random.random() * 2 - 1)
        sample = noise * envelope * volume
        result.append(sample)
    return result


def generate_ride(duration: float = 0.3, volume: float = 0.3) -> list[float]:
    """Generate a ride cymbal sound."""
    samples = int(SAMPLE_RATE * duration)
    result = []
    for i in range(samples):
        t = i / SAMPLE_RATE
        envelope = math.exp(-t * 5)
        noise = (random.random() * 2 - 1) * 0.6
        tone = math.sin(2 * math.pi * 400 * t) * 0.4
        sample = (noise + tone) * envelope * volume
        result.append(sample)
    return result


def generate_shaker(duration: float = 0.08, volume: float = 0.25) -> list[float]:
    """Generate a shaker sound."""
    samples = int(SAMPLE_RATE * duration)
    result = []
    for i in range(samples):
        t = i / SAMPLE_RATE
        envelope = math.exp(-t * 30)
        noise = (random.random() * 2 - 1)
        sample = noise * envelope * volume
        result.append(sample)
    return result


def generate_cowbell(duration: float = 0.15, volume: float = 0.4) -> list[float]:
    """Generate a cowbell sound."""
    samples = int(SAMPLE_RATE * duration)
    result = []
    for i in range(samples):
        t = i / SAMPLE_RATE
        envelope = math.exp(-t * 12)
        tone1 = math.sin(2 * math.pi * 560 * t) * 0.6
        tone2 = math.sin(2 * math.pi * 845 * t) * 0.4
        sample = (tone1 + tone2) * envelope * volume
        result.append(sample)
    return result


DRUM_GENERATORS = {
    "Kick": generate_kick,
    "Snare": generate_snare,
    "HiHat": generate_hihat,
    "Clap": generate_clap,
    "OpenHat": generate_openhat,
    "Tom": generate_tom,
    "Crash": generate_crash,
    "Ride": generate_ride,
    "Shaker": generate_shaker,
    "Cowbell": generate_cowbell,
}


def render_beat(data: dict) -> bytes:
    """Render beat data to WAV audio."""
    bpm = data.get("bpm", 120)
    piano_seq = data.get("pianoSequence", {})
    drum_seq = data.get("drumSequence", {})

    # Calculate timing
    seconds_per_beat = 60.0 / bpm
    seconds_per_step = seconds_per_beat / 4  # 16th notes

    # Total duration: 16 steps + extra for decay
    total_duration = 16 * seconds_per_step + 1.0
    total_samples = int(SAMPLE_RATE * total_duration)

    # Initialize stereo buffer
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    # Render piano notes
    for note, steps in piano_seq.items():
        if note in NOTE_FREQS:
            freq = NOTE_FREQS[note]
            for step in steps:
                start_sample = int(step * seconds_per_step * SAMPLE_RATE)
                sound = generate_sine(freq, 0.3)
                for i, sample in enumerate(sound):
                    if start_sample + i < total_samples:
                        left[start_sample + i] += sample * 0.7
                        right[start_sample + i] += sample * 0.7

    # Render drum sounds
    for drum, steps in drum_seq.items():
        if drum in DRUM_GENERATORS:
            generator = DRUM_GENERATORS[drum]
            for step in steps:
                start_sample = int(step * seconds_per_step * SAMPLE_RATE)
                sound = generator()
                for i, sample in enumerate(sound):
                    if start_sample + i < total_samples:
                        left[start_sample + i] += sample
                        right[start_sample + i] += sample

    # Normalize and convert to 16-bit PCM
    max_val = max(max(abs(s) for s in left), max(abs(s) for s in right), 0.001)
    if max_val > 1.0:
        scale = 0.9 / max_val
        left = [s * scale for s in left]
        right = [s * scale for s in right]

    # Convert to bytes
    audio_data = bytearray()
    for l, r in zip(left, right):
        l_int = int(max(-32768, min(32767, l * 32767)))
        r_int = int(max(-32768, min(32767, r * 32767)))
        audio_data.extend(struct.pack('<hh', l_int, r_int))

    # Build WAV file
    data_size = len(audio_data)
    wav_data = bytearray()

    # RIFF header
    wav_data.extend(b'RIFF')
    wav_data.extend(struct.pack('<I', 36 + data_size))
    wav_data.extend(b'WAVE')

    # fmt chunk
    wav_data.extend(b'fmt ')
    wav_data.extend(struct.pack('<I', 16))  # Chunk size
    wav_data.extend(struct.pack('<H', 1))   # PCM format
    wav_data.extend(struct.pack('<H', CHANNELS))
    wav_data.extend(struct.pack('<I', SAMPLE_RATE))
    wav_data.extend(struct.pack('<I', SAMPLE_RATE * CHANNELS * BITS_PER_SAMPLE // 8))  # Byte rate
    wav_data.extend(struct.pack('<H', CHANNELS * BITS_PER_SAMPLE // 8))  # Block align
    wav_data.extend(struct.pack('<H', BITS_PER_SAMPLE))

    # data chunk
    wav_data.extend(b'data')
    wav_data.extend(struct.pack('<I', data_size))
    wav_data.extend(audio_data)

    return bytes(wav_data)


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 render_wav.py <beat.json> <output.wav>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        with open(input_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Set random seed for reproducibility
    random.seed(42)

    wav_data = render_beat(data)

    with open(output_path, "wb") as f:
        f.write(wav_data)

    print(f"WAV rendered: {output_path}")


if __name__ == "__main__":
    main()

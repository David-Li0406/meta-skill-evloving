#!/usr/bin/env python3
"""
Sound Effects Generator for Multiplayer Racer

Generates programmatic audio for game sound effects:
- Engine sounds (idle, rev)
- Collision sounds (soft, hard)
- Tire screech
- UI sounds (player join chime, button click)
"""

import numpy as np
from scipy.io import wavfile
import os
import subprocess
import sys

SAMPLE_RATE = 44100
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../../static/audio/sfx')


def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_sound(samples, filename, use_mp3=True):
    """Save samples to audio file"""
    # Normalize to prevent clipping
    max_val = np.max(np.abs(samples))
    if max_val > 0:
        samples = samples / max_val * 0.9

    # Convert to 16-bit
    samples_16bit = (samples * 32767).astype(np.int16)

    filepath = os.path.join(OUTPUT_DIR, filename)
    wav_path = filepath.replace('.mp3', '.wav')

    # Save as WAV
    wavfile.write(wav_path, SAMPLE_RATE, samples_16bit)
    print(f"  Saved: {wav_path}")

    # Convert to MP3 if requested
    if use_mp3 and filename.endswith('.mp3'):
        try:
            subprocess.run([
                'ffmpeg', '-y', '-i', wav_path,
                '-codec:a', 'libmp3lame', '-b:a', '128k',
                filepath
            ], capture_output=True, check=True)
            os.remove(wav_path)
            print(f"  Converted to: {filepath}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"  Warning: Could not convert to MP3 (ffmpeg not available?)")
            print(f"  Keeping WAV file: {wav_path}")


def generate_engine_idle():
    """Generate low rumbling idle engine sound (loopable)"""
    print("Generating engine_idle...")
    duration = 2.5
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    base_freq = 65  # Low rumble

    # Slight random wobble for realism
    wobble = 1 + 0.015 * np.sin(2 * np.pi * 3.5 * t)
    wobble += 0.01 * np.sin(2 * np.pi * 7 * t)

    # Multiple harmonics
    sound = 0.5 * np.sin(2 * np.pi * base_freq * wobble * t)
    sound += 0.25 * np.sin(2 * np.pi * base_freq * 2 * wobble * t)
    sound += 0.12 * np.sin(2 * np.pi * base_freq * 3 * wobble * t)
    sound += 0.06 * np.sin(2 * np.pi * base_freq * 4 * wobble * t)

    # Add filtered noise for texture
    noise = np.random.uniform(-1, 1, len(t))
    # Simple low-pass by averaging
    noise_filtered = np.convolve(noise, np.ones(100)/100, mode='same')
    sound += noise_filtered * 0.08

    # Crossfade for seamless loop
    fade_samples = int(SAMPLE_RATE * 0.1)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)

    sound[:fade_samples] = sound[:fade_samples] * fade_in + sound[-fade_samples:] * fade_out
    sound = sound[:-fade_samples]  # Trim end for perfect loop

    save_sound(sound, 'engine_idle.mp3')


def generate_engine_rev():
    """Generate higher-pitched engine rev sound (loopable)"""
    print("Generating engine_rev...")
    duration = 2.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    base_freq = 120  # Higher for revving

    # More aggressive wobble
    wobble = 1 + 0.03 * np.sin(2 * np.pi * 8 * t)
    wobble += 0.02 * np.sin(2 * np.pi * 12 * t)

    # Richer harmonics
    sound = 0.4 * np.sin(2 * np.pi * base_freq * wobble * t)
    sound += 0.3 * np.sin(2 * np.pi * base_freq * 2 * wobble * t)
    sound += 0.2 * np.sin(2 * np.pi * base_freq * 3 * wobble * t)
    sound += 0.1 * np.sin(2 * np.pi * base_freq * 4 * wobble * t)
    sound += 0.05 * np.sin(2 * np.pi * base_freq * 5 * wobble * t)

    # More noise for aggressive character
    noise = np.random.uniform(-1, 1, len(t))
    noise_filtered = np.convolve(noise, np.ones(50)/50, mode='same')
    sound += noise_filtered * 0.12

    # Crossfade for loop
    fade_samples = int(SAMPLE_RATE * 0.08)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    sound[:fade_samples] = sound[:fade_samples] * fade_in + sound[-fade_samples:] * fade_out
    sound = sound[:-fade_samples]

    save_sound(sound, 'engine_rev.mp3')


def generate_collision_soft():
    """Generate soft collision/bump sound"""
    print("Generating collision_soft...")
    duration = 0.25
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Quick decay envelope
    envelope = np.exp(-t * 25)

    # Low thump
    thump = np.sin(2 * np.pi * 80 * t) * envelope

    # Noise burst
    noise = np.random.uniform(-1, 1, len(t)) * envelope * 0.3

    sound = thump * 0.7 + noise * 0.3
    save_sound(sound, 'collision_soft.mp3')


def generate_collision_hard():
    """Generate hard collision/crash sound"""
    print("Generating collision_hard...")
    duration = 0.5
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Slower decay for more impact
    envelope = np.exp(-t * 12)

    # Deep thump
    thump = np.sin(2 * np.pi * 60 * t) * envelope

    # Add mid-range impact
    mid = np.sin(2 * np.pi * 200 * t) * envelope * 0.3

    # Metallic ring
    ring = np.sin(2 * np.pi * 1200 * t) * np.exp(-t * 30) * 0.15

    # More noise
    noise = np.random.uniform(-1, 1, len(t)) * envelope * 0.4

    sound = thump * 0.5 + mid + ring + noise * 0.3
    save_sound(sound, 'collision_hard.mp3')


def generate_tire_screech():
    """Generate tire screech/skid sound (loopable)"""
    print("Generating tire_screech...")
    duration = 1.5
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # High-frequency noise base
    noise = np.random.uniform(-1, 1, len(t))

    # Band-pass effect: differentiate then integrate slightly
    screech = np.diff(noise, prepend=noise[0])
    screech = np.convolve(screech, np.ones(3)/3, mode='same')

    # Pitch modulation for realism
    mod = np.sin(2 * np.pi * 12 * t) * 0.3 + np.sin(2 * np.pi * 5 * t) * 0.2
    pitch = 3000 + 800 * mod
    carrier = np.sin(2 * np.pi * np.cumsum(pitch / SAMPLE_RATE))

    sound = screech * 0.4 + carrier * 0.15

    # Fade ends for loop
    fade = int(0.1 * SAMPLE_RATE)
    envelope = np.ones(len(t))
    envelope[:fade] *= np.linspace(0, 1, fade)
    envelope[-fade:] *= np.linspace(1, 0, fade)

    sound = sound * envelope * 0.6
    save_sound(sound, 'tire_screech.mp3')


def generate_player_join():
    """Generate pleasant chime for player join notification"""
    print("Generating player_join...")
    duration = 0.5
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Two-note ascending chime (C5 -> E5)
    freq1, freq2 = 523, 659

    half = len(t) // 2
    note1_t = t[:half]
    note2_t = t[half:]

    note1 = np.sin(2 * np.pi * freq1 * note1_t) * np.exp(-note1_t * 4)
    note2 = np.sin(2 * np.pi * freq2 * (note2_t - note2_t[0])) * np.exp(-(note2_t - note2_t[0]) * 4)

    sound = np.concatenate([note1, note2]) * 0.5
    save_sound(sound, 'player_join.mp3')


def generate_button_click():
    """Generate short UI click sound"""
    print("Generating button_click...")
    duration = 0.06
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Quick pop with fast decay
    freq = 1200
    sound = np.sin(2 * np.pi * freq * t) * np.exp(-t * 80) * 0.4

    # Add a tiny click transient
    click = np.zeros(len(t))
    click[:int(0.002 * SAMPLE_RATE)] = 0.3

    sound = sound + click
    save_sound(sound, 'button_click.mp3')


def generate_countdown_beep():
    """Generate countdown beep (for 3-2-1)"""
    print("Generating countdown_beep...")
    duration = 0.15
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    freq = 880  # A5
    sound = np.sin(2 * np.pi * freq * t) * np.exp(-t * 15) * 0.5

    save_sound(sound, 'countdown_beep.mp3')


def generate_countdown_go():
    """Generate 'GO!' sound (higher pitch, longer)"""
    print("Generating countdown_go...")
    duration = 0.4
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Rising pitch sweep
    freq_start, freq_end = 600, 1200
    freq = freq_start + (freq_end - freq_start) * (t / duration)

    sound = np.sin(2 * np.pi * np.cumsum(freq / SAMPLE_RATE))
    sound += 0.3 * np.sin(2 * np.pi * np.cumsum(freq * 2 / SAMPLE_RATE))

    envelope = np.exp(-t * 4) * 0.6
    sound = sound * envelope

    save_sound(sound, 'countdown_go.mp3')


def main():
    print("=" * 50)
    print("Sound Effects Generator for Multiplayer Racer")
    print("=" * 50)

    ensure_output_dir()
    print(f"\nOutput directory: {OUTPUT_DIR}\n")

    # Generate all sounds
    generate_engine_idle()
    generate_engine_rev()
    generate_collision_soft()
    generate_collision_hard()
    generate_tire_screech()
    generate_player_join()
    generate_button_click()
    generate_countdown_beep()
    generate_countdown_go()

    print("\n" + "=" * 50)
    print("All sounds generated successfully!")
    print("=" * 50)


if __name__ == '__main__':
    main()

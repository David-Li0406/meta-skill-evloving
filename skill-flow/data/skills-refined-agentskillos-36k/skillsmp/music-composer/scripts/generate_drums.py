#!/usr/bin/env python3
"""
Generate drum patterns and rhythms.
"""

import argparse
import random
from midi_utils import (
    create_midi_file, add_note, beats_to_ticks, bars_to_ticks, DRUM_MAP
)


# Drum patterns by style
DRUM_PATTERNS = {
    'rock': {
        'kick': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        'snare': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        'closed_hat': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    },
    'disco': {
        'kick': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        'snare': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        'closed_hat': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'open_hat': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    },
    'techno': {
        'kick': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        'clap': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        'closed_hat': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        'open_hat': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    },
    'jazz': {
        'kick': [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],  # Triplet feel
        'snare': [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
        'ride': [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    },
    'hiphop': {
        'kick': [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        'closed_hat': [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    },
    'dnb': {  # Drum and Bass
        'kick': [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        'closed_hat': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    },
    'reggaeton': {
        'kick': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        'snare': [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        'closed_hat': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    },
}


def generate_pattern(style, bars=4, tempo=120, variations=False):
    """Generate drum pattern.
    
    Args:
        style: Style name
        bars: Number of bars
        tempo: BPM
        variations: Add variations to pattern
    
    Returns:
        MIDI file
    """
    if style not in DRUM_PATTERNS:
        raise ValueError(f"Unknown style: {style}")
    
    pattern = DRUM_PATTERNS[style]
    
    mid = create_midi_file(tempo=tempo)
    track = mid.tracks[0]
    
    # Calculate timing
    steps_per_bar = max(len(p) for p in pattern.values())
    ticks_per_step = bars_to_ticks(1, 4) // steps_per_bar
    
    print(f"Generating {style} pattern:")
    print(f"  Bars: {bars}")
    print(f"  Tempo: {tempo} BPM")
    print(f"  Steps per bar: {steps_per_bar}")
    
    # Generate for each bar
    for bar in range(bars):
        for instrument, hits in pattern.items():
            if instrument not in DRUM_MAP:
                continue
            
            note = DRUM_MAP[instrument]
            
            for step, hit in enumerate(hits):
                if hit:
                    # Calculate timing
                    absolute_step = bar * steps_per_bar + step
                    
                    # Velocity variations
                    if variations:
                        if step % 4 == 0:  # Downbeat
                            velocity = random.randint(100, 115)
                        else:
                            velocity = random.randint(70, 90)
                    else:
                        velocity = 100 if step % 4 == 0 else 80
                    
                    # Duration (short for drums)
                    duration = ticks_per_step // 4
                    
                    # Delay (calculated from step position)
                    if absolute_step == 0:
                        delay = 0
                    else:
                        delay = 0  # Encoded in previous note
                    
                    add_note(track, note, velocity, duration, delay, channel=9)
    
    return mid


def main():
    parser = argparse.ArgumentParser(description='Generate drum patterns')
    parser.add_argument('--style', default='rock',
                       choices=list(DRUM_PATTERNS.keys()),
                       help='Drum style')
    parser.add_argument('--tempo', type=int, default=120, help='Tempo in BPM')
    parser.add_argument('--bars', type=int, default=4, help='Number of bars')
    parser.add_argument('--variations', action='store_true',
                       help='Add velocity variations')
    parser.add_argument('--output', default='drums.mid', help='Output file')
    parser.add_argument('--list-styles', action='store_true',
                       help='List available styles')
    
    args = parser.parse_args()
    
    if args.list_styles:
        print("Available drum styles:")
        for style in sorted(DRUM_PATTERNS.keys()):
            instruments = ', '.join(DRUM_PATTERNS[style].keys())
            print(f"  {style:15s} ({instruments})")
        return
    
    # Generate
    mid = generate_pattern(args.style, args.bars, args.tempo, args.variations)
    
    # Save
    mid.save(args.output)
    print(f"\n✅ Saved to {args.output}")


if __name__ == "__main__":
    main()

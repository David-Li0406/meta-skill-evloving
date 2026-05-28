#!/usr/bin/env python3
"""
Generate melodic lines using various algorithms.
"""

import argparse
import random
from midi_utils import (
    create_midi_file, add_note, get_scale_notes, note_name_to_number,
    beats_to_ticks, humanize_velocity, humanize_timing
)


def generate_random_walk_melody(scale_notes, length, start_note=None):
    """Generate melody using random walk algorithm.
    
    Args:
        scale_notes: List of available notes
        length: Number of notes to generate
        start_note: Starting note (random if None)
    
    Returns:
        List of MIDI note numbers
    """
    if start_note is None:
        current_idx = len(scale_notes) // 2
    else:
        current_idx = scale_notes.index(start_note)
    
    melody = [scale_notes[current_idx]]
    
    for _ in range(length - 1):
        # Random walk: move up, down, or stay
        move = random.choice([-2, -1, 0, 1, 2])
        current_idx = max(0, min(len(scale_notes) - 1, current_idx + move))
        melody.append(scale_notes[current_idx])
    
    return melody


def generate_contour_melody(scale_notes, length, contour='arch'):
    """Generate melody with specific contour.
    
    Args:
        scale_notes: List of available notes
        length: Number of notes
        contour: Shape - 'arch', 'valley', 'ascending', 'descending'
    
    Returns:
        List of MIDI note numbers
    """
    melody = []
    
    if contour == 'arch':
        # Start low, rise to peak, descend
        for i in range(length):
            position = (i / (length - 1)) if length > 1 else 0
            if position < 0.5:
                idx = int(position * 2 * len(scale_notes))
            else:
                idx = int((1 - (position - 0.5) * 2) * len(scale_notes))
            melody.append(scale_notes[min(idx, len(scale_notes) - 1)])
    
    elif contour == 'valley':
        # Start high, descend to valley, ascend
        for i in range(length):
            position = (i / (length - 1)) if length > 1 else 0
            if position < 0.5:
                idx = int((1 - position * 2) * len(scale_notes))
            else:
                idx = int(((position - 0.5) * 2) * len(scale_notes))
            melody.append(scale_notes[min(idx, len(scale_notes) - 1)])
    
    elif contour == 'ascending':
        # Gradually ascend
        for i in range(length):
            idx = int((i / length) * len(scale_notes))
            melody.append(scale_notes[min(idx, len(scale_notes) - 1)])
    
    elif contour == 'descending':
        # Gradually descend
        for i in range(length):
            idx = int((1 - i / length) * len(scale_notes))
            melody.append(scale_notes[min(idx, len(scale_notes) - 1)])
    
    return melody


def generate_rhythmic_pattern(length, complexity='medium'):
    """Generate rhythmic pattern.
    
    Args:
        length: Number of notes
        complexity: 'simple', 'medium', 'complex'
    
    Returns:
        List of durations in beats
    """
    if complexity == 'simple':
        # Mostly quarter and half notes
        durations = [1, 1, 1, 1, 2, 2]
    elif complexity == 'medium':
        # Mix of quarter, eighth, half
        durations = [0.5, 0.5, 1, 1, 1, 2]
    else:  # complex
        # Include sixteenths and dotted notes
        durations = [0.25, 0.5, 0.75, 1, 1.5, 2]
    
    pattern = []
    beats_so_far = 0
    target_beats = length * 0.75  # Average duration
    
    while len(pattern) < length:
        duration = random.choice(durations)
        pattern.append(duration)
        beats_so_far += duration
    
    return pattern[:length]


def main():
    parser = argparse.ArgumentParser(description='Generate melodic MIDI lines')
    parser.add_argument('--key', default='C', help='Key (C, D, E, F, G, A, B)')
    parser.add_argument('--scale', default='major', 
                       help='Scale type (major, minor, pentatonic_major, etc.)')
    parser.add_argument('--octave', type=int, default=4, help='Starting octave')
    parser.add_argument('--length', type=int, default=16, help='Number of notes')
    parser.add_argument('--tempo', type=int, default=120, help='Tempo in BPM')
    parser.add_argument('--algorithm', default='random_walk',
                       choices=['random_walk', 'arch', 'valley', 'ascending', 'descending'],
                       help='Melody generation algorithm')
    parser.add_argument('--rhythm', default='medium',
                       choices=['simple', 'medium', 'complex'],
                       help='Rhythmic complexity')
    parser.add_argument('--output', default='melody.mid', help='Output MIDI file')
    parser.add_argument('--velocity', type=int, default=80, help='Base velocity')
    parser.add_argument('--humanize', action='store_true', 
                       help='Add human-like variations')
    
    args = parser.parse_args()
    
    # Get scale notes
    scale_notes = get_scale_notes(args.key, args.octave, args.scale, num_octaves=2)
    
    # Generate melody
    if args.algorithm == 'random_walk':
        melody = generate_random_walk_melody(scale_notes, args.length)
    else:
        melody = generate_contour_melody(scale_notes, args.length, args.algorithm)
    
    # Generate rhythm
    rhythms = generate_rhythmic_pattern(args.length, args.rhythm)
    
    # Create MIDI file
    mid = create_midi_file(tempo=args.tempo)
    track = mid.tracks[0]
    
    # Add melody notes
    ticks_per_beat = 480
    for i, (note, duration) in enumerate(zip(melody, rhythms)):
        velocity = args.velocity
        duration_ticks = beats_to_ticks(duration, ticks_per_beat)
        delay = 0 if i == 0 else 0  # Delay is encoded in previous note_off
        
        if args.humanize:
            velocity = humanize_velocity(velocity, variation=10)
            duration_ticks = humanize_timing(duration_ticks, variation=15)
        
        add_note(track, note, velocity, duration_ticks, delay)
    
    # Save
    mid.save(args.output)
    print(f"✅ Melody saved to {args.output}")
    print(f"   Key: {args.key} {args.scale}")
    print(f"   Length: {args.length} notes")
    print(f"   Algorithm: {args.algorithm}")
    print(f"   Tempo: {args.tempo} BPM")


if __name__ == "__main__":
    main()

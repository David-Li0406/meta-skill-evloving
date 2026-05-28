#!/usr/bin/env python3
"""
Generate chord progressions and output to MIDI.
"""

import argparse
from midi_utils import (
    create_midi_file, add_chord, get_chord_notes, note_name_to_number,
    bars_to_ticks, NOTE_NAMES
)


# Common chord progressions by genre
PROGRESSIONS = {
    # Pop/Rock
    'pop': ['I', 'V', 'vi', 'IV'],
    'pop_alternative': ['vi', 'IV', 'I', 'V'],
    'rock': ['I', 'bVII', 'IV', 'I'],
    'blues': ['I', 'I', 'I', 'I', 'IV', 'IV', 'I', 'I', 'V', 'IV', 'I', 'V'],
    
    # Jazz
    'jazz_251': ['ii', 'V', 'I'],
    'jazz_blues': ['I7', 'IV7', 'I7', 'I7', 'IV7', 'IV7', 'I7', 'I7', 'ii', 'V7', 'I7', 'V7'],
    'rhythm_changes': ['I', 'vi', 'ii', 'V'],
    
    # Classical
    'classical': ['I', 'IV', 'V', 'I'],
    'plagal': ['I', 'IV', 'I'],
    'andalusian': ['i', 'bVII', 'bVI', 'V'],
    
    # Electronic/EDM
    'edm': ['vi', 'IV', 'I', 'V'],
    'progressive': ['I', 'bVII', 'bVI', 'bVII'],
}


def parse_roman_numeral(numeral, key_note, scale='major'):
    """Convert Roman numeral to chord.
    
    Args:
        numeral: Roman numeral (e.g., 'I', 'ii', 'V7', 'bVII')
        key_note: Root note of the key
        scale: Major or minor scale
    
    Returns:
        Tuple of (root_note_name, chord_type)
    """
    # Parse the numeral
    flat = numeral.startswith('b')
    if flat:
        numeral = numeral[1:]
    
    # Extract quality and extensions
    base = numeral.rstrip('0123456789')
    extensions = numeral[len(base):]
    
    # Determine chord type from case
    is_minor = base.islower()
    base_upper = base.upper()
    
    # Scale degrees (0-indexed)
    scale_degrees = {
        'major': [0, 2, 4, 5, 7, 9, 11],
        'minor': [0, 2, 3, 5, 7, 8, 10]
    }
    
    roman_to_degree = {
        'I': 0, 'II': 1, 'III': 2, 'IV': 3,
        'V': 4, 'VI': 5, 'VII': 6
    }
    
    degree = roman_to_degree.get(base_upper, 0)
    root_offset = scale_degrees[scale][degree]
    
    if flat:
        root_offset -= 1
    
    # Calculate absolute note
    key_num = NOTE_NAMES[key_note]
    root_num = (key_num + root_offset) % 12
    
    # Find note name for this number
    root_name = None
    for name, num in NOTE_NAMES.items():
        if num == root_num and '#' not in name:  # Prefer natural names
            root_name = name
            break
    if not root_name:
        for name, num in NOTE_NAMES.items():
            if num == root_num:
                root_name = name
                break
    
    # Determine chord quality
    if '7' in extensions:
        if is_minor:
            chord_type = 'min7'
        else:
            if base_upper == 'VII':
                chord_type = 'min7b5'  # Half-diminished
            else:
                chord_type = 'dom7' if base_upper == 'V' else 'maj7'
    elif 'dim' in extensions:
        chord_type = 'dim'
    else:
        chord_type = 'minor' if is_minor else 'major'
    
    return root_name, chord_type


def get_progression_chords(progression_name, key_note, octave=3):
    """Get chords for a named progression.
    
    Args:
        progression_name: Name of progression
        key_note: Root note of key
        octave: Bass octave for chords
    
    Returns:
        List of tuples (chord_notes, chord_name)
    """
    if progression_name not in PROGRESSIONS:
        raise ValueError(f"Unknown progression: {progression_name}")
    
    numerals = PROGRESSIONS[progression_name]
    chords = []
    
    for numeral in numerals:
        root_name, chord_type = parse_roman_numeral(numeral, key_note)
        notes = get_chord_notes(root_name, octave, chord_type)
        chords.append((notes, f"{root_name}{chord_type}"))
    
    return chords


def main():
    parser = argparse.ArgumentParser(description='Generate chord progression MIDI')
    parser.add_argument('--progression', default='pop',
                       help='Progression name or custom (e.g., "I-IV-V-I")')
    parser.add_argument('--key', default='C', help='Key (C, D, E, F, G, A, B)')
    parser.add_argument('--octave', type=int, default=3, help='Bass octave')
    parser.add_argument('--tempo', type=int, default=120, help='Tempo in BPM')
    parser.add_argument('--duration', type=float, default=2.0,
                       help='Duration per chord in beats')
    parser.add_argument('--voicing', default='root',
                       choices=['root', 'first_inv', 'second_inv'],
                       help='Chord voicing')
    parser.add_argument('--output', default='chords.mid', help='Output file')
    parser.add_argument('--list-progressions', action='store_true',
                       help='List available progressions')
    
    args = parser.parse_args()
    
    if args.list_progressions:
        print("Available progressions:")
        for name, prog in sorted(PROGRESSIONS.items()):
            print(f"  {name:20s} {' - '.join(prog)}")
        return
    
    # Get chords
    if '-' in args.progression and args.progression not in PROGRESSIONS:
        # Custom progression
        numerals = args.progression.split('-')
        chords = []
        for numeral in numerals:
            root_name, chord_type = parse_roman_numeral(numeral, args.key)
            notes = get_chord_notes(root_name, args.octave, chord_type)
            chords.append((notes, f"{root_name}{chord_type}"))
    else:
        # Named progression
        chords = get_progression_chords(args.progression, args.key, args.octave)
    
    # Apply voicing
    voiced_chords = []
    for notes, name in chords:
        if args.voicing == 'first_inv' and len(notes) >= 3:
            # Move lowest note up an octave
            notes = notes[1:] + [notes[0] + 12]
        elif args.voicing == 'second_inv' and len(notes) >= 3:
            # Move two lowest notes up an octave
            notes = notes[2:] + [notes[0] + 12, notes[1] + 12]
        voiced_chords.append((notes, name))
    
    # Create MIDI
    mid = create_midi_file(tempo=args.tempo)
    track = mid.tracks[0]
    
    ticks_per_beat = 480
    duration_ticks = int(args.duration * ticks_per_beat)
    
    print(f"Progression: {args.progression}")
    print(f"Key: {args.key}")
    print(f"Chords:")
    
    for i, (notes, name) in enumerate(voiced_chords):
        print(f"  {i+1}. {name}")
        delay = 0 if i == 0 else 0
        add_chord(track, notes, velocity=80, duration=duration_ticks, delay=delay)
    
    # Save
    mid.save(args.output)
    print(f"\n✅ Saved to {args.output}")


if __name__ == "__main__":
    main()

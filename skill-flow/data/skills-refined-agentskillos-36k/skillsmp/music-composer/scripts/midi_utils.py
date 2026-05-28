#!/usr/bin/env python3
"""
Shared MIDI utilities for music composition.
"""

import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage

# Scale definitions (semitones from root)
SCALES = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
    'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'phrygian': [0, 1, 3, 5, 7, 8, 10],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'pentatonic_major': [0, 2, 4, 7, 9],
    'pentatonic_minor': [0, 3, 5, 7, 10],
    'blues': [0, 3, 5, 6, 7, 10],
    'whole_tone': [0, 2, 4, 6, 8, 10],
    'chromatic': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
}

# Note names to MIDI numbers
NOTE_NAMES = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
    'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
}

# General MIDI drum map (channel 10)
DRUM_MAP = {
    'kick': 36,
    'snare': 38,
    'closed_hat': 42,
    'open_hat': 46,
    'crash': 49,
    'ride': 51,
    'tom_low': 45,
    'tom_mid': 47,
    'tom_high': 50,
    'clap': 39,
    'rim': 37,
}


def note_name_to_number(note_name, octave=4):
    """Convert note name and octave to MIDI note number.
    
    Args:
        note_name: Note name (C, C#, Db, etc.)
        octave: Octave number (default 4, middle C = C4)
    
    Returns:
        MIDI note number (0-127)
    """
    return NOTE_NAMES[note_name] + (octave + 1) * 12


def get_scale_notes(root_note, octave, scale_name, num_octaves=1):
    """Get all notes in a scale.
    
    Args:
        root_note: Root note name (C, D, etc.)
        octave: Starting octave
        scale_name: Name of scale (major, minor, etc.)
        num_octaves: Number of octaves to generate
    
    Returns:
        List of MIDI note numbers
    """
    root = note_name_to_number(root_note, octave)
    scale = SCALES.get(scale_name.lower(), SCALES['major'])
    
    notes = []
    for oct in range(num_octaves):
        for interval in scale:
            notes.append(root + interval + (oct * 12))
    
    return notes


def create_midi_file(tempo=120, time_signature=(4, 4)):
    """Create a new MIDI file with basic setup.
    
    Args:
        tempo: BPM (beats per minute)
        time_signature: Tuple of (numerator, denominator)
    
    Returns:
        MidiFile object
    """
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    # Set tempo (microseconds per beat)
    track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo)))
    
    # Set time signature
    track.append(MetaMessage('time_signature', 
                            numerator=time_signature[0],
                            denominator=time_signature[1]))
    
    return mid


def add_note(track, note, velocity, duration, delay=0, channel=0):
    """Add a note to a track.
    
    Args:
        track: MidiTrack object
        note: MIDI note number (0-127)
        velocity: Velocity (0-127)
        duration: Duration in ticks
        delay: Delay before note in ticks
        channel: MIDI channel (0-15)
    """
    track.append(Message('note_on', note=note, velocity=velocity, 
                        time=delay, channel=channel))
    track.append(Message('note_off', note=note, velocity=0, 
                        time=duration, channel=channel))


def add_chord(track, notes, velocity, duration, delay=0, channel=0):
    """Add a chord (multiple notes) to a track.
    
    Args:
        track: MidiTrack object
        notes: List of MIDI note numbers
        velocity: Velocity (0-127)
        duration: Duration in ticks
        delay: Delay before chord in ticks
        channel: MIDI channel (0-15)
    """
    # All notes start at the same time
    for i, note in enumerate(notes):
        track.append(Message('note_on', note=note, velocity=velocity,
                           time=delay if i == 0 else 0, channel=channel))
    
    # All notes end at the same time
    for i, note in enumerate(notes):
        track.append(Message('note_off', note=note, velocity=0,
                           time=duration if i == 0 else 0, channel=channel))


def get_chord_notes(root_note, octave, chord_type='major'):
    """Get notes for a chord.
    
    Args:
        root_note: Root note name
        octave: Octave number
        chord_type: Type of chord (major, minor, dim, aug, maj7, min7, dom7)
    
    Returns:
        List of MIDI note numbers
    """
    root = note_name_to_number(root_note, octave)
    
    chord_intervals = {
        'major': [0, 4, 7],
        'minor': [0, 3, 7],
        'dim': [0, 3, 6],
        'aug': [0, 4, 8],
        'sus2': [0, 2, 7],
        'sus4': [0, 5, 7],
        'maj7': [0, 4, 7, 11],
        'min7': [0, 3, 7, 10],
        'dom7': [0, 4, 7, 10],
        'min7b5': [0, 3, 6, 10],
        'dim7': [0, 3, 6, 9],
    }
    
    intervals = chord_intervals.get(chord_type, chord_intervals['major'])
    return [root + i for i in intervals]


def humanize_velocity(base_velocity, variation=10):
    """Add human-like variation to velocity.
    
    Args:
        base_velocity: Base velocity value
        variation: Maximum variation (+/-)
    
    Returns:
        Humanized velocity value
    """
    import random
    velocity = base_velocity + random.randint(-variation, variation)
    return max(1, min(127, velocity))


def humanize_timing(base_time, variation=10):
    """Add human-like variation to timing.
    
    Args:
        base_time: Base time value in ticks
        variation: Maximum variation in ticks (+/-)
    
    Returns:
        Humanized time value
    """
    import random
    time = base_time + random.randint(-variation, variation)
    return max(0, time)


# Conversion utilities
def beats_to_ticks(beats, ticks_per_beat=480):
    """Convert beats to MIDI ticks."""
    return int(beats * ticks_per_beat)


def bars_to_ticks(bars, time_sig_numerator=4, ticks_per_beat=480):
    """Convert bars to MIDI ticks."""
    return int(bars * time_sig_numerator * ticks_per_beat)


if __name__ == "__main__":
    # Example usage
    print("Music Composer MIDI Utilities")
    print(f"Middle C (C4) = MIDI note {note_name_to_number('C', 4)}")
    print(f"C Major scale: {get_scale_notes('C', 4, 'major')}")
    print(f"C Major chord: {get_chord_notes('C', 4, 'major')}")

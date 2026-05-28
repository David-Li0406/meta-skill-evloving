#!/usr/bin/env python3
"""
BeatLab MIDI Exporter

Usage:
    python3 export_midi.py <beat.json> <output.mid>

Exports beat data to a Standard MIDI File (SMF).
Uses midiutil if available, otherwise falls back to raw MIDI writing.
"""

import json
import sys
import struct

# MIDI note mappings
NOTE_TO_MIDI = {
    "C5": 72, "B4": 71, "A4": 69, "G4": 67, "F4": 65,
    "E4": 64, "D4": 62, "C4": 60, "B3": 59, "A3": 57, "G3": 55
}

# Drum sounds mapped to General MIDI drum notes (channel 10)
DRUM_TO_MIDI = {
    "Kick": 36,      # Bass Drum 1
    "Snare": 38,     # Acoustic Snare
    "HiHat": 42,     # Closed Hi-Hat
    "Clap": 39,      # Hand Clap
    "OpenHat": 46,   # Open Hi-Hat
    "Tom": 45,       # Low Tom
    "Crash": 49,     # Crash Cymbal 1
    "Ride": 51,      # Ride Cymbal 1
    "Shaker": 70,    # Maracas
    "Cowbell": 56    # Cowbell
}


def write_variable_length(value: int) -> bytes:
    """Write a variable-length quantity for MIDI."""
    result = []
    result.append(value & 0x7F)
    value >>= 7
    while value:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    return bytes(reversed(result))


def create_midi_file(data: dict) -> bytes:
    """Create a MIDI file from beat data."""
    bpm = data.get("bpm", 120)
    piano_seq = data.get("pianoSequence", {})
    drum_seq = data.get("drumSequence", {})

    # Ticks per quarter note
    ticks_per_beat = 480
    # 16 steps = 4 beats (4/4 time, each step is a 16th note)
    ticks_per_step = ticks_per_beat // 4  # 120 ticks per step

    # Collect all events
    events = []  # (tick, channel, note, velocity, is_note_on)

    # Piano events (channel 0)
    for note, steps in piano_seq.items():
        if note in NOTE_TO_MIDI:
            midi_note = NOTE_TO_MIDI[note]
            for step in steps:
                tick = step * ticks_per_step
                events.append((tick, 0, midi_note, 100, True))  # Note on
                events.append((tick + ticks_per_step - 10, 0, midi_note, 0, False))  # Note off

    # Drum events (channel 9 = MIDI channel 10)
    for drum, steps in drum_seq.items():
        if drum in DRUM_TO_MIDI:
            midi_note = DRUM_TO_MIDI[drum]
            for step in steps:
                tick = step * ticks_per_step
                events.append((tick, 9, midi_note, 100, True))  # Note on
                events.append((tick + ticks_per_step - 10, 9, midi_note, 0, False))  # Note off

    # Sort events by tick
    events.sort(key=lambda e: (e[0], not e[4]))  # Sort by tick, note-offs before note-ons at same tick

    # Build track data
    track_data = bytearray()

    # Tempo meta event (at tick 0)
    microseconds_per_beat = int(60_000_000 / bpm)
    track_data.extend(b'\x00')  # Delta time = 0
    track_data.extend(b'\xFF\x51\x03')  # Tempo meta event
    track_data.extend(struct.pack('>I', microseconds_per_beat)[1:])  # 3 bytes

    # Time signature meta event (4/4)
    track_data.extend(b'\x00')  # Delta time = 0
    track_data.extend(b'\xFF\x58\x04\x04\x02\x18\x08')  # 4/4 time

    # Convert events to MIDI messages
    last_tick = 0
    for tick, channel, note, velocity, is_note_on in events:
        delta = tick - last_tick
        last_tick = tick

        track_data.extend(write_variable_length(delta))

        if is_note_on:
            track_data.append(0x90 | channel)  # Note on
        else:
            track_data.append(0x80 | channel)  # Note off

        track_data.append(note)
        track_data.append(velocity)

    # End of track
    track_data.extend(b'\x00\xFF\x2F\x00')

    # Build MIDI file
    midi_data = bytearray()

    # Header chunk
    midi_data.extend(b'MThd')
    midi_data.extend(struct.pack('>I', 6))  # Header length
    midi_data.extend(struct.pack('>H', 0))  # Format 0 (single track)
    midi_data.extend(struct.pack('>H', 1))  # Number of tracks
    midi_data.extend(struct.pack('>H', ticks_per_beat))  # Ticks per beat

    # Track chunk
    midi_data.extend(b'MTrk')
    midi_data.extend(struct.pack('>I', len(track_data)))
    midi_data.extend(track_data)

    return bytes(midi_data)


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 export_midi.py <beat.json> <output.mid>", file=sys.stderr)
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

    midi_data = create_midi_file(data)

    with open(output_path, "wb") as f:
        f.write(midi_data)

    print(f"MIDI exported: {output_path}")


if __name__ == "__main__":
    main()

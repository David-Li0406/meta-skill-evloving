# Assets Directory

## Templates

This directory contains MIDI templates for quick project starts.

### Creating a Template MIDI File

Use the scripts to generate starting templates:

```bash
# Empty track template
python ../scripts/generate_chords.py --key C --progression "I-IV-V-I" --output templates/chord_template.mid

# Drum pattern template
python ../scripts/generate_drums.py --style rock --bars 4 --output templates/drums_rock.mid
```

### Custom Templates

Create your own templates by:
1. Generating MIDI using the scripts
2. Opening in a DAW
3. Adjusting as needed
4. Saving back to this directory

### Template Usage

Copy templates to your project folder as a starting point:
```bash
cp templates/chord_template.mid my_song.mid
```

## Recommended Template Structure

For a complete project template:
1. Track 1: Drums (channel 10)
2. Track 2: Bass
3. Track 3: Chords/Piano
4. Track 4: Lead/Melody
5. Track 5+: Additional instruments

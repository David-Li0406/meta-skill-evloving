# Terminal Print Workflow

Detailed documentation for the terminal-print skill.

## Pipeline Architecture

````
┌─────────────────────────────────────────────────────────────────────┐
│                        INPUT (Clipboard or File)                     │
│                     pbpaste  OR  cat file.txt                        │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │      Strip ANSI Codes       │
                    │   sed 's/\x1b\[[0-9;]*m//g' │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │   Wrap in Markdown Code     │
                    │   Block with ```text        │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │   pandoc + xelatex          │
                    │   Markdown → PDF            │
                    │   (Letter, landscape,       │
                    │    DejaVu Sans Mono)        │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │   Preview in Preview.app    │
                    │   (unless --no-preview)     │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │   Confirm & Print           │
                    │   lpr → HP printer          │
                    │   (single-sided)            │
                    └─────────────────────────────┘
````

## Design Decisions

### Why Strip ANSI Instead of Converting to Colors?

1. **Target printer is B&W**: HP LaserJet Pro MFP 3101 is a monochrome printer
2. **Simpler pipeline**: No HTML intermediate, no color-to-grayscale mapping
3. **cc-skills pattern**: Follows existing Markdown → LaTeX → PDF workflow
4. **Reliability**: Avoids pandoc HTML table issues with `<br>` tags

### Why Markdown Code Blocks?

1. **Monospace rendering**: Proper character alignment for terminal output
2. **Native pandoc support**: Direct LaTeX conversion without HTML
3. **Syntax highlighting**: Optional via `--highlight-style` (not enabled by default)

### Why Landscape Orientation?

Terminal output typically has 80-120 character lines. Landscape orientation:

- Fits ~120 characters per line at 9pt font
- Reduces line wrapping
- Better matches terminal aspect ratio

## Customization

### Change Default Printer

Edit `assets/print-terminal.sh` line 19:

```bash
PRINTER="Your_Printer_Name_Here"
```

Find your printer name with: `lpstat -p -d`

### Change Font Size

Edit the pandoc command in `assets/print-terminal.sh`:

```bash
-V fontsize=9pt   # Default
-V fontsize=8pt   # Smaller (more content per page)
-V fontsize=10pt  # Larger (easier to read)
```

### Enable Syntax Highlighting

Add to the pandoc command:

```bash
--highlight-style=tango
```

Available styles: `pygments`, `tango`, `espresso`, `zenburn`, `kate`, `monochrome`

### Change Paper Size

Edit the geometry variable:

```bash
-V geometry:letterpaper,landscape   # US Letter (default)
-V geometry:a4paper,landscape       # A4 (international)
```

## Integration with cc-skills

This skill follows the cc-skills pattern established by:

- **pandoc-pdf-generation**: Universal build script pattern
- **asciinema-converter**: ANSI stripping pattern
- **Shell command portability**: Heredoc invocation for zsh compatibility

## Files

| File                       | Purpose                          |
| -------------------------- | -------------------------------- |
| `SKILL.md`                 | Skill definition and quick start |
| `assets/print-terminal.sh` | Main execution script            |
| `references/workflow.md`   | This detailed documentation      |

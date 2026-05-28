---
name: clean-language-reactor
description: Clean up Russian vocabulary CSV exports from Language Reactor (YouTube subtitle learning extension). Use when the user asks to process or clean up a Language Reactor CSV file.
---

# Clean YouTube Subtitle Vocabulary Exports

Transform vocabulary exports from YouTube subtitle extensions into flashcards for recognition practice.

Supports multiple formats:
- Language Reactor exports (WORD| prefix format)
- Simple CSV exports (word, sentence, timestamp, videoTitle, videoId)

## Workflow

1. **Preprocess** the raw export:
   ```bash
   python3 preprocess_language_reactor.py export.csv -o preprocessed.csv
   ```
   This will:
   - Auto-detect the CSV format
   - Parse the export and extract word data
   - Identify multi-word chunks (collocations) - marked with "Is Chunk=yes"
   - Automatically fetch the YouTube transcript
   - Output `preprocessed.csv` and `preprocessed.transcript.txt`

2. **Clean up** the preprocessed file (with Claude):
   - Read both the preprocessed CSV and the transcript
   - Convert chunks to nominative form (e.g., "собственным успехом" → "со́бственный успе́х")
   - Add translations
   - Create simpler example sentences
   - Add stress marks
   - Output the final 4-column CSV

## Examples

See the `examples/` directory:
- **Preprocessed input**: `examples/language-reactor-preprocessed.csv`
- **Transcript**: `examples/language-reactor-preprocessed.transcript.txt`
- **Cleaned output**: `examples/language-reactor-cleaned.csv`

## Card Purpose

These cards are for **recognition** (passive vocabulary), not production:
- **Front**: Russian word + example sentence
- **Back**: English translation

Use `--mode recognition` when creating the deck:
```bash
python3 create_deck.py --mode recognition cleaned.csv -o passive.apkg
```

## CSV Output Format

4 columns, comma-separated:

| Column | Content |
|--------|---------|
| 1 | Russian word/phrase with stress marks |
| 2 | English translation |
| 3 | Example sentence in Russian |
| 4 | English translation of example |

## Processing Rules

### 1. Read Both Files

When cleaning up, read:
- The preprocessed CSV (word, translation, context, POS)
- The transcript file (full video text for understanding context)

### 2. Handle Chunks and Collocations

**Pre-selected chunks**: Entries marked "Is Chunk=yes" were selected as multi-word phrases by the user. Keep these as collocations but convert to nominative form:
- `собственным успехом` → `со́бственный успе́х` (one's own success)
- `качественной медицине` → `ка́чественная медици́на` (quality healthcare)

**Identify additional collocations**: Some single words should be studied with their common collocations. Use the transcript to identify:
- `птичий` → `на пти́чьих права́х` (on precarious terms)
- `поразить` → `пораже́ны в права́х` (disenfranchised)
- `доступ` → `до́ступ к (+ dat.)` (access to)

### 3. Create Simpler Example Sentences

The subtitle context is often:
- Incomplete (cut off mid-sentence)
- Too long or complex for flashcards
- Contains multiple clauses

Create a **simpler, clearer sentence** that:
- Uses the word with the same meaning as in the video
- Is short enough for a flashcard (under 15 words ideally)
- Is grammatically complete

Use the full transcript to understand the meaning and context.

### 4. Stress Marks (Column 1 Only)

- Add stress mark (´) on the stressed vowel for multisyllabic words
- Skip monosyllables
- Skip words with ё (always stressed)

### 5. Gender for Soft Sign Nouns

- For nouns ending in soft sign (ь), indicate gender with `(m.)` if masculine
- Most soft-sign nouns are feminine, so only mark masculine ones
- Examples: `день (m.)` — day, `гость (m.)` — guest, `дождь (m.)` — rain

### 6. Verb Pairs
- When the word is a verb, include both the perfective and imperfective forms
- When the verb is used with a preposition in the context, include that preposition and the case used with that preposition in this context
Format: `imperfective/perfective` (e.g., `ви́деть/уви́деть`)
- Only include one form if the other isn't commonly used or doesn't make sense
- Include both when learners should know the pair

### 7. CSV Quoting

Wrap any field containing commas in double quotes.

## Example Transformation

**Preprocessed** (from `examples/language-reactor-preprocessed.csv`):
```csv
Word,Translation,Context (RU),Context (EN),POS
птичий,"bird's, avian",Пока у тебя нет гражданства ты всегда на птичьих правах,Until you have citizenship you're always on precarious terms,Adj
```

**Cleaned output** (see `examples/language-reactor-cleaned.csv`):
```
на пти́чьих права́х,on precarious terms (no legal rights),Без гражданства ты на птичьих правах.,Without citizenship you're on precarious terms.
```

Note: The single word `птичий` became the collocation `на пти́чьих права́х` because that's how it was used in context.

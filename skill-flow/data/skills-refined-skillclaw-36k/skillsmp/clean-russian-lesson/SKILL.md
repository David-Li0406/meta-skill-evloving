---
name: clean-russian-lesson
description: Clean up Russian vocabulary CSV files from Italki lessons or tutoring sessions. Use when the user asks to clean up, format, or process a lesson CSV file.
---

# Clean Russian Lesson Notes

Transform lesson notes into properly formatted vocabulary CSV files for Anki.

## Examples

See the `examples/` directory:
- **Raw input**: `examples/lesson-raw.csv`
- **Cleaned output**: `examples/lesson-cleaned.csv`

## CSV Output Format

4 columns, comma-separated:

| Column | Content |
|--------|---------|
| 1 | Russian word/phrase with stress marks |
| 2 | English translation |
| 3 | Example sentence in Russian |
| 4 | English translation of example |

## Processing Rules

### 1. Extract Key Vocabulary

Lesson notes often contain full Russian sentences or phrases. Extract:
- The key word or expression being taught
- Useful collocations (e.g., `ма́лый би́знес`, `за го́родом`)
- Grammar patterns with case markers (e.g., `зави́сеть от (+ gen.)`)

### 2. Stress Marks (Column 1 Only)

- Add stress mark (´) on the stressed vowel for multisyllabic words
- Skip monosyllables (e.g., да, нет, шерсть)
- Skip words with ё (always stressed)
- Only add stress marks in column 1, not in example sentences

### 3. Gender for Soft Sign Nouns

- For nouns ending in soft sign (ь), indicate gender with `(m.)` if masculine
- Most soft-sign nouns are feminine, so only mark masculine ones
- Examples: `день (m.)` — day, `гость (m.)` — guest, `дождь (m.)` — rain

### 4. Verb Pairs
- When the word is a verb, include both the perfective and imperfective forms
- When the verb is used with a preposition in the context, include that preposition and the case used with that preposition in this context
  Format: `imperfective/perfective` (e.g., `ви́деть/уви́деть`)
- Only include one form if the other isn't commonly used or doesn't make sense
- Include both when learners should know the pair

### 5. Grammar Notes

When a word requires a specific case or preposition, include it:
- `гото́виться к (+ dat.)` — to prepare for
- `зави́сеть от (+ gen.)` — to depend on
- `знако́миться с (+ instr.)` — to meet

### 6. Full Sentences

- Create complete example sentences if the notes only have fragments
- Use the original sentence from the lesson if it's already complete
- Keep examples natural and relevant

### 7. Remove Duplicates

- If the same phrase appears multiple times, keep only one entry
- Merge related entries when appropriate

### 8. CSV Quoting

- Wrap any field containing commas in double quotes
- Example: `"Зависит от того, чем ты занимаешься."`

## Example Transformation

**Raw notes** (from `examples/lesson-raw.csv`):
```
Так бывает
Семья моей жены
Зависит от того, чем ты занимаешься
```

**Cleaned output** (see `examples/lesson-cleaned.csv`):
```
так быва́ет,that's how it is,Так бывает в жизни.,That's how it is in life.
семья́ жены́,wife's family,Семья моей жены живёт в Бельгии.,My wife's family lives in Belgium.
зави́сеть от (+ gen.),to depend on,"Зависит от того, чем ты занимаешься.","It depends on what you do."
```
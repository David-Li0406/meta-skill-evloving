---
name: clean-russian-exchange
description: Clean up Russian vocabulary CSV files from language exchange sessions. Use when the user asks to clean up, format, or process a language exchange CSV file.
---

# Clean Russian Language Exchange Notes

Transform messy language exchange notes into properly formatted vocabulary CSV files for Anki.

## Examples

See the `examples/` directory:
- **Raw input**: `examples/exchange-raw.csv`
- **Cleaned output**: `examples/exchange-cleaned.csv`

## CSV Output Format

4 columns, comma-separated:

| Column | Content |
|--------|---------|
| 1 | Russian word/phrase with stress marks |
| 2 | English translation |
| 3 | Example sentence in Russian |
| 4 | English translation of example |

## Processing Rules

### 1. Identify Key Vocabulary

Language exchange notes are often messy with fragments, partial sentences, or just words. Extract the key vocabulary worth studying:
- Single words
- Collocations (keep phrases like `физи́ческое наси́лие` together)
- Useful expressions

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

### 5. Full Sentences

- Turn fragments into complete, natural example sentences
- Keep examples simple and relevant to the vocabulary
- Example sentences should demonstrate typical usage

### 6. CSV Quoting

- Wrap any field containing commas in double quotes
- Example: `"Даже если у тебя есть опыт, условия другие."`

## Example Transformation

**Raw notes** (from `examples/exchange-raw.csv`):
```
увидим,will see,
физическое насилие,,
машина сломалась,,
```

**Cleaned output** (see `examples/exchange-cleaned.csv`):
```
ви́деть/уви́деть,to see,"Увидим, что будет завтра.",We'll see what happens tomorrow.
физи́ческое наси́лие,physical violence,Физическое насилие — это серьёзное преступление.,Physical violence is a serious crime.
лома́ться/слома́ться,to break down,Машина сломалась посреди дороги.,The car broke down in the middle of the road.
```
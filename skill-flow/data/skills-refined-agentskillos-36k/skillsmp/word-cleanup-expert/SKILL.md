---
name: "word-cleanup-expert"
description: "Deduplicates word lists (prioritizing word.txt) and suggests spelling corrections. Invoke when user wants to clean up, deduplicate, or fix word files."
---

# Word Cleanup Expert

This skill manages the integrity of the project's word lists: `__doc__/word.txt` (master) and `__doc__/word_mid.txt`.

## Capabilities

1.  **De-duplication**:
    -   Reads both `word.txt` and `word_mid.txt`.
    -   Identifies words in `word_mid.txt` that already exist in `word.txt`.
    -   Removes these duplicates from `word_mid.txt` to ensure `word.txt` remains the source of truth for these words.

2.  **Spelling Correction**:
    -   Analyzes words in both lists for potential spelling errors.
    -   Suggests corrections for identified typos.
    -   **Note**: Does not automatically apply spelling fixes without user confirmation, but provides a report.

## Usage Instructions

When invoked:
1.  Read the content of `__doc__/word.txt` and `__doc__/word_mid.txt`.
2.  Perform intersection check (case-insensitive is recommended).
3.  List duplicates found in `word_mid.txt`.
4.  List suspected misspelled words with suggestions.
5.  Ask for user confirmation to proceed with:
    -   Removing duplicates from `word_mid.txt`.
    -   Applying specific spelling corrections (if requested).
6.  Upon confirmation, write the updated content to `__doc__/word_mid.txt` (and `__doc__/word.txt` if corrections apply there).

## File Paths
- Master List: `__doc__/word.txt`
- Intermediate List: `__doc__/word_mid.txt`

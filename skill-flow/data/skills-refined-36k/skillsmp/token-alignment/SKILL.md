---
name: token-alignment
description: Debug token-level penalty alignment issues. Use when banned tokens aren't being penalized correctly or when investigating tokenizer edge cases.
---

## When to Use This Skill
- Debugging why certain banned words aren't penalized
- Investigating subword tokenization issues
- Verifying token offset mapping

## Debugging Steps

### 1. Print token-level breakdown
```python
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B-Instruct-2507")

text = "The coin shows Heads"
enc = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
for i, (token_id, offset) in enumerate(zip(enc["input_ids"], enc["offset_mapping"])):
    print(f"{i}: {tokenizer.decode([token_id])!r} -> chars {offset}")
```

### 2. Check all token variants
Always check these variants for any banned word:
- `"Heads"` (no space)
- `" Heads"` (leading space - SentencePiece!)
- `"HEADS"`, `"heads"`, `"Head"`, `"head"`

```python
banned_word = "Heads"
variants = [
    banned_word,
    f" {banned_word}",
    banned_word.upper(),
    banned_word.lower(),
    banned_word.capitalize(),
]
for v in variants:
    ids = tokenizer.encode(v, add_special_tokens=False)
    print(f"{v!r} -> {ids} -> {[tokenizer.decode([i]) for i in ids]}")
```

### 3. Verify overlap detection
```python
def check_overlap(char_start, char_end, token_start, token_end):
    """Returns True if character span overlaps with token span."""
    return max(char_start, token_start) < min(char_end, token_end)

# Test: banned word at chars [15, 20], token spans from offset_mapping
for i, (tok_start, tok_end) in enumerate(enc["offset_mapping"]):
    if check_overlap(15, 20, tok_start, tok_end):
        print(f"Token {i} overlaps banned region: {tokenizer.decode([enc['input_ids'][i]])!r}")
```

### 4. Debug boundary detection
```python
import re

def find_cot_boundaries(text):
    """Find character boundaries of <think>...</think> regions."""
    pattern = r"<think>(.*?)</think>"
    boundaries = []
    for match in re.finditer(pattern, text, re.DOTALL):
        boundaries.append((match.start(1), match.end(1)))
    return boundaries

# Only penalize tokens WITHIN these boundaries
cot_bounds = find_cot_boundaries(completion)
for tok_idx, (tok_start, tok_end) in enumerate(offset_mapping):
    in_cot = any(check_overlap(cot_s, cot_e, tok_start, tok_end) 
                 for cot_s, cot_e in cot_bounds)
    if in_cot and is_banned_token(tok_idx):
        penalties[tok_idx] = -penalty_weight
```

## Common Gotchas

| Issue | Solution |
|-------|----------|
| Qwen uses SentencePiece | Leading spaces become part of tokens - always check `" Heads"` |
| Unicode lookalikes | `U+2217` (∗) vs `*` can bypass bans - normalize first |
| Case sensitivity | Handle explicitly with `.lower()` or check all variants |
| Multi-token words | `"Tails"` might be `["T", "ails"]` - check all subword tokens |
| Offset mapping gaps | Some tokenizers don't return perfect offsets - validate |

## Quick Validation Script
```python
# scripts/debug_tokenization.py
def validate_ban_coverage(text, banned_words, tokenizer):
    """Verify all banned word occurrences are captured by token penalties."""
    enc = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
    
    for word in banned_words:
        for match in re.finditer(re.escape(word), text, re.IGNORECASE):
            word_start, word_end = match.span()
            covered = False
            for tok_start, tok_end in enc["offset_mapping"]:
                if check_overlap(word_start, word_end, tok_start, tok_end):
                    covered = True
                    break
            if not covered:
                print(f"WARNING: '{word}' at [{word_start}:{word_end}] not covered!")
```

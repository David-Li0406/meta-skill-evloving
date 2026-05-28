# Integration Guide

How to chain asciinema-converter with other asciinema-tools skills.

## Skill Chain Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   .cast     │────▶│   convert   │────▶│    .txt     │
│  (NDJSON)   │     │             │     │ (clean text)│
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
                    ▼                          ▼                          ▼
            ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
            │   analyze   │            │  summarize  │            │    Read     │
            │ (keywords)  │            │ (AI deep)   │            │ (manual)    │
            └─────────────┘            └─────────────┘            └─────────────┘
```

## Single File Chains

### Convert → Analyze

Extract keywords and patterns from a single converted file:

```bash
# Step 1: Convert
/asciinema-tools:convert ~/Downloads/session.cast

# Step 2: Analyze (auto-chained with --analyze flag)
/asciinema-tools:convert ~/Downloads/session.cast --analyze
```

Or run separately:

```bash
/asciinema-tools:analyze ~/Downloads/session.txt
```

### Convert → Summarize

Deep AI analysis of session content:

```bash
# Convert first
/asciinema-tools:convert ~/Downloads/session.cast -o ~/tmp/session.txt

# Then summarize
/asciinema-tools:summarize ~/tmp/session.txt
```

---

## Batch Chains

### Batch Convert → Batch Analyze

Convert all files, then analyze all outputs:

```bash
# Step 1: Batch convert
/asciinema-tools:convert --batch --source ~/Downloads --output-dir ~/cast-txt/

# Step 2: Batch analyze (if skill supports it)
/asciinema-tools:analyze --batch --source ~/cast-txt/
```

### Post-Session Workflow

Complete workflow for session wrap-up:

```bash
/asciinema-tools:post-session
```

This internally chains:

1. `finalize` - Stop active recordings
2. `convert` - Convert to .txt
3. `summarize` - Generate AI summary

---

## File Path Conventions

### Naming Pattern

Output files preserve base name:

| Input                    | Output                  |
| ------------------------ | ----------------------- |
| `session.cast`           | `session.txt`           |
| `20260118_232025.*.cast` | `20260118_232025.*.txt` |
| `path/to/recording.cast` | `path/to/recording.txt` |

### Directory Structure

When using `--output-dir`:

| Source                     | Output                         |
| -------------------------- | ------------------------------ |
| `~/Downloads/session.cast` | `~/cast-txt/session.txt`       |
| `~/asciinemalogs/rec.cast` | `~/Downloads/cast-txt/rec.txt` |

### Index Files

When `--index` flag used:

| Base           | Index               |
| -------------- | ------------------- |
| `session.txt`  | `session.index.txt` |
| `session.cast` | `session.index.txt` |

---

## Manifest Files (Advanced)

For automated pipelines, batch convert generates a manifest:

```json
{
  "source_dir": "/Users/terryli/Downloads",
  "output_dir": "/Users/terryli/cast-txt",
  "converted": [
    {
      "source": "session1.cast",
      "output": "session1.txt",
      "size_input": 104857600,
      "size_output": 131072,
      "compression_ratio": 800
    }
  ],
  "skipped": ["session2.cast"],
  "failed": [],
  "timestamp": "2026-01-19T12:00:00Z"
}
```

Location: `$OUTPUT_DIR/.convert-manifest.json`

### Using Manifest for Downstream Skills

```bash
# Read manifest and process converted files
jq -r '.converted[].output' ~/cast-txt/.convert-manifest.json | \
  while read -r txt_file; do
    /asciinema-tools:analyze "$txt_file"
  done
```

---

## Workflow Commands

### Full Workflow

Record, convert, and analyze in one command:

```bash
/asciinema-tools:full-workflow
```

Chains:

1. `record` → Start recording
2. (user works)
3. `convert` → Convert to .txt
4. `analyze` → Extract insights

### Bootstrap

Pre-session setup:

```bash
/asciinema-tools:bootstrap
```

Outputs a script to start recording before entering Claude Code.

### Post-Session

End-of-session cleanup:

```bash
/asciinema-tools:post-session
```

Chains:

1. `finalize` → Stop orphaned recordings
2. `convert` → Convert recent .cast files
3. `summarize` → AI analysis

---

## Error Handling in Chains

### Fail-Fast (Single File)

If convert fails, subsequent skills don't run:

```bash
# This aborts if conversion fails
/asciinema-tools:convert session.cast --analyze
```

### Continue-on-Error (Batch)

Batch mode continues even if individual files fail:

```bash
# Converts all possible files, reports failures at end
/asciinema-tools:convert --batch
```

### Chain Recovery

If a downstream skill fails:

```bash
# Re-run just the failed step
/asciinema-tools:analyze ~/cast-txt/session.txt

# Don't re-convert (already done)
```

---

## Performance Considerations

### Chaining Overhead

| Chain                   | Overhead     | Notes                 |
| ----------------------- | ------------ | --------------------- |
| convert only            | Baseline     | ~5s per 100MB         |
| convert → analyze       | +2-3s        | Keyword extraction    |
| convert → summarize     | +30-60s      | AI API calls          |
| batch convert           | Baseline × N | Parallelizable        |
| batch convert → analyze | +2s × N      | Sequential by default |

### Parallel Batch Analysis

For large batches, run analysis in parallel:

```bash
# Convert first (sequential for disk I/O)
/asciinema-tools:convert --batch --output-dir ~/cast-txt/

# Then analyze in parallel (CPU-bound)
find ~/cast-txt -name "*.txt" | parallel -j4 '/asciinema-tools:analyze {}'
```

---

## Related

- [Anti-Patterns](./anti-patterns.md) - Common mistakes to avoid
- [Batch Processing](./batch-processing.md) - Bulk conversion patterns
- [asciinema-analyzer skill](../../asciinema-analyzer/SKILL.md) - Keyword extraction
- [asciinema-summarizer skill](../../asciinema-summarizer/SKILL.md) - AI analysis

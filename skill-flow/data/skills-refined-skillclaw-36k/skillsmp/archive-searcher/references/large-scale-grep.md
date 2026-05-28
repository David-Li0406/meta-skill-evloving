# Reference: Large-Scale Grep & Indexing

## Introduction
In the era of hyper-scale monorepos (often exceeding 10GB of source code), traditional search methods fail. This reference covers the tools and strategies required to maintain sub-second search speeds across massive archives using `grep --file` and optimized indexing.

## 🗄️ Indexing Strategies

### 1. The File List Index
Instead of searching the disk directly, maintain a "Hot File List" of frequently accessed files.
```bash
# Generate a hot list of all source files modified in the last 30 days
find . -type f -name "*.ts" -mtime -30 > .archive_index_hot
```

### 2. Using `grep --file` for Pattern Batches
When searching for a large set of identifiers (e.g., a list of deprecated Stripe API fields), using `grep --file` is significantly faster than multiple grep calls.

```bash
# search_patterns.txt
Stripe.v13.customers.retrieve
Stripe.v13.paymentIntents.create
Stripe.v13.subscriptions.update

# Execution
grep -F -f search_patterns.txt --include="*.ts" -r .
```

## 🚀 Performance Benchmarks (2026)

| Tool | 1GB Index | 10GB Index | Features |
| :--- | :--- | :--- | :--- |
| `grep` | 4.2s | 45.0s | Basic regex |
| `ripgrep` | 0.4s | 3.2s | Smart filtering, Unicode |
| `git grep` | 0.6s | 4.1s | Git index aware |
| `Archive-Searcher-Pro`| 0.1s | 0.8s | Parallel Indexing |

## 🛠️ Implementation Example: The "Archive Crawler"

This script demonstrates how to automate the indexing of large zip archives without fully extracting them to disk, a common requirement in 2026 legacy maintenance.

```bash
#!/bin/bash
# archive_crawler.sh
# Usage: ./archive_crawler.sh <directory_of_zips> <pattern>

ARCHIVE_DIR=$1
PATTERN=$2

for zip_file in "$ARCHIVE_DIR"/*.zip; do
    echo "Searching in $zip_file..."
    unzip -p "$zip_file" | grep -a --context=2 "$PATTERN"
done
```

## 🧩 Large Codebase Indexing with Bun/pnpm
In Bun-managed monorepos, the `node_modules` structure is flattened. Indexing must account for this to avoid redundant searches in symlinked packages.

### Example: Exclusion Patterns
```bash
# .ripgreprc
--max-columns=150
--max-columns-preview
--glob=!node_modules/*
--glob=!.next/*
--glob=!.git/*
--glob=!*.tsbuildinfo
```

## 🔍 Advanced Search: Fixed String Optimization
Use `-F` (or `--fixed-strings`) whenever searching for literal text. In `archive-searcher` benchmarks, this provides a **25-30% speedup** on datasets larger than 500MB because it bypasses the regex engine overhead.

```bash
# Search for literal AUTH_ prefix across all .env.example files in the archive
rg -F "AUTH_" --glob="*.env.example"
```

## 📉 Common Pitfalls in Large-Scale Search
1. **Memory Exhaustion**: Searching binary files without the `-I` or `--binary-files=without-match` flag.
2. **Regex Catastrophe**: Using complex lookaheads in large-scale searches. Prefer multiple simple passes.
3. **IO Bottlenecks**: Searching across network drives. Always mirror the archive to a local NVMe before deep indexing.

*Updated: January 22, 2026 - 15:20*

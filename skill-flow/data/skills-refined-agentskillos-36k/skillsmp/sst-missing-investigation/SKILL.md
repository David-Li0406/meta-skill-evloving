---
name: sst-missing-investigation
description: Investigate missing SST (NoSuchKey) incidents in TiKV/TiFlash/S3 logs. Use when you need to trace an SST ID across pods, map it to shard_id/region_id, correlate compaction and cleanup events, and update investigation notes with evidence.
---

# SST Missing Investigation

## Overview
Analyze missing SST errors by correlating TiFlash FATAL logs, TiKV compaction/read logs, and s3clean cleanup records. Produce a pod-scoped timeline and evidence list with file+line references.

## Investigation summary (distilled)
- Confirm the first TiFlash FATAL and extract all missing SST IDs from NoSuchKey.
- Map each SST ID to shard_id/region per TiKV pod using compaction metadata.
- Capture read/create/compaction-delete timing per pod (do not merge pods).
- Normalize time: s3clean timestamps are UTC+0 unless stated; convert to +08:00 when comparing.
- Check HA chaos windows and TiKV restarts (look for "Welcome to TiKV" and preceding error burst).
- Build a timeline and evidence section with exact file:line and raw log lines.
- Log phase conclusions into `investigate.md`, then use that as the base for deeper follow-up queries.

## Quick Start
1. Ensure logs exist in the analysis directory (use `copy-logs-from-k8s` skill if needed).
2. Locate missing SST IDs in TiFlash FATAL logs.
3. Map each SST ID to shard/region in TiKV per pod.
4. Correlate with s3clean removal and HA chaos kill windows.
5. Update `investigate.md` with timeline + evidence.

## Workflow

### 1) Identify missing SST IDs (TiFlash)
- Use TiFlash proxy logs to extract NoSuchKey IDs.
- Commands:
  - `rg -z -n "FATAL" tc-tiflash-*/tiflash_tikv.log`
  - `rg -z -n "NoSuchKey\(\\\"file" tc-tiflash-*/tiflash_tikv.log`

### 2) Map SST to shard_id/region_id (TiKV, per pod)
- Search compaction metadata for the SST ID; record `shard_id` and `region` for each pod.
- Commands:
  - `rg -n "table_creates \{ id: <sst-id>" tc-tikv-*`
  - `rg -n "shard meta apply change set" tc-tikv-* | rg "<sst-id>"`
- Extract `region="[store:shard:ver]"` and keep pods separate (`tc-tikv-0/1/2/3`).

### 3) Find compaction delete/obsolescence timing
- Use `bottom_deletes` to identify when the SST is obsoleted by compaction.
- Command:
  - `rg -n "bottom_deletes: <sst-id>" tc-tikv-*`

### 4) Check TiKV read/create context
- Confirm read timing or create timing if available.
- Commands:
  - `rg -n "read file <sst-id>" tc-tikv-*`
  - `rg -n "create file <sst-id>" tc-tikv-*`

### 4.1) Check TiKV restart/error window (if HA kill or gap suspected)
- Identify restart by "Welcome to TiKV" and measure gap from last error.
- Commands:
  - `rg -n "Welcome to TiKV" tc-tikv-*/tikv-*.log`
  - `rg -n "handle raft message err" tc-tikv-*/tikv-*.log`
  - `nl -ba <file> | sed -n '<line1>,<line2>p'`

### 5) Correlate s3clean removal
- Verify removal and permanent deletion timestamps.
- Command:
  - `rg -n "<sst-id>" s3clean-0/s3clean.log`

### 6) Correlate TiFlash region activity near FATAL
- Tie `region_id` activity to the FATAL window.
- Commands:
  - `rg -n "region_id=<id>" tc-tiflash-*/tiflash_tikv.log`
  - `rg -n "pre apply snapshot|region is applying snapshot" tc-tiflash-*/tiflash_tikv.log`

### 7) Build timeline and evidence
- Sort by timestamp and keep pod boundaries explicit.
- Record evidence with `file:line` and raw log line.
- Use `rg -n` for line numbers; extract exact lines with `sed -n '<line>p' <file>`.

## Tooling tips
- Use `rg -z` to search `.gz` files without manual decompression.
- Use `rg -C <N>` to capture context around matches.
- Keep all timestamps in the log timezone; note UTC explicitly when present.
- Use `nl -ba` when you need stable line numbers for evidence references.

## Outputs
- Update `investigate.md` with:
  - error cause summary
  - per-pod shard/region mapping
  - timeline (with timestamps)
  - evidence logs (file+line + raw content)
  - phase conclusions (when a partial answer is ready)
- Create translations (e.g., `investigate.chinese.md`) when requested.

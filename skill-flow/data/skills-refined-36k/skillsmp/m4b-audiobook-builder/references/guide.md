# M4B Audiobook Build Guide (Linux)

## Table of contents

- Overview
- Encoding assumptions
- Core tools
- Common pipeline
- Scenario 0: Subdirectories as chapters
- Scenario A: Mixed audio files to one M4B
- Scenario B: Multi-part M4B to one M4B
- Validation
- Recommendations

## Overview

Build a single M4B from multiple audio files (MP3, M4A, AAC, FLAC, OGG, WAV) or merge multiple M4B parts into one. Preserve metadata, normalize text to UTF-8, and generate chapter markers with correct timestamps.

## Encoding assumptions

Any non-UTF-8 text in filenames, tags, or auxiliary text files is assumed to be Russian and must be converted to UTF-8 (typically from CP1251 or KOI8-R). Keep all intermediate text files strictly UTF-8.

## Core tools

- coreutils: `find`, `sort -V`, `xargs`, `printf`
- convmv: convert filenames to UTF-8
- mutagen/mid3iconv: normalize MP3 ID3 tags to Unicode
- ffmpeg/ffprobe: decode, encode, concat, import chapters
- exiftool: inspect/edit metadata with charset control
- AtomicParsley: write iTunes-compatible MP4 metadata
- mp4chaps (mp4v2): export/import chapters
- MP4Box (gpac): import chapters from text files
- Bento4 (mp4info/mp4dump): inspect MP4/M4B structure

## Common pipeline

1. Prepare input files (ordering, filenames, encodings, formats).
2. Determine the actual part order, best metadata source, and cover source.
3. Normalize heterogeneous formats into one processing flow.
4. Normalize tags and character encodings.
5. Inspect durations and metadata.
6. Generate chapters.
7. Concatenate and encode into M4B.
8. Write audiobook-specific metadata and cover art.
9. Validate the result.

Before any destructive or time-consuming merge, present a single action plan with your recommended order, metadata source, and cover source. Ask for confirmation once, then proceed to merge/recode and apply the confirmed metadata without further follow-ups.

## Scenario 0: Subdirectories as chapters

Directory structure (example):

```
book/
├── 01_Intro/
│   ├── 01.mp3
│   └── 02.mp3
├── 02_Chapter_1/
│   ├── 01.mp3
│   └── 02.mp3
└── 03_Chapter_2/
    └── 01.mp3
```

Playback order is driven by directory order and file order. Chapters are derived from directory names. Chapter start is the first file in each directory.

Generate a global concat list (recursive):

```bash
find . -type f \
  \( -iname '*.mp3' -o -iname '*.m4a' -o -iname '*.aac' -o -iname '*.flac' -o -iname '*.ogg' -o -iname '*.wav' \) \
  -print0 \
| sort -zV \
| xargs -0 -I{} printf "file '%s'\n" "$PWD/{}" \
> files.txt
```

For chapters, prefer the helper script (`scripts/build_m4b_inputs.py`) to build both `files.txt` and `meta.txt` from this directory structure.

## Scenario A: Mixed audio files to one M4B

### 0. Optional metadata scan

If you need to confirm title/author/narrator metadata from a source file, prefer JSON output to avoid truncation in terminal output.

```bash
exiftool -json -Title -Artist -Album -AlbumArtist -TrackNumber -DiscNumber part01.mp3
```

If tags are incomplete, fall back to the folder name and filenames for a clean, user-confirmed metadata set.

### 1. Build an ordered file list

```bash
find . -maxdepth 1 -type f \
  \( -iname '*.mp3' -o -iname '*.m4a' -o -iname '*.aac' -o -iname '*.flac' -o -iname '*.ogg' -o -iname '*.wav' \) \
  -print0 \
| sort -zV \
| xargs -0 -I{} printf "file '%s'\n" "$PWD/{}" \
> files.txt
```

### 2. Generate chapter metadata (`meta.txt`)

FFmpeg metadata format:

```
;FFMETADATA1
[CHAPTER]
TIMEBASE=1/1000
START=0
END=123456
title=Chapter 1
```

Generate `meta.txt` using the helper script or a custom workflow based on `ffprobe` durations. When using per-file chapters, the helper script prefers embedded track titles when present.
If per-file chapters are too granular compared to the real book chapters, generate chapters per directory or hand-curate the chapter list instead of per-file chapters.

Helper script example (also emits `ffmpeg.sh` and `atomicparsley.sh` with ready-to-run command lines):

```bash
python3 scripts/build_m4b_inputs.py --root . --chapter-mode file --files-out files.txt --meta-out meta.txt --ffmpeg-out ffmpeg.sh --output-m4b book.m4b
```

To build a safe output filename from author/title (the script also appends `.m4b` if missing). By default, author and narrator names are reordered to `Last First` when building the filename and AtomicParsley command; use `--name-order keep` to preserve the input.

```bash
python3 scripts/build_m4b_inputs.py --root . --chapter-mode file --files-out files.txt --meta-out meta.txt --output-author "Author" --output-title "Title"
```

If you prefer a plain text filename:

```bash
python3 scripts/build_m4b_inputs.py --root . --chapter-mode file --files-out files.txt --meta-out meta.txt --ffmpeg-out ffmpeg.txt --output-m4b book.m4b
```

#### Curated chapter list example

Use a manual chapter list when you want timestamps aligned to real book chapters (not file boundaries).

`chapters.txt` (QuickTime-style for mp4chaps):

```
00:00:00.000 Introduction
00:12:34.500 Chapter 1
00:45:10.000 Chapter 2
```

Apply to an existing M4B (after concat). `mp4chaps` reads `chapters.txt` from the current directory:

```bash
mp4chaps -i -Q book.m4b
```

Alternative (MP4Box format with `chapters.txt`):

```bash
MP4Box -chap chapters.txt book.m4b
```

### 3. Build the M4B file

```bash
ffmpeg -f concat -safe 0 -i files.txt \
  -f ffmetadata -i meta.txt \
  -map 0:a:0 -vn \
  -c:a aac -b:a 96k -threads 0 \
  -map_metadata 1 -map_chapters 1 \
  -movflags +faststart \
  book.m4b
```

If the transcode is large (multi-hour), set a sufficiently long timeout up front in your runner to avoid re-runs.
If the source files include embedded cover art, mapping audio only (as above) avoids accidentally creating a video stream.

### 4. Final metadata pass

```bash
AtomicParsley book.m4b \
  --stik Audiobook \
  --artist "Performer Name" \
  --albumArtist "Author Name" \
  --artwork cover.jpg \
  --overWrite
```

Format person names as `Last First` in both `--artist` (narrator) and `--albumArtist` (author).

### Cover art handling

If a cover image exists alongside the audio files (common names: `cover.jpg`, `folder.jpg`, `front.jpg`, `artwork.jpg`), use it.
If cover art is embedded in a source file, extract it and embed it into the final M4B.

Find possible embedded cover tags:

```bash
exiftool -G1 -a -s -CoverArt -Picture -APIC part01.m4b
```

Extract the embedded cover (use the tag that exists in the output above):

```bash
exiftool -b -CoverArt part01.m4b > cover.jpg
```

```bash
exiftool -b -Picture part01.mp3 > cover.jpg
```

Then embed it into the final M4B with AtomicParsley as shown above.

Helper script (extract sidecar or embedded cover + embed):

```bash
python3 scripts/cover_art.py --root . --recursive --output cover.jpg --embed book.m4b
```

## Scenario B: Multi-part M4B to one M4B

Use this when source files are already M4B containers.

### 0. Determine the actual part order (do not trust lexical sort)

Check track/disc metadata and chapter titles to infer the correct sequence before merging. If the order is still ambiguous, ask the user to confirm the intended order.

Example metadata scan:

```bash
exiftool -G1 -a -s -TrackNumber -DiskNumber -Title -Album -Artist -Duration *.m4b
```

Optionally inspect chapters:

```bash
mp4chaps -x part01.m4b
```

Helper script (propose order + metadata/cover suggestions + optional `files.txt`):

```bash
python3 scripts/propose_m4b_order.py --root . --files-out files.txt
```

### 1. List source M4B files in confirmed order

If lexical order matches the confirmed order, you can use the sorted command below. Otherwise, write `files.txt` manually in the correct sequence.

```bash
find . -maxdepth 1 -type f -iname '*.m4b' -print0 \
| sort -zV \
| xargs -0 -I{} printf "file '%s'\n" "$PWD/{}" \
> files.txt
```

### 2. Extract and merge chapters

For each part:

```bash
mp4chaps -x part01.m4b
```

Shift timestamps by cumulative duration and merge into `chapters.txt` (QuickTime format recommended).

### 3. Concatenate without re-encoding

```bash
ffmpeg -f concat -safe 0 -i files.txt \
  -c copy \
  -movflags +faststart \
  book.m4b
```

### 4. Import combined chapters

```bash
mp4chaps -i -Q book.m4b
```

### 5. Embed cover art (if present)

If a cover image is available alongside the parts or embedded in a source file, extract it and embed it into `book.m4b` (see “Cover art handling” above).

## Validation

- `mediainfo book.m4b`
- `mp4info book.m4b`
- Verify chapters in target players (Apple Books, Smart AudioBook Player, VLC).

## Recommendations

- Prefer QuickTime-style chapters for broad compatibility.
- Derive chapter titles from directory names, ID3 title, or filenames.
- Normalize encodings early and keep all text files in UTF-8.
- Automate the pipeline with scripts or a Makefile for repeatable builds.
- If files represent fragments rather than real chapters, avoid per-file chapters and build chapter timestamps that match the actual book structure.
- If a source uses an exotic or poorly supported codec, re-encode to a well-supported format (AAC for M4B).
- Keep author (book author) distinct from performer/narrator; map performer to `artist` and author to `albumArtist`.
- Use multi-threaded modes where tools support them (e.g., ffmpeg `-threads`) to speed up transcoding.
- If ffmpeg emits non-monotonic DTS warnings and playback glitches appear, retry with `-fflags +genpts -avoid_negative_ts make_zero`.

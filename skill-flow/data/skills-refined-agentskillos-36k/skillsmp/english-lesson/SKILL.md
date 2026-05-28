---
name: english-lesson
description: Generate English lesson feedback from audio transcription
allowed-tools: Bash(cd *), Bash(ls *), Bash(find *), Bash(uv *), Write, Read, Glob, LS, Edit, MultiEdit
disable-model-invocation: true
---

# English Lesson Feedback Generator

## Your task

1. Check and transcribe audio files from input directory
2. Read the latest transcript file
3. Load previous feedback for comparison
4. Generate detailed feedback and save to 04_EngStudy folder

### Arguments

`/english-lesson YYYY-MM-DD` format to specify the lesson date.

- With argument → Use the specified date
- Without argument → Use today's date

### Step 1: Check Audio Files and Transcribe

```bash
ls .claude/skills/scripts/audio_video_to_text/input/
cd .claude/skills/scripts/audio_video_to_text && uv run audio_video_to_text.py
```

### Step 2: Read Latest Transcript

```bash
ls -la .claude/skills/scripts/audio_video_to_text/output/
```

Find and read the latest `*_transcript.txt` file from output directory.

After reading, cleanup output files.

```bash
cd .claude/skills/scripts/audio_video_to_text && uv run audio_video_to_text.py --cleanup
```

### Step 3: Load Previous Feedback

- IMPORTANT - Current directory is `.claude/`, so you MUST search from parent directory
- Use bash command - `find ../04_EngStudy -name "*-feedback.md" -type f | sort -r | head -1` to find latest feedback
- Alternative - Use Glob with `Glob(path="..", pattern="04_EngStudy/**/*-feedback.md")`
- Read the latest feedback file (format - `yyyy-mm-dd-feedback.md`)

### Step 4: Generate Feedback

Analyze the lesson transcript and generate detailed feedback. Use the specified date (or today's date if no argument) and save to `04_EngStudy/YYYY-MM-DD-feedback.md`.

Important - Read transcript and previous feedback before analysis.

#### Feedback Requirements

Generate detailed feedback in English including

#### Lesson Overview & Summary

- Content covered in today's lesson
- Vocabulary learned (with English and Japanese meanings)
- Materials and topics used
- Lesson flow and structure

#### English Proficiency Assessment

- Pronunciation and reading issues
- Fluency and naturalness
- Comprehension (response quality to instructor questions)

#### Grammar & Expression Improvements

- Grammar mistakes and unnatural expressions (quote specific utterances and explain why they're incorrect)
- Better expression suggestions (clear Before/After format)
- Vocabulary improvement suggestions

※Consolidate all errors in one section with comprehensive coverage

For grammar/expression improvements and long-term challenges, use this specific format

- Actual utterance - "exact quote from recording"
- Issue - detailed explanation of why this is incorrect
- Correct expression - "proper expression"
- Improvement method - specific learning/practice approach

#### Basic Communication Scenarios - Grammar & Expression Suggestions

- Appropriate greetings and grammar patterns
- Self-introduction sentence structure and vocabulary choices
- Natural response patterns to "Do you have any questions?"
- Appropriate farewell expressions at lesson end
- Other basic conversational grammar patterns

#### Strengths & Growth Areas

- Expressions used appropriately
- Improvements from previous sessions (if any)

#### Progress Tracking

- Comparison with previous feedback (specific improvements and recurring issues)
- Improvement trajectory (what has gotten better over time)
- Persistent challenges requiring continued focus

Execute all steps and report the generated feedback file path to user.

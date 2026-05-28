---
name: srt-summaries
description: Use this when you have an SRT subtitle file and want to generate two types of summaries.
---

# Reusable Prompt for SRT File Summaries

Please analyze the `*.srt` file in this directory and create 2 summary files:

1. **01-short-summary.md** - Quick reference summary
   - Brief overview of main topic
   - Key framework/concepts (4-5 bullet points max per section)
   - Main problems addressed
   - What was implemented/done
   - Top 5-7 lessons learned (with emoji indicators ✅ ⚠️)
   - Impact/results in 2-3 bullets
   - Bottom line takeaway
   - Resources links
   - Target length: Quick scan

2. **02-summary-with-timestamps.md** - Timeline-based summary with exact timestamps
   - Include video duration from SRT file
   - Create timeline with timestamp ranges [HH:MM:SS - HH:MM:SS]
   - Organize by chronological sections (Introduction, Main Talk, Q&A)
   - For each timestamp section:
     - Topic/section title
     - Key points covered (bullet points)
   - Include separate section for Q&A with individual question timestamps
   - Add "Key Quotes" section at end with quotes and their timestamps
   - Make it easy to jump to specific parts of video
   - Target length: Detailed timeline

**Formatting Guidelines:**

- Use markdown headers (##, ###, ####) for structure
- Use bullet points, numbered lists, and tables where appropriate
- Include emojis sparingly for visual markers (✅ ❌ ⚠️ 📊)
- Use **bold** for emphasis on key terms
- Use > blockquotes for important quotes
- Use horizontal rules (---) to separate major sections
- Include metadata at top (event, speaker, duration)

**File Naming:**

- Must be exactly: 01-short-summary.md, 02-summary-with-timestamps.md
- Save all files in the root directory (not subdirectories)

---

## Tips for Best Results

1. **For Short Summary**: Prioritize actionable insights and quick scanning
2. **For Timestamp Summary**: Make it easy to navigate video by topic
3. **All Summaries**: Extract the narrative flow (problem → solution → results)
4. **Be Specific**: Include names, numbers, examples mentioned in talk
5. **Context Matters**: Note if speaker is sharing personal experience vs. theory
6. **Capture Nuance**: Include caveats, debates, and different perspectives from Q&A

---

## Quality Checklist

- [ ] All 2 files created with correct names
- [ ] Metadata included (event, speaker, duration)
- [ ] Main framework/topic clearly explained
- [ ] Problems and solutions identified
- [ ] Implementation examples included
- [ ] Lessons learned captured
- [ ] Q&A highlights summarized
- [ ] Resources and links extracted
- [ ] Timestamps accurate (for file #2)
- [ ] Markdown formatting clean and consistent
- [ ] Files saved in root directory
